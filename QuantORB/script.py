from AlgorithmImports import *

class OpeningRangeBreakoutAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)
        
        # Universe selection
        self.UniverseSettings.Resolution = Resolution.Minute
        self.AddUniverse(self.CoarseSelectionFunction)
        
        # Schedule the ORB strategy to run at the beginning of each trading day
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen("SPY", 5), self.ORBStrategy)
        
        # Dictionary to store high and low prices for each stock
        self.high = {}
        self.low = {}

    def CoarseSelectionFunction(self, coarse):
        # Filtering universe based on price and volume criteria
        selected = [x.Symbol for x in coarse if x.HasFundamentalData and x.Price > 5 and x.DollarVolume > 1000000]
        return selected

    def ORBStrategy(self):
        # Fetch the top 20 stocks with highest relative volume
        top_stocks = self.GetTopRelativeVolumeStocks(20)
        
        # Trade each stock based on ORB strategy
        for symbol in top_stocks:
            if self.Securities[symbol].Price > self.high[symbol]:
                self.SetHoldings(symbol, 1)
            elif self.Securities[symbol].Price < self.low[symbol]:
                self.Liquidate(symbol)

    def OnData(self, data):
        pass
    
    def OnSecuritiesChanged(self, changes):
        for security in changes.RemovedSecurities:
            if security.Invested:
                self.Liquidate(security.Symbol)
    
    def GetTopRelativeVolumeStocks(self, count):
        # Fetch volume data for the last 14 days
        history = self.History(["SPY"], 14, Resolution.Daily)
        if not history.empty:
            avg_volume = history.loc["SPY"]["volume"].mean()
        else:
            return []
        
        # Calculate relative volume for each stock
        relative_volumes = {}
        for symbol in self.Securities.Keys:
            if symbol == "SPY":
                continue
            security = self.Securities[symbol]
            volume = security.Volume
            relative_volume = volume / avg_volume
            relative_volumes[symbol] = relative_volume
        
        # Sort stocks by relative volume and get top 'count' stocks
        top_stocks = sorted(relative_volumes, key=relative_volumes.get, reverse=True)[:count]
        
        return top_stocks

# Create your algorithm instance
algorithm = OpeningRangeBreakoutAlgorithm()

# Set up the Interactive Brokers connection
algorithm.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage,
                            AccountType.Margin)

# Set the data resolution for the backtest
algorithm.SetStartDate(2020, 1, 1)
algorithm.SetEndDate(2021, 1, 1)
algorithm.SetCash(100000)

# Run the backtest
backtest = algorithm.RunBacktest()

# Plot the results
backtest.plot()
