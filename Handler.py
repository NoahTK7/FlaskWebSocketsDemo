# from https://stackoverflow.com/questions/44371041/python-socketio-and-flask-how-to-stop-a-loop-in-a-background-thread
class Handler(object):
    switch = False

    def __init__(self, socketio):
        """
        assign socketio object to emit
        """
        self.socketio = socketio
        self.switch = False
        self.active = False
        self.count = 0

    def loop(self):
        pass

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
