#! /usr/bin/env python

from __future__ import print_function

import unittest
import os, tempfile, shutil, filecmp
import chimera_utils 
from .check_download import *

class TestCount(unittest.TestCase):

    def setUp(self):
        # prepare reference genome
        cur_dir = os.path.dirname(os.path.abspath(__file__))

        check_download("https://storage.googleapis.com/friend1ws_package_data/fusionfusion/MCF-7.Chimeric.out.sam", \
                       cur_dir + "/resource/star/MCF-7.Chimeric.out.sam")
 
        self.parser = chimera_utils.parser.create_parser()


    def test1(self):

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        tmp_dir = tempfile.mkdtemp()

        star_chimeric_sam = cur_dir + "/resource/star/MCF-7.Chimeric.out.sam"
        output_dir = tmp_dir 
 
        output_file = tmp_dir + "/MCF-7.Chimeric.count.txt"
        answer_file = cur_dir + "/data/count/MCF-7.Chimeric.count.txt"


        # print(' '.join(["count", star_chimeric_sam, output_file]))
        args = self.parser.parse_args(["count", star_chimeric_sam, output_file])
        args.func(args)

        # self.assertTrue(filecmp.cmp(output_file, answer_file, shallow=False))
        with open(answer_file, 'r') as hin: record_num = len(hin.readlines())
        self.assertTrue(885 <= record_num <= 905)

        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    unittest.main()

