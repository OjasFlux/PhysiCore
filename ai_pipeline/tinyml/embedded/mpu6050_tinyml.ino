#include <Wire.h>
#include <math.h>
#include "mpu6050_decision_tree.h"

// =====================================================
// PHYSICORE MPU6050 LIVE TINYML
// Arduino UNO Q
//
// Sensor configuration:
//   Accelerometer: +/-8g
//   Gyroscope:     +/-1000 deg/s
//
// Processing:
//   Sampling rate : 50 Hz
//   Window size   : 100 samples
//   Window time   : 2 seconds
//   Features      : 56
//
// Units:
//   Accelerometer -> m/s^2
//   Gyroscope     -> deg/s
//
// Classes:
//   0 = Normal
//   1 = Minor Fault
//   2 = Moderate Fault
//   3 = Severe Fault
// =====================================================


// =====================================================
// MPU6050 REGISTERS
// =====================================================

#define MPU6050_ADDR  0x68

#define PWR_MGMT_1    0x6B
#define ACCEL_CONFIG  0x1C
#define GYRO_CONFIG   0x1B
#define ACCEL_XOUT_H  0x3B
#define WHO_AM_I_REG  0x75


// =====================================================
// WINDOW SETTINGS
// =====================================================

const int WINDOW_SIZE = 100;
const int FEATURE_COUNT = 56;

const unsigned long SAMPLE_INTERVAL_US = 20000;


// =====================================================
// SENSOR SCALE
//
// Accelerometer:
// +/-8g = 4096 LSB/g
//
// Gyroscope:
// +/-1000 deg/s = 32.8 LSB/(deg/s)
// =====================================================

const float G_TO_MS2 = 9.80665f;

const float ACCEL_SCALE =
    G_TO_MS2 / 4096.0f;

const float GYRO_SCALE =
    1.0f / 32.8f;


// =====================================================
// GYROSCOPE CALIBRATION
// =====================================================

const int CALIBRATION_SAMPLES = 500;

float gyroBiasX = 0.0f;
float gyroBiasY = 0.0f;
float gyroBiasZ = 0.0f;


// =====================================================
// SENSOR BUFFERS
// =====================================================

float ax[WINDOW_SIZE];
float ay[WINDOW_SIZE];
float az[WINDOW_SIZE];

float gx[WINDOW_SIZE];
float gy[WINDOW_SIZE];
float gz[WINDOW_SIZE];


// =====================================================
// FEATURE VECTOR
// =====================================================

float features[FEATURE_COUNT];


// =====================================================
// SENSOR STATUS
// =====================================================

bool sensorReady = false;


// =====================================================
// WRITE REGISTER
// =====================================================

bool writeRegister(
    uint8_t reg,
    uint8_t value
)
{
    Wire.beginTransmission(
        MPU6050_ADDR
    );

    Wire.write(reg);
    Wire.write(value);

    uint8_t error =
        Wire.endTransmission();

    return error == 0;
}


// =====================================================
// READ ONE REGISTER
// =====================================================

bool readRegister(
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

    uint8_t buffer[14];

    for (
        int i = 0;
        i < 14;
        i++
    ) {

        if (!Wire.available()) {
            return false;
        }

        buffer[i] =
            Wire.read();
    }


    // ---------------------------------------------
    // ACCELEROMETER
    // ---------------------------------------------

    rawAx =
        (int16_t)(
            ((uint16_t)buffer[0] << 8) |
            buffer[1]
        );

    rawAy =
        (int16_t)(
            ((uint16_t)buffer[2] << 8) |
            buffer[3]
        );

    rawAz =
        (int16_t)(
            ((uint16_t)buffer[4] << 8) |
            buffer[5]
        );


    // ---------------------------------------------
    // BUFFER 6,7 = TEMPERATURE
    // ---------------------------------------------


    // ---------------------------------------------
    // GYROSCOPE
    // ---------------------------------------------

    rawGx =
        (int16_t)(
            ((uint16_t)buffer[8] << 8) |
            buffer[9]
        );

    rawGy =
        (int16_t)(
            ((uint16_t)buffer[10] << 8) |
            buffer[11]
        );

    rawGz =
        (int16_t)(
            ((uint16_t)buffer[12] << 8) |
            buffer[13]
        );

    return true;
}


// =====================================================
// CHECK SENSOR
// =====================================================

bool checkSensor()
{
    uint8_t whoAmI = 0;

    if (
        !readRegister(
            WHO_AM_I_REG,
            whoAmI
        )
    ) {
        return false;
    }

    Serial.print(
        "WHO_AM_I=0x"
    );

    if (whoAmI < 16) {
        Serial.print("0");
    }

    Serial.println(
        whoAmI,
        HEX
    );

    return (
        whoAmI == 0x68
    );
}


