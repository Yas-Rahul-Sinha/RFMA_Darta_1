import pandas as pd
from main import portfolios

market = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Market News')
advisor_list = ["Advisor 1 ", "Advisor 2 ", "Advisor 3 ", "Advisor 4 "]
temp = []
adv_market_temp = {}
adv_market = {}
market = market.transpose()

for i in advisor_list:
    index = 0
    for j in portfolios["Advisor"]:
        if i == j and portfolios["Security Description"][index] not in temp:
            temp.append(portfolios["Security Description"][index])
        index+=1
    adv_market_temp[i] = temp.copy()
    temp.clear()
for advisor in adv_market_temp:
    for security in adv_market_temp[advisor]:
        for sec in market:
            if market[sec]["Description"] == security:
                market[sec]["Market News - Date"] = str(market[sec]["Market News - Date"])
                temp.append(market[sec].to_dict())
    adv_market[advisor] = temp.copy()
    temp.clear()
# print(adv_market['Advisor 1 '])



