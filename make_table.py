import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
from pandas import DataFrame

def findtoon(today):
    timetable_df = DataFrame(columns=['title'], index=range(0))
    # tooni_url 뒤에 날짜 문자열을 붙여야됨 형식: YYYYMMDD
    tooni_url = "http://tooniverse.tving.com/tooniverse/schedule?startDate="+today
    htmlcode = urllib.request.urlopen(tooni_url).read()
    soup = BeautifulSoup(htmlcode, "html.parser")

    rank = soup.find_all("td", class_="programInfo")
    for i in rank:
        time = i.find("em", class_="airTime").get_text().split()
        if len(time) == 1:
            timetable_df.loc[time[0]] = [[]]
            title_temp = i.find("div", class_="program").get_text().split()
            title = ""
            for j in title_temp:
                title += j + " "
            title = str(title[:-1])
            timetable_df.iloc[-1]['title'].append(title)
        else:
            title_temp = i.find("div", class_="program").get_text().split()
            title = ""
            for j in title_temp:
                title += j + " "
            title = str(title[:-1]).replace(",", "\",\"")
            timetable_df.iloc[-1]['title'].append(title)

    timetable_df.rename(index={' ': 'time'}, inplace=True)
    timetable_df.to_html("toon" + today + ".html", justify='center')
    # 어떤 글자들 때문에 에러 발생

def findanibox(today):
    year = today[:4]
    month = today[4:6]
    day = today[6:8]
    anibox_url = "http://aniboxtv.com/schedule/day.php?prev=" + year + "-" + month + "-" + day
    htmlcode = urllib.request.urlopen(anibox_url).read()
    soup = BeautifulSoup(htmlcode, "html.parser")

    rank = soup.find_all("table", class_="schedtable")
    tables = str(rank[1])
    timetable_df = pd.read_html(tables)[0].set_index(0)
    timetable_df[1] = timetable_df[1] + timetable_df[2]
    del timetable_df[2]
    del timetable_df[3]
    timetable_df.rename(columns={1:'title'}, inplace=True)
    timetable_df.to_html("anib" + today + ".html", justify='center')



print("7일치 가져오기")
oneday = timedelta(days = 1)
today = datetime.today()
for i in range(7):
    today_edit = str(today.year) + (('0'+str(today.month)) if len(str(today.month))==1 else str(today.month)) + (('0'+str(today.day)) if len(str(today.day))==1 else str(today.day))
    print(today_edit)
    findtoon(today_edit)
    findanibox(today_edit)
    today = today + oneday