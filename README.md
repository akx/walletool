# Walletool - Read wallet.dat files

## Access [Bitcoin-Core](https://bitcoin.org/en/bitcoin-core/) and [Litecoin-Core](https://litecoin.org/) wallets __addresses__ and __private keys__

-----------------------------------------------------------

## Requirements

* Install python 3.6+
* Install `requirements.py` by running:
  * `$pip install -r requirements.txt`
* Your wallet must be **UNENCRYPTED**!

## Installation

<!-- - Install the `bsddb3` module (if you're on Windows, use Gohlke's site). -->


-----------------------------------------------------------

## Wallet location on different OS's

### _Linux_

* `~/.bitcoin/wallets/[WALLET_NAME]/wallet.dat`

### _Windows_

default location:  

* TODO: Add default location

-----------------------------------------------------------
### Types / CoinType

* For Bitcoin, run `python3 main.py -d wallet.dat -v 0`
* For Litecoin, run `python3 main.py -d wallet.dat -v 48`

-----------------------------------------------------------

### _Output_

Print / Log - Wallet addresses and private keys

<!-- Install berkely DB
https://www.linuxfromscratch.org/blfs/view/svn/server/db.html

Alt: 
  `$ sudo apt install libdb-dev && pip install bsddb3` -->