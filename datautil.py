import pandas as pd
from main import portfolios
# for i in portfolios["Investor Name"]:
#     print(i)
def fetchMarketValue(client, instrument):
    index = 0
    for cli in portfolios["Investor Name"]:
        if cli == client and portfolios["Security Description"][index] == instrument:
            return portfolios["Market Value"][index]
        index+=1


def calculateMarketValue(client, instrument, input):
    index = 0
    type = input.split('%')
    current_market_value = fetchMarketValue(client, instrument)
    for cli in portfolios["Investor Name"]:
        if cli == client and portfolios["Security Description"][index] == instrument:
            if len(type) == 1:
                return current_market_value + float(input)
            elif len(type) == 2:
                return ((float(type[0])/100)*current_market_value) + current_market_value
            else:
                return "PLease Enter value in Proper Format"
        index+=1

def totalMarketValue(client):
    total_market_value = 0
    index=0
    for cli in portfolios["Investor Name"]:
        if cli == client:
            total_market_value += portfolios["Market Value"][index]
        index+=1
    return total_market_value

def totalBookValue(client):
    total_book_value = 0
    index = 0
    for cli in portfolios["Investor Name"]:
        if cli == client:
            total_book_value += portfolios["Account Investment Book Value"][index]
        index += 1
    return total_book_value

def newTotalMarketValue(client, instrument, input):
    current_total_market_value = totalMarketValue(client)
    current_instrument_market_value = fetchMarketValue(client,instrument)
    new_instrument_market_value = calculateMarketValue(client,instrument,input)
    return current_total_market_value-current_instrument_market_value+new_instrument_market_value

def clientTotalValueAnalysis(book_value,old_value,new_value):
    res = {}
    market_value_change = ((new_value-old_value)/old_value)*100
    original_market_to_book_value = ((old_value-book_value)/book_value)*100
    new_market_to_book_value = ((new_value-book_value)/book_value)*100
    res["market_value_change"] = market_value_change
    res["original_market_to_book_value"] = original_market_to_book_value
    res["new_market_to_book_value"] = new_market_to_book_value
    return res

def overallCalculations(data):
    cmv = []
    nmv = []
    ctmv = totalMarketValue(data[0].client)
    ctbv = totalBookValue(data[0].client)
    for i in data:
        cmv.append(fetchMarketValue(data[i].client, data[i].instrument))
        nmv.append(calculateMarketValue(data[i].client), data[i].instrument, data[i].input)
    dmv = [a - b for a, b in zip(nmv, cmv)]
    ocmv = sum(dmv)
    ntmv = ctmv + ocmv
    percent_change_mv = (ocmv/ctmv)*100
    nmv_to_bv = ((ntmv-ctbv)/ctbv)*100
    res = {'percent_change_mv':percent_change_mv, 'nmv_to_bv':nmv_to_bv}
    return res