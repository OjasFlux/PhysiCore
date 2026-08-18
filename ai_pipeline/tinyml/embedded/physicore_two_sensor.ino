#include <Wire.h>
#include <math.h>

#include "mpu6050_decision_tree.h"
#include "piezo_decision_tree.h"


// =====================================================
// PHYSICORE TWO-SENSOR TINYML
//
// Sensors:
//   1. MPU6050
//   2. Piezo
//
// Classes:
//   0 = Normal
//   1 = Minor Fault
//   2 = Moderate Fault
//   3 = Severe Fault
//
// MPU6050:
//   100 samples
//   50 Hz
//   56 features
//
// Piezo:
//   100 samples
//   50 Hz
//   9 features
//
// Fusion:
//   Agree      -> agreed class
//   Disagree   -> higher severity class
// =====================================================


// =====================================================
// PIEZO
// =====================================================

const int PIEZO_PIN = A0;

const int PIEZO_WINDOW_SIZE = 100;

const float PIEZO_SAMPLE_RATE = 50.0f;

const unsigned long PIEZO_INTERVAL_US = 20000;


// =====================================================
// MPU6050
// =====================================================

#define MPU6050_ADDR  0x68

#define PWR_MGMT_1    0x6B
#define ACCEL_CONFIG  0x1C
#define GYRO_CONFIG   0x1B
#define ACCEL_XOUT_H  0x3B
#define WHO_AM_I_REG  0x75

const int MPU_WINDOW_SIZE = 100;

const int MPU_FEATURE_COUNT = 56;

const unsigned long MPU_INTERVAL_US = 20000;


// =====================================================
// MPU6050 SCALE
// =====================================================

const float G_TO_MS2 = 9.80665f;

const float ACCEL_SCALE =
    G_TO_MS2 / 4096.0f;

const float GYRO_SCALE =
    1.0f / 32.8f;


// =====================================================
// GYRO CALIBRATION
// =====================================================

const int CALIBRATION_SAMPLES = 500;

float gyroBiasX = 0.0f;
float gyroBiasY = 0.0f;
float gyroBiasZ = 0.0f;


// =====================================================
// MPU6050 BUFFERS
// =====================================================

float mpuAx[MPU_WINDOW_SIZE];
float mpuAy[MPU_WINDOW_SIZE];
float mpuAz[MPU_WINDOW_SIZE];

float mpuGx[MPU_WINDOW_SIZE];
float mpuGy[MPU_WINDOW_SIZE];
float mpuGz[MPU_WINDOW_SIZE];

float mpuFeatures[
    MPU_FEATURE_COUNT
];


// =====================================================
// PIEZO BUFFERS
// =====================================================

float piezoSignal[
    PIEZO_WINDOW_SIZE
];

float piezoFeatures[9];


// =====================================================
// WRITE MPU REGISTER
// =====================================================

bool writeMpuRegister(
    uint8_t reg,
    uint8_t value
)
{
    Wire.beginTransmission(
        MPU6050_ADDR
    );

    Wire.write(reg);
    Wire.write(value);

    return (
        Wire.endTransmission() == 0
    );
}


// =====================================================
// READ MPU REGISTER
// =====================================================

bool readMpuRegister(
    uint8_t reg,
    uint8_t &value
)
{
    Wire.beginTransmission(
        MPU6050_ADDR
    );

    Wire.write(reg);

    if (
        Wire.endTransmission(false)
        != 0
    ) {
        return false;
    }

    uint8_t count =
        Wire.requestFrom(
            MPU6050_ADDR,
            (uint8_t)1,
            (uint8_t)true
        );

    if (
        count != 1 ||
        !Wire.available()
    ) {
        return false;
    }

    value = Wire.read();

    return true;
}


// =====================================================
// READ MPU6050
// =====================================================

bool readMPU6050(
    int16_t &rawAx,
    int16_t &rawAy,
    int16_t &rawAz,
    int16_t &rawGx,
    int16_t &rawGy,
    int16_t &rawGz
)
{
    Wire.beginTransmission(
        MPU6050_ADDR
    );

    Wire.write(
        ACCEL_XOUT_H
    );

    if (
        Wire.endTransmission(false)
        != 0
    ) {
        return false;
    }

    uint8_t count =
        Wire.requestFrom(
            MPU6050_ADDR,
            (uint8_t)14,
            (uint8_t)true
        );

    if (count != 14) {
        return false;
    }

    uint8_t b[14];

    for (
        int i = 0;
        i < 14;
        i++
    ) {

        if (!Wire.available()) {
            return false;
        }

        b[i] = Wire.read();
    }


    rawAx =
        (int16_t)(
            ((uint16_t)b[0] << 8) |
            b[1]
        );

    rawAy =
        (int16_t)(
            ((uint16_t)b[2] << 8) |
            b[3]
        );

    rawAz =
        (int16_t)(
            ((uint16_t)b[4] << 8) |
            b[5]
        );


    rawGx =
        (int16_t)(
            ((uint16_t)b[8] << 8) |
            b[9]
        );

    rawGy =
        (int16_t)(
            ((uint16_t)b[10] << 8) |
            b[11]
        );

    rawGz =
        (int16_t)(
            ((uint16_t)b[12] << 8) |
            b[13]
        );

    return true;
}


