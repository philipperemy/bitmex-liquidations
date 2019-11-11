import logging
import sys

from bitmex_liquidation import BitMEXLiquidation

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)12s - %(message)s', level=logging.INFO)
    _symbol = sys.argv[1] if len(sys.argv) > 1 else None
    BitMEXLiquidation(symbol=_symbol)
