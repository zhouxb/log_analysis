
from multiprocessing import Process
import puremvc.patterns.command
import puremvc.interfaces
import main, model

class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        self.facade.registerProxy(model.TempProxy())

        self.sendNotification(main.AppFacade.INOTIFY, 'Inotify')
            #self.facade.registerProxy(model.PostProxy())

class InotifyCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        print 'nnd'
        print dir(note)
        print note.body

        tempProxy = self.facade.retrieveProxy(model.TempProxy.NAME)
        tempProxy.test()
        self.sendNotification(main.AppFacade.OTHER)


class OtherCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        print 'here'

        #p = Process(target=f, args=('bbb', ))
        #p.start()
        #p.join()

        #tempProxy.change_data(2)


