# Real-data collection protocol
Obtain faculty approval for the study design and consent wording before recruiting. Participation must be optional and participants can stop without penalty.

Use anonymous codes, not names or college IDs. Explain what is saved: session code, timestamp, six numeric typing features and a 0–10 current self-report rating. Explain storage location, who can access it, retention and deletion. Do not collect private typed text.

Collect repeated sessions over different days under comparable conditions. Keep keyboard/device and language consistent where feasible. Use the same neutral passage, record practice effects, and avoid deliberately distressing participants. Collect strain ratings independently of typing measurements. Do not infer labels from typing speed, corrections or the app output.

This app stores one observed passage per contributed session. Record relevant context such as device changes, sleep, interruption and typing experience in a separately consented research form if required. Ratings are self-reports, not diagnostic ground truth. Research questions and sample size should be justified with faculty; 10 participants is only the script's minimum split guard.

For a stronger personalised study, collect multiple reference sessions and evaluate future sessions chronologically. Do not build references from held-out labels. Split by participant for generalisation to new users. Publish only appropriately de-identified aggregate findings. Raw CSVs and trained models should be reviewed for privacy before sharing.

To remove a contribution, stop the app, remove rows for that participant code from data/sessions.csv, then retrain or delete models trained on those rows. Provide this procedure and a real contact/retention period in the study consent form.
