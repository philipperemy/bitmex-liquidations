import json
import logging
import sys
import threading
from datetime import datetime
from time import sleep

import websocket

logger = logging.getLogger(__name__)


class LiquidationPrinter:
    # Just to have a colorful console.
    class BColor:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    @staticmethod
    def print_header():
        LiquidationPrinter.print_to_console('Symbol', 'B/S', 'USD Value', 'Quantity', 'Price', 'Time')

    @staticmethod
    def print_to_console(symbol, bs, usd_value, qty, price, time):
        if bs == 'Buy':
            is_long = LiquidationPrinter.BColor.OKGREEN
        elif bs == 'Sell':
            is_long = LiquidationPrinter.BColor.FAIL
        else:
            is_long = ''
        line = is_long
        line += symbol.ljust(10)
        line += bs.ljust(6)
        try:
            usd_value = format(int(usd_value), ",d")
        except ValueError:
            pass
        line += usd_value.ljust(12)
        try:
            qty = format(int(qty), ",d")
        except ValueError:
            pass
        line += qty.ljust(10)
        line += '@'.ljust(4)
        line += str(price).ljust(11)
        try:
            time = time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        except AttributeError:
            pass
        line += time
        line += LiquidationPrinter.BColor.ENDC
        logger.info(line)


class BitMEXLiquidation:

    def __init__(self, url='wss://www.bitmex.com/realtime?subscribe=liquidation', symbol=None):
        if symbol is not None:
            url += ':' + symbol
        logger.info("Connecting to %s." % url)
        self._connect(url)
        self.num_pongs = 0
        logger.info('Connected to WS.')
        sleep(5)  # Just wait for BitMEX to answer. Welcome to the BitMEX Realtime API!
        LiquidationPrinter.print_header()

    def exit(self):
        """Call this to exit - will close websocket."""
        logger.info('exit()')
        self.ws.close()

    def _connect(self, url):
        """Connect to the websocket in a thread."""
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_close=self._on_close,
                                         on_open=self._on_open,
                                         on_error=self._on_error,
                                         header=[],
                                         on_pong=self._on_pong)

        # https://www.bitmex.com/app/wsAPI#Heartbeats
        self.wst = threading.Thread(target=lambda: self.ws.run_forever(ping_interval=5),
                                    daemon=False)
        self.wst.start()

    def _on_pong(self, ws, message):
        self.num_pongs += 1

    def _on_message(self, ws, message):
        """Handler for parsing WS messages."""
        message = json.loads(message)
        if 'action' in message and message['action'] == 'insert':
            assert len(message['data']) == 1
            liquidation = message['data'][0]
            qty = float(liquidation['leavesQty'])
            price = float(liquidation['price'])
            side = liquidation['side']
            symbol = liquidation['symbol']
            usd_value = price * qty if not symbol.startswith('XBT') else qty
            LiquidationPrinter.print_to_console(symbol, side, usd_value, qty, price, datetime.now())
        elif 'info' in message:
            logger.info('[<] ' + message['info'])
        elif 'subscribe' in message:
            logger.info('[<] Subscribed to %s' % message['subscribe'] + '.')

    def _on_error(self, ws, error):
        """Called on fatal websocket errors. We exit on these."""
        logger.info('on_error()', error)

    def _on_open(self, ws):
        """Called when the WS opens."""
        logger.info("Websocket Opened.")

    def _on_close(self, ws):
        """Called on websocket close."""
        logger.info('Websocket Closed')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)12s - %(message)s', level=logging.INFO)
    _symbol = sys.argv[1] if len(sys.argv) > 1 else None
    ws = BitMEXLiquidation(symbol=_symbol)