// =====================================================
// GYRO CALIBRATION
// =====================================================

bool calibrateGyroscope()
{
    Serial.println();
    Serial.println(
        "GYRO CALIBRATION"
    );

    Serial.println(
        "KEEP MPU6050 STILL"
    );

    delay(1500);

    double sumX = 0.0;
    double sumY = 0.0;
    double sumZ = 0.0;

    int valid = 0;

    for (
        int i = 0;
        i < CALIBRATION_SAMPLES;
        i++
    ) {

        int16_t ax;
        int16_t ay;
        int16_t az;

        int16_t gx;
        int16_t gy;
        int16_t gz;

        if (
            readMPU6050(
                ax,
                ay,
                az,
                gx,
                gy,
                gz
            )
        ) {

            sumX +=
                gx * GYRO_SCALE;

            sumY +=
                gy * GYRO_SCALE;

            sumZ +=
                gz * GYRO_SCALE;

            valid++;
        }

        delay(4);
    }

    if (valid < 400) {
        return false;
    }

    gyroBiasX =
        sumX / valid;

    gyroBiasY =
        sumY / valid;

    gyroBiasZ =
        sumZ / valid;

    Serial.print(
        "Gyro bias: "
    );

    Serial.print(
        gyroBiasX,
        4
    );

    Serial.print(
        ", "
    );

    Serial.print(
        gyroBiasY,
        4
    );

    Serial.print(
        ", "
    );

    Serial.println(
        gyroBiasZ,
        4
    );

    return true;
}


// =====================================================
// EXTRACT 7 FEATURES
// =====================================================

void extractSevenFeatures(
    float *signal,
    int length,
    float *output
)
{
    float sum = 0.0f;
    float sumSquares = 0.0f;

    float minimum = signal[0];
    float maximum = signal[0];

    for (
        int i = 0;
        i < length;
        i++
    ) {

        float x = signal[i];

        sum += x;

        sumSquares +=
            x * x;

        if (
            x < minimum
        ) {
            minimum = x;
        }

        if (
            x > maximum
        ) {
            maximum = x;
        }
    }


    float mean =
        sum / length;

    float rms =
        sqrtf(
            sumSquares /
            length
        );


    float varianceSum = 0.0f;

    for (
        int i = 0;
        i < length;
        i++
    ) {

        float d =
            signal[i] -
            mean;

        varianceSum +=
            d * d;
    }

    float variance =
        varianceSum /
        length;

    float std =
        sqrtf(
            variance
        );

    float peakToPeak =
        maximum -
        minimum;


    output[0] = mean;
    output[1] = std;
    output[2] = variance;
    output[3] = rms;
    output[4] = maximum;
    output[5] = minimum;
    output[6] = peakToPeak;
}


// =====================================================
// MPU MAGNITUDE
// =====================================================

void calculateMagnitude(
    float *output,
    float *x,
    float *y,
    float *z,
    int length
)
{
    for (
        int i = 0;
        i < length;
        i++
    ) {

        output[i] =
            sqrtf(
                x[i] * x[i] +
                y[i] * y[i] +
                z[i] * z[i]
            );
    }
}


// =====================================================
// MPU FEATURES
// =====================================================

void calculateMpuFeatures()
{
    extractSevenFeatures(
        mpuAx,
        MPU_WINDOW_SIZE,
        &mpuFeatures[0]
    );

    extractSevenFeatures(
        mpuAy,
        MPU_WINDOW_SIZE,
        &mpuFeatures[7]
    );

    extractSevenFeatures(
        mpuAz,
        MPU_WINDOW_SIZE,
        &mpuFeatures[14]
    );

    extractSevenFeatures(
        mpuGx,
        MPU_WINDOW_SIZE,
        &mpuFeatures[21]
    );

    extractSevenFeatures(
        mpuGy,
        MPU_WINDOW_SIZE,
        &mpuFeatures[28]
    );

    extractSevenFeatures(
        mpuGz,
        MPU_WINDOW_SIZE,
        &mpuFeatures[35]
    );


    float accelMag[
        MPU_WINDOW_SIZE
    ];

    float gyroMag[
        MPU_WINDOW_SIZE
    ];


    calculateMagnitude(
        accelMag,
        mpuAx,
        mpuAy,
        mpuAz,
        MPU_WINDOW_SIZE
    );

    calculateMagnitude(
        gyroMag,
        mpuGx,
        mpuGy,
        mpuGz,
        MPU_WINDOW_SIZE
    );


    extractSevenFeatures(
        accelMag,
        MPU_WINDOW_SIZE,
        &mpuFeatures[42]
    );

    extractSevenFeatures(
        gyroMag,
        MPU_WINDOW_SIZE,
        &mpuFeatures[49]
    );
}


