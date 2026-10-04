#!/usr/bin/env python3
"""Query a local llama.cpp server once and save unedited response and timing."""
import argparse
import hashlib
import json
import pathlib
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--base-url', default='http://127.0.0.1:8080')
    ap.add_argument('--model-file', required=True)
    ap.add_argument('--output', required=True)
    a = ap.parse_args()
    model_file = pathlib.Path(a.model_file).resolve()
    if not model_file.is_file():
        ap.error('Model GGUF file does not exist')
    output = pathlib.Path(a.output).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        ap.error('Output already exists; preserve the earlier run')
    prompt = 'Reply with only the word READY if you can read this message.'
    payload = {'model': 'local-gemma4', 'messages': [{'role': 'user', 'content': prompt}],
               'temperature': 0, 'max_tokens': 96, 'stream': False}
    req = urllib.request.Request(a.base_url.rstrip('/') + '/v1/chat/completions',
                                 json.dumps(payload).encode(), {'Content-Type': 'application/json'})
    began = time.monotonic()
    with urllib.request.urlopen(req, timeout=180) as response:
        body = json.loads(response.read())
    record = {'created_utc': datetime.now(timezone.utc).isoformat(),
              'model_file': str(model_file), 'model_bytes': model_file.stat().st_size,
              'model_sha256': sha256(model_file), 'seconds': round(time.monotonic()-began, 3),
              'request': payload, 'response': body}
    output.write_text(json.dumps(record, indent=2) + '\n')
    print('Model response saved:', output)
    print('Text:', body.get('choices', [{}])[0].get('message', {}).get('content'))
    print('Usage:', body.get('usage', {}))

if __name__ == '__main__':
    main()
