from threading import Lock

from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO, emit

from NodeHandler import NodeHandler
from WebHandler import WebHandler

PORT = "5000"
# HOST = "10.140.164.149"
HOST = "127.0.0.1"

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

web_thread = None
web_thread_lock = Lock()

node_thread = None
node_thread_lock = Lock()

connected_node_clients = {}
connected_web_clients = {}

node_handler = None
web_handler = None


# based on https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/app.py
def web_background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('server_message',
                      {'message': 'Server generated event', 'id': count},
                      namespace='/web')
        print("[Server] sent server event to /web. id: " + str(count))


def node_background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('server_message',
                      {'message': 'Server generated event', 'id': count},
                      namespace='/node')
        print("[Server] sent server event to /node. id: " + str(count))


@app.route('/')
def index():
    return render_template("index.html", async_mode=socketio.async_mode)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@socketio.on('my_ping', namespace='/web')
def ping_pong():
    emit('my_pong')


# Web client handling #

@socketio.on('connect', namespace='/web')
def web_connect():
    global web_handler
    if web_handler is None:
        web_handler = WebHandler(socketio)

    '''
    global web_thread
    with web_thread_lock:
        if web_thread is None:
            web_thread = socketio.start_background_task(web_background_thread)
    '''


@socketio.on('web_connected', namespace='/web')
def on_web_connected(data):
    connected_web_clients[request.sid] = data['id']
    print("[Web] client " + connected_web_clients[request.sid] + " (" + request.sid + ") connected")

    if not web_handler.is_running():
        if web_handler.is_active():
            web_handler.restart()
        else:
            socketio.start_background_task(target=web_handler.loop)
    else:
        pass


@socketio.on('disconnect', namespace='/web')
def web_disconnect():
    if request.sid in connected_web_clients:
        print("[Web] client " + connected_web_clients[request.sid] + " (" + request.sid + ") disconnected")
        del connected_web_clients[request.sid]
    else:
        print("[Web] " + request.sid + "disconnected but not tracked")

    if len(connected_web_clients) == 0:
        web_handler.stop()


# Node client handling #

@socketio.on('connect', namespace='/node')
def node_connect():
    global node_handler
    if node_handler is None:
        node_handler = NodeHandler(socketio)

    '''
    global node_thread
    with node_thread_lock:
        if node_thread is None:
            node_thread = socketio.start_background_task(node_background_thread)
    '''


@socketio.on('node_connected', namespace='/node')
def on_node_connected(data):
    connected_node_clients[request.sid] = data['id']
    print("[Node] client " + connected_node_clients[request.sid] + " (" + request.sid + ") connected")

    if not node_handler.is_running():
        if node_handler.is_active():
            node_handler.restart()
        else:
            socketio.start_background_task(target=node_handler.loop)
    else:
        pass


@socketio.on('disconnect', namespace='/node')
def on_node_disconnect():
    if request.sid in connected_node_clients:
        print("[Node] client " + connected_node_clients[request.sid] + " (" + request.sid + ") disconnected")
        del connected_node_clients[request.sid]
    else:
        print("[Node] " + request.sid + "disconnected but not tracked")

    if len(connected_node_clients) == 0:
        node_handler.stop()


# main entry point
if __name__ == '__main__':
    print("Starting web server...")

    print("Running Flask-SocketIO server: Flask server using WebSockets protocol.")
    print("URL: http://"+HOST+":"+PORT)

    socketio.run(app, host=HOST, port=PORT, debug=False)

# TODO implement client id tracking, thread control for web client
#  investigate flask.request, flask.session for useful attributes
