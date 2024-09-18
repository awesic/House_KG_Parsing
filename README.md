
# **Market Analysis Lab for the Automotive Sector**

Below you will find a script for parsing data from the [Mashina.kg](https://m.mashina.kg/search/all) website. There is also a parsing script `parsing.py` that you can run.
Retrieve new data and compare the market conditions with historical data `Mashina_kg_10k.csv` from April 2023. Perform in-depth analytics and visualization.


When running the script, you need to specify the number of pages you want to parse. Each page on the website contains 20 listings.
There can be around 1500 pages in total, but verify this number on the [website](https://m.mashina.kg/search/all).


```
git clone https://github.com/simonlobgromov/Mashina_KG_Parsing
cd Mashina_KG_Parsing
pip install -r requirements.txt

python parsing.py
```

# Рекоммендации

* Процесс получения ссылок изолировать. И все ссылки сохранить как csv (txt)
* Процесс парсинга исуществлять на основании чтения дока с сылками.
* Каждые 50-100 спарсенных объяв сохранять (дополнять в файл)
* Логгирование - в отдельный файл
