from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the forex pairs to trade
        self.forex_pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD"]
        # Parameters for the moving averages and breakout
        self.sma_short_window = 10
        self.sma_long_window = 50
        self.breakout_lookback = 20  # Lookback period to determine the breakout high price

    @property
    def assets(self):
        return self.forex_pairs

    @property
    def interval(self):
        return "1day"  # Daily interval for checking the trading signals

    def run(self, data):
        allocation_dict = {}
        for pair in self.forex_pairs:
            sma_short = SMA(pair, data["ohlcv"], self.sma_short_window)[-1]
            sma_long = SMA(pair, data["ohlcv"], self.sma_long_window)[-1]
            current_price = data["ohlcv"][-1][pair]['close']
            past_prices = [data["ohlcv"][i][pair]['close'] for i in range(-self.breakout_lookback, 0)]
            breakout_high = max(past_prices)

            # Check for momentum breakout condition
            # Condition 1: Short SMA crosses above Long SMA indicating a potential uptrend
            # Condition 2: Current price breaks above the recent high, confirming strong momentum
            if sma_short > sma_long and current_price > breakout_high:
                allocation_dict[pair] = 1.0 / len(self.forex_pairs)  # Allocate equally among selected forex pairs
            else:
                allocation_dict[pair] = 0  # No allocation if conditions are not met

        log("Allocations: " + str(allocation_dict))
        return TargetAllocation(allocation_dict)