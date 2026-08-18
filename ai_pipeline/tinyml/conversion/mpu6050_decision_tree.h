#ifndef MPU6050_DECISION_TREE_H
#define MPU6050_DECISION_TREE_H

// =============================================
// PhysiCore MPU6050 Decision Tree
// Automatically generated from Python
// Feature count: 56
// Classes: 0=Normal, 1=Minor, 2=Moderate, 3=Severe
// =============================================

static inline int mpu6050_predict(const float *features) {
        if (features[50] <= 1.17802554f) {
        if (features[49] <= 0.280236483f) {
        if (features[2] <= 0.709071577f) {
        return 0;
        } else {
        return 1;
        }
        } else {
        return 2;
        }
        } else {
        return 3;
        }
}

#endif
