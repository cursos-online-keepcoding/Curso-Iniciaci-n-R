#!/usr/bin/python3
import requests
import json
import datetime
from datetime import datetime as dt
import pandas as pd
from .valueinfo import ValueInfo


def get_ticket(ISIN: str, errors='ignore') -> dict:
    url = f"https://lt.morningstar.com/api/rest.svc/klr5zyak8x/security/screener?page=1&pageSize=10&sortOrder=LegalName%20asc&outputType=json&version=1&languageId=es-ES&currencyId=EUR&universeIds=FOESP%24%24ALL&securityDataPoints=SecId%7CName%7CPriceCurrency%7CTenforeId%7CLegalName%7CClosePrice%7CYield_M12%7CCategoryName%7CAnalystRatingScale%7CStarRatingM255%7CQuantitativeRating%7CSustainabilityRank%7CReturnD1%7CReturnW1%7CReturnM1%7CReturnM3%7CReturnM6%7CReturnM0%7CReturnM12%7CReturnM36%7CReturnM60%7CReturnM120%7CFeeLevel%7CManagerTenure%7CMaxDeferredLoad%7CInitialPurchase%7CFundTNAV%7CEquityStyleBox%7CBondStyleBox%7CAverageMarketCapital%7CAverageCreditQualityCode%7CEffectiveDuration%7CMorningstarRiskM255%7CAlphaM36%7CBetaM36%7CR2M36%7CStandardDeviationM36%7CSharpeM36%7CTrackRecordExtension&filters=&term={ISIN}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Error, unexpected HTTP response code: {r.status_code}")

    json_r = r.json()['rows']
    if len(json_r) != 1:
        if errors == 'ignore':
            return None
        else:
            raise Exception(f"Error ticket not found")

    ticket = json_r[0]
    return ticket


def get_historical_data_from_ticket(ticket: dict,
                                      start_date: datetime.date, end_date: datetime.date = None,
                                      currency: str = None):

    security_id = ticket["SecId"]
    if currency is None:
        currency = ticket["PriceCurrency"]
    if end_date is None:
        end_date = datetime.date.today()
    start_date_str = dt.strftime(start_date, "%Y-%m-%d")
    end_date_str = dt.strftime(end_date, "%Y-%m-%d")

    url = f"https://tools.morningstar.es/api/rest.svc/timeseries_cumulativereturn/2nhcdckzon?id={security_id}&currencyId={currency}&frequency=daily&startDate={start_date_str}&endDate={end_date_str}&outputType=COMPACTJSON"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Error, unexpected HTTP response code: {r.status_code}")
    json_txt = f"""{{"columns":["date","value"], "data":{r.text} }}"""
    # Pandas is smart enough to convert the timestamp into date automatically because the column is called date
    df = pd.read_json(json_txt, orient='split')
    df.value = (df.value + 100)
    return df


class MorningStar(ValueInfo):
    tickets = {}

    def __init__(self, ISINs: list, currency: str = None, start_date: datetime.date = dt(2000, 1, 1)):
        self.currency = currency
        df_values = None
        if ISINs is not None:
            df_values = self.__get_historical_data_ISIN_list(ISINs, currency, start_date)
            if df_values is None:
                raise Exception("ERROR: No fund found!")
        ValueInfo.__init__(self, df_values)

    def _get_historical_data_from_ISIN(self, ISIN: str,
                                        start_date: datetime.date = dt(2018, 1, 1),
                                        currency: str = None) -> pd.DataFrame:
        ticket = get_ticket(ISIN)
        if ticket is None:
            return None
        self.tickets[ISIN] = ticket
        data = get_historical_data_from_ticket(ticket, start_date, currency=currency)
        return data.rename(columns={'value': ISIN}).set_index('date')

    def __get_historical_data_ISIN_list(self, ISINs: list,
                                        currency: str = None,
                                        start_date: datetime.date = dt(2000, 1, 1)):
        df_all = None
        for isin in ISINs:
            df = self._get_historical_data_from_ISIN(isin, currency=currency, start_date=start_date)
            if df_all is None:
                df_all = df
            elif df is not None:
                df_all = df_all.merge(df, on="date", how="outer")

        return df_all
