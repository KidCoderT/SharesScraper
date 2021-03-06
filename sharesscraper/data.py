import lxml
import json
import requests
import datetime
from bs4 import BeautifulSoup

my_table_data = []
base_url = "https://trendlyne.com/portfolio/superstar-shareholders/index/"
page = requests.get(base_url)
soup = BeautifulSoup(page.content, 'lxml')
page_table = soup.find("div", class_="content-wrapper").find("div", class_="tl_carousel").find("div",
                                                                                               class_="scrolling-wrapper").find(
    "div", class_="row").find("div", class_="card")
page_rows = page_table.find_all("div", class_="dbdr")

index = 1
for div in page_rows:
    dt = datetime.datetime.today()
    splited_data = div.find("div", class_="col-lg-5").find("a").get("href").split('/')
    splited_data[4] = f"Q1-{dt.year}"
    final_string = ""
    if dt.day >= 22:
        final_string = div.find("div", class_="col-lg-5").find("a").get("href")
    else:
        for foo in splited_data:
            final_string += f"/{foo}"
    my_table_data.append((
        div.find("div", class_="col-lg-5").find("a").text,
        div.find_all("div", class_="col-lg-3")[1].text,
        div.find_all("div", class_="col-lg-3")[0].text,
        "https://trendlyne.com" + str(final_string),
        index
    ))

    index += 1

def find_chart_data(chart_box):
    chart_box_data = chart_box.find("div", class_="Ltop nobdr gchart PieChart newE").find("div", class_="nav-link gchartLink active cen full-width").get("data-jsondata")
    return chart_box_data

def detailed_data(url, dataset):
    print(url)
    data = {
        "name": "",
        "heroTile": "",
        "heroSubtitle": []
    }

    chart_data = {
        "boughtSharesInData": {
            "xData": [],
            "yData": []
        },
        "soldSharesIn": {
            "xData": [],
            "yData": []
        },
        "netWorthHistoryData": {
            "xData": [],
            "yData": []
        }
    }

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'lxml')

    data["name"] = dataset[0]

    data["heroTitle"] = soup.find("div", class_="container-fluid content-wrapper").find_all("div", class_="row")[0].find("div", class_="col-md-12 col-xs-12 card m0 p-t-2 p-x-1 p-x-2-md-up nobdrrad").find("div", class_="col-xs-12 m-b-1 p-x-0").find("div", class_="em17").text

    data["heroSubtitle"].append(
        f"As per the latest corporate shareholdings filed, {dataset[0]} publicly holds {dataset[2]} stocks with a net worth of over Rs.{dataset[1]}."
    )
    data["heroSubtitle"].append(
        f"These are shares held by {dataset[0]} as per the shareholding data filed with the exchanges. The latest quarter tends to have missing data since not all companies may have reported their shareholding data till now."
    )

    chart_table = soup.find("div", class_="container-fluid content-wrapper").find_all("div", class_="row")[4].find("div", class_="col-xs-12 card tlcard p-y-2 p-x-1").find("div", class_="tl_carousel").find("div", class_="scrolling-wrapper").find("div", class_="row").find_all("div", class_="col-xs-12 col-md-6 col-lg-4 m-b-1 p-x-0 scroll-card p-x-1")

    net_worth = json.loads(find_chart_data(chart_table[0]))
    del net_worth[0]

    chart_data["netWorthHistoryData"] = {
        "xData": [],
        "yData": []
    }
    for i in net_worth:
        chart_data["netWorthHistoryData"]["xData"].append(i[0])
        chart_data["netWorthHistoryData"]["yData"].append(i[1])

    bought_shares = json.loads(find_chart_data(chart_table[1]))
    for i in range(0, len(bought_shares)):
        del bought_shares[i][2]
    del bought_shares[0]

    chart_data["boughtSharesInData"] = {
        "xData": [],
        "yData": []
    }
    for i in bought_shares:
        chart_data["boughtSharesInData"]["xData"].append(i[0])
        chart_data["boughtSharesInData"]["yData"].append(i[1])

    chart_data["soldSharesIn"] = {
        "xData": [],
        "yData": []
    }

    try:
        sold_shares = json.loads(find_chart_data(chart_table[2]))
        for i in range(0, len(sold_shares)):
            del sold_shares[i][2]
        del sold_shares[0]

        for i in sold_shares:
            chart_data["soldSharesIn"]["xData"].append(i[0])
            chart_data["soldSharesIn"]["yData"].append(i[1])

    except:
        chart_data["soldSharesIn"]["xData"].append("No Data has been sold!!")
        chart_data["soldSharesIn"]["yData"].append(0)

    return data, chart_data
