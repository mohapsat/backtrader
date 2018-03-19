# REF
# https://www.backtrader.com/docu/analyzers/analyzers.html#a-quick-example
# https://backtest-rookies.com/2017/06/11/using-analyzers-backtrader/

import backtrader as bt
from datetime import datetime
from collections import OrderedDict


class MyStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period = 21)

    def next(self):

        if not self.position:
            if self.rsi < 30:
                self.buy(size=10)
        else:
            if self.rsi > 70:
                self.sell(size=10)


def printTradeAnalysis(analyzer):
    '''
    Function to print the Technical Analysis results in a nice format.
    '''
    # Get the results we are interested in
    total_open = analyzer.total.open
    total_closed = analyzer.total.closed
    total_won = analyzer.won.total
    total_lost = analyzer.lost.total
    win_streak = analyzer.streak.won.longest
    lose_streak = analyzer.streak.lost.longest
    pnl_net = round(analyzer.pnl.net.total, 2)
    strike_rate = (total_won / total_closed) * 100
    # Designate the rows
    h1 = ['Total Open', 'Total Closed', 'Total Won', 'Total Lost']
    h2 = ['Strike Rate', 'Win Streak', 'Losing Streak', 'PnL Net']
    r1 = [total_open, total_closed, total_won, total_lost]
    r2 = [strike_rate, win_streak, lose_streak, pnl_net]
    # Check which set of headers is the longest.
    if len(h1) > len(h2):
        header_length = len(h1)
    else:
        header_length = len(h2)
    # Print the rows
    print_list = [h1, r1, h2, r2]
    row_format = "{:<15}" * (header_length + 1)
    print("Trade Analysis Results:")
    for row in print_list:
        print(row_format.format('', *row))


def printSQN(analyzer):
    sqn = round(analyzer.sqn, 2)
    print('SQN: {}'.format(sqn))





# Variable for our starting cash
startcash = 100000

# Create an instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy
cerebro.addstrategy(MyStrategy)

# Get Apple data from Yahoo Finance.
data = bt.feeds.YahooFinanceData(
    dataname='AAPL',
    fromdate=datetime(2009, 1, 1),
    todate=datetime(2017, 1, 1),
    buffered=True
)

# Add the data to Cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(startcash)

# Add the analyzers we are interested in
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
cerebro.addanalyzer(bt.analyzers.SQN, _name="sqn")
cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(bt.analyzers.SharpeRatio_A, _name='mysharpe_a')
cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')

# Run over everything
strategies = cerebro.run()
firstStrat = strategies[0]

# print the analyzers
printTradeAnalysis(firstStrat.analyzers.ta.get_analysis())
printSQN(firstStrat.analyzers.sqn.get_analysis())
print('Sharpe Ratio:', firstStrat.analyzers.mysharpe.get_analysis())
print('Sharpe_A Ratio:', firstStrat.analyzers.mysharpe_a.get_analysis())
print('DrawDown:', firstStrat.analyzers.drawdown.get_analysis())
# Get final portfolio Value
portvalue = cerebro.broker.getvalue()

# Print out the final result
print('Final Portfolio Value: ${}'.format(portvalue))

# Finally plot the end results
cerebro.plot(style='candlestick')