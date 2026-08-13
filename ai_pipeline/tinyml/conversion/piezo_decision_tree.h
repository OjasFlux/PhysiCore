// =====================================================
// PhysiCore - Piezo Decision Tree
// Auto-generated from scikit-learn model
// DO NOT EDIT MANUALLY
// =====================================================

#ifndef PIEZO_DECISION_TREE_H
#define PIEZO_DECISION_TREE_H

#include <stdint.h>

#define PIEZO_TREE_NODES 11
#define PIEZO_FEATURE_COUNT 9
#define PIEZO_CLASS_COUNT 4

// Feature order used by the model:
// 0: Mean
// 1: Std
// 2: Variance
// 3: RMS
// 4: Maximum
// 5: Minimum
// 6: Peak_to_Peak
// 7: Dominant_Frequency
// 8: Spectral_Energy

static const int8_t piezo_tree_feature[PIEZO_TREE_NODES] = {
    1,
    -2,
    1,
    -2,
    6,
    0,
    -2,
    -2,
    6,
    -2,
    -2,
};

static const float piezo_tree_threshold[PIEZO_TREE_NODES] = {
    2.8175663948f,
    -2.0000000000f,
    54.7536029816f,
    -2.0000000000f,
    729.5000000000f,
    31.6549997330f,
    -2.0000000000f,
    -2.0000000000f,
    761.0000000000f,
    -2.0000000000f,
    -2.0000000000f,
};

static const int16_t piezo_tree_left[PIEZO_TREE_NODES] = {
    1,
    -1,
    3,
    -1,
    5,
    6,
    -1,
    -1,
    9,
    -1,
    -1,
};

static const int16_t piezo_tree_right[PIEZO_TREE_NODES] = {
    2,
    -1,
    4,
    -1,
    8,
    7,
    -1,
    -1,
    10,
    -1,
    -1,
};

static const int8_t piezo_tree_class[PIEZO_TREE_NODES] = {
    -1,
    0,
    -1,
    1,
    -1,
    -1,
    2,
    2,
    -1,
    3,
    3,
};

static inline int piezo_predict(
    const float features[PIEZO_FEATURE_COUNT]
) {
    int node = 0;

    while (piezo_tree_left[node] != piezo_tree_right[node]) {

        int feature = piezo_tree_feature[node];

        if (features[feature] <= piezo_tree_threshold[node]) {
            node = piezo_tree_left[node];
        } else {
            node = piezo_tree_right[node];
        }
    }

    return piezo_tree_class[node];
}

#endif
