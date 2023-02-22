import pandas as pd
from main import portfolios
# for i in portfolios["Investor Name"]:
#     print(i)
def fetchMarketValue(client, instrument):
    index = 0
    for cli in portfolios["Investor_Name"]:
        if cli == client and portfolios["Security_Description"][index] == instrument:
            return round(portfolios["Market_Value"][index],2)
        index+=1


def calculateMarketValue(client, instrument, input):
    index = 0
    type = input.split('%')
    current_market_value = fetchMarketValue(client, instrument)
    for cli in portfolios["Investor_Name"]:
        if cli == client and portfolios["Security_Description"][index] == instrument:
            if len(type) == 1:
                return round(current_market_value + float(input),2)
            elif len(type) == 2:
                return round(((float(type[0])/100)*current_market_value) + current_market_value,2)
            else:
                return "PLease Enter value in Proper Format"
        index+=1

def totalMarketValue(client):
    total_market_value = 0
    index=0
    for cli in portfolios["Investor_Name"]:
        if cli == client:
            total_market_value += portfolios["Market_Value"][index]
        index+=1
    return round(total_market_value,2)

def totalBookValue(client):
    total_book_value = 0
    index = 0
    for cli in portfolios["Investor_Name"]:
        if cli == client:
            total_book_value += portfolios["Account_Investment_Book_Value"][index]
        index += 1
    return round(total_book_value,2)

def newTotalMarketValue(client, instrument, input):
    current_total_market_value = totalMarketValue(client)
    current_instrument_market_value = fetchMarketValue(client,instrument)
    new_instrument_market_value = calculateMarketValue(client,instrument,input)
    return round(current_total_market_value-current_instrument_market_value+new_instrument_market_value,2)

def clientTotalValueAnalysis(book_value,old_value,new_value):
    res = {}
    market_value_change = round(((new_value-old_value)/old_value)*100,2)
    original_market_to_book_value = round(((old_value-book_value)/book_value)*100,2)
    new_market_to_book_value = round(((new_value-book_value)/book_value)*100,2)
    res["market_value_change"] = market_value_change
    res["original_market_to_book_value"] = original_market_to_book_value
    res["new_market_to_book_value"] = new_market_to_book_value
    return res

def overallCalculations(data):
    cmv = []
    nmv = []
    ctmv = totalMarketValue(data[0]['client'])
    ctbv = totalBookValue(data[0]['client'])
    for i in data:
        cmv.append(fetchMarketValue(i['client'], i['instrument']))
        nmv.append(calculateMarketValue(i['client'], i['instrument'], i['input']))
    dmv = [a - b for a, b in zip(nmv, cmv)]
    ocmv = sum(dmv)
    ntmv = ctmv + ocmv
    percent_change_mv = round((ocmv/ctmv)*100,2)
    nmv_to_bv = round(((ntmv-ctbv)/ctbv)*100,2)
    res = {'percent_change_mv':percent_change_mv, 'nmv_to_bv':nmv_to_bv}
    return res

def fetchMarketValuePercentage(client, instrument):
    totalMV = totalMarketValue(client)
    instrumentMV = fetchMarketValue(client,instrument)
    return round(((instrumentMV/totalMV)*100),2)

def percentageImpact(market_value, projected_value):
    if market_value != 0:
        return round((((projected_value-market_value)/market_value)*100),2)
    else:
        return 0

def getClientForInstrument(instrument, advisor):
    filter_df = portfolios[portfolios["Security_Description"] == instrument]
    filter_df = filter_df[filter_df["Advisor"] == advisor]
    # print(filter_df[["Investor_Name","Investor_Type_Desc","Account","Security_Description", "Account_Investment_Book_Value", "Market_Value"]])
    return filter_df[["Investor_Name","Investor_Type_Desc","Account","Security_Description", "Account_Investment_Book_Value", "Market_Value"]]

def impactOnAccount(account, instrument, projected_market_value):
    data = portfolios[portfolios["Account"] == account]
    index = data.index
    total_market_value = data["Market_Value"].sum()
    currrent_market_value = fetchMarketValue(data["Investor_Name"][index[0]],instrument)
    diff = projected_market_value - currrent_market_value
    percentage_impact = (diff/total_market_value)*100
    return round(percentage_impact,3)
def marketSignalImpact(instrument, advisor, input):
    data = getClientForInstrument(instrument,advisor)
    index = data.index
    pointer = 0
    temp = {}
    return_data = []
    for i in data["Investor_Name"]:
        projected_value = calculateMarketValue(i, instrument, input)
        if projected_value > data["Market_Value"][index[pointer]]:
            up_down = "Up"
        elif projected_value < data["Market_Value"][index[pointer]]:
            up_down = "Down"
        else:
            up_down = "No Impact"
        percentage_impact = impactOnAccount(data["Account"][index[pointer]],instrument,projected_value)
        temp["Investor_Name"] = i
        temp["Account"] = data["Account"][index[pointer]]
        temp["Market_Value"] = data["Market_Value"][index[pointer]]
        temp["Projected_Value"] = projected_value
        temp["Up/Down"] = up_down
        temp["Percentage_Impact"] = percentage_impact
        return_data.append(temp.copy())
        pointer+=1
    return {"data": return_data}
