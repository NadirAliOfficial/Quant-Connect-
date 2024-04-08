import quantconnect as qc
import pandas as pd
from datetime import timedelta

class RankIndicator(qc.Indicator):
    def __init__(self, quandl_code):
        self.rank = self.AddData(qc.QuandlWmData(quandl_code))

    def Update(self, context, data):
        self.rank[-1] = self.rank[-1][-1]

class RankBasedStrangleAlgorithm(qc.Algorithm):
    def __init__(self, quandl_code):
        self.rank_indicator = RankIndicator(quandl_code)
        self.short_date = None
        self.long_date = None

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetCash(100000)
        self.SetWarmUp(50)
        self.SetBrokerageModel(qc.BrokerageName.InteractiveBrokersBrokerage, AccountType.Margin)

        self.symbol = self.AddEquity('SPY', leverage=1.0).Symbol

        self.Schedule.On(self.DateRules.EveryDay('SPY'), self.TimeRules.AfterMarketOpen('SPY', 30), self.ComputeDates)

    def OnData(self, slice):
        if not self.short_date or not self.long_date:
            return

        if self.rank_indicator.rank.Current.Value > 90:
            self.short_strangle(slice)

    def short_strangle(self, slice):
        short_call = None
        short_put = None

        options = slice.OptionChains
        if options is not None:
            chain = options[self.symbol]
            contracts = list(chain)
            contracts = [x for x in contracts if x.Expiry == self.short_date]

            if len(contracts) > 0:
                contracts = sorted(contracts, key=lambda x: abs(x.Strike - self.Securities[self.symbol].Price))
                for contract in contracts:
                    if contract.Right == qc.Right.Call and contract.Delta < 0.1:
                        short_call = contract
                        break

                for contract in contracts:
                    if contract.Right == qc.Right.Put and contract.Delta < -0.1:
                        short_put = contract
                        break

        if short_call and short_put:
            self.MarketOrder(short_call.Symbol, -1)
            self.MarketOrder(short_put.Symbol, -1)

    def ComputeDates(self):
        self.short_date = self.Time + timedelta(days=30)
        self.long_date = self.Time + timedelta(days=45)

# Replace 'YOUR_QUANDL_CODE' with the actual Quandl code for your ranking data
qc.Run(RankBasedStrangleAlgorithm('YOUR_QUANDL_CODE'))
