#!/usr/bin/python
from multiprocessing import Queue, Process, current_process
from yapsy.PluginManager import PluginManager

from textfile import divide_into_chunks, divide_into_parts
from dnslog import parse_chunk


def divide_chunks(filename, blocksize, proc_num, queue):
	map(lambda chunk: queue.put(chunk), divide_into_chunks(filename, blocksize))
	for _ in range(proc_num):
		queue.put((0, 0))

def divide_parts(filename, part_num,  task_queue):
	map(lambda part: task_queue.put(part), divide_into_parts(filename, part_num))
	for _ in range(part_num):
		task_queue.put((0, 0))

def handle_chunk(filename, plugins, task_queue, logger):
    while True:
        with open(filename) as fp:
			begin, end = task_queue.get()
			if (begin, end) == (0, 0):
				break
			logger.info("process %d handles the chunk with bytes from %d to %d " % (current_process().pid, begin, end))
			fp.seek(begin)
			contents = fp.read(end - begin)
			entries = parse_chunk(contents)
			for p in plugins:
				p.analysis(entries, logger)

def run_analysis(filename, analysis_chains, parts_num, logger):
    task_queue = Queue()

    allocator_proc = Process(target=divide_parts, args=(filename, parts_num, task_queue))
    allocator_proc.start()

    analysis_procs = [Process(target=handle_chunk, args=(filename, analysis_chains, task_queue, logger)) for i in range(parts_num)]
    map(lambda proc: proc.start(), analysis_procs)

    allocator_proc.join()
    map(lambda proc: proc.join(), analysis_procs)

def run_collector(plugins, log_queue):
    collect_procs = [Process(target=p.collect, args=(log_queue,)) for p in plugins]
    map(lambda proc: proc.start(), collect_procs)
    map(lambda proc: proc.join(), collect_procs)

def load_plugins(path):
    manager = PluginManager(plugin_info_ext="info")
    manager.setPluginPlaces([path])
    manager.collectPlugins()
    for plugin in manager.getAllPlugins():
        plugin.plugin_object.activate()
        yield plugin.plugin_object
