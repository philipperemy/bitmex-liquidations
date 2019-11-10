# BitMEX Liquidation
Minimal code to show how to receive the liquidations in realtime on Bitmex.

## Installation
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```
python liquidate.py               # All instruments.
python liquidate.py XBTUSD        # Only XBTUSD.
```

Useful links: https://app.rek.to/
