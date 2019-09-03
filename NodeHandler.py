# from https://stackoverflow.com/questions/44371041/python-socketio-and-flask-how-to-stop-a-loop-in-a-background-thread
class NodeHandler(object):
    switch = False

    def __init__(self, socketio):
        """
        assign socketio object to emit
        """
        self.socketio = socketio
        self.switch = False
        self.active = False
        self.count = 0

    # based on https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/app.py
    def node_background_thread(self):
        """Example of how to send server generated events to clients."""
        self.switch = True
        self.active = True
        while True:
            if self.switch:
                self.count += 1
                self.socketio.emit('server_message',
                              {'message': 'Server generated event', 'id': self.count},
                              namespace='/node')
                print("[Server] sent server event to /node. id: " + str(self.count))
            self.socketio.sleep(5)

    def stop(self):
        """
        stop the loop
        """
        self.switch = False

    def is_running(self):
        return self.switch

    def is_active(self):
        return self.active

    def restart(self):
        self.switch = True
