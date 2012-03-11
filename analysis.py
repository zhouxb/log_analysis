#!/usr/bin/python
import logging
import util
import dnslog
import os

import yapsy.PluginManager
from multiprocessing import Queue, Process

def assign_task(filename, task_size, proc_num, task_queue):
    with open(filename) as f:
        for lines in util.split_every(task_size, f):
            entries = dnslog.parse_chunk(lines)
            task_queue.put(entries)
	for _ in range(proc_num):
		task_queue.put([])

def handle_task(plugins, task_queue):
    while True:
        task = task_queue.get()
        if not task:
            break
        logging.debug("process [%d] handle a chunk with %d lines" % (os.getpid(), len(task)))
        for p in plugins:
            p.analysis(task)

def run_analysis(filename, plugins, task_size, proc_num):
    task_queue = Queue()

    allocate_proc = Process(target=assign_task, args=(filename, task_size, proc_num, task_queue))
    allocate_proc.start()

    analysis_procs = [Process(target=handle_task, args=(plugins, task_queue)) for i in range(proc_num)]
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
        yield plugin.plugin_object
