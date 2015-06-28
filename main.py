import datetime
import time

from flask import Flask, render_template, send_from_directory, jsonify

from sensormgr import SensorMgr
from switchmgr import SwitchMgr
from controller import ControllerThread

app = Flask(__name__, static_url_path="")

sensormgr = SensorMgr()
switchmgr = SwitchMgr()

@app.route("/")
def hello():
    print('Hot Water')
    now = datetime.datetime.now()
    template_data = {
        'title': 'Hot Water',
        'time': now.strftime("%Y-%m-%d %H:%M")
    }
    return render_template('main.html', **template_data)

@app.route('/scripts/<path:path>')
def send_js(path):
    return send_from_directory('scripts', path)

# GET shouldn't act like this at all, but we keep as is for now
@app.route("/Gable/On")
def turnGablePumpAlwaysOn():
    switchmgr.turn_gable_pump_always_on()
    return jsonify(response="Success!")

@app.route("/Gable/Off")
def turnGablePumpAlwaysOff():
    switchmgr.turn_gable_pump_always_off()
    return jsonify(response="Success!")

@app.route("/Gable/Auto")
def setGablePumpAutomatic():
    switchmgr.set_gable_pump_automatic()
    return jsonify(response="Success!")

@app.route("/tempsensors")
def get_tempsensors():
    values = sensormgr.get_tempsensors()
    return jsonify(tempsensors=values)

if __name__ == "__main__":
    controller = ControllerThread(sensormgr, switchmgr)
    controller.start()
    app.run(host='0.0.0.0', port=80, debug=True)
