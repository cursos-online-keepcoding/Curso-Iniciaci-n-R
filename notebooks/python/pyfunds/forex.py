from .valueinfo import ValueInfo
import requests
from bs4 import BeautifulSoup
import io
import zipfile
import pandas as pd
import datetime
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

# TODO: https://www.histdata.com/download-free-forex-data/
"""
EUR/USD, EUR/CHF, EUR/GBP, EUR/JPY, EUR/AUD, USD/CAD, USD/CHF, USD/JPY, USD/MXN, GBP/CHF, GBP/JPY, GBP/USD, AUD/JPY, AUD/USD, CHF/JPY, NZD/JPY, NZD/USD, XAU/USD, EUR/CAD, AUD/CAD, CAD/JPY, EUR/NZD, GRX/EUR, NZD/CAD, SGD/JPY, USD/HKD, USD/NOK, USD/TRY, XAU/AUD, AUD/CHF, AUX/AUD, EUR/HUF, EUR/PLN, FRX/EUR, HKX/HKD, NZD/CHF, SPX/USD, USD/HUF, USD/PLN, USD/ZAR, XAU/CHF, ZAR/JPY, BCO/USD, ETX/EUR, EUR/CZK, EUR/SEK, GBP/AUD, GBP/NZD, JPX/JPY, UDX/USD, USD/CZK, USD/SEK, WTI/USD, XAU/EUR, AUD/NZD, CAD/CHF, EUR/DKK, EUR/NOK, EUR/TRY, GBP/CAD, NSX/USD, UKX/GBP, USD/DKK, USD/SGD, XAG/USD, XAU/GBP
"""


class Forex(ValueInfo):
    pair = ""
    base_url = "https://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes"

    valid_pairs = "EUR/USD, EUR/CHF, EUR/GBP, EUR/JPY, EUR/AUD, USD/CAD, USD/CHF, USD/JPY, USD/MXN, GBP/CHF, GBP/JPY, GBP/USD, AUD/JPY, AUD/USD, CHF/JPY, NZD/JPY, NZD/USD, XAU/USD, EUR/CAD, AUD/CAD, CAD/JPY, EUR/NZD, GRX/EUR, NZD/CAD, SGD/JPY, USD/HKD, USD/NOK, USD/TRY, XAU/AUD, AUD/CHF, AUX/AUD, EUR/HUF, EUR/PLN, FRX/EUR, HKX/HKD, NZD/CHF, SPX/USD, USD/HUF, USD/PLN, USD/ZAR, XAU/CHF, ZAR/JPY, BCO/USD, ETX/EUR, EUR/CZK, EUR/SEK, GBP/AUD, GBP/NZD, JPX/JPY, UDX/USD, USD/CZK, USD/SEK, WTI/USD, XAU/EUR, AUD/NZD, CAD/CHF, EUR/DKK, EUR/NOK, EUR/TRY, GBP/CAD, NSX/USD, UKX/GBP, USD/DKK, USD/SGD, XAG/USD, XAU/GBP"
    columns = ["date", "open", "high", "low", "close", "volume"]
    fx_pair = None
    fx_inverted = False

    def __init__(self, fx_base: str, fx_trade: str,
                 start_date: datetime.date = None,
                 end_date: datetime.date = None):
        list_valid_pairs = self.valid_pairs.replace(" ", "").split(",")
        self.fx_base = fx_base.upper()
        self.fx_trade = fx_trade.upper()

        fx_upper_pair = f"{self.fx_base}/{self.fx_trade}"
        if fx_upper_pair in list_valid_pairs:
            self.fx_inverted = False
            self.fx_pair = f"{fx_base.lower()}{fx_trade.lower()}"
        else:
            fx_upper_pair = f"{self.fx_trade}/{self.fx_base}"
            if fx_upper_pair in list_valid_pairs:
                self.fx_inverted = True
                self.fx_pair = f"{fx_trade.lower()}{fx_base.lower()}"
            else:
                raise Exception('fx pair', 'Invalid FX pair')

        if start_date is None:
            self.df_values = pd.DataFrame(columns=self.columns[1:])
        else:
            if end_date is None:
                end_date = datetime.date.today()
            num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

            for inc_month in range(0, num_months + 1):
                new_date = start_date + relativedelta(months=inc_month)
                if new_date.year >= 2020:
                    self.fetch_month(new_date.year, new_date.month)
                else:
                    if self.df_values is None or not any(self.df_values.index.year==new_date.year):
                        self.fetch_month(new_date.year, None)

    def fetch_month(self, year: int, month: int):
        token = self._get_token(year, month)
        df = self._get_month(year, month, token)
        df_forex = pd.concat([self.df_values, df])
        df_forex = df_forex[~df_forex.index.duplicated(keep='first')]
        self.df_values = df_forex.sort_index()

    def _get_token(self, year: int, month: int):
        if month is None:
            url = f"{self.base_url}/{self.fx_pair}/{year}"
        else:
            url = f"{self.base_url}/{self.fx_pair}/{year}/{str(month).zfill(2)}"
        page = requests.get(url)
        if page.status_code != 200:
            return None
        soup = BeautifulSoup(page.content, 'html.parser')
        token = soup.find('form', {'id': 'file_down'}).find("input", {'id': 'tk'}).get_attribute_list("value")[0]
        return token

    def _get_month(self, year, month, token):
        if month is None:
            datemonth = f"{year}"
        else:
            datemonth = f"{year}{str(month).zfill(2)}"
        #smonth = str(month).zfill(2)
        data = {'tk': token,
                'date': year,
                'datemonth': f'{datemonth}',
                'platform': 'ASCII',
                'timeframe': 'M1',
                'fxpair': self.fx_pair.upper()
                }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9,es-ES;q=0.8,es;q=0.7,ca;q=0.6',
            'Cookie': 'cookielawinfo-checkbox-non-necessary=yes; viewed_cookie_policy=yes',
            'Referer': f"{self.base_url}/{self.fx_pair}/{year}/",
            'sec-ch-ua': '"Google Chrome";v="87", " Not;A Brand";v="99", "Chromium";v="87"',
            'sec-ch-ua-mobile': '?0',
            'Sec-Fetch-Dest': 'iframe',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
        }
        page = requests.post("https://www.histdata.com/get.php", data=data, headers=headers)
        zipdata = io.BytesIO(page.content)
        unzipped_data = zipfile.ZipFile(zipdata)
        files = unzipped_data.namelist()
        csv_filename = None
        for f in files:
            if f.endswith(".csv"):
                csv_filename = f

        csv_file = unzipped_data.open(csv_filename)
        df_forex = pd.read_csv(csv_file, sep=";", names=self.columns)
        df_forex["date"] = pd.to_datetime(df_forex["date"], format='%Y%m%d %H%M%S', errors='ignore')
        df_forex["date"] = df_forex.date.dt.tz_localize('EST').dt.tz_convert('CET')
        if self.fx_inverted is False:
            df_forex["open"] = 1/df_forex["open"]
            df_forex["high"] = 1 / df_forex["high"]
            df_forex["low"] = 1 / df_forex["low"]
            df_forex["close"] = 1 / df_forex["close"]
        df_forex = df_forex.set_index("date")
        return df_forex

    def summary(self,resolution='D'):
        # https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#timeseries-offset-aliases
        df_forex = self.df_values
        df_forex["trunc_date"]=df_forex.index.floor(resolution)
        df_forex = df_forex.groupby("trunc_date").agg(
            {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})

        fx = Forex(fx_base=self.fx_base, fx_trade=self.fx_trade)
        fx.df_values = df_forex
        return fx


    def get_forex(self):
        return self.df_values
