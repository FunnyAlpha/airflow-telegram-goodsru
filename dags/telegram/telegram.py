import requests
import json
import psycopg2
import pandas as pd

with open("config.json","r") as read_file:

    data = json.load(read_file)


telegram_chatid = data['telegram_chatid']
telegram_token = data['telegram_token']

# print(telegram_chatid)
# print(telegram_token)


telegram_chatid = str(telegram_chatid)


hostname = 'localhost'
username = 'postgres'  # the username when you create the database
password = 'Fender1580'  # change to your password
database = 'goods_parsing'

connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
cur = connection.cursor()

cur.execute("select * from products")

query_rez = cur

# print(query_rez)

r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]

# print(str(r))

message = json.dumps(r,default=str,ensure_ascii=False,indent=4)

cur.close()
connection.close()

# json_output = json.dumps(r,default=str).encode("utf-8")

# print(json_output)


# message = json_output
# print(message)

# send_text = 'https://api.telegram.org/bot'+telegram_token+'/sendMessage?chat_id='+telegram_chatid+'&parse_mode=Markdown&text='+message
# requests.get(send_text)

r = json.loads(message)

pd.set_option('display.max_columns',None)

df = pd.DataFrame(r)

x = []
y = []
z = []
n = []

for i in df["art_id"].unique().tolist():

    df_single = df[df["art_id"]==i].sort_values(by=['date_insert'])

    y.append(df_single['price'].tolist())
    x.append(df_single['date_insert'].tolist())
    z.append(df_single['review_amt'].tolist())
    n.append(df_single['name'].tolist())


# sendImage()

import numpy as np
import matplotlib.pyplot as plt

fig,ax = plt.subplots(len(x),2,figsize = (12,9))

for i in range(len(x)):

    ax[i,0].bar(x[i],y[i])
    ax[i,0].set_title(n[i][1], fontdict={'fontsize': 7})
    ax[i,0].set_xlabel('Дата')
    ax[i,0].set_ylabel('Стоимость')
    ax[i,0].set_facecolor('seashell')

    ax[i,1].bar(x[i],z[i])
    ax[i,1].set_title(n[i][1],fontdict={'fontsize' : 7})
    ax[i,1].set_xlabel('Дата')
    ax[i,1].set_ylabel('Количество отзывов')
    ax[i,1].set_facecolor('seashell')

plt.tight_layout()
plt.savefig("test1.jpg")
# plt.show()

def sendImage():
    url = 'https://api.telegram.org/bot'+telegram_token+'/sendPhoto?chat_id='+telegram_chatid
    files = {'photo': open('test1.jpg', 'rb')}
    r= requests.post(url, files=files)
    # print(r.status_code, r.reason, r.content)

sendImage()