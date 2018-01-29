#! /usr/bin/env python

from run import *
import argparse

def create_parser():

    parser = argparse.ArgumentParser(prog = "chimera_utils")
    parser.add_argument("--version", action = "version", version = "sv_utils-0.4.0b1")

    subparsers = parser.add_subparsers()

    ##########
    # imple intron retention count 

    count = subparsers.add_parser("count",
                                         help = "count supporting read pairs for each chimera junction")

    count.add_argument("chimeric_sam", metavar = "Chimeric.out.sam", default = None, type = str,
                              help = "the path to the chimeric read file generated at STAR alignment step")

    count.add_argument("output_file", metavar = "output_file", default = None, type = str, 
                              help = "the path to the output")

    count.add_argument("--abnormal_insert_size", type = int, default = 500000,
                       help = "size of abnormal insert size. used for checking the consistency of paired read of breakpoint containing reads (default: %(default)s)")

    count.add_argument("--min_major_clipping_size", type = int, default = 15,
                       help = "minimum number of clipped bases for junction read (default: %(default)s)")

    count.add_argument("--min_read_pair_num", type = int, default = 3,
                       help = "minimum required number of supporting junction read pairs (default: %(default)s)")

    count.add_argument("--min_cover_size", type = int, default = 30,
                       help = "region size which have to be covered by aligned short reads (default: %(default)s)")

    count.add_argument("--anchor_size_thres", type = int, default = 10,
                       help = "at least an anchor size of one chimeric read have to be equal or larger than the specified value (default: %(default)s)")
     
    count.add_argument("--min_chimeric_size", type = int, default = 1000,
                       help = "threshold of minimum chimeric transcript sizes (default: %(default)s)")

    count.add_argument("--debug", default = False, action = 'store_true', help = "keep intermediate files")

    count.set_defaults(func = count_main)
    ##########

    # merge control 
    merge_control = subparsers.add_parser("merge_control",
                                          help = "merge, compress and index chimeric count files generated by count command")

    merge_control.add_argument("chimeric_count_list", metavar = "chimeric_count_list.txt", default = None, type = str,
                               help = "chimeric count file list")

    merge_control.add_argument("output_file", default = None, type = str,
                               help = "the path of the output file")

    merge_control.set_defaults(func = merge_control_main)

    """
    ##########
    # filter

    filter = subparsers.add_parser("filter",
                                   help = "filter out intron retentions that do not satisty specified conditions")

    filter.add_argument("intron_retention_file", metavar = "intron_retention.txt", default = None, type = str,
                        help = "the path to intron retention file generated by simple_count command")

    filter.add_argument("output_file", metavar = "output.txt", default = None, type = str,
                        help = "the path to the output file")

    filter.add_argument("--num_thres", type = int, default = 3,
                        help = "remove intron retentions whose supporting read numbers are below this value (default: %(default)s)")

    filter.add_argument("--ratio_thres", type = int, default = 0.05,
                        help = "remove intron retentions whose whose ratios (Intron_Retention_Read_Count / Edge_Read_Count) \
                        are below this value (default: %(default)s)")
                               
    filter.add_argument("--pooled_control_file", default = None, type = str,
                        help = "the path to control data created by merge_control (default: %(default)s)")

    filter.set_defaults(func = filter_main)
    """
    ##########
    # associate

    associate = subparsers.add_parser("associate",
                                      help = "associate chimeras with SVs")

    associate.add_argument("chimera_file", metavar = "chimera.txt", default = None, type = str,
                           help = "the path to chimera file")

    associate.add_argument("genomonSV_file", metavar = "genomonSV.result.txt", default = None, type = str,
                           help = "the path to GenomonSV result file")

    associate.add_argument("output_file", metavar = "output.txt", default = None, type = str,
                             help = "the path to the output")

    associate.add_argument("--margin", default = 10, type = int,
                              help = "the margin for comparing gene fusions")

    associate.add_argument("--sv_margin_major", default = 500000, type = int,
                              help = "the margin for comparing gene fusions and SVs")

    associate.add_argument("--sv_margin_minor", default = 10, type = int,
                              help = "the margin for comparing gene fusions and SVs")

    associate.add_argument("--genome_id", choices = ["hg19", "hg38", "mm10"], default = "hg19",
                           help = "the genome id used for selecting UCSC-GRC chromosome name corresponding files (default: %(default)s)")

    associate.add_argument("--is_grc", default = False, action = 'store_true',
                           help = "convert chromosome names to Genome Reference Consortium nomenclature (default: %(default)s)")

    associate.add_argument("--debug", default = False, action = 'store_true', help = "keep intermediate files")

    associate.set_defaults(func = associate_main)
    ##########

    return parser

