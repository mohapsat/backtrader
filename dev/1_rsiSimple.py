# dev/1_rsiSimple.py

'''
Entry
    When RSI < 30
Exit
    When RSI > 70
Trade Management and Position Sizing
    No trade management shall be implemented. No scaling in / out. Just simple buying and selling with a single open position at a time.
    Position size wise, we will keep things simple and just buy / sell 100 shares at a time without doing any calculations to see if we have enough cash for position size. (if we don’t have enough cash, backtrader is smart enough to reject the order)
Indicator Settings
    Period = 21
    Lets use a longer look back period than the default 14. In theory this should result in less false signals and price should have to come down / rise much further before it is considered overbought / over sold.
'''

import backtrader as bt
from datetime import datetime


class firstStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data, period = 14)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=100)
                print("executed buy")
        else:
            if self.rsi > 70:
                self.sell(size=100)
                print("executed sell")

#starting cash
startCash = 10000

# create a new instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy to cerebro
cerebro.addstrategy(firstStrategy)

data = bt.feeds.YahooFinanceData(
    dataname='AAPL',
    fromdate=datetime(2016, 1, 1),
    todate=datetime(2018, 1, 1),
    # buffered=True
)

# add data to cerebro
cerebro.adddata(data)

# run cerebro
cerebro.run()

# get final portfolio value
finalPortVal = cerebro.broker.getvalue()
pnl = finalPortVal - startCash

# Print final portfolio value
print('final portfolio value = %2d' % finalPortVal)
print('PnL = %2d' % pnl)

# plot
cerebro.plot()
