import random
import pyfunds.simulation as simulation
from pyfunds import ValueInfo
from pyfunds.robots import MainRobot


class MovingAverage(MainRobot):

    def __init__(self, value_info: ValueInfo, column_value:str, short_period=5, long_period=60):
        if short_period >= long_period:
            raise Exception(f"Error: short_period={short_period} must be lower than long_period={long_period}")
        self.short_period = short_period
        self.long_period = long_period
        MainRobot.__init__(self, value_info, column_value)

    def _calc_buy_sell(self, df_values):
        mn_short_now = df_values.iloc[-self.short_period:-1, self.column_index].mean()
        mn_long_now = df_values.iloc[-self.long_period:-1, self.column_index].mean()
        if mn_long_now < mn_short_now:
            return True
        else:
            return False

    def calc_buy_order(self, df_values):
        return self._calc_buy_sell(df_values)

    def calc_sell_order(self, df_values):
        return not self._calc_buy_sell(df_values)
