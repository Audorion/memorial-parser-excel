# Парсинг на Python с Beautiful Soup
# https://pythonru.com/biblioteki/parsing-na-python-s-beautiful-soup
# https://ru.stackoverflow.com/questions/856773/Вывод-в-csv-по-столбцам-python

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from collections import OrderedDict

# Списки демобилизации https://obd-memorial.ru/html/info.htm?id=
START_ID = 60000755815  # 60000755840 ошибка по ID
END_ID = 60000756820
exist_table = False
# 60000758858

df = pd.DataFrame()
for i in range(START_ID, END_ID + 1):
    url = f'https://obd-memorial.ru/html/info.htm?id={i}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    ids = soup.find(id="id_res")
    #    titles = soup.find_all('span', class_="card_param-title")
    titles = soup.find_all('span', class_='card_param-title')
    results = soup.find_all('span', class_='card_param-result')
    titles_text = []
    results_text = []
    for title in titles:
        titles_text.append(title.text)
    for result in results:
        results_text.append(result.text)
    try:
        titles_text.remove('ID')
        dic = dict(OrderedDict(zip(titles_text, results_text)))
        df1 = pd.DataFrame([dic], index=[id.text for id in ids])
        if not exist_table:
            df = df1
            exist_table = True
        else:
            frames = [df, df1]
            df = pd.concat(frames)
    except:
        print("По такому ID нет данных")

df.to_excel("demob.xlsx", encoding='utf-8-sig')
