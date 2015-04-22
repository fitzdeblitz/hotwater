from flask import Flask, request, render_template
app = Flask(__name__)
import datetime

@app.route("/")
def hello():
    print('Hello World')
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
    return render_template('main.html', **templateData)


import time

import Thermostats
import Switches

sensorMgr = Thermostats.SensorMgr()
switchMgr = Switches.SwitchMgr()


@app.route("/Gable/On")
def turnGablePumpAlwaysOn():
    switchMgr.turnGablePumpAlwaysOn()
    return "Success!"

@app.route("/Gable/Off")
def turnGablePumpAlwaysOff():
    switchMgr.turnGablePumpAlwaysOff()
    return "Success!"

@app.route("/Gable/Auto")
def setGablePumpAutomatic():
    switchMgr.setGablePumpAutomatic()
    return "Success!"

def mainHTML():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
      'title' : 'HELLO!',
      'time': timeString
      }
    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

while True:
    if sensorMgr.isGableHotterThanTank():
        switchMgr.turnGablePumpOn()
    else:
        switchMgr.turnGablePumpOff()

    time.sleep(1)