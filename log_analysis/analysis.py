#!/usr/bin/python
import logging
import util
import dnslog
import os
import settings

import yapsy.PluginManager
from multiprocessing import Queue, Process

def assign_task(fileobj, task_size, proc_num, task_queue):
    for lines in util.split_every(task_size, fileobj):
        logging.debug("read %d lines" % len(lines))
        task = dnslog.parse_chunk(lines)
        task_queue.put(task)
        logging.debug("put %d entries into task_queue" % len(task))
    for _ in range(proc_num):
        task_queue.put([])

def handle_task(plugins, task_queue):
    while True:
        task = task_queue.get()
        if not task:
            logging.debug("process [%d] exits for no more task received" %
                          os.getpid())
            break
        map(lambda p: p.analysis(task), plugins)
        logging.debug("process [%d] handle a chunk with %d lines" %  \
                      (os.getpid(), len(task)))

def run_analysis(fileobj, plugins, task_size, proc_num):
    task_queue = Queue()

    allocate_proc = Process(target=assign_task, args=(fileobj, task_size, 
                                                      proc_num, task_queue))
    allocate_proc.start()

    analysis_procs = [Process(target=handle_task, args=(plugins, task_queue)) \
                      for i in range(proc_num)]
    map(lambda proc: proc.start(), analysis_procs)

    allocate_proc.join()
    map(lambda proc: proc.join(), analysis_procs)

def run_collector(plugins):
    collect_procs = [Process(target=p.collect) for p in plugins]
    map(lambda proc: proc.start(), collect_procs)
    map(lambda proc: proc.join(), collect_procs)

def load_plugins(path):
    manager = yapsy.PluginManager.PluginManager(plugin_info_ext="info")
    manager.setPluginPlaces([path])
    manager.collectPlugins()
    for plugin in manager.getAllPlugins():
        plugin.plugin_object.activate()
        if plugin.name in settings.PLUGINS:
            yield plugin.plugin_object
