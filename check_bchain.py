import json
import re
import requests
import argparse

var_re = re.compile('var (.+?) = (.+?);')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file', help='address file; one address per line')
    ap.add_argument('--coin', required=True, help='e.g. XPM')
    ap.add_argument('--ignore-no-tx', action='store_true')
    args = ap.parse_args()
    for line in open(args.file):
        line = line.strip()
        r = requests.get('https://bchain.info/%s/addr/%s' % (args.coin, line))
        if r.status_code == 404:
            continue
        vs = {}
        for m in var_re.finditer(r.text):
            key, value = m.groups()
            if key == 'startTime':
                continue
            try:
                value = json.loads(value.replace('\'', '"'))
            except json.JSONDecodeError:
                pass
            vs[key] = value
        if args.ignore_no_tx and vs['total_tx'] == 0:
            continue
        print(vs)

if __name__ == '__main__':
    main()