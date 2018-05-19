#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 11:19:21 2014

@author: thomas
"""
import sys
import csv
import re
import os
#import json

# constants
SF = 4     # scaling factor
SEP = ","  # csv separator
CSZ = 600  # chunksize


# functions
def med(v):
    return 3 * sum(v) / len(v) - max(v) - min(v)


# down samples the array in such a way that the max min and a medium value
# are returned in the correct order
# medium value is choosen such that the mean will be preserved
def down_samp(v):
    result = []
    min_val = min(v)
    max_val = max(v)
    med_val = med(v)
    if v.index(min_val) < v.index(max_val):
        result = result + [min_val, max_val]
    else:
        result = result + [max_val, min_val]

    gaps = [
        v.index(result[0]),
        v.index(result[1]) - v.index(result[0]) - 1,
        len(v) - v.index(result[1])
    ]

    # insert the medium val where the gap is biggest
    ins_pos = gaps.index(max(gaps))
    result.insert(ins_pos, med_val)

    return(result)


class RwHandles:

    def __init__(self, fname_in, level, multiple_files):
        self.level = level
        self.in_cnt = 1
        self.out_cnt = 1
        self.base_cnt = 1
        self.open_read(fname_in)
        self.multiple_files = multiple_files
        p = re.compile("\..{3}$")
        self.fname_base = p.sub('', fname_in)

        fname_out = \
            self.fname_base + "_" + \
            str(self.level + 1) + "_" + \
            str(self.out_cnt) + ".csv"
        self.open_write(fname_out)

        fname_basechunk = \
            self.fname_base + "_" + \
            str(self.level) + "_" + \
            str(self.base_cnt) + ".csv"
        self.open_basechunk(fname_basechunk)

    def open_read(self, fname):
        if os.path.exists(fname):
            self.file_in = open(fname, 'r')
            self.reader = csv.reader(self.file_in)
            return(True)
        else:
            return(False)

    def open_write(self, fname):
        self.file_out = open(fname, 'w')
        self.writer = csv.writer(self.file_out, delimiter=SEP)

    def open_basechunk(self, fname):
        self.file_basechunk = open(fname, 'w')
        self.basechunk = csv.writer(self.file_basechunk, delimiter=SEP)

    def get_next_row(self):
        try: # try to read from current file
            row = self.reader.next()
        except: # if fails read from next
            if self.next_read() & self.multiple_files:
                row = self.reader.next()
            else: # if there's no next file return empty row
                row = []
        return(row) # returns next row or []

    def next_read(self):
        self.close_read()
        self.in_cnt += 1
        fname = \
            self.fname_base + "_" + \
            str(self.level) + "_" + \
            str(self.in_cnt) + ".csv"

        if os.path.exists(fname):
            self.open_read(fname)
            return(True)
        else:
            return(False)

    def next_basechunk(self):
        self.close_basechunk()
        self.base_cnt += 1
        fname = \
            self.fname_base + "_" + \
            str(self.level) + "_" + \
            str(self.base_cnt) + ".csv"
        self.open_basechunk(fname)

    def next_write(self):
        self.close_write()
        self.out_cnt += 1
        fname = \
            self.fname_base + "_" + \
            str(self.level + 1) + "_" + \
            str(self.out_cnt) + ".csv"
        self.open_write(fname)

    def close_read(self):
        self.file_in.close()

    def close_write(self):
        self.file_out.close()

    def close_basechunk(self):
        self.file_basechunk.close()

    def close_all(self):
        self.close_read()
        self.close_write()
        self.close_basechunk()


def gen_ds_data(fname_in, multiple_files, level):
    if multiple_files:
        fname_in = \
            fname_in + "_" + \
            str(level) + "_1.csv"
    rw_hand = RwHandles(fname_in=fname_in, multiple_files=multiple_files, level=level)

    row = val_names = rw_hand.get_next_row()
    # create list of columns
    val_list = {}
    for i in range(len(val_names)):
        val_list[i] = []

    print(val_names)

    # go through all the other lines
    #for line_num, line in enumerate(file_in.readlines()):
    line_num = 0
    while row != []:
        row = rw_hand.get_next_row()

    #for line_num, row in enumerate(rw_hand.reader):

        # go through all columns and put values in val_list
        for col, val in enumerate(row):
            val_list[col].append(float(val))

        rw_hand.basechunk.writerow(row)

        # downsample every 3 * sample factor values to 3 values
        # the three downsampled values are max, min and medium value
        if line_num % (3*SF) == (3*SF - 1):
            for i in xrange(3):
                out_tab = []
                # asuming we only have numerical data
                for col in val_list.keys():
                    out_tab.append(down_samp(val_list[col])[i])

                rw_hand.writer.writerow(out_tab)

            #reset val_list after each downsample cycle
            for i in range(len(val_names)):
                val_list[i] = []

        # open a new file every CSZ (chunk size)
        if line_num % CSZ == CSZ - 1:
            rw_hand.next_basechunk()
            print(rw_hand.file_basechunk.name)

        if line_num % (CSZ*SF) == CSZ*SF - 1:
            rw_hand.next_write()
            print(rw_hand.file_out.name)

        line_num += 1

    rw_hand.close_all()


# main body #==================================================================

fname_in = ''
if len(sys.argv) > 0:
    fname_in = sys.argv[1]
else:
    raise NameError('No input file specified!')


gen_ds_data(fname_in=fname_in, multiple_files=False, level=1)
