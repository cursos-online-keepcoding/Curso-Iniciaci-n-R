from datetime import timedelta, date

from pyfunds import ValueInfo
from pyfunds.simulation import OrderType
import pyfunds.simulation as simulation


def daterange(from_date, to_date):
    for n in range(int((to_date - from_date).days)):
        yield from_date + timedelta(n)


class MainRobot:
    orders = None

    def __init__(self, value_info: ValueInfo = None, column_value: str = None):
        self.value_info = value_info
        self.column_value = column_value
        self.column_index = value_info.get_data().columns.get_loc(self.column_value)

    def train(self, from_date, to_date):
        pass

    def calc_buy_order(self, values):
        pass

    def calc_sell_order(self, values):
        pass

    def test(self, from_date, to_date):
        orders = simulation.Orders()
        next_order = OrderType.BUY
        for mydate in daterange(from_date, to_date):
            values = self.value_info.get_data(max_date=mydate)
            if next_order == OrderType.BUY:
                if self.calc_buy_order(values):
                    orders.add_buy_order(mydate)
                    next_order = OrderType.SELL
            elif next_order == OrderType.SELL:
                if self.calc_sell_order(values):
                    orders.add_sell_order(mydate)
                    next_order = OrderType.BUY
        return orders
