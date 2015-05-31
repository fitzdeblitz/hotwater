
from flask import Flask, render_template, send_from_directory, jsonify

import datetime
import time
import thermostats
import switches

app = Flask(__name__, static_url_path="")

sensorMgr = thermostats.SensorMgr()
switchMgr = switches.SwitchMgr()

@app.route("/")
def hello():
    print('Hot Water')
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'Hot Water',
      'time': timeString
      }
    return render_template('main.html', **templateData)

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

# GET shouldn't act like this at all, but we keep as is for now
@app.route("/Gable/On")
def turnGablePumpAlwaysOn():
    switchMgr.turnGablePumpAlwaysOn()
    return jsonify(response="Success!")

@app.route("/Gable/Off")
def turnGablePumpAlwaysOff():
    switchMgr.turnGablePumpAlwaysOff()
    return jsonify(response="Success!")

@app.route("/Gable/Auto")
def setGablePumpAutomatic():
    switchMgr.setGablePumpAutomatic()
    return jsonify(response="Success!")

@app.route("/thermostats")
def get_thermostats():
    values = sensorMgr.get_thermostats()
    return jsonify(thermostats=values)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

while True:
    if sensorMgr.isGableHotterThanTank():
        switchMgr.turnGablePumpOn()
    else:
        switchMgr.turnGablePumpOff()

    time.sleep(1)