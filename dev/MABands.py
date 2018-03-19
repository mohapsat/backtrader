'''
if the close is positive i.e. greater than open
and high - close = 0
buy next day and sell 2 days later
'''


import backtrader as bt
from datetime import datetime
import backtrader.analyzers as btanalyzers

class MABandStrategy(bt.Strategy):

    params = (
        ('num_closes', 9),
        ('num_prior_closes', 4),
        ('maperiod',20)
    )


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open

        # Add a MovingAverageSimple indicator
        self.sma50 = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.params.maperiod)
        self.sma50Open = bt.indicators.SimpleMovingAverage(self.datas[0].open, period=self.params.maperiod)
        # self.middleband = bt.indicators.SimpleMovingAverage(self.datas[0] + self.datas[0]*0.025, period=50)
        self.sma200 = bt.indicators.SimpleMovingAverage(self.datas[0], period=200)
        self.sma50upperband2 = bt.indicators.SimpleMovingAverage(self.datas[0] + self.datas[0]*0.1, period=self.params.maperiod)
        self.sma50upperband1 = bt.indicators.SimpleMovingAverage(self.datas[0] + self.datas[0]*0.05, period=self.params.maperiod)
        self.sma50lowerband2 = bt.indicators.SimpleMovingAverage(self.datas[0] - self.datas[0]*0.05, period=self.params.maperiod)


    def next(self):

# Buy when:
# close[-1] < middleband[-1]
# close[0] >= middleband[0]


# Sell when
# close[0] >= sma50upperband2_60[0]
# close[-1] < sma50upperband2_60[-1]

        if not self.position:
            if self.dataclose[-1] < self.sma50[-1]:
                if self.dataclose[0] >= self.sma50[0]:
                    self.buy()
                    self.log('BUY CREATE AT OPEN, %.2f' % self.dataopen[0])
        else:
            if self.dataopen[-1] < self.dataopen[0]:
                if self.dataopen[0] >= self.sma50upperband1[0]:
                    self.sell()
                    self.log('SELL CREATE AT CLOSE, %.2f' % self.dataopen[0])

#starting cash
startCash = 10000

# create a new instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy to cerebro
cerebro.addstrategy(MABandStrategy)

data = bt.feeds.YahooFinanceData(
    dataname='V',
    fromdate=datetime(2016, 1, 1),
    todate=datetime(2018, 4, 1),
    # buffered=True
)

# add data to cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(startCash)

# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=100)

# Add the analyzers we are interested in
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='mysharpe_a')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

# run cerebro
strategies = cerebro.run()
MABandStrat = strategies[0]

# get final portfolio value
finalPortVal = cerebro.broker.getvalue()
pnl = finalPortVal - startCash

# Print final portfolio value
print('final portfolio value = %2d' % finalPortVal)
print('PnL = %2d' % pnl)


# print the analyzers
print('Sharpe Ratio:', MABandStrat.analyzers.mysharpe.get_analysis())
print('Sharpe_A Ratio:', MABandStrat.analyzers.mysharpe_a.get_analysis())
print('DrawDown:', MABandStrat.analyzers.drawdown.get_analysis())


# plot
cerebro.plot(style='candlestick',barup='green', bardown='red')
