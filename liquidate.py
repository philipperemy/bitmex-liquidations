import json
import threading
import sys
import websocket
import logging

logger = logging.getLogger(__name__)

class BitMEXLiquidation:

    def __init__(self, url='wss://www.bitmex.com/realtime?subscribe=liquidation', symbol=None):
        if symbol is not None:
            url += ':' + symbol
        logger.info("Connecting to %s" % url)
        self._connect(url)
        self.num_pongs = 0
        logger.info('Connected to WS.')

    def exit(self):
        '''Call this to exit - will close websocket.'''
        logger.info('exit()')
        self.exited = True
        self.ws.close()

    def _connect(self, url):
        '''Connect to the websocket in a thread.'''
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_close=self._on_close,
                                         on_open=self._on_open,
                                         on_error=self._on_error,
                                         header=[],
                                         on_pong=self._on_pong)

        # https://www.bitmex.com/app/wsAPI#Heartbeats
        self.wst = threading.Thread(target=lambda: self.ws.run_forever(ping_interval=5))
        self.wst.daemon = False
        self.wst.start()

    def _on_pong(self, ws, msg):
        if self.num_pongs % 100 == 0:
            logger.info('Waiting for liquidation... Might take a while... Check https://app.rek.to/')
        self.num_pongs += 1

    def _on_message(self, ws, message):
        '''Handler for parsing WS messages.'''
        message = json.loads(message)
        logger.info(json.dumps(message, indent=2, sort_keys=True))

    def _on_error(self, ws, error):
        '''Called on fatal websocket errors. We exit on these.'''
        logger.info('on_error()', error)

    def _on_open(self, ws):
        '''Called when the WS opens.'''
        logger.info("Websocket Opened.")

    def _on_close(self, ws):
        '''Called on websocket close.'''
        logger.info('Websocket Closed')


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)12s - %(message)s', level=logging.INFO)
    _symbol = sys.argv[1] if len(sys.argv) > 1 else None
    ws = BitMEXLiquidation(symbol=_symbol)
