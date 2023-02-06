from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_wtf import FlaskForm
from urllib.parse import unquote
from wtforms import SelectField
from main import advisor
from escalation import temp2
from escalation import temp3
from market_news import adv_market
from client_instrument import adv_investor_investments
from datautil import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
class Form(FlaskForm):
    client = SelectField('Client_Name', choices=[])
    # description_type = SelectField('Description_Type', choices=[])
    instrument = SelectField('Instrument', choices=[])
@app.route("/")
def table():
    return render_template("login.html")

@app.route('/select', methods=['POST', 'GET'])
def select():
    value = request.form['advisor']
    return render_template("tables.html", advisor_name=value, advisor=advisor[value], escalation=temp2[value], crm=temp3[value], market_news=adv_market[value], classs="")

@app.route('/market_signal_impact', methods=['POST', 'GET'])
def clientSelect():
    clientlist = []
    adv = request.form['advisor']
    for i in advisor[adv]["Investor Name"]:
        clientlist.append((i,i))
    form = Form()
    form.client.choices = clientlist

    # if request.method == 'POST':
    #     client = request.form["client"]
    #     instrument = request.form["instrument"]
    #     market_value = fetchMarketValue(client,instrument)
        # return render_template("market_signal_impact.html", advisor=adv, form=form, market_value=market_value)
    return render_template("market_signal_impact.html", advisor=adv, form=form)
@app.route('/market_signal_impact/param')
def typeSelect():
    advisor = request.args.get('advisor', None)
    investor = request.args.get('investor', None)
    return jsonify({'client':adv_investor_investments[advisor][investor]})

@app.route('/market_signal_impact/param/result', methods=['POST', 'GET'])
def result():
    client = request.form['client']
    instrument = unquote(request.form['instrument'])
    value = request.form['input_data']
    current_market_value = fetchMarketValue(client,instrument)
    new_market_value = calculateMarketValue(client,instrument,value)
    total_book_value = totalBookValue(client)
    total_market_value = totalMarketValue(client)
    new_total_market_value = newTotalMarketValue(client,instrument,value)
    analysis = clientTotalValueAnalysis(total_book_value,total_market_value,new_total_market_value)
    print(analysis)
    return render_template('result.html', current_market_value=current_market_value, new_market_value=new_market_value, total_book_value=total_book_value, total_market_value=total_market_value, new_total_market_value=new_total_market_value, analysis=analysis)


