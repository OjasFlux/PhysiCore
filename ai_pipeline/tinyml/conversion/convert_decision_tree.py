import os
import joblib
import pandas as pd
import numpy as np

# =========================================================
# PATHS
# =========================================================

MODEL_FILE = r"ai_pipeline\models\piezo_decision_tree.pkl"

OUTPUT_FOLDER = r"ai_pipeline\tinyml\conversion"

OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "piezo_decision_tree.h"
)

TEST_FILE = r"ai_pipeline\training\dataset_split\X_test.csv"

# =========================================================
# FEATURE ORDER
# IMPORTANT:
# This MUST match the order used during training.
# =========================================================

FEATURE_NAMES = [
    "Mean",
    "Std",
    "Variance",
    "RMS",
    "Maximum",
    "Minimum",
    "Peak_to_Peak",
    "Dominant_Frequency",
    "Spectral_Energy"
]

# =========================================================
# LOAD MODEL
# =========================================================

print("Loading Decision Tree...")

model = joblib.load(MODEL_FILE)

tree = model.tree_

print("Tree loaded.")
print("Number of nodes:", tree.node_count)
print("Tree depth:", tree.max_depth)
print("Number of leaves:", model.get_n_leaves())

# =========================================================
# READ TEST DATA FOR VERIFICATION
# =========================================================

X_test = pd.read_csv(TEST_FILE)

print("\nTest samples:", len(X_test))

# =========================================================
# EXTRACT TREE ARRAYS
# =========================================================

children_left = tree.children_left
children_right = tree.children_right
features = tree.feature
thresholds = tree.threshold
values = tree.value

node_count = tree.node_count

# =========================================================
# DETERMINE CLASS AT EACH LEAF
# =========================================================

leaf_classes = []

for node in range(node_count):

    # Leaf node
    if children_left[node] == children_right[node]:

        class_id = int(
            np.argmax(values[node][0])
        )

    else:

        class_id = -1

    leaf_classes.append(class_id)

# =========================================================
# VERIFY PYTHON TREE LOGIC
# =========================================================

def predict_tree_python(feature_values):

    node = 0

    while children_left[node] != children_right[node]:

        feature_index = features[node]

        if feature_values[feature_index] <= thresholds[node]:
            node = children_left[node]
        else:
            node = children_right[node]

    return leaf_classes[node]


sklearn_predictions = model.predict(X_test)

converted_predictions = []

for _, row in X_test.iterrows():

    feature_values = row[
        FEATURE_NAMES
    ].to_numpy(dtype=float)

    prediction = predict_tree_python(
        feature_values
    )

    converted_predictions.append(prediction)

converted_predictions = np.array(
    converted_predictions
)

verification = np.array_equal(
    sklearn_predictions,
    converted_predictions
)

print("\n======================================")
print("CONVERSION VERIFICATION")
print("======================================")

if verification:

    print("Python tree logic matches sklearn: YES")

else:

    print("Python tree logic matches sklearn: NO")
    raise RuntimeError(
        "Conversion verification failed."
    )

# =========================================================
# CREATE OUTPUT DIRECTORY
# =========================================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)

# =========================================================
# GENERATE C HEADER
# =========================================================

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "// =====================================================\n"
    )
    file.write(
        "// PhysiCore - Piezo Decision Tree\n"
    )
    file.write(
        "// Auto-generated from scikit-learn model\n"
    )
    file.write(
        "// DO NOT EDIT MANUALLY\n"
    )
    file.write(
        "// =====================================================\n\n"
    )

    file.write(
        "#ifndef PIEZO_DECISION_TREE_H\n"
    )
    file.write(
        "#define PIEZO_DECISION_TREE_H\n\n"
    )

    file.write(
        "#include <stdint.h>\n\n"
    )

    # ---------------------------------------------
    # Constants
    # ---------------------------------------------

    file.write(
        f"#define PIEZO_TREE_NODES {node_count}\n"
    )

    file.write(
        f"#define PIEZO_FEATURE_COUNT {len(FEATURE_NAMES)}\n"
    )

    file.write(
        "#define PIEZO_CLASS_COUNT 4\n\n"
    )

    # ---------------------------------------------
    # Feature names
    # ---------------------------------------------

    file.write(
        "// Feature order used by the model:\n"
    )

    for index, name in enumerate(FEATURE_NAMES):

        file.write(
            f"// {index}: {name}\n"
        )

    file.write("\n")

    # ---------------------------------------------
    # Feature index array
    # ---------------------------------------------

    file.write(
        "static const int8_t piezo_tree_feature[PIEZO_TREE_NODES] = {\n"
    )

    for value in features:

        file.write(
            f"    {int(value)},\n"
        )

    file.write("};\n\n")

    # ---------------------------------------------
    # Threshold array
    # ---------------------------------------------

    file.write(
        "static const float piezo_tree_threshold[PIEZO_TREE_NODES] = {\n"
    )

    for value in thresholds:

        file.write(
            f"    {float(value):.10f}f,\n"
        )

    file.write("};\n\n")

    # ---------------------------------------------
    # Left child
    # ---------------------------------------------

    file.write(
        "static const int16_t piezo_tree_left[PIEZO_TREE_NODES] = {\n"
    )

    for value in children_left:

        file.write(
            f"    {int(value)},\n"
        )

    file.write("};\n\n")

    # ---------------------------------------------
    # Right child
    # ---------------------------------------------

    file.write(
        "static const int16_t piezo_tree_right[PIEZO_TREE_NODES] = {\n"
    )

    for value in children_right:

        file.write(
            f"    {int(value)},\n"
        )

    file.write("};\n\n")

    # ---------------------------------------------
    # Leaf class
    # ---------------------------------------------

    file.write(
        "static const int8_t piezo_tree_class[PIEZO_TREE_NODES] = {\n"
    )

    for value in leaf_classes:

        file.write(
            f"    {int(value)},\n"
        )

    file.write("};\n\n")

    # ---------------------------------------------
    # Prediction function
    # ---------------------------------------------

    file.write(
        "static inline int piezo_predict(\n"
    )

    file.write(
        "    const float features[PIEZO_FEATURE_COUNT]\n"
    )

    file.write(
        ") {\n"
    )

    file.write(
        "    int node = 0;\n\n"
    )

    file.write(
        "    while (piezo_tree_left[node] != "
        "piezo_tree_right[node]) {\n\n"
    )

    file.write(
        "        int feature = piezo_tree_feature[node];\n\n"
    )

    file.write(
        "        if (features[feature] <= "
        "piezo_tree_threshold[node]) {\n"
    )

    file.write(
        "            node = piezo_tree_left[node];\n"
    )

    file.write(
        "        } else {\n"
    )

    file.write(
        "            node = piezo_tree_right[node];\n"
    )

    file.write(
        "        }\n"
    )

    file.write(
        "    }\n\n"
    )

    file.write(
        "    return piezo_tree_class[node];\n"
    )

    file.write(
        "}\n\n"
    )

    file.write(
        "#endif\n"
    )

# =========================================================
# FINAL INFORMATION
# =========================================================

print("\n======================================")
print("MODEL CONVERSION COMPLETED")
print("======================================")

print("Output:")
print(OUTPUT_FILE)

print("\nFeature count:", len(FEATURE_NAMES))
print("Tree nodes:", node_count)
print("Tree depth:", tree.max_depth)
print("Leaves:", model.get_n_leaves())

print("\nConversion verification: PASSED")
