import ast

from flask import Flask, jsonify
from flask_restful import Resource,Api,reqparse,abort

from wtforms import SelectField
from main import advisor
from escalation import temp2
from escalation import temp3
from client_portfolio import getAccountPortfolio
from market_news import adv_market
from client_instrument import adv_investor_investments
from datautil import *

app = app = Flask(__name__)
api = Api(app)

post_data = reqparse.RequestParser()
post_data.add_argument('data',action='append',help='Array of objects containing relevent information', required=True)

class ClientList(Resource):
    def get(self, adv):
        return advisor[adv]

class MarketNews(Resource):
    def get(self, adv):
        return {adv: adv_market[adv]}

class ClientEscalation(Resource):
    def get(self, adv):
        return {adv:temp2[adv]}

class CRM(Resource):
    def get(self, adv):
        return {adv:temp3[adv]}

class PortfolioData(Resource):
    def get(self,adv,client,account):
        return getAccountPortfolio(adv,client,account)

class MarketSignalImpact(Resource):
    def post(self):
        response = {}
        temp = {}
        args = post_data.parse_args()
        for i in args["data"]:
            j = ast.literal_eval(i)
            temp["Existing Value"] = fetchMarketValue(j["investor"], j["instrument"])
            temp["Projected Value"] = calculateMarketValue(j["investor"], j["instrument"], j["value"])
            temp["Percentage Impact"] = percentageImpact(temp["Existing Value"], temp["Projected Value"])
            if temp["Existing Value"] > temp["Projected Value"]:
                temp["Up/Down"] = "Down"
            elif temp["Existing Value"] < temp["Projected Value"]:
                temp["Up/Down"] = "Up"
            else:
                temp["Up/Down"] = "No Impact"
            response[j['instrument']] = temp.copy()
        return response

class ClientInstrumentData(Resource):
    def get(self,adv):
        return adv_investor_investments[adv]

api.add_resource(ClientList, '/<string:adv>/clientList')
api.add_resource(MarketNews, '/<string:adv>/marketNews')
api.add_resource(ClientEscalation, '/<string:adv>/clientEscalation')
api.add_resource(CRM, '/<string:adv>/CRM')
api.add_resource(PortfolioData, '/portfolioData/<string:adv>/<string:client>/<int:account>')
api.add_resource(MarketSignalImpact, '/marketSignalImpact')
api.add_resource(ClientInstrumentData, '/clientInstrumentData/<string:adv>')
if __name__ == '__main__':
    app.run(debug=True)