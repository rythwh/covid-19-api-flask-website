#!/usr/local/bin/python

from flask import Flask, session, redirect, url_for, request, render_template
from markupsafe import escape

import MySQLdb
import MySQLdb.cursors

try:
    import requests
except ImportError:
    print("\033[101m The 'requests' API is not installed and is required for the lab to run. Please install it with 'pip install requests' \033[0m")

import json
import time

app = Flask(__name__, static_url_path="")
app.debug = False

# Not really secret...
app.secret_key = "X*37[F84VfgRh$gCB^6tstg*9&mDWoi8"

@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username varchar(32) NOT NULL PRIMARY KEY, password varchar(32) NOT NULL);")
    db.commit()

    if 'username' in session:
        return redirect(url_for('covid'))    
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST", "PUT", "DELETE"])
def login():

    error = False

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchall()

        if len(result) == 0:
            cursor.execute("INSERT IGNORE INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()

            if cursor.rowcount == 0:
                error = True
                return render_template('index.html', login = True, error = error)

        session['username'] = request.form['username']
        data("Canada", "Canada")
        return redirect(url_for('index'))
    return render_template('index.html', login = True, error = error)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/covid", methods=["GET", "POST", "PUT", "DELETE"])
def covid():
    error = None
    if request.method == 'POST':
        return redirect(url_for('logout'))
    return render_template('index.html', login = False, error = error)

@app.route("/data/<regionShort>,<regionLong>", methods=["GET"])
def data(regionShort, regionLong):
    error = None
    summaryResponse = requests.get("https://api.covid19tracker.ca/summary" + ("/split" if regionShort != "Canada" else "")).json()
    reportResponse = requests.get("https://api.covid19tracker.ca/reports" + ("/province/" + regionShort if regionShort != "Canada" else "") + "?stat=cases").json()
    session['region'] = regionLong
    session['regionShort'] = regionShort
    session['percentage'] = {}

    index = 0
    if (regionShort != "Canada"):
        for i in range(len(summaryResponse['data'])):
            if summaryResponse['data'][i]['province'] == regionShort:
                index = i
                break

    cases_change = parse_int(summaryResponse['data'][index]['change_cases'])
    cases_total = parse_int(summaryResponse['data'][index]['total_cases'])

    hospitalizations_change = parse_int(summaryResponse['data'][index]['change_hospitalizations'])
    hospitalizations_total = parse_int(summaryResponse['data'][index]['total_hospitalizations'])

    criticals_change = parse_int(summaryResponse['data'][index]['change_criticals'])
    criticals_total = parse_int(summaryResponse['data'][index]['total_criticals'])

    deaths_change = parse_int(summaryResponse['data'][index]['change_fatalities'])
    deaths_total = parse_int(summaryResponse['data'][index]['total_fatalities'])

    recoveries_change = parse_int(summaryResponse['data'][index]['change_recoveries'])
    recoveries_total = parse_int(summaryResponse['data'][index]['total_recoveries'])

    tests_change = parse_int(summaryResponse['data'][index]['change_tests'])
    tests_total = parse_int(summaryResponse['data'][index]['total_tests'])

    session['percentage']['cases'] = round((cases_change / float(cases_total)) * 100, 2) if cases_total != 0 else 0
    session['percentage']['hospitalizations'] = round((hospitalizations_change / float(hospitalizations_total)) * 100, 2) if hospitalizations_total != 0 else 0
    session['percentage']['criticals'] = round((criticals_change / float(criticals_total)) * 100, 2) if criticals_total != 0 else 0
    session['percentage']['deaths'] = round((deaths_change / float(deaths_total)) * 100, 2) if deaths_total != 0 else 0
    session['percentage']['recoveries'] = round((recoveries_change / float(recoveries_total)) * 100, 2) if recoveries_total != 0 else 0
    session['percentage']['tests'] = round((tests_change / float(tests_total)) * 100, 2) if tests_total != 0 else 0

    session['covid'] = {}

    session['covid']['last_updated'] = summaryResponse['last_updated']

    session['covid']['cases_change'] = cases_change
    session['covid']['cases_total'] = cases_total

    session['covid']['hospitalizations_change'] = hospitalizations_change
    session['covid']['hospitalizations_total'] = hospitalizations_total

    session['covid']['criticals_change'] = criticals_change
    session['covid']['criticals_total'] = criticals_total

    session['covid']['deaths_change'] = deaths_change
    session['covid']['deaths_total'] = deaths_total

    session['covid']['recoveries_change'] = recoveries_change
    session['covid']['recoveries_total'] = recoveries_total

    session['covid']['tests_change'] = tests_change
    session['covid']['tests_total'] = tests_total

    session['covid']['chart_data'] = {}
    session['covid']['chart_data']['labels'] = []
    session['covid']['chart_data']['data'] = {}
    session['covid']['chart_data']['data']['change_cases'] = []
    session['covid']['chart_data']['data']['total_cases'] = []

    for day in reportResponse['data']:
        session['covid']['chart_data']['labels'].append(int(day['date'].replace('-', '')))
        session['covid']['chart_data']['data']['change_cases'].append(day['change_cases'] if day['change_cases'] != None else 0)
        session['covid']['chart_data']['data']['total_cases'].append(day['total_cases'] if day['total_cases'] != None else 0)

    return render_template('index.html', login = False, error = error)

def get_db():
    database = MySQLdb.connect(host="dursley.socs.uoguelph.ca", user="rwhite08", passwd="0967628", db="rwhite08")
    return database

def parse_int(s):
    try:
        return int(s)
    except:
        return 0