// =====================================================
// GYRO CALIBRATION
//
// Keep sensor completely still.
// =====================================================

bool calibrateGyroscope()
{
    Serial.println();
    Serial.println(
        "======================================"
    );

    Serial.println(
        "GYROSCOPE CALIBRATION"
    );

    Serial.println(
        "KEEP MPU6050 COMPLETELY STILL"
    );

    Serial.print(
        "Samples: "
    );

    Serial.println(
        CALIBRATION_SAMPLES
    );

    Serial.println(
        "======================================"
    );

    delay(1500);


    double sumX = 0.0;
    double sumY = 0.0;
    double sumZ = 0.0;

    int validSamples = 0;


    for (
        int i = 0;
        i < CALIBRATION_SAMPLES;
        i++
    ) {

        int16_t rawAx = 0;
        int16_t rawAy = 0;
        int16_t rawAz = 0;

        int16_t rawGx = 0;
        int16_t rawGy = 0;
        int16_t rawGz = 0;


        if (
            readMPU6050(
                rawAx,
                rawAy,
                rawAz,
                rawGx,
                rawGy,
                rawGz
            )
        ) {

            float gxValue =
                rawGx *
                GYRO_SCALE;

            float gyValue =
                rawGy *
                GYRO_SCALE;

            float gzValue =
                rawGz *
                GYRO_SCALE;


            sumX += gxValue;
            sumY += gyValue;
            sumZ += gzValue;

            validSamples++;
        }

        delay(4);
    }


    if (
        validSamples < 400
    ) {

        Serial.println(
            "CALIBRATION FAILED"
        );

        return false;
    }


    gyroBiasX =
        sumX /
        validSamples;

    gyroBiasY =
        sumY /
        validSamples;

    gyroBiasZ =
        sumZ /
        validSamples;


    Serial.println();

    Serial.print(
        "Gyro Bias X: "
    );

    Serial.println(
        gyroBiasX,
        6
    );

    Serial.print(
        "Gyro Bias Y: "
    );

    Serial.println(
        gyroBiasY,
        6
    );

    Serial.print(
        "Gyro Bias Z: "
    );

    Serial.println(
        gyroBiasZ,
        6
    );

    Serial.println(
        "CALIBRATION COMPLETE"
    );

    return true;
}


// =====================================================
// EXTRACT 7 FEATURES
//
// Mean
// Std
// Variance
// RMS
// Maximum
// Minimum
// Peak-to-Peak
// =====================================================

void extractAxisFeatures(
    float signal[],
    int offset
)
{
    float sum = 0.0f;

    float sumSquares = 0.0f;

    float minimum =
        signal[0];

    float maximum =
        signal[0];


    // ---------------------------------------------
    // FIRST PASS
    // ---------------------------------------------

    for (
        int i = 0;
        i < WINDOW_SIZE;
        i++
    ) {

        float value =
            signal[i];

        sum += value;

        sumSquares +=
            value * value;


        if (
            value < minimum
        ) {
            minimum =
                value;
        }


        if (
            value > maximum
        ) {
            maximum =
                value;
        }
    }


    float mean =
        sum /
        WINDOW_SIZE;


    float rms =
        sqrtf(
            sumSquares /
            WINDOW_SIZE
        );


    // ---------------------------------------------
    // VARIANCE
    // ---------------------------------------------

    float varianceSum =
        0.0f;


    for (
        int i = 0;
        i < WINDOW_SIZE;
        i++
    ) {

        float difference =
            signal[i] -
            mean;

        varianceSum +=
            difference *
            difference;
    }


    float variance =
        varianceSum /
        WINDOW_SIZE;


    float standardDeviation =
        sqrtf(
            variance
        );


    float peakToPeak =
        maximum -
        minimum;


    // ---------------------------------------------
    // STORE
    // ---------------------------------------------

    features[offset + 0] =
        mean;

    features[offset + 1] =
        standardDeviation;

    features[offset + 2] =
        variance;

    features[offset + 3] =
        rms;

    features[offset + 4] =
        maximum;

    features[offset + 5] =
        minimum;

    features[offset + 6] =
        peakToPeak;
}


// =====================================================
// CALCULATE MAGNITUDE
// =====================================================

