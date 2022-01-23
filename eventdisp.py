class Dispatcher:
    def __init__(self):
        self.listeners = dict()

    def add_listener(self, event_name, callback):

        self.listeners[event_name] = callback

    def emmit(self, event_name, params=None):
        self.listeners[event_name](params)
        print('emmit', event_name)