// =====================================================
// COLLECT MPU WINDOW
// =====================================================

bool collectMpuWindow()
{
    unsigned long nextTime =
        micros();

    for (
        int i = 0;
        i < MPU_WINDOW_SIZE;
        i++
    ) {

        while (
            (long)(
                micros() -
                nextTime
            ) < 0
        ) {
        }


        int16_t rawAx;
        int16_t rawAy;
        int16_t rawAz;

        int16_t rawGx;
        int16_t rawGy;
        int16_t rawGz;


        if (
            !readMPU6050(
                rawAx,
                rawAy,
                rawAz,
                rawGx,
                rawGy,
                rawGz
            )
        ) {
            return false;
        }


        mpuAx[i] =
            rawAx *
            ACCEL_SCALE;

        mpuAy[i] =
            rawAy *
            ACCEL_SCALE;

        mpuAz[i] =
            rawAz *
            ACCEL_SCALE;


        mpuGx[i] =
            rawGx *
            GYRO_SCALE -
            gyroBiasX;

        mpuGy[i] =
            rawGy *
            GYRO_SCALE -
            gyroBiasY;

        mpuGz[i] =
            rawGz *
            GYRO_SCALE -
            gyroBiasZ;


        nextTime +=
            MPU_INTERVAL_US;
    }

    return true;
}


// =====================================================
// PIEZO TIME FEATURES
// =====================================================

void calculatePiezoTimeFeatures()
{
    extractSevenFeatures(
        piezoSignal,
        PIEZO_WINDOW_SIZE,
        piezoFeatures
    );
}


// =====================================================
// PIEZO FREQUENCY FEATURES
// =====================================================

void calculatePiezoFrequencyFeatures()
{
    float mean =
        piezoFeatures[0];

    float maxMagnitude =
        -1.0f;

    float dominantFrequency =
        0.0f;

    float spectralEnergy =
        0.0f;


    for (
        int k = 0;
        k <= PIEZO_WINDOW_SIZE / 2;
        k++
    ) {

        float realPart = 0.0f;
        float imagPart = 0.0f;


        for (
            int n = 0;
            n < PIEZO_WINDOW_SIZE;
            n++
        ) {

            float centered =
                piezoSignal[n] -
                mean;

            float angle =
                2.0f *
                PI *
                k *
                n /
                PIEZO_WINDOW_SIZE;


            realPart +=
                centered *
                cos(angle);

            imagPart -=
                centered *
                sin(angle);
        }


        float magnitude =
            sqrtf(
                realPart *
                realPart
                +
                imagPart *
                imagPart
            );


        if (
            k == 0
        ) {
            magnitude = 0.0f;
        }


        spectralEnergy +=
            magnitude *
            magnitude;


        if (
            magnitude >
            maxMagnitude
        ) {

            maxMagnitude =
                magnitude;

            dominantFrequency =
                (
                    (float)k *
                    PIEZO_SAMPLE_RATE
                )
                /
                PIEZO_WINDOW_SIZE;
        }
    }


    piezoFeatures[7] =
        dominantFrequency;

    piezoFeatures[8] =
        spectralEnergy;
}


// =====================================================
// COLLECT PIEZO
// =====================================================

void collectPiezoWindow()
{
    unsigned long nextTime =
        micros();


    for (
        int i = 0;
        i < PIEZO_WINDOW_SIZE;
        i++
    ) {

        while (
            (long)(
                micros() -
                nextTime
            ) < 0
        ) {
        }


        piezoSignal[i] =
            (float)
            analogRead(
                PIEZO_PIN
            );


        nextTime +=
            PIEZO_INTERVAL_US;
    }
}


// =====================================================
// PIEZO FEATURES
// =====================================================

void calculatePiezoFeatures()
{
    calculatePiezoTimeFeatures();

    calculatePiezoFrequencyFeatures();
}


// =====================================================
// SENSOR FUSION
//
// 0 Normal
// 1 Minor
// 2 Moderate
// 3 Severe
// =====================================================

int fusePredictions(
    int mpuPrediction,
    int piezoPrediction
)
{
    if (
        mpuPrediction ==
        piezoPrediction
    ) {

        return mpuPrediction;
    }


    // Conservative rule:
    // choose higher severity

    if (
        mpuPrediction >
        piezoPrediction
    ) {

        return mpuPrediction;
    }

    return piezoPrediction;
}


