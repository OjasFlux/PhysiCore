import os
import joblib
import pandas as pd
import numpy as np

# =========================================================
# PATHS
# =========================================================

MODEL_FILE = r"ai_pipeline\models\mpu6050_decision_tree.pkl"

OUTPUT_FOLDER = r"ai_pipeline\tinyml\conversion"

OUTPUT_FILE = os.path.join(
    OUTPUT_FOLDER,
    "mpu6050_decision_tree.h"
)

TEST_FILE = (
    r"ai_pipeline\training\mpu6050_dataset_split"
    r"\X_test.csv"
)

# =========================================================
# LOAD MODEL
# =========================================================

print("Loading MPU6050 Decision Tree...")

model = joblib.load(MODEL_FILE)

tree = model.tree_

print("Tree loaded.")
print("Nodes:", tree.node_count)
print("Depth:", tree.max_depth)
print("Leaves:", model.get_n_leaves())

# =========================================================
# GET EXACT FEATURE ORDER
# =========================================================

if hasattr(model, "feature_names_in_"):

    feature_names = list(
        model.feature_names_in_
    )

else:

    feature_names = [
        f"Feature_{i}"
        for i in range(model.n_features_in_)
    ]

print("\nNumber of features:", len(feature_names))

print("\nFeature order:")

for index, name in enumerate(feature_names):

    print(
        f"{index}: {name}"
    )

# =========================================================
# LOAD TEST DATA
# =========================================================

X_test = pd.read_csv(TEST_FILE)

X_test = X_test[
    feature_names
]

print("\nTest samples:", len(X_test))

# =========================================================
# TREE ARRAYS
# =========================================================

children_left = tree.children_left

children_right = tree.children_right

features = tree.feature

thresholds = tree.threshold

values = tree.value

node_count = tree.node_count

# =========================================================
# LEAF CLASSES
# =========================================================

leaf_classes = []

for node in range(node_count):

    # Leaf node
    if children_left[node] == children_right[node]:

        class_id = int(
            np.argmax(
                values[node][0]
            )
        )

    else:

        class_id = -1

    leaf_classes.append(
        class_id
    )

# =========================================================
# VERIFY CONVERTED TREE LOGIC
# =========================================================

def predict_tree_python(
    feature_values
):

    node = 0

    while (
        children_left[node]
        !=
        children_right[node]
    ):

        feature_index = features[node]

        if (
            feature_values[feature_index]
            <=
            thresholds[node]
        ):

            node = children_left[node]

        else:

            node = children_right[node]

    return leaf_classes[node]


sklearn_predictions = model.predict(
    X_test
)

converted_predictions = []

for _, row in X_test.iterrows():

    feature_values = row[
        feature_names
    ].to_numpy(
        dtype=float
    )

    prediction = (
        predict_tree_python(
            feature_values
        )
    )

    converted_predictions.append(
        prediction
    )

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

    print(
        "Python tree logic matches sklearn: YES"
    )

else:

    print(
        "Python tree logic matches sklearn: NO"
    )

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
        "// PhysiCore - MPU6050 Decision Tree\n"
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
        "#ifndef MPU6050_DECISION_TREE_H\n"
    )

    file.write(
        "#define MPU6050_DECISION_TREE_H\n\n"
    )

    file.write(
        "#include <stdint.h>\n\n"
    )

    # -----------------------------------------------------
    # Constants
    # -----------------------------------------------------

    file.write(
        f"#define MPU6050_TREE_NODES {node_count}\n"
    )

    file.write(
        f"#define MPU6050_FEATURE_COUNT "
        f"{len(feature_names)}\n"
    )

    file.write(
        f"#define MPU6050_CLASS_COUNT "
        f"{model.n_classes_}\n\n"
    )

    # -----------------------------------------------------
    # Feature names
    # -----------------------------------------------------

    file.write(
        "// Feature order used by the model:\n"
    )

    for index, name in enumerate(
        feature_names
    ):

        file.write(
            f"// {index}: {name}\n"
        )

    file.write("\n")

    # -----------------------------------------------------
    # Feature indices
    # -----------------------------------------------------

    file.write(
        "static const int8_t "
        "mpu6050_tree_feature"
        "[MPU6050_TREE_NODES] = {\n"
    )

    for value in features:

        file.write(
            f"    {int(value)},\n"
        )

    file.write(
        "};\n\n"
    )

    # -----------------------------------------------------
    # Thresholds
    # -----------------------------------------------------

    file.write(
        "static const float "
        "mpu6050_tree_threshold"
        "[MPU6050_TREE_NODES] = {\n"
    )

    for value in thresholds:

        file.write(
            f"    {float(value):.10f}f,\n"
        )

    file.write(
        "};\n\n"
    )

    # -----------------------------------------------------
    # Left child
    # -----------------------------------------------------

    file.write(
        "static const int16_t "
        "mpu6050_tree_left"
        "[MPU6050_TREE_NODES] = {\n"
    )

    for value in children_left:

        file.write(
            f"    {int(value)},\n"
        )

    file.write(
        "};\n\n"
    )

    # -----------------------------------------------------
    # Right child
    # -----------------------------------------------------

    file.write(
        "static const int16_t "
        "mpu6050_tree_right"
        "[MPU6050_TREE_NODES] = {\n"
    )

    for value in children_right:

        file.write(
            f"    {int(value)},\n"
        )

    file.write(
        "};\n\n"
    )

    # -----------------------------------------------------
    # Leaf classes
    # -----------------------------------------------------

    file.write(
        "static const int8_t "
        "mpu6050_tree_class"
        "[MPU6050_TREE_NODES] = {\n"
    )

    for value in leaf_classes:

        file.write(
            f"    {int(value)},\n"
        )

    file.write(
        "};\n\n"
    )

    # -----------------------------------------------------
    # Prediction function
    # -----------------------------------------------------

    file.write(
        "static inline int "
        "mpu6050_predict(\n"
    )

    file.write(
        "    const float features"
        "[MPU6050_FEATURE_COUNT]\n"
    )

    file.write(
        ") {\n"
    )

    file.write(
        "    int node = 0;\n\n"
    )

    file.write(
        "    while ("
        "mpu6050_tree_left[node] "
        "!="
        " mpu6050_tree_right[node]) {\n\n"
    )

    file.write(
        "        int feature = "
        "mpu6050_tree_feature[node];\n\n"
    )

    file.write(
        "        if (features[feature] <= "
        "mpu6050_tree_threshold[node]) {\n"
    )

    file.write(
        "            node = "
        "mpu6050_tree_left[node];\n"
    )

    file.write(
        "        } else {\n"
    )

    file.write(
        "            node = "
        "mpu6050_tree_right[node];\n"
    )

    file.write(
        "        }\n"
    )

    file.write(
        "    }\n\n"
    )

    file.write(
        "    return "
        "mpu6050_tree_class[node];\n"
    )

    file.write(
        "}\n\n"
    )

    file.write(
        "#endif\n"
    )

# =========================================================
# FINAL RESULT
# =========================================================

print("\n======================================")
print("MPU6050 MODEL CONVERSION COMPLETED")
print("======================================")

print(
    "Output:",
    OUTPUT_FILE
)

print(
    "Features:",
    len(feature_names)
)

print(
    "Nodes:",
    node_count
)

print(
    "Depth:",
    model.get_depth()
)

print(
    "Leaves:",
    model.get_n_leaves()
)

print(
    "Classes:",
    model.n_classes_
)

print(
    "\nConversion verification: PASSED"
)
