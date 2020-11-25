import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


class sub_class:
    def __init__(self):
        self.summary_info = ""

    def eng_to_upjong(self,summary_info):

        self.summary_info = summary_info

        csv_Data = pd.read_csv("d.csv")
        Data_name_col = csv_Data.iloc[:, 9:11]

        for i in range(Data_name_col.shape[0]):
            if Data_name_col.iloc[i, 1] == self.summary_info:
                find_index = Data_name_col.iloc[i, 0]

        while find_index > 100:
            find_index = find_index / 10

        find_index = int(find_index)

        return find_index
