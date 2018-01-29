#! /usr/bin/env python

import unittest
import os, tempfile, shutil, filecmp
import chimera_utils 

class TestAssociate(unittest.TestCase):

    def setUp(self):
        # prepare reference genome
        cur_dir = os.path.dirname(os.path.abspath(__file__))

        self.parser = chimera_utils.parser.create_parser()


    def test1(self):

        cur_dir = os.path.dirname(os.path.abspath(__file__))
        tmp_dir = tempfile.mkdtemp()

        count_file = cur_dir + "/data/count/K562.Chimeric.count.txt"
        sv_file = cur_dir + "/data/sv/CCLE-K-562-DNA-08.genomonSV.result.txt"
        output_file = tmp_dir + "/K562.Chimeric.count.associate.txt"
        answer_file = cur_dir + "/data/associate/K562.Chimeric.count.associate.txt"

        args = self.parser.parse_args(["associate", count_file, sv_file, output_file, "--grc"])
        args.func(args)

        self.assertTrue(filecmp.cmp(output_file, answer_file, shallow=False))

        shutil.rmtree(tmp_dir)

if __name__ == "__main__":
    unittest.main()

