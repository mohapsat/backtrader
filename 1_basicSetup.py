from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt

if __name__ == '__main__':

    cerebro = bt.Cerebro()  # instantiate cerebro engine
    # cerebro engine creates a broker  instance in the background w some cash (10K default) to start
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run() # run cerebro engine (loop over data)
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
