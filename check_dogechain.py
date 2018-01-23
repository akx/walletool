import argparse
import json
import requests
import sys
import time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file', help='address file; one address per line')
    ap.add_argument('--ignore-empty', action='store_true')
    args = ap.parse_args()
    for line in open(args.file):
        line = line.strip()
        while True:
            r = requests.get('https://dogechain.info/api/v1/address/balance/%s' % line)
            if r.status_code == 429:  # Too Many Requests
                print('Throttled, hold on...', file=sys.stderr)
                time.sleep(60)
                continue
            break
        r.raise_for_status()
        r = r.json()
        if args.ignore_empty and float(r['balance']) == 0:
            continue
        r['addr'] = line
        print(r)
        time.sleep(0.5)

if __name__ == '__main__':
    main()
