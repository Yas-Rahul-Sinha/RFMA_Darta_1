import pandas as pd
from main import portfolios
from main import advisor

adv_investor_investments = {}
investor_investments = {}
temp1 = []
temp2 = {}
for adv in advisor:
    for inv in advisor[adv]["Investor Name"]:
        index = 0
        for investor in portfolios["Investor Name"]:
            if inv == investor:
                temp2["Instrument_Type"] = portfolios["Instrument Type"][index]
                temp2["Description"] = portfolios["Security Description"][index]
                temp2["Units"] = portfolios["Units"][index]
                temp2["Market Value"] = portfolios["Market Value"][index]
                temp2["Book Value"] = portfolios["Account Investment Book Value"][index]
                temp1.append(temp2.copy())
            index+=1
        investor_investments[inv] = temp1.copy()
        temp1.clear()
    adv_investor_investments[adv] = investor_investments.copy()
    investor_investments.clear()
# for i in adv_investor_investments["Advisor 1 "]:
#     print(i)


