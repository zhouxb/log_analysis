import os
from lettuce import step, world
from analysis import get_file_size

@step(u'Given I have a filename (\w+)')
def given_i_have_a_filename_tmp_log(step, filename):
    world.full_path = "/tmp/" + filename
    os.system("touch %s" % world.full_path)

@step(u'When I write 100 bytes chars into the file, and compute its size')
def hen_i_write_100_bytes_chars_into_the_file_and_compute_its_size(step):
    os.system("dd if=/dev/zero of=%s bs=100 count=1 > /dev/null 2>&1" % world.full_path)

@step(u'Then I see the number (\d+)')
def then_i_see_the_number_100(step, filesize):
    assert get_file_size(world.full_path) == int(filesize)

