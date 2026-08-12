# Evaluation

Evaluation measures how well trained models perform on unseen test data.

## Workflow

```text
Trained Model
    ↓
Unseen Test Dataset
    ↓
Predictions
    ↓
Accuracy / Precision / Recall / F1
    ↓
Confusion Matrix
```

## Piezo

Current model:

```text
ai_pipeline/models/piezo_random_forest.pkl
```

Test data:

```text
ai_pipeline/training/dataset_split/X_test.csv
ai_pipeline/training/dataset_split/y_test.csv
```

Main script:

```text
evaluate_piezo_model.py
```

Output:

```text
piezo_evaluation.txt
```

## Status

- [x] Piezo model evaluation
- [x] Accuracy
- [x] Precision
- [x] Recall
- [x] F1-score
- [x] Confusion matrix
