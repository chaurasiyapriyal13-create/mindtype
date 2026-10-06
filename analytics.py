"""Content-free typing features. No health diagnosis or hand-made strain score."""
import math
import statistics as stats

FEATURES = ['median_interval_ms', 'interval_variability', 'median_dwell_ms', 'pause_rate', 'backspace_rate', 'error_rate']

def analyse(events):
    if not isinstance(events, list) or not 40 <= len(events) <= 10000:
        raise ValueError('Please capture between 40 and 10,000 keystrokes.')
    clean = []
    for event in events:
        row = {}
        for key in ['interval', 'dwell', 'backspace', 'error']:
            value = float(event.get(key, 0))
            if not math.isfinite(value) or value < 0:
                raise ValueError('Invalid timing data.')
            row[key] = value
        if row['interval'] > 600000 or row['dwell'] > 600000 or row['backspace'] not in (0,1) or row['error'] not in (0,1):
            raise ValueError('Invalid event values.')
        clean.append(row)
    intervals = [r['interval'] for r in clean if r['interval'] > 0]
    dwells = [r['dwell'] for r in clean if r['dwell'] > 0]
    if len(intervals) < 30 or len(dwells) < 30:
        raise ValueError('Insufficient complete timing events. Please type again.')
    med = stats.median(intervals)
    mean = stats.mean(intervals)
    return dict(zip(FEATURES, [round(med,2), round(stats.pstdev(intervals)/max(mean,1),4), round(stats.median(dwells),2), round(sum(v>1000 for v in intervals)/len(intervals),4), round(sum(r['backspace'] for r in clean)/len(clean),4), round(sum(r['error'] for r in clean)/len(clean),4)]))

def compare(current, baseline):
    return {k: round(current[k]-baseline[k],4) for k in FEATURES}
