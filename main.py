import argparse
from walletool.wallet_files import read_wallet_dat
from walletool.wallet_items import parse_wallet_dict, KeyWalletItem
from walletool.consts import addressTypes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dat', help='wallet.dat path',
                    required=True, dest='filename')
    ap.add_argument('-t', '--type',
                    help='address version, as integer, 0xHEX, or any of the following known coins:\n[%s]' % ', '.join(sorted(addressTypes)), required=True)
    args = ap.parse_args()
    if args.type.startswith('0x'):
        version = int(args.type[2:], 16)
    elif args.type.isdigit():
        version = int(args.type)
    else:
        if args.type not in addressTypes:
            raise ValueError('invalid type (see --help)')
        version = addressTypes[args.type]
    w_data = read_wallet_dat(args.filename)
    addr_tuples = []
    for item in parse_wallet_dict(w_data):
        if isinstance(item, KeyWalletItem):
            address = item.get_address(version=version)
            privkey = item.get_private_key(version=version)
            addr_tuples.append((address, privkey))
    for address, privkey in addr_tuples:
        print(address, privkey)


if __name__ == '__main__':
    main()
