import random
from client_instrument import adv_investor_investments
from datautil import *


weights = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,12,10,10,10,12,12,10,12,11,11,10,11,10,10,10,9,8,7,6,5,4]
projected_value = random.choices(range(-20,21), weights=weights, k=1)
# print(projected_value)

def getAccountPortfolio(advisor, investor, account):
    K = len(adv_investor_investments[advisor][investor][account])
    projection = random.choices(range(-20,21), weights=weights, k=K)
    print(projection)
    temp = {}
    portfolio_data = {}
    index = 0
    total_market_value = 0
    total_projected_value = 0
    updn = ""
    for i in adv_investor_investments[advisor][investor][account]:
        temp['Description'] = i['Description']
        temp['Instrument_Type'] = i['Instrument_Type']
        temp['Market Value'] = i['Market Value']
        # print(str(projection[index])+'%')
        temp['Projected Value'] = calculateMarketValue(investor, i['Description'], str(projection[index])+'%')
        if temp['Market Value'] > temp['Projected Value']:
            temp['Up/Down'] = 'Down'
        elif temp['Market Value'] < temp['Projected Value']:
            temp['Up/Down'] = 'Up'
        else:
            temp['Up/Down'] = 'No Impact'
        temp['Percentage Impact'] = percentageImpact(temp['Market Value'], temp['Projected Value'])
        portfolio_data[i['Description']] = temp.copy()
        total_market_value += temp['Market Value']
        total_projected_value += temp['Projected Value']
        index+=1
    if total_projected_value > total_market_value:
        updn = 'Up'
    elif total_market_value > total_projected_value:
        updn = "Down"
    else:
        updn = "No Impact"
    temp['Description'] = "Total"
    temp['Instrument_Type'] = "Total"
    temp['Market Value'] = total_market_value
    temp['Projected Value'] = total_projected_value
    temp['Up/Down'] = updn
    temp['Percentage Impact'] = percentageImpact(total_market_value, total_projected_value)
    portfolio_data["Total"] = temp.copy()
    return portfolio_data


