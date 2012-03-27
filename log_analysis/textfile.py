# textfile is a module contains many useful functions dealing with tough tasks
import os

def get_file_size(filename):
    '''Return the exact size of a given file, it's said this is a way more
    reliable than using os.stat when the file is growing'''
    with open(filename) as fp:
        fp.seek(0, os.SEEK_END)
        size = fp.tell()
    return size

def seek_newline(fp, position):
    ''' Seek for the first newline in a text file backwardly from the given
    positionition, and return its positionition.  If nothing is found, return
    -1 instead'''
    if position < 0:
        raise ValueError("position should not be a negtive number")
    orignal_position = fp.tell()
    fp.seek(position)
    while fp.tell() > 0 and fp.read(1) != '\n':
        fp.seek(-2, os.SEEK_CUR)
    current_position = fp.tell()
    fp.seek(orignal_position)
    return current_position - 1

def divide_into_chunks(filename, blocksize):
    '''Divide the given file into chunks without even breaking a line, the size
    of a chunk is less than or equal with the blocksize, and yield each begin
    and end positon in tuples. Be careful with that the range is left
    bounded'''
    if blocksize <= 0:
        raise ValueError("blocksize is non-positive number")
    with open(filename) as fp:
        begin_pos = 0
        while True:
            filesize = get_file_size(filename)
            if filesize == 0:
                yield (0, 0)
                break
            if begin_pos + blocksize >= filesize:
                newline_pos = seek_newline(fp, filesize - 1)
                end_pos = newline_pos + 1
                if begin_pos > end_pos:
                    raise Exception("blocksize is too small")
                yield((begin_pos, end_pos))
                break

            end_pos = seek_newline(fp, (begin_pos + blocksize - 1)) + 1
            yield(begin_pos, end_pos)
            if begin_pos == end_pos:
                break
            begin_pos = end_pos

def divide_into_parts(filename, num):
    '''Divide the given file into num parts'''
    filesize = get_file_size(filename)
    blocksize = filesize / num
    n = 1
    last_end = 0
    for part in divide_into_chunks(filename, blocksize):
        if n == num:
            yield (last_end, filesize)
            break
        yield part
        last_end = part[1]
        n += 1
