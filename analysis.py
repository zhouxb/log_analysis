#!/usr/bin/python
import re
import signal
import sys

import settings
from multiprocessing import Queue, Process, cpu_count, current_process
from multiprocessing.sharedctypes import Value
from os import SEEK_END, SEEK_CUR
from pyinotify import ProcessEvent, WatchManager, Notifier, IN_MODIFY
from pymongo import Connection
from yapsy.PluginManager import PluginManager

from textfile import seek_newline, get_file_size, divide_into_chunks, divide_into_parts
from dnslog import parse_log_entry
from gather import gather_result

class EventHandler(ProcessEvent):
    def __init__(self, end_pos, action):
        super(EventHandler, self).__init__()
        self.end_pos = end_pos
        self.action = action
    def process_IN_MODIFY(self, event):
        self.end_pos = self.action(self.end_pos)

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

def divide_chunk_with_growing_file(filename, blocksize, proc_number, queue):
    def when_file_grow(end_pos):
        with open(filename) as fp:
            begin_pos = end_pos
            while True:
                filesize = get_file_size(filename)
                if begin_pos + blocksize >= filesize:
                    end_pos = seek_newline(fp, filesize - 1) + 1
                    queue.put((begin_pos, end_pos))
                    return end_pos
                else:
                    end_pos = seek_newline(fp, (begin_pos + blocksize -1)) + 1
                    queue.put((begin_pos, end_pos))
                    begin_pos = end_pos
    end = 0
    for chunk in divide_into_chunks(filename, blocksize):
        queue.put(chunk)
        end = chunk[1]

    wm = WatchManager()
    wm.add_watch(filename, IN_MODIFY)
    handler = EventHandler(end, when_file_grow)
    notifier = Notifier(wm, handler, read_freq=1, threshold=2)
    notifier.loop()

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
                cmd.apply(entrys)

def run_analysis(filename, analysis_chains, blocksize, proc_number, parts_num):
    queue = Queue()

    #allocator_proc = Process(target=divide_chunks, args=(logfile, blocksize, proc_number, queue))
    #for i in range(proc_number):
        #analysis_proc = Process(target=handle_chunk, args=(logfile, analysis_chains, queue))
        #analysis_proc.start()
    #allocator_proc.join()

    allocator_proc = Process(target=divide_parts, args=(logfile, parts_num, queue))
    allocator_proc.start()

    analysis_procs = []
    for i in range(parts_num):
        analysis_proc = Process(target=handle_chunk, args=(logfile, analysis_chains, queue))
        analysis_proc.start()
        analysis_procs.append(analysis_proc)
    allocator_proc.join()

    for proc in analysis_procs:
        proc.join()

def load_plugins(path, db):
    manager = PluginManager(plugin_info_ext="info")
    manager.setPluginPlaces([path])
    manager.collectPlugins()
    for plugin in manager.getAllPlugins():
        plugin.plugin_object.con = con
        plugin.plugin_object.activate()
        yield plugin.plugin_object

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        sys.exit(0)
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    logfile     = settings.LOG_FILE_PATH
    plugin_path = settings.PLUGIN_PATH
    procs_num    = settings.PROCESSORS_TO_USE
    blocksize   = settings.BLOCK_SIZE
    parts_num    = 8
    con = Connection("localhost")

    analysis_chains = [plugin for plugin in load_plugins(plugin_path, con)]
    run_analysis(logfile, analysis_chains, blocksize, procs_num, parts_num)
    gather_proc = Process(target=gather_result, args=("output",))
    gather_proc.start()
    gather_proc.join()
