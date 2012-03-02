#!/usr/bin/python
from multiprocessing import Queue, Process, current_process
from yapsy.PluginManager import PluginManager

from textfile import divide_into_chunks, divide_into_parts
from dnslog import parse_log_entry


def divide_chunks(filename, blocksize, proc_number, queue):
    for chunk in divide_into_chunks(filename, blocksize):
        queue.put(chunk)
    for i in range(proc_number):
        queue.put((0, 0))

def divide_parts(filename, num,  queue):
    for part in divide_into_parts(filename, num):
        queue.put(part)
    for i in range(num):
        queue.put((0, 0))

def handle_chunk(filename, analysis_chains, queue):
    while True:
        with open(filename) as fp:
            begin, end = queue.get()
            if (begin, end) == (0, 0):
                break
            print "%d : handle a chunk" % current_process().pid, "bytes from", begin, "to", end
            fp.seek(begin)
            contents = fp.read(end - begin)
            entrys = [parse_log_entry(line) for line in contents.splitlines() if not line.count("flexi-dns:")]
            for cmd in analysis_chains:
                cmd.analysis(entrys)

def run_analysis(filename, analysis_chains, parts_num):
    queue = Queue()

    allocator_proc = Process(target=divide_parts, args=(filename, parts_num, queue))
    allocator_proc.start()

    analysis_procs = [Process(target=handle_chunk, args=(filename, analysis_chains, queue)) for i in range(parts_num)]
    map(lambda proc: proc.start(), analysis_procs)

    allocator_proc.join()
    map(lambda proc: proc.join(), analysis_procs)

def run_collector(plugins):
    collect_procs = [Process(target=p.collect) for p in plugins]
    map(lambda proc: proc.start(), collect_procs)
    map(lambda proc: proc.join(), collect_procs)

def load_plugins(path, server):
    manager = PluginManager(plugin_info_ext="info")
    manager.setPluginPlaces([path])
    manager.collectPlugins()
    for plugin in manager.getAllPlugins():
        plugin.plugin_object.activate()
        plugin.plugin_object.server = server
        yield plugin.plugin_object
