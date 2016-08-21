#! /usr/bin/env python

import sys, subprocess
import count
import fusionfusion.parseJunctionInfo
from fusionfusion.config import *

def count_main(args):

    param_conf.debug = args.debug
    param_conf.abnormal_insert_size = args.abnormal_insert_size
    param_conf.min_major_clipping_size = args.min_major_clipping_size
    param_conf.min_read_pair_num = args.min_read_pair_num
    param_conf.min_cover_size = args.min_cover_size
    param_conf.anchor_size_thres = args.anchor_size_thres
    param_conf.min_chimeric_size = args.min_chimeric_size
    # param_conf.min_allowed_contig_match_diff = args.min_allowed_contig_match_diff
    # param_conf.check_contig_size_other_breakpoint = args.check_contig_size_other_breakpoint
    # param_conf.filter_same_gene = args.filter_same_gene
    # param_conf.reference_genome = args.reference_genome
    # param_conf.resource_dir = args.resource_dir


    fusionfusion.parseJunctionInfo.parseJuncInfo_STAR(args.chimeric_sam, args.output_file + ".chimeric.tmp.txt")

    hout = open(args.output_file + ".chimeric.txt", 'w')
    subprocess.call(["sort", "-k1,1", "-k2,2n", "-k4,4", "-k5,5n", args.output_file + ".chimeric.tmp.txt"], stdout = hout)
    hout.close()

    fusionfusion.parseJunctionInfo.clusterJuncInfo(args.output_file + ".chimeric.txt",
                                                   args.output_file + ".chimeric.clustered.txt")

    count.get_chimera_info(args.output_file + ".chimeric.clustered.txt", args.output_file)

    if param_conf.debug == False:
        subprocess.call(["rm", "-rf", args.output_file + ".chimeric.tmp.txt"])
        subprocess.call(["rm", "-rf", args.output_file + ".chimeric.txt"])
        subprocess.call(["rm", "-rf", args.output_file + ".chimeric.clustered.txt"])

