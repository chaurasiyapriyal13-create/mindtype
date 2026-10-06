# MindType Studio
A minimal, local-first typing behaviour research prototype by Priyal Chaurasiya.

Explore keyboard rhythm without additional sensors. The browser captures press/release timing and correction flags inside a dedicated typing box. Python computes features and compares two identical neutral passages. Typed content is not sent to the backend.

**This project does not determine mental health, diagnose disorders, or offer a validated strain score.** The default app reports measured behaviour only. Optional ML predicts a participant's self-reported current strain rating after real-data training.

## Quick start — no packages needed for the prototype
Install Python 3.10 or later. Extract this folder, open it in VS Code and run:

```bash
python app.py
```
Open http://127.0.0.1:8501. Windows users can also double-click `start_windows.bat` (requires the `py` launcher).

1. Copy the reference passage at your natural pace.
2. Copy the same passage again.
3. See timing, pauses, corrections and the rhythm chart; download the JSON report.
4. Optionally contribute numeric features and a 0–10 self-report using a repeatable anonymous participant code.

Only the optional Save action writes participant data to `data/sessions.csv`. The reference and raw events remain in page memory. Reload to clear them. Reports downloaded by the user persist until deleted. Stored research CSVs are plaintext; keep access restricted and do not publish them. This local-only server is not production hosting software.

## Data science workflow
From the project root:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m src.eda --data data/sessions.csv
python -m src.train --data data/sessions.csv --source real
```
Restart the app after training. Its results panel will show an experimental predicted self-report. Do not label synthetic input `real`. Only load model files you trained yourself: joblib/pickle files are executable when loaded.

Training compares a mean baseline, scaled Ridge regression and random forest. Group cross-validation selects the candidate using training participants only. A separate participant-held-out split provides MAE and RMSE. Scalers live inside the model pipeline. There is no participant overlap and no label-derived typing baseline. The minimum participant check is a software guard, not a claim of scientific adequacy.

### Synthetic smoke test
```bash
python -m src.demo_data
python -m src.eda --data data/synthetic_demo.csv
python -m src.train --data data/synthetic_demo.csv --source synthetic
```
Synthetic models are saved to `models/synthetic_demo/`, never automatically used by the live app. Their metrics test the pipeline, not real people.

### Verification
```bash
python -m unittest discover -s tests
```

## Structure
- `app.py`: local HTTP server, input validation, opt-in CSV writes and optional model inference.
- `web/`: responsive ivory/sage interface, reduced-motion support, typing capture and report download.
- `src/analytics.py`: robust feature computation, event checks and session differences.
- `src/train.py`: participant-separated model comparison.
- `src/eda.py`: statistics, correlations and exported plots.
- `src/demo_data.py`: explicitly synthetic pipeline data.
- `docs/`: collection protocol, model card and portfolio wording.
- `tests/`: numerical feature and invalid-input tests.

## Changes from the original ZIP
Replaces synthetic-trained LSTM live scoring with measurements plus optional real-data regression. Removes unvalidated calm/strained labels, arbitrary 0–100 health scores and passage-agreement confidence. Uses matching passages to reduce task difficulty confounding. Corrects key-up matching using the associated key code. Removes bundled encryption secrets and identifiable logs. Adds consent, participant-held-out evaluation, EDA, documentation and a minimal responsive UI.

The original LSTM was intentionally not carried forward: deep learning on simulated labels is not a stronger result than properly evaluated baselines. An LSTM can be added as a comparison once enough real sequential labelled data is collected.

## Limitations
Repeated passage practice affects timing. A single session reference is not a verified calm state. Device, language, typing skill, fatigue, interruptions and accessibility needs can affect features. Desktop keyboard capture is the supported prototype; mobile IME/dictation requires separate instrumentation and validation. No clinical validation, calibrated uncertainty or causal claims. The self-report label is a subjective research target. The app never monitors typing outside its own box.

Research background: https://mental.jmir.org/2023/1/e44986/ — reports weak associations and limited cross-sectional clinical prediction. It does not validate this app.
