import puremvc.patterns.command
import puremvc.interfaces
import settings
import main, model
import monitor
import analysis
import log

from multiprocessing import Queue, Process

class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
		log_queue = Queue()
		logger = log.QueueLogger(log_queue)

		log_proc = Process(target=log.run_log, args=(log_queue,))
		log_proc.start()

		self.sendNotification(main.AppFacade.MONIT, logger)

class MonitCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        logger = note.body
        monitor.monit_directory(settings.DNS_LOG_DIR, lambda filename: self.sendNotification(main.AppFacade.PREPROCESS, (filename, logger)))

class PreprocessCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        filename, logger  = note.body
        logger.info("done some preproces with %s" % filename)
        self.sendNotification(main.AppFacade.ANALYSIS, (filename, logger))

class AnalysisCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        filename, logger = note.body
        plugin_path = settings.PLUGINS_PATH
        parts_num   = settings.PARTS_NUMBER

        plugins = [plugin for plugin in analysis.load_plugins(plugin_path)]
        analysis.run_analysis(filename, plugins, parts_num, logger)
        self.sendNotification(main.AppFacade.COLLECT, (plugins, logger))

class CollectCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        plugins, log_queue = note.body
        analysis.run_collector(plugins, log_queue)
        self.sendNotification(main.AppFacade.POSTPROCESS, log_queue)

class PostprocessCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        logger = note.body
        logger.info("some postprocess work")