void calculateMagnitude(
    float output[],
    float x[],
    float y[],
    float z[]
)
{
    for (
        int i = 0;
        i < WINDOW_SIZE;
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
// CALCULATE 56 FEATURES
// =====================================================

void calculateFeatures()
{
    // Ax
    extractAxisFeatures(
        ax,
        0
    );

    // Ay
    extractAxisFeatures(
        ay,
        7
    );

    // Az
    extractAxisFeatures(
        az,
        14
    );

    // Gx
    extractAxisFeatures(
        gx,
        21
    );

    // Gy
    extractAxisFeatures(
        gy,
        28
    );

    // Gz
    extractAxisFeatures(
        gz,
        35
    );


    float accelMagnitude[
        WINDOW_SIZE
    ];

    float gyroMagnitude[
        WINDOW_SIZE
    ];


    calculateMagnitude(
        accelMagnitude,
        ax,
        ay,
        az
    );

    calculateMagnitude(
        gyroMagnitude,
        gx,
        gy,
        gz
    );


    // Acceleration magnitude
    extractAxisFeatures(
        accelMagnitude,
        42
    );

    // Gyroscope magnitude
    extractAxisFeatures(
        gyroMagnitude,
        49
    );
}


// =====================================================
// CHECK ZERO / INVALID WINDOW
// =====================================================

bool isInvalidWindow()
{
    bool allZero =
        true;


    for (
        int i = 0;
        i < WINDOW_SIZE;
        i++
    ) {

        if (
            fabsf(ax[i]) > 0.0001f ||
            fabsf(ay[i]) > 0.0001f ||
            fabsf(az[i]) > 0.0001f ||
            fabsf(gx[i]) > 0.0001f ||
            fabsf(gy[i]) > 0.0001f ||
            fabsf(gz[i]) > 0.0001f
        ) {

            allZero =
                false;

            break;
        }
    }


    return allZero;
}


// =====================================================
// COLLECT 100 SAMPLES
// =====================================================

bool collectWindow()
{
    unsigned long nextSample =
        micros();


    for (
        int i = 0;
        i < WINDOW_SIZE;
        i++
    ) {

        // ---------------------------------------------
        // 50 Hz timing
        // ---------------------------------------------

        while (
            (long)(
                micros() -
                nextSample
            ) < 0
        ) {
        }


        int16_t rawAx = 0;
        int16_t rawAy = 0;
        int16_t rawAz = 0;

        int16_t rawGx = 0;
        int16_t rawGy = 0;
        int16_t rawGz = 0;


        bool success =
            readMPU6050(
                rawAx,
                rawAy,
                rawAz,
                rawGx,
                rawGy,
                rawGz
            );


        if (!success) {

            Serial.println(
                "SENSOR_READ_ERROR"
            );

            return false;
        }


        // ---------------------------------------------
        // ACCELEROMETER
        // +/-8g -> m/s^2
        // ---------------------------------------------

        ax[i] =
            rawAx *
            ACCEL_SCALE;

        ay[i] =
            rawAy *
            ACCEL_SCALE;

        az[i] =
            rawAz *
            ACCEL_SCALE;


        // ---------------------------------------------
        // GYROSCOPE
        // +/-1000 deg/s
        // Remove calibrated bias
        // ---------------------------------------------

        gx[i] =
            (
                rawGx *
                GYRO_SCALE
            ) -
            gyroBiasX;

        gy[i] =
            (
                rawGy *
                GYRO_SCALE
            ) -
            gyroBiasY;

        gz[i] =
            (
                rawGz *
                GYRO_SCALE
            ) -
            gyroBiasZ;


        nextSample +=
            SAMPLE_INTERVAL_US;
    }


    return true;
}


// =====================================================
// PRINT LIVE SUMMARY
// =====================================================

void printSummary()
{
    Serial.println();
    Serial.println(
        "LIVE FEATURES"
    );

    Serial.print(
        "AccelMag Mean : "
    );

    Serial.println(
        features[42],
        6
    );

    Serial.print(
        "AccelMag Std  : "
    );

    Serial.println(
        features[43],
        6
    );

    Serial.print(
        "AccelMag RMS  : "
    );

    Serial.println(
        features[45],
        6
    );

    Serial.print(
        "AccelMag P2P  : "
    );

    Serial.println(
        features[48],
        6
    );

    Serial.print(
        "GyroMag Mean  : "
    );

    Serial.println(
        features[49],
        6
    );

    Serial.print(
        "GyroMag Std   : "
    );

    Serial.println(
        features[50],
        6
    );

    Serial.print(
        "GyroMag RMS   : "
    );

    Serial.println(
        features[52],
        6
    );

    Serial.print(
        "GyroMag P2P   : "
    );

    Serial.println(
        features[55],
        6
    );
}


// =====================================================
// PREDICT
// =====================================================

int predictClass()
{
    return mpu6050_predict(
        features
    );
}


// =====================================================
// PRINT PREDICTION
// =====================================================

void printPrediction(
    int windowNumber,
    int prediction
)
{
    Serial.println();
    Serial.println(
        "======================================"
    );

    Serial.println(
        "MPU6050 TINYML PREDICTION"
    );

    Serial.println(
        "======================================"
    );

    Serial.print(
        "Window: "
    );

    Serial.println(
        windowNumber
    );

    Serial.print(
        "Class ID: "
    );

    Serial.println(
        prediction
    );


    switch (
        prediction
    ) {

        case 0:

            Serial.println(
                "Prediction: NORMAL"
            );

            break;


        case 1:

            Serial.println(
                "Prediction: MINOR FAULT"
            );

            break;


        case 2:

            Serial.println(
                "Prediction: MODERATE FAULT"
            );

            break;


        case 3:

            Serial.println(
                "Prediction: SEVERE FAULT"
            );

            break;


        default:

            Serial.println(
                "Prediction: UNKNOWN"
            );

            break;
    }


    Serial.println(
        "======================================"
    );


    // Machine-readable output
    Serial.print(
        "PREDICTION,"
    );

    Serial.print(
        windowNumber
    );

    Serial.print(
        ","
    );

    Serial.println(
        prediction
    );
}


// =====================================================
// SETUP
// =====================================================

void setup()
{
    Serial.begin(
        115200
    );

    delay(
        1000
    );


    Wire.begin();


    // ---------------------------------------------
    // Check MPU6050
    // ---------------------------------------------

    sensorReady =
        checkSensor();


    if (!sensorReady) {

        Serial.println(
            "MPU6050 NOT DETECTED"
        );

        while (true) {

            delay(
                1000
            );
        }
    }


    // ---------------------------------------------
    // Wake sensor
    // ---------------------------------------------

    if (
        !writeRegister(
            PWR_MGMT_1,
            0x00
        )
    ) {

        Serial.println(
            "PWR CONFIG ERROR"
        );

        while (true) {

            delay(
                1000
            );
        }
    }


    // ---------------------------------------------
    // Accelerometer +/-8g
    // ---------------------------------------------

    writeRegister(
        ACCEL_CONFIG,
        0x10
    );


    // ---------------------------------------------
    // Gyroscope +/-1000 deg/s
    // ---------------------------------------------

    writeRegister(
        GYRO_CONFIG,
        0x10
    );


    delay(
        100
    );


    // ---------------------------------------------
    // Header
    // ---------------------------------------------

    Serial.println();

    Serial.println(
        "PHYSICORE_MPU6050_LIVE_FINAL"
    );

    Serial.println(
        "BOARD=ARDUINO_UNO_Q"
    );

    Serial.println(
        "ACCEL_RANGE=+/-8g"
    );

    Serial.println(
        "GYRO_RANGE=+/-1000dps"
    );

    Serial.println(
        "ACCEL_UNIT=m/s2"
    );

    Serial.println(
        "GYRO_UNIT=deg/s"
    );

    Serial.println(
        "WINDOW_SIZE=100"
    );

    Serial.println(
        "SAMPLE_RATE=50Hz"
    );

    Serial.println(
        "FEATURE_COUNT=56"
    );


    // ---------------------------------------------
    // Gyro calibration
    // ---------------------------------------------

    if (
        !calibrateGyroscope()
    ) {

        Serial.println(
            "FATAL_CALIBRATION_ERROR"
        );

        while (true) {

            delay(
                1000
            );
        }
    }


    Serial.println();
    Serial.println(
        "LIVE_SYSTEM_READY"
    );
}


// =====================================================
// LOOP
// =====================================================

void loop()
{
    static int windowNumber = 0;


    // ---------------------------------------------
    // Collect
    // ---------------------------------------------

    if (
        !collectWindow()
    ) {

        delay(
            200
        );

        return;
    }


    // ---------------------------------------------
    // Reject invalid zero window
    // ---------------------------------------------

    if (
        isInvalidWindow()
    ) {

        Serial.println();
        Serial.println(
            "INVALID_ZERO_WINDOW"
        );

        Serial.println(
            "WINDOW_DISCARDED"
        );

        delay(
            200
        );

        return;
    }


    // ---------------------------------------------
    // Features
    // ---------------------------------------------

    calculateFeatures();


    // ---------------------------------------------
    // Summary
    // ---------------------------------------------

    printSummary();


    // ---------------------------------------------
    // Prediction
    // ---------------------------------------------

    int prediction =
        predictClass();


    windowNumber++;


    printPrediction(
        windowNumber,
        prediction
    );


    delay(
        100
    );
}
