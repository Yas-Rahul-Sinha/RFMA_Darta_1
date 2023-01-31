import math
import pandas as pd
portfolios = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio')
master_price = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Instrument Master Price')
portfolios = portfolios.transpose()
for port in portfolios:
    index = 0
    for ins in master_price["Security Description"]:
        if(portfolios[port]["Security Description"] == ins):
            portfolios[port]["Market Value"] = portfolios[port]["Units"]*master_price["Price - As of date"][index]
            portfolios[port]["Market Value as of 31st Dec 2022"] = portfolios[port]["Units"]*master_price["Price - 12/31/2022"][index]
            portfolios[port]["Market Value as of 30th Sept 2022"] = portfolios[port]["Units"]*master_price["Price 09/30/2022"][index]
            portfolios[port]["Market Value as of 30th June 2022"] = portfolios[port]["Units"]*master_price["Price 06/30/2022"][index]
            portfolios[port]["Market Value as of 31th March 2022"] = portfolios[port]["Units"]*master_price["Price 03/31/2022"][index]
            portfolios[port]["Market Value as of 31th Dec 2021"] = portfolios[port]["Units"]*master_price["Price 12/31/2021"][index]
            portfolios[port]["Market Value as of 31th Dec 2020"] = portfolios[port]["Units"]*master_price["Price 12/31/2020"][index]
            break
        index+=1
    if math.isnan(portfolios[port]["Market Value"]):
        portfolios[port]["Market Value"] = 0
portfolios = portfolios.transpose()
print(portfolios["Market Value"][5])
import dataframe_image as dfi
# portfolio = pd.read_excel('WM Manager Dashboard Data SetV2.xlsx', sheet_name='Portfolio', usecols=[0, 1, 5, 11])
temp = portfolios.Advisor[0]
rows, columns = portfolios.shape
# print(rows)
# print(temp)
temp2 = portfolios["Investor Name"][0]
bookSum = 0
advisor = {}
investor = {}
iterator = 0
for ind in portfolios.Advisor:
    if ind != temp or iterator == rows-1:
        # print(ind != temp)
        investor.update({temp2: {"Amount": bookSum, "Currency": portfolios["Account Currency"][iterator]}})
        temp2 = portfolios["Investor Name"][iterator]
        bookSum = portfolios["Market Value"][iterator]
        advisor.update({temp:{'Investor Name': investor.copy()}})
        # print(advisor)
        temp = ind
        # print(temp)
        investor.clear()
    elif ind == temp:
        if temp2 != portfolios["Investor Name"][iterator]:
            # print(temp2)
            investor.update({temp2: {"Amount": bookSum, "Currency": portfolios["Account Currency"][iterator]}})
            temp2 = portfolios["Investor Name"][iterator]
            # print(investor)
            bookSum = portfolios["Market Value"][iterator]
        elif temp2 == portfolios["Investor Name"][iterator]:
            bookSum += portfolios["Market Value"][iterator]
            # print(bookSum)

    iterator += 1
# for i in advisor["Advisor 1 "]["Investor Name"]:
    # print(advisor["Advisor 1 "]["Investor Name"][i]["Currency"])
with open('all_dfs.csv','a') as f:
    for adv in advisor:
        f.write(adv)
        f.write('\n')
        f.write('\n')
        for inv in advisor[adv]:
            f.write(inv)
            out = pd.DataFrame(data=advisor[adv][inv]).transpose()
            out.to_csv(f, index='true', lineterminator='\n')
        f.write('\n')
