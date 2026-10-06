# Model card
Intended use: exploratory prediction of a self-reported current strain rating from six session-level typing features. Not medical screening, diagnosis, employment or education decisions.

Default status: no real-trained model shipped. Live output is descriptive typing analysis. Synthetic demonstration artifacts are isolated from live inference.

Inputs: median inter-key interval, interval coefficient of variation, median dwell time, pause fraction (>1 second), backspace fraction and passage-mismatch fraction. Output after optional real training: predicted self-report on 0–10 scale, clipped for display.

Evaluation: group cross-validation within training participants; held-out participants for final MAE/RMSE. Mean predictor included. Results are dataset-specific and exploratory. No calibrated confidence or clinical accuracy is claimed. Inspect whether the selected model improves on the mean baseline.

Known issues: task practice, device effects, accessibility differences, position-based mismatch detection, no mobile IME support, subjective labels and small samples. Use repeated independent sessions and report uncertainty in research analysis. A model's failure to predict self-report is a valid finding.
