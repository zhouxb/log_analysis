import puremvc.patterns.command
import puremvc.interfaces
import settings
import main, model
import monitor
import analysis

class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        self.facade.registerProxy(model.TempProxy())
        self.sendNotification(main.AppFacade.MONIT)

class MonitCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        monitor.monit_directory(settings.LOG_DIR, lambda filename: self.sendNotification(main.AppFacade.PREPROCESS, filename))

class PreprocessCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        filename = note.body
        print "done some preproces with %s" % filename
        self.sendNotification(main.AppFacade.ANALYSIS, filename)

class AnalysisCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        filename = note.body
        plugin_path = settings.PLUGIN_PATH
        parts_num   = settings.PARTS_NUMBER
        server = settings.SERVER

        plugins = [plugin for plugin in analysis.load_plugins(plugin_path, server)]
        analysis.run_analysis(filename, plugins, parts_num)
        self.sendNotification(main.AppFacade.COLLECT, plugins)

class CollectCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        plugins = note.body
        analysis.run_collector(plugins)
        self.sendNotification(main.AppFacade.POSTPROCESS)

class PostprocessCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        print "some postprocess work"

