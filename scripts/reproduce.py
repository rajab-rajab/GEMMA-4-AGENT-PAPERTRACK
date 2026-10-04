#!/usr/bin/env python3
"""Screen one historical bug: fixed-revision regression test is red before fix, green after."""
import argparse
import json
import pathlib
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / 'cases.json').read_text())


def invoke(args, cwd=None, timeout=600):
    return subprocess.run(args, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=timeout, check=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', required=True, choices=CASES)
    parser.add_argument('--python', required=True, help='Absolute Python 3.8 executable with group dependencies')
    parser.add_argument('--output', required=True, help='New output directory; existing paths are refused')
    parser.add_argument('--repo-source', help='Optional existing local clone for development; defaults to public GitHub')
    args = parser.parse_args()
    # Preserve the virtualenv launcher path: resolve() follows its symlink to
    # the base interpreter and silently discards the installed dependencies.
    python = pathlib.Path(args.python).expanduser().absolute()
    if not python.is_file():
        parser.error('--python must point to an existing executable')
    out = pathlib.Path(args.output).resolve()
    if out.exists():
        parser.error('Output already exists; choose a new path so prior evidence is preserved')
    out.mkdir(parents=True)
    case = CASES[args.case]
    repo = out / 'verification-repo'
    source = args.repo_source or case['repo']
    clone = ['git', 'clone', '--quiet']
    if not args.repo_source:
        clone += ['--filter=blob:none']
    else:
        clone += ['--shared']
    clone += [source, str(repo)]
    started = time.monotonic()
    result = {'case': args.case, 'repo': case['repo'], 'buggy': case['buggy'],
              'fixed': case['fixed'], 'selector': case['selector'],
              'python': str(python), 'started_utc': datetime.now(timezone.utc).isoformat(),
              'test_source': 'fixed revision test file, used for both checks'}
    try:
        cloned = invoke(clone, timeout=600)
        if cloned.returncode:
            raise RuntimeError('Clone failed: ' + cloned.stdout.decode(errors='replace')[-1200:])
        test_blob = invoke(['git', 'show', case['fixed'] + ':' + case['test_file']], cwd=repo)
        if test_blob.returncode:
            raise RuntimeError('Cannot read fixed test: ' + test_blob.stdout.decode(errors='replace')[-1200:])
        for label, commit in [('buggy', case['buggy']), ('fixed', case['fixed'])]:
            if label == 'fixed':
                invoke(['git', 'reset', '--hard'], cwd=repo)
                # Ignored __pycache__ files can survive a checkout. Historical
                # commits may have equal file sizes and second-level mtimes,
                # causing Python to execute stale buggy bytecode on the fix.
                invoke(['git', 'clean', '-fdx'], cwd=repo)
            checkout = invoke(['git', 'checkout', '--quiet', '--detach', commit], cwd=repo)
            if checkout.returncode:
                raise RuntimeError(label + ' checkout failed: ' + checkout.stdout.decode(errors='replace')[-1200:])
            test_path = repo / case['test_file']
            test_path.parent.mkdir(parents=True, exist_ok=True)
            test_path.write_bytes(test_blob.stdout)
            command = [str(python), '-B', '-m', 'pytest', '-q']
            if case['group'] == 'httpie':
                command.append('--noconftest')
            command.append(case['selector'])
            began = time.monotonic()
            try:
                test = invoke(command, cwd=repo, timeout=180)
                log = test.stdout.decode(errors='replace')
                exit_code = test.returncode
            except subprocess.TimeoutExpired as exc:
                log = (exc.stdout or b'').decode(errors='replace') + '\nTIMEOUT after 180 seconds\n'
                exit_code = 124
            (out / (label + '.log')).write_text(log)
            result[label] = {'exit_code': exit_code, 'seconds': round(time.monotonic() - began, 3),
                             'command': command, 'revision': commit,
                             'assertion_failure': ('FAILED ' in log and 'failed' in log.lower()),
                             'passed': (' passed' in log.lower() and exit_code == 0)}
        result['red_green'] = bool(result['buggy']['assertion_failure'] and result['fixed']['passed'])
        result['status'] = 'screened' if result['red_green'] else 'needs_review'
    except Exception as exc:
        result['status'] = 'setup_error'
        result['error'] = str(exc)
    result['elapsed_seconds'] = round(time.monotonic() - started, 3)
    (out / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result.get(key) for key in ('case', 'status', 'red_green', 'elapsed_seconds', 'error')}, indent=2))
    return 0 if result['status'] == 'screened' else 1


if __name__ == '__main__':
    sys.exit(main())