// =====================================================
// PRINT CLASS NAME
// =====================================================

void printClassName(
    int classId
)
{
    switch (
        classId
    ) {

        case 0:
            Serial.print(
                "NORMAL"
            );
            break;

        case 1:
            Serial.print(
                "MINOR FAULT"
            );
            break;

        case 2:
            Serial.print(
                "MODERATE FAULT"
            );
            break;

        case 3:
            Serial.print(
                "SEVERE FAULT"
            );
            break;

        default:
            Serial.print(
                "UNKNOWN"
            );
            break;
    }
}


// =====================================================
// SETUP
// =====================================================

void setup()
{
    Serial.begin(
        115200
    );

    delay(1000);

    Wire.begin();


    // ---------------------------------------------
    // MPU6050
    // ---------------------------------------------

    uint8_t who = 0;

    if (
        !readMpuRegister(
            WHO_AM_I_REG,
            who
        )
    ) {

        Serial.println(
            "MPU6050 READ ERROR"
        );

        while (true) {
            delay(1000);
        }
    }


    Serial.print(
        "MPU6050 WHO_AM_I=0x"
    );

    Serial.println(
        who,
        HEX
    );


    if (
        !writeMpuRegister(
            PWR_MGMT_1,
            0x00
        )
    ) {

        Serial.println(
            "MPU6050 POWER ERROR"
        );

        while (true) {
            delay(1000);
        }
    }


    // +/-8g

    writeMpuRegister(
        ACCEL_CONFIG,
        0x10
    );


    // +/-1000 deg/s

    writeMpuRegister(
        GYRO_CONFIG,
        0x10
    );


    delay(100);


    // ---------------------------------------------
    // PIEZO
    // ---------------------------------------------

    pinMode(
        PIEZO_PIN,
        INPUT
    );


    // ---------------------------------------------
    // CALIBRATION
    // ---------------------------------------------

    if (
        !calibrateGyroscope()
    ) {

        Serial.println(
            "GYRO CALIBRATION FAILED"
        );

        while (true) {
            delay(1000);
        }
    }


    Serial.println();
    Serial.println(
        "======================================"
    );

    Serial.println(
        "PHYSICORE TWO SENSOR TINYML"
    );

    Serial.println(
        "MPU6050 + PIEZO"
    );

    Serial.println(
        "======================================"
    );

    Serial.println(
        "MPU6050: 100 samples / 50 Hz"
    );

    Serial.println(
        "Piezo  : 100 samples / 50 Hz"
    );

    Serial.println(
        "Fusion : higher severity on disagreement"
    );

    Serial.println(
        "SYSTEM_READY"
    );
}


// =====================================================
// LOOP
// =====================================================

void loop()
{
    // ---------------------------------------------
    // Collect both sensor windows
    // ---------------------------------------------

    if (
        !collectMpuWindow()
    ) {

        Serial.println(
            "MPU6050_READ_ERROR"
        );

        delay(500);

        return;
    }


    collectPiezoWindow();


    // ---------------------------------------------
    // Features
    // ---------------------------------------------

    calculateMpuFeatures();

    calculatePiezoFeatures();


    // ---------------------------------------------
    // Individual predictions
    // ---------------------------------------------

    int mpuPrediction =
        mpu6050_predict(
            mpuFeatures
        );


    int piezoPrediction =
        piezo_predict(
            piezoFeatures
        );


    // ---------------------------------------------
    // Fusion
    // ---------------------------------------------

    int finalPrediction =
        fusePredictions(
            mpuPrediction,
            piezoPrediction
        );


    // ---------------------------------------------
    // Output
    // ---------------------------------------------

    Serial.println();

    Serial.println(
        "======================================"
    );

    Serial.println(
        "PHYSICORE LIVE RESULT"
    );

    Serial.println(
        "======================================"
    );


    Serial.print(
        "MPU6050 : "
    );

    printClassName(
        mpuPrediction
    );

    Serial.println();


    Serial.print(
        "Piezo   : "
    );

    printClassName(
        piezoPrediction
    );

    Serial.println();


    Serial.print(
        "FINAL   : "
    );

    printClassName(
        finalPrediction
    );

    Serial.println();


    Serial.print(
        "Agreement: "
    );

    if (
        mpuPrediction ==
        piezoPrediction
    ) {

        Serial.println(
            "YES"
        );

    } else {

        Serial.println(
            "NO"
        );
    }


    Serial.println(
        "======================================"
    );


    // Machine-readable line
    Serial.print(
        "FUSION,"
    );

    Serial.print(
        mpuPrediction
    );

    Serial.print(
        ","
    );

    Serial.print(
        piezoPrediction
    );

    Serial.print(
        ","
    );

    Serial.println(
        finalPrediction
    );
}
