from Handler import Handler


# from https://stackoverflow.com/questions/44371041/python-socketio-and-flask-how-to-stop-a-loop-in-a-background-thread
class NodeHandler(Handler):

    def __init__(self, socketio):
        super().__init__(socketio)

    # based on https://github.com/miguelgrinberg/Flask-SocketIO/blob/master/example/app.py
    def loop(self):
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
