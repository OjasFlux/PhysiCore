# Models

Contains trained machine-learning models for PhysiCore fault detection.

## Current Models

### Random Forest

```text
piezo_random_forest.pkl
```

Used as the initial PC-side baseline.

### Decision Tree

```text
piezo_decision_tree.pkl
```

Current TinyML candidate.

Model characteristics:

```text
Tree depth : 4
Leaves     : 6
Test accuracy : 99.57%
```

## Output Classes

| ID | Condition |
|---:|---|
| 0 | Normal |
| 1 | Minor Fault |
| 2 | Moderate Fault |
| 3 | Severe Fault |

## Status

- [x] Random Forest baseline
- [x] Decision Tree candidate
- [x] Validation
- [x] Evaluation
- [x] TinyML candidate selected
- [ ] Final embedded implementation
