# -*- coding: utf-8 -*-
from lettuce import step, world
import time
import os
import gzip

@step(u'Given I have an non-exist file in ([a-zA-Z0-9./\-]+)')
def startup_with_non_exist_file(step, filename):
    world.filename = filename

@step(u'Given I have an empty gz-compressed file in ([a-zA-Z0-9./\-]+)')
def given_i_have_an_empty_gz_compressed_file_in_data_empty_gz(step, filename ):
    os.system("touch %s" % filename[:-3])
    os.system("gzip -f %s"  % filename[:-3])
    world.filename = filename

@step(u'Given I have an gz-compressed file in ([a-zA-Z0-9./\-]+)')
def given_i_have_an_gz_compressed_file(step, filename):
    world.filename = filename

@step(u'When I run log_analysis on it')
def when_i_run_log_analysis_on_it(step):
    os.system("log_analysis/main.py --file %s" % world.filename)

@step(u'Then I see no exceptions')
def then_i_see_no_exceptions(step):
    pass

@step(u'When I run all the analysis on it')
def when_i_run_all_analysis_on_it(step):
    os.system("log_analysis/main.py --file %s" % world.filename)

@step(u'When I run (\w+) analysis on it')
def when_i_run_plugin_analysis_on_it(step, plugin):
    os.system("log_analysis/main.py --plugins %s --file %s" % (plugin, world.filename))

@step(u'Given I have some log records:')
def given_i_have_some_log_records(step):
    world.records = step.multiline

@step(u'Then I create an gzip file named ([a-zA-Z0-9./\-]+) with these records')
def then_i_create_an_gz_compressed_file(step, fullpath):
    gzip.open(fullpath, "w").write(world.records)
    world.filename = fullpath

@step(u'Then I see (\d+) records in (\w+).(\w+)')
def then_i_see_records_in_database(step, num, database, collection):
    assert world.conn[database][collection].find().count() == int(num)


@step(u'And I sleep for (\d+) seconds')
def and_i_sleep_for_1_seconds(step, n):
    time.sleep(int(n))

@step(u'When I select following from (\w+).(\w+):')
def when_i_select_following_from_db(step, database, collection):
    query = step.hashes
    world.result = world.conn[database][collection].find(query)

