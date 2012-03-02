from pyinotify import ProcessEvent, WatchManager, Notifier, IN_CLOSE_WRITE

class EventHandler(ProcessEvent):
    def __init__(self, directory, action):
        super(EventHandler, self).__init__()
        self.directory = directory
        self.action = action
    def process_IN_CLOSE_WRITE(self, event):
        self.action(event.pathname)

def monit_directory(directory, action):
    wm = WatchManager()
    wm.add_watch(directory, IN_CLOSE_WRITE)
    handler = EventHandler(directory, action)
    notifier = Notifier(wm, handler)
    notifier.loop()
