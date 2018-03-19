# https://medium.com/@danjrod/interactive-brokers-in-python-with-backtrader-23dea376b2fc

# Buy 1 unit as soon as DATA.LIVE is notified ( Market order). A stake of 1 is the default so we will just issue a self.buy()
# Sell 1 unit 3 bars later ( Market order) for which we’ll issue a self.sell()
# The reason: we don’t want to wait for moving averages crossing over or stochatic or rsi indicators going overbought or oversold.



from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt


class St(bt.Strategy):
    def logdata(self):
        txt = []
        txt.append('{}'.format(len(self)))

        txt.append('{}'.format(
            self.data.datetime.datetime(0).isoformat())
        )
        txt.append('{:.2f}'.format(self.data.open[0]))
        txt.append('{:.2f}'.format(self.data.high[0]))
        txt.append('{:.2f}'.format(self.data.low[0]))
        txt.append('{:.2f}'.format(self.data.close[0]))
        txt.append('{:.2f}'.format(self.data.volume[0]))
        print(','.join(txt))

    def next(self):
        self.logdata()

    data_live = False

    def notify_data(self, data, status, *args, **kwargs):
        print('*' * 5, 'DATA NOTIF:', data._getstatusname(status),
              *args)
        if status == data.LIVE:
            self.data_live = True


def run(args=None):
    cerebro = bt.Cerebro(stdstats=False)

    store = bt.stores.IBStore(port=7497)
    data = store.getdata(dataname='TWTR',
                         timeframe=bt.TimeFrame.Ticks)

    cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds,
                         compression=10)

    cerebro.broker = store.getbroker()

    cerebro.addstrategy(St)

    cerebro.run()


if __name__ == '__main__':
    run()