#下載資料套件
import urllib3
from bs4 import BeautifulSoup

#資料處理套件
import pandas as pd
from datetime import datetime, date

#畫圖套件
import matplotlib.pyplot as plt
#%matplotlib inline -- IPython中的魔法函數(Magic Function)

print("查詢日期區間")
queryStartDate = input()
queryEndDate = input()

# Part 1: 下載期交所30天內選擇權Put/Call Ratio
http = urllib3.PoolManager()
url = "https://www.taifex.com.tw/cht/3/pcRatio"
res = http.request(
     'GET',
      url,
      fields={
         'queryStartDate': queryStartDate,
         'queryEndDate': queryEndDate
      }
 )
html_doc = res.data
#print(html_doc)

soup = BeautifulSoup(html_doc, 'html.parser')
table = soup.table
df = pd.read_html(str(table))
pc_ratio = df[3]
#print(pc_ratio)

# Part 2 : 將下載的個股資料另存成csv檔
pc_ratio.to_csv("pc_ratio.csv", encoding='big5')

# Part 3 : 畫出選擇權Put/Call Ration
# 資料轉型：把日期從字串(string)換成時間(datetime)
for row in range(pc_ratio.shape[0]):
    date2 = pc_ratio.iloc[row, 0].split('/')
    pc_ratio.iloc[row, 0] = datetime(int(date2[0]), int(date2[1]), int(date2[2]))

pc_ratio.head(10)

fig = plt.figure(figsize = (20, 5))
plt.title('TXO Put/Call Ratio')

plt.plot(pc_ratio['日期'], pc_ratio['買賣權成交量比率%'])
plt.plot(pc_ratio['日期'], pc_ratio['買賣權未平倉量比率%'])

plt.legend(['Put/Call Volume Ratio%', 'Put/Call OI Ratio%'])
print(pc_ratio)
plt.show()

print('1211')