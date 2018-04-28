from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit

from main import *

import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

Data = {'led':{'r':0,'g':0,'b':0},'motor':[0,0,0,0],'temp':0,'humi':0}

@app.route('/')
def home():
	global Data
	Data['humi'] = request.args.get('humi') if request.args.get('humi') else 0
	Data['temp'] = request.args.get('temp') if request.args.get('temp') else 0
	socketio.emit('status', json.dumps(Data) , broadcast=True)
	loop()
	return(
		str(Data['motor'][0])+
		str(Data['motor'][1])+
		str(Data['motor'][2])+
		str(Data['motor'][3])+
		("{0:0=3d}".format(Data['led']['r']))+
		("{0:0=3d}".format(Data['led']['g']))+
		("{0:0=3d}".format(Data['led']['b'])) )

@app.route('/control')
def control():
	return render_template('home.html', 
		ledR=Data['led']['r'], 
		ledG=Data['led']['g'], 
		ledB=Data['led']['b'], 
		humi=Data['humi'], 
		temp=Data['temp'] )

@socketio.on('updates')
def message(message):
	global Data
	inputs = message.split(",")
	Data['motor'][0] = int(inputs[0])
	Data['motor'][1] = int(inputs[1])
	Data['motor'][2] = int(inputs[2])
	Data['motor'][3] = int(inputs[3])
	Data['led']['r'] = int(inputs[4])
	Data['led']['g'] = int(inputs[5])
	Data['led']['b'] = int(inputs[6])
	socketio.emit('status', json.dumps(Data) , broadcast=True)
