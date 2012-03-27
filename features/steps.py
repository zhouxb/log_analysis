# -*- coding: utf-8 -*-
from lettuce import step, world
import os

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

@step(u'Then I see the number 1')
def then_i_see_the_number_1(step):
    pass

