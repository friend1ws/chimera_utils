#! /usr/bin/env python

import sys, os, subprocess
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


def merge_control_main(args):

    # make directory for output if necessary
    # if os.path.dirname(args.output_file) != "" and not os.path.exists(os.path.dirname(args.output_file)):
    #     os.makedirs(os.path.dirname(args.output_file))

    subprocess.call(["touch", args.output_file + ".unsorted"])
    hout = open(args.output_file + ".unsorted", 'a')

    with open(args.chimeric_count_list, 'r') as hin:
        for line in hin:
            count_file = line.rstrip('\n')
            with open(count_file, 'r') as hin2:
                subprocess.call(["cut", "-f1-7", count_file], stdout = hout)

    hout.close()


    hout = open(args.output_file + ".sorted", 'w')
    s_ret = subprocess.call(["sort", "-k1,1", "-k2,2n", "-k4,4", "-k5,5n", "-u", args.output_file + ".unsorted"], stdout = hout)
    hout.close()

    hout = open(args.output_file, 'w')
    s_ret = subprocess.call(["bgzip", "-f", "-c", args.output_file + ".sorted"], stdout = hout)
    hout.close()

    if s_ret != 0:
        print >> sys.stderr, "Error in compression merged junction file"
        sys.exit(1)


    s_ret = subprocess.call(["tabix", "-p", "vcf", args.output_file])
    if s_ret != 0:
        print >> sys.stderr, "Error in indexing merged junction file"
        sys.exit(1)

    subprocess.call(["rm", "-f", args.output_file + ".unsorted"])
    subprocess.call(["rm", "-f", args.output_file + ".sorted"])


