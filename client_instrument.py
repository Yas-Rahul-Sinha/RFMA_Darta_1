import pandas as pd
from main import portfolios
from main import advisor
from datautil import fetchMarketValuePercentage

adv_investor_investments = {}
investor_investments = {}
temp1 = []
temp2 = {}
temp3 = {}
for adv in advisor:
    for inv in advisor[adv]["Investor"]:
        index = 0
        for investor in portfolios["Investor Name"]:
            if inv == investor:
                temp2["Instrument_Type"] = portfolios["Instrument Type"][index]
                temp2["Description"] = portfolios["Security Description"][index]
                temp2["Units"] = portfolios["Units"][index]
                temp2["Market Value"] = round(portfolios["Market Value"][index],2)
                temp2["Book Value"] = round(portfolios["Account Investment Book Value"][index],2)
                temp2["Portfolio Weightage"] = fetchMarketValuePercentage(inv, portfolios["Security Description"][index])
                temp2["Account"] = portfolios["Account"][index]
                if index == len(portfolios["Investor Name"])-1:
                    temp1.append(temp2.copy())
                    temp3[temp2["Account"]] = temp1.copy()
                    temp1.clear()
                elif temp2["Account"] != portfolios["Account"][index+1]:
                    temp1.append(temp2.copy())
                    temp3[temp2["Account"]] = temp1.copy()
                    temp1.clear()
                else:
                    temp1.append(temp2.copy())
            index+=1
        investor_investments[inv] = temp3.copy()
        temp3.clear()
    adv_investor_investments[adv] = investor_investments.copy()
    investor_investments.clear()
# print(adv_investor_investments['Advisor 1 '])
# for i in adv_investor_investments["Advisor 1 "]:
#     print(i)


