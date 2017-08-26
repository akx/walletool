walletool ~ a tool for reading wallet.dat files
===============================================

Installation
------------

* Install Python 3.x.
* Install the `bsddb3` module (if you're on Windows, use Gohlke's site).

Extracting private keys from Bitcoin-QT/Litecoin-QT wallets
-----------------------------------------------------------

* Have your `wallet.dat` handy.
* For Bitcoin, run `python wt_extract_keys.py -d wallet.dat -v 0`
* For Litecoin, run `python wt_extract_keys.py -d wallet.dat -v 48`

A list of addresses / private keys is printed.

YMMV :)
