from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import BB
from surmount.logging import log

class TradingStrategy(Strategy):
    @property
    def assets(self):
        # The assets that this strategy will operate on
        # In this case, we're focused solely on SPY for shorting
        return ["SPY"]

    @property
    def interval(self):
        # Defines the time interval for the data points.
        # This can vary based on how frequently you want to trade or check for signals.
        return "1day"

    def run(self, data):
        # Initialize allocation with no position as default
        allocation_dict = {"SPY": 0}
        
        # Assuming data contains OHLCV information for SPY
        spy_data = data["ohlcv"]
        
        # Calculate the Bollinger Bands for SPY using a 20-day period and standard deviation of 2 
        # which are common parameters for Bollinger Bands.
        spy_bbands = BB("SPY", spy_data, 20, 2)
        
        if len(spy_data) < 20:
            # If there's not enough data to compute Bollinger Bands, do nothing.
            return TargetAllocation(allocation_dict)
        
        current_price = spy_data[-1]["SPY"]['close']
        upper_band = spy_bbands['upper'][-1]
        
        if current_price > upper_band:
            # If the current closing price of SPY is above the upper band,
            # it suggests the stock is potentially overbought, so we short SPY.
            log("Shorting SPY")
            allocation_dict["SPY"] = -1  # A negative value indicates a short position
        
        return TargetAllocation(allocation_dict)