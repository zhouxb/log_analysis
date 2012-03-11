import main
import monitor
import analysis
import log
import logging
import settings
import puremvc.patterns.command
import puremvc.interfaces

import multiprocessing

class StartupCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        log.setup_logger()

        log_queue = log.global_log_queue
        log_proc = multiprocessing.Process(target=log.run_log_listener, args=(log_queue,))
        log_proc.start()

        self.sendNotification(main.AppFacade.MONIT)

class MonitCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        monitor.monit_directory(settings.DNS_LOG_DIR, lambda filename: self.sendNotification(main.AppFacade.PREPROCESS, filename))

class PreprocessCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        filename = note.body
        logging.info("doing some preproces with %s" % filename)
        self.sendNotification(main.AppFacade.ANALYSIS, filename)

class AnalysisCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        filename    = note.body
        plugin_path = settings.PLUGINS_PATH
        task_size   = settings.TASK_SIZE
        proc_num    = settings.PROC_NUM

        plugins = [plugin for plugin in analysis.load_plugins(plugin_path)]
        analysis.run_analysis(filename, plugins, task_size, proc_num)
        self.sendNotification(main.AppFacade.COLLECT, plugins)

class CollectCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        plugins  = note.body
        analysis.run_collector(plugins)
        self.sendNotification(main.AppFacade.POSTPROCESS)

class PostprocessCommand(puremvc.patterns.command.SimpleCommand, puremvc.interfaces.ICommand):
    def execute(self, note):
        logging.info("some postprocess work")
