import pandas as pd
import datetime as dt


class Tracker:
    def __init__(self):
        try:
            self.df = pd.read_csv("log.csv", index_col="Date")
            print("Dataframe imported")
        except FileNotFoundError:
            print('Creating new dataframe...')
            dictionary = {"Date": [dt.datetime.today().strftime("S%Y%m%d")]}
            self.df = pd.DataFrame.from_dict(dictionary)
            self.df.set_index("Date", inplace=True)

        self.df.drop(index=self.df.index[self.df.isnull().all(1)], inplace=True)

    def save_df(self):
        self.df.to_csv("log.csv")

    def add_price(self, product, price, date: dt.datetime = dt.datetime.today()):
        """Record price for product at specified date."""
        self.df.at[date.strftime("S%Y%m%d"), product.title()] = price
        self.save_df()

    def price_threshold(self, product: str):
        """Calculate threshold price at Mean-2*stD."""
        if product.title() in self.df.columns.values:
            mean = self.df[product.title()].mean()
            std = self.df[product.title()].std()
            threshold = mean - (1.5 * std)
            print(f"Threshold price: {threshold}")
            return threshold
        else:
            print("Product prices not found")

    def remove_column(self, column):
        self.df.drop(columns=column, inplace=True)
        self.save_df()

#
# class Watchlist:
#     def __init__(self):
#         try:
#             self.df = pd.read_csv("watchlist.csv")
#         except FileNotFoundError:
#             dictionary = {"url":[]}
#             self.df = pd.DataFrame.from_dict(dictionary)
#
#         self.df.drop(index=self.df.index[self.df.isnull().all(1)], inplace=True)
#
#     def values(self):
#         return self.df['url'].values
#
#     def add_url(self, url):
#         self.df.at[len(self.df), 'url'] = url
#         self.save_df()
#
#     def save_df(self):
#         self.df.to_csv("watchlist.csv")


if __name__ == "__main__":
    my_tracker = Tracker()
    my_tracker.save_df()

