import pandas as pd
from .valueinfo import ValueInfo

from enum import Enum


class WrongOrderDateException(Exception):
    pass


class OrderType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    CONDITIONAL_SELL = "CONDITIONAL_SELL"
    CONDITIONAL_BUY = "CONDITIONAL_BUY"


class Orders:

    def __init__(self, buy_fee=0, sell_fee=0):
        self.orders = pd.DataFrame(columns=["date", "type", "confidence"])
        self.buy_fee = 0
        self.sell_fee = 0

    def add_order(self, date: pd.Timestamp, order_type: OrderType, confidence: float):
        if self.orders.shape[0] > 0:
            last_order = self.orders.iloc[-1]
            if last_order.type == order_type:
                print(f"Warning: Last order date:{last_order.date} was of type {last_order.type}")
            if last_order.date >= date:
                raise WrongOrderDateException(f"ERROR: Last order date:{last_order.date}")
        self.orders = self.orders.append({"date": date, "type": order_type, "confidence": confidence},
                                         ignore_index=True)

    def add_buy_order(self, date, confidence=1.0):
        self.add_order(pd.to_datetime(date), OrderType.BUY, confidence)

    def add_sell_order(self, date, confidence=1.0):
        self.add_order(pd.to_datetime(date), OrderType.SELL, confidence)

    def get_num_orders(self):
        return self.orders.shape[0]

    def __iter__(self):
        return OrdersIterator(self)

    def __str__(self):
        out = "Orders:"
        for order in self:
            out = f"{out}\n{order.date} - {order.type}[{order.confidence}]"

        return out


class OrdersIterator:

    def __init__(self, orders):
        # Team object reference
        self._orders = orders
        # member variable to keep track of current index
        self._index = 0

    def __next__(self):
        ''''Returns the next value from team object's lists '''
        if self._index < self._orders.get_num_orders():
            result = self._orders.orders.iloc[self._index]
            self._index += 1
            return result
        # End of Iteration
        raise StopIteration


class Simulation:

    def __init__(self, value_info: ValueInfo, col):
        self.value_info = value_info
        self.value_info._sort()
        self.column = col
        self.df_sim = pd.DataFrame(columns=["date_buy", "date_sell", "confidence", "buy", "sell", "roi", "accum_roi"])

    def calc_for_orders(self, orders: OrderType, confidence=1.0):
        total_inc = 1
        buy_value = None
        buy_date = None

        for order in orders:
            diff_days = (self.value_info.df_values.index - order["date"]).total_seconds()
            value = self.value_info.df_values[diff_days >= 0].iloc[0][self.column]
            if order.type == OrderType.BUY and order.confidence >= confidence:
                buy_value = value
                buy_date = order.date
            elif order.type == OrderType.SELL and order.confidence >= confidence:
                if buy_date is None:
                    raise WrongOrderDateException(f"ERROR: Sell order before buy")

                total_inc = total_inc * value / buy_value
                self.df_sim = self.df_sim.append(
                    {"date_buy": buy_date, "date_sell": order.date, "confidence": confidence,
                     "buy": buy_value, "sell": value, "roi": value / buy_value, "accum_roi": total_inc},
                    ignore_index=True)
                buy_date = None
        return total_inc

    def __str__(self):
        out = "Simulation:"
        nrows = self.df_sim.shape[0]
        for i in range(nrows):
            row = self.df_sim.iloc[i]
            out = f"{out}\n BUY date:{row.date_buy} at {row.buy} - SELL date:{row.date_sell} at {row.sell} - ROI: {round(row.roi, 2)} ACC_ROI: {round(row.accum_roi, 2)}"

        return out
