# BitMEX Liquidation
Minimal code to show how to receive the liquidations in realtime on Bitmex. It does work and does not hang randomly.

<p align="center">
  <img src="banner.png" width="400">
</p>

NOTE: From my experience, even though the feed is realtime according to Bitmex, by the time you receive the liquidation messages, they already happened a few seconds earlier. So it would be hard to profit from it directly. But it could use as a data feature.

## Installation
```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run
```
python example.py               # All instruments.
python example.py XBTUSD        # Only XBTUSD.
```

And be patient! You might have to wait more than one hour to see your first liquidation.

Browse this link for more information: https://app.rek.to/.

## Output

```
2019-11-10 16:33:11,486 - Connecting to wss://www.bitmex.com/realtime?subscribe=liquidation.
2019-11-10 16:33:11,486 - Connected to WS.
2019-11-10 16:33:12,478 - Websocket Opened.
2019-11-10 16:33:12,479 - [<] Welcome to the BitMEX Realtime API.
2019-11-10 16:33:12,479 - [<] Subscribed to liquidation.
2019-11-10 16:33:16,493 - Symbol    B/S   USD Value   Quantity  @   Price     Time
2019-11-10 17:02:34,396 - EOSZ19    Buy   0           600       @   0.0004007 2019-11-10 17:02:34.396
2019-11-10 17:30:08,324 - XBTUSD    Sell  68,000      68,000    @   8829.5    2019-11-10 17:30:08.324
2019-11-10 17:30:14,103 - XBTUSD    Sell  807         807       @   8827.0    2019-11-10 17:30:14.103
2019-11-10 18:44:40,254 - XBTUSD    Sell  1,013       1,013     @   8818.5    2019-11-10 18:44:40.254
```

## Messages

This message corresponds to the first line of the banner:
```json
{ 
   "table":"liquidation",
   "action":"insert",
   "data":[ 
      { 
         "orderID":"8b4a95db-815a-f93a-c9a2-ffbbabeddbac",
         "symbol":"TRXZ19",
         "side":"Buy",
         "price":2.17e-06,
         "leavesQty":5000
      }
   ]
}
```
