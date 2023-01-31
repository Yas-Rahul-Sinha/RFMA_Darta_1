from flask import Flask, render_template, request
from main import advisor
from escalation import temp2
from escalation import temp3

app = Flask(__name__)

@app.route("/")
def table():
    return render_template("login.html")

@app.route('/select', methods=['POST', 'GET'])
def select():
    value = request.form['advisor']
    return render_template("tables.html", advisor_name=value, advisor=advisor[value], escalation=temp2[value], crm=temp3[value])