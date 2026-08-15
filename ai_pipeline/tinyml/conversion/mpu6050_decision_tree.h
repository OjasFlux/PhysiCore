// =====================================================
// PhysiCore - MPU6050 Decision Tree
// Auto-generated from scikit-learn model
// DO NOT EDIT MANUALLY
// =====================================================

#ifndef MPU6050_DECISION_TREE_H
#define MPU6050_DECISION_TREE_H

#include <stdint.h>

#define MPU6050_TREE_NODES 7
#define MPU6050_FEATURE_COUNT 56
#define MPU6050_CLASS_COUNT 4

// Feature order used by the model:
// 0: Ax_Mean
// 1: Ax_Std
// 2: Ax_Variance
// 3: Ax_RMS
// 4: Ax_Maximum
// 5: Ax_Minimum
// 6: Ax_Peak_to_Peak
// 7: Ay_Mean
// 8: Ay_Std
// 9: Ay_Variance
// 10: Ay_RMS
// 11: Ay_Maximum
// 12: Ay_Minimum
// 13: Ay_Peak_to_Peak
// 14: Az_Mean
// 15: Az_Std
// 16: Az_Variance
// 17: Az_RMS
// 18: Az_Maximum
// 19: Az_Minimum
// 20: Az_Peak_to_Peak
// 21: Gx_Mean
// 22: Gx_Std
// 23: Gx_Variance
// 24: Gx_RMS
// 25: Gx_Maximum
// 26: Gx_Minimum
// 27: Gx_Peak_to_Peak
// 28: Gy_Mean
// 29: Gy_Std
// 30: Gy_Variance
// 31: Gy_RMS
// 32: Gy_Maximum
// 33: Gy_Minimum
// 34: Gy_Peak_to_Peak
// 35: Gz_Mean
// 36: Gz_Std
// 37: Gz_Variance
// 38: Gz_RMS
// 39: Gz_Maximum
// 40: Gz_Minimum
// 41: Gz_Peak_to_Peak
// 42: AccelMag_Mean
// 43: AccelMag_Std
// 44: AccelMag_Variance
// 45: AccelMag_RMS
// 46: AccelMag_Maximum
// 47: AccelMag_Minimum
// 48: AccelMag_Peak_to_Peak
// 49: GyroMag_Mean
// 50: GyroMag_Std
// 51: GyroMag_Variance
// 52: GyroMag_RMS
// 53: GyroMag_Maximum
// 54: GyroMag_Minimum
// 55: GyroMag_Peak_to_Peak

static const int8_t mpu6050_tree_feature[MPU6050_TREE_NODES] = {
    50,
    49,
    2,
    -2,
    -2,
    -2,
    -2,
};

static const float mpu6050_tree_threshold[MPU6050_TREE_NODES] = {
    1.1780255437f,
    0.2802364826f,
    0.7205217481f,
    -2.0000000000f,
    -2.0000000000f,
    -2.0000000000f,
    -2.0000000000f,
};

static const int16_t mpu6050_tree_left[MPU6050_TREE_NODES] = {
    1,
    2,
    3,
    -1,
    -1,
    -1,
    -1,
};

static const int16_t mpu6050_tree_right[MPU6050_TREE_NODES] = {
    6,
    5,
    4,
    -1,
    -1,
    -1,
    -1,
};

static const int8_t mpu6050_tree_class[MPU6050_TREE_NODES] = {
    -1,
    -1,
    -1,
    0,
    1,
    2,
    3,
};

static inline int mpu6050_predict(
    const float features[MPU6050_FEATURE_COUNT]
) {
    int node = 0;

    while (mpu6050_tree_left[node] != mpu6050_tree_right[node]) {

        int feature = mpu6050_tree_feature[node];

        if (features[feature] <= mpu6050_tree_threshold[node]) {
            node = mpu6050_tree_left[node];
        } else {
            node = mpu6050_tree_right[node];
        }
    }

    return mpu6050_tree_class[node];
}

#endif
