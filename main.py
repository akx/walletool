import argparse
from walletool.wallet_files import read_wallet_dat
from walletool.wallet_items import parse_wallet_dict, KeyWalletItem
from walletool.consts import addressTypes


def main():

    # Parser Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument('-d', '--dat', help='wallet.dat path',
                    required=True, dest='wallet')
    ap.add_argument('-t', '--type',
                    help='address version, as integer, 0xHEX, or any of the following known coins:\n[%s]' % ', '.join(sorted(addressTypes)), required=True)
    args = ap.parse_args()

    # Parser Logic - Checking for hex
    if args.type.startswith('0x'):
        coinType = int(args.type[2:], 16)
    elif args.type.isdigit():  # Else: Use set addressTypes
        coinType = int(args.type)
    else:
        if args.type not in addressTypes:
            raise ValueError('invalid type (see --help)')
        version = addressTypes[args.type]

    # Start reading wallet information
    wallet_data = read_wallet_dat(args.wallet)
    addr_list = ['', '']
    for item in parse_wallet_dict(wallet_data):
        if isinstance(item, KeyWalletItem):
            address = item.get_address(version=coinType)
            privkey = item.get_private_key(version=coinType)
            addr_list[0] += address
            addr_list[1] += privkey
    
    # Log address and private key
    log = input("Save log of Output? (Y/n): ")
    if (log.lower() == "n"):
        print(f'\nAddress:\n{addr_list[0]} \n\nPrivate-Key: \n{addr_list[1]}')
    elif (log.lower() == "y"):
        file_output = open('wallet-output.txt', "w")
        file_output.write(f'Address:\n{addr_list[0]} \n\nPrivate-Key: \n{addr_list[1]}')
        print(f'\nAddress:\n{addr_list[0]} \n\nPrivate-Key: \n{addr_list[1]}')
        print('\n>> Output saved as {wallet-output.txt}. <<')
    else:
        file_output = open('wallet-output.txt', "w")
        file_output.write(f'Address:\n{addr_list[0]} \n\nPrivate-Key: \n{addr_list[1]}')
        print('\n>> Output saved as {wallet-output.txt}. <<')
            


if __name__ == '__main__':
    main()
