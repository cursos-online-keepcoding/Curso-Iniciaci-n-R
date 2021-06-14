import requests
import pandas as pd
import re
import dryscrape
import bs4 as bs
import datetime
from datetime import datetime as dt
import os.path

IDX_COL_AVG = 3
IDX_COL_BIAS = 10




class ForecastFX:

    url = "https://www.fxstreet.com/rates-charts/forecast"
    columns = ["name","avg_week", "bias_week", "avg_month", "bias_month", "avg_quart", "bias_quart" ]

    def __init__(self, csv_file=None):

        self.filename = csv_file
        if csv_file is not None and os.path.isfile(csv_file):
            self.df_forecast = pd.read_csv(csv_file)
        else:
            self.df_forecast = pd.DataFrame(columns=self.columns)

    def _parse_table_data(self, table_data):
        def parse_row(row):
            name = regex.sub('', row[0])
            avg_week = float(row[1].split("\n")[IDX_COL_AVG])
            avg_month = float(row[2].split("\n")[IDX_COL_AVG])
            avg_quart = float(row[3].split("\n")[IDX_COL_AVG])
            bias_week = row[1].split("\n")[IDX_COL_BIAS]
            bias_month = row[2].split("\n")[IDX_COL_BIAS]
            bias_quart = row[3].split("\n")[IDX_COL_BIAS]

            return [name, avg_week, bias_week, avg_month, bias_month, avg_quart, bias_quart]

        regex = re.compile('[^a-zA-Z]')
        table_out = []
        for idx in range(1, len(table_data) - 1):
            row = parse_row(table_data[idx])
            table_out.append(row)
        df_forecast_today = pd.DataFrame(table_out, columns=self.columns)
        today = datetime.date.today()
        df_forecast_today["date"] = dt.strftime(today, "%Y-%m-%d")
        return df_forecast_today

    def get_new_asset(self):
        dryscrape.start_xvfb()
        sess = dryscrape.Session()
        sess.set_attribute('auto_load_images', False)
        sess.visit(self.url)
        sess.wait_for(lambda: sess.at_xpath("//section[contains(@class, 'fxs_widget_summary')]"),timeout=30)
        source = sess.body()

        soup = bs.BeautifulSoup(source, "html.parser")
        html_data = soup.find("section", {'class': "fxs_widget_summary"}).findAll("tr")
        table_data = [[cell.text for cell in row("td")]
                      for row in html_data]
        df_data=self._parse_table_data(table_data)
        self.df_forecast = pd.concat([self.df_forecast, df_data]).drop_duplicates(subset=["name","date"])
        return df_data



    def save(self):
        self.df_forecast.to_csv(self.filename, index=False)

