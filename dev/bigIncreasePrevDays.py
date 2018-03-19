'''
if the close is positive i.e. greater than open
and high - close = 0
buy next day and sell 2 days later
'''


import backtrader as bt
from datetime import datetime

class numberIndicatorStrategy(bt.Strategy):

    params = (
        ('num_closes', 9),
        ('num_prior_closes', 4),
    )


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        # Keep a reference to the "open" line in the data[0] dataseries
        self.dataopen = self.datas[0].open
        # Keep a reference to the "High" line in the data[0] dataseries
        self.datahigh = self.datas[0].high
        # Keep a reference to the "High" line in the data[0] dataseries
        self.datalow = self.datas[0].low


    def next(self):
        # self.log('Close, %.2f' % self.dataclose[0])

        if not self.position:
            if self.dataclose[-3] > self.dataopen[-3]:
                if self.dataclose[-2] > self.dataopen[-2]:
                    # if (self.datahigh[-2] - self.dataclose[-2])/self.dataclose[-2] < 0.1: #10%
                    self.buy()
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
        else:
            if self.dataclose[-3] > self.dataopen[-3]:
                if self.dataclose[-2] > self.dataopen[-2]:
                    # if self.dataclose[-1] > self.dataopen[-1]:
                    #     if (self.datahigh[-1] - self.dataclose[-1])/self.dataclose[-1] < 0.1: #10%
                    self.sell()
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])

#starting cash
startCash = 10000

# create a new instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy to cerebro
cerebro.addstrategy(numberIndicatorStrategy)

data = bt.feeds.YahooFinanceData(
    dataname='V',
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
