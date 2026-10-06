"""Local-only web server; standard library runtime, optional ML dependencies."""
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime, timezone
import json, csv, re, uuid, threading, argparse, math
from src.analytics import analyse, compare, FEATURES
ROOT = Path(__file__).resolve().parent
LOCK = threading.Lock()

class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        paths = {'/':'index.html','/style.css':'style.css','/app.js':'app.js'}
        if self.path not in paths:
            return self.send_json(404, {'error':'Not found'})
        p = ROOT/'web'/paths[self.path]
        body = p.read_bytes(); self.send_response(200)
        self.send_header('Content-Type', {'html':'text/html; charset=utf-8','css':'text/css','js':'text/javascript'}[p.suffix[1:]])
        self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_POST(self):
        # Browser requests must originate from this local app; no cross-origin writes.
        if self.headers.get('Origin') != 'http://'+self.headers.get('Host',''):
            return self.send_json(403, {'error':'Open the app from its local address.'})
        try:
            length = int(self.headers.get('Content-Length',0))
            if not 0 < length <= 2000000: raise ValueError('Invalid request size.')
            payload = json.loads(self.rfile.read(length))
            if self.path == '/api/analyse':
                features = analyse(payload.get('events'))
                baseline = payload.get('baseline')
                if baseline is not None:
                    if not isinstance(baseline,dict) or any(not isinstance(baseline.get(k),(int,float)) or not math.isfinite(baseline[k]) for k in FEATURES): raise ValueError('Invalid baseline.')
                return self.send_json(200, {'features':features,'delta':compare(features,baseline) if baseline else None, 'model':self.predict(features), 'event_count':len(payload['events'])})
            if self.path == '/api/save':
                if payload.get('consent') is not True: raise ValueError('Consent is required to save.')
                participant = payload.get('participant','')
                if not re.fullmatch(r'[A-Za-z0-9_-]{3,40}',participant): raise ValueError('Use a participant code of 3–40 letters, numbers, underscores or hyphens.')
                rating = float(payload['rating'])
                if not 0 <= rating <= 10: raise ValueError('Rating must be 0–10.')
                features = analyse(payload.get('events'))
                row = {'participant_id':participant,'session_id':uuid.uuid4().hex,'timestamp':datetime.now(timezone.utc).isoformat(),'self_report_strain':rating, **features}
                path=ROOT/'data'/'sessions.csv'
                with LOCK:
                    exists=path.exists()
                    with path.open('a',newline='') as f:
                        writer=csv.DictWriter(f,fieldnames=list(row));
                        if not exists: writer.writeheader()
                        writer.writerow(row)
                return self.send_json(200, {'saved':True,'session_id':row['session_id']})
            return self.send_json(404, {'error':'Not found'})
        except (ValueError,TypeError,KeyError,json.JSONDecodeError) as e:
            return self.send_json(400, {'error':str(e)})
    def predict(self, features):
        path=ROOT/'models'/'regressor.joblib'
        if not path.exists(): return {'available':False}
        import joblib
        import pandas as pd
        bundle=joblib.load(path)
        value=float(bundle['model'].predict(pd.DataFrame([features])[FEATURES])[0])
        return {'available':True,'predicted_self_report':round(max(0,min(10,value)),1),'training_source':bundle['source'],'label':'Experimental estimate of self-reported strain; not a diagnosis'}
    def log_message(self,*args): pass

if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8501); args=parser.parse_args()
    print(f'MindType Studio → http://127.0.0.1:{args.port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
