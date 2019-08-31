import time
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO

PORT = "5000"
# HOST = "10.140.164.149"
HOST = "127.0.0.1"


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@socketio.on('message')
def handle_message(message):
    print('received message: ' + str(message))
    return "got it!"  # returned to client


@socketio.on('connect')
def on_client_connect():
    print("connected")


@socketio.on('disconnect')
def on_client_disconnect():
    print("disconnected")


@socketio.on('start')
def on_start():
    print("start")
    send_data(1)
    # TODO: multi-threading


def send_data(num):
    for _ in range(num):
        socketio.emit('time', {'time': int(round(time.time() * 1000))})


@socketio.on('time_response')
def on_time_response(data):
    now = int(round(time.time() * 1000))
    # print("time from server to client (in ms): " + str((data['time_current'] - data['time_original'])))
    # print("time from client to server (in ms): " + str((now - data['time_current'])))
    print("time round trip (in ms): " + str((now - data['time_original'])))


if __name__ == '__main__':
    print("Starting web server...")

    print("Running Flask-SocketIO server: Flask server using WebSockets protocol.")
    print("URL: http://"+HOST+":"+PORT)

    socketio.run(app, host=HOST, port=PORT, debug=False)

