import os
import gzip
import multiprocessing

import main
import monitor
import analysis
import log
import logging
import settings

from puremvc.patterns.command import SimpleCommand
from  puremvc.interfaces import ICommand

class StartupCommand(SimpleCommand, ICommand):
    def execute(self, note):
        log.setup_logger()
        log_queue = log.global_log_queue
        log_proc = multiprocessing.Process(target=log.run_log_listener, 
                                           args=(log_queue,))
        log_proc.start()
        
        logging.info("app starts")
        self.sendNotification(main.AppFacade.MONIT)

class MonitCommand(SimpleCommand, ICommand):
    def execute(self, note):
        func = lambda filename: \
            self.sendNotification(main.AppFacade.PREPROCESS, filename)
        monitor.monit_directory(settings.DNS_LOG_DIR, func)

class PreprocessCommand(SimpleCommand, ICommand):
    def execute(self, note):
		filename = note.body
		basename = os.path.basename(filename)
		match = settings.DNS_LOG_FILENAME_PATTERN.match(basename)
		if not match:
			logging.warning("filename %s doesn't match pattern in settings.py \
, ignore it" % filename)
			return
		settings.PROVINCE = match.group("PROVINCE")
		fileobj = gzip.open(filename)
		logging.info("open %s" % filename)
		self.sendNotification(main.AppFacade.ANALYSIS, fileobj)

class AnalysisCommand(SimpleCommand, ICommand):
    def execute(self, note):
        fileobj     = note.body
        plugin_path = settings.PLUGINS_PATH
        task_size   = settings.TASK_SIZE
        proc_num    = settings.PROC_NUM

        plugins = [plugin for plugin in analysis.load_plugins(plugin_path)]
        analysis.run_analysis(fileobj, plugins, task_size, proc_num)
        self.sendNotification(main.AppFacade.COLLECT, plugins)

class CollectCommand(SimpleCommand, ICommand):
    def execute(self, note):
        plugins  = note.body
        analysis.run_collector(plugins)
        self.sendNotification(main.AppFacade.POSTPROCESS)

class PostprocessCommand(SimpleCommand, ICommand):
    def execute(self, note):
        logging.info("some postprocess work")
