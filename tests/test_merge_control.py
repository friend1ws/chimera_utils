#! /usr/bin/env python

import unittest
import os, glob, tempfile, shutil, filecmp
import chimera_utils 

class TestMergeControl(unittest.TestCase):

    def setUp(self):
        # prepare reference genome
        cur_dir = os.path.dirname(os.path.abspath(__file__))

        self.parser = chimera_utils.parser.create_parser()


    def test1(self):

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        tmp_dir = tempfile.mkdtemp()

        all_count_file = glob.glob(cur_dir + "/data/count/*.Chimeric.count.txt")
        with open(tmp_dir + "/chimera_utils.count_list.txt", 'w') as hout:
            for count_file in sorted(all_count_file):
                print >> hout, count_file

        count_list_file = tmp_dir + "/chimera_utils.count_list.txt"
 
        output_file = tmp_dir + "/merge_control/merge_control.txt.gz"
        answer_file = cur_dir + "/data/merge_control/merge_control.txt.gz"


        args = self.parser.parse_args(["merge_control", count_list_file, output_file])
        args.func(args)

        self.assertTrue(filecmp.cmp(output_file, answer_file, shallow=False))

        shutil.rmtree(tmp_dir)


if __name__ == "__main__":
    unittest.main()

