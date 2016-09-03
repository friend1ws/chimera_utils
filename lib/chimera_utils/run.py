#! /usr/bin/env python

import sys, os, subprocess
import count, process
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



def associate_main(args): 


    process.convert_to_bedpe(args.chimera_file, args.output_file + ".fusion.bedpe", args.sv_margin_major, args.sv_margin_minor)
    process.convert_to_bedpe(args.genomonSV_file, args.output_file + ".genomonSV.bedpe", args.margin, args.margin)

    hout = open(args.output_file + ".fusion_comp.bedpe", 'w')
    subprocess.check_call(["bedtools", "pairtopair", "-a", args.output_file + ".fusion.bedpe", "-b", args.output_file + ".genomonSV.bedpe"], stdout = hout)
    hout.close()

    # create dictionary
    chimera2sv = {}
    hin = open(args.output_file + ".fusion_comp.bedpe", 'r')
    for line in hin:
        F = line.rstrip('\n').split('\t')
        chimera2sv[F[6]] = F[16]
    
    hin.close()

    from annot_utils.gene import *
    from annot_utils.exon import *
    from annot_utils.annotation import *

    make_gene_info(args.output_file + ".refGene.bed.gz", "ref", args.genome_id, args.is_grc, False)
    make_exon_info(args.output_file + ".refExon.bed.gz", "ref", args.genome_id, args.is_grc, False)
    make_gene_info(args.output_file + ".ensGene.bed.gz", "ens", args.genome_id, args.is_grc, False)
    make_exon_info(args.output_file + ".ensExon.bed.gz", "ens", args.genome_id, args.is_grc, False)

    ref_gene_tb = pysam.TabixFile(args.output_file + ".refGene.bed.gz")
    ref_exon_tb = pysam.TabixFile(args.output_file + ".refExon.bed.gz")
    ens_gene_tb = pysam.TabixFile(args.output_file + ".ensGene.bed.gz")
    ens_exon_tb = pysam.TabixFile(args.output_file + ".ensExon.bed.gz")


    # add SV annotation to fusion
    hin = open(args.chimera_file, 'r')
    hout = open(args.output_file, 'w')
    for line in hin:
        F = line.rstrip('\n').split('\t')
        ID = ','.join([F[0], F[1], F[2], F[3], F[4], F[5], F[6]])

        if ID not in chimera2sv: continue
        SV_info = chimera2sv[ID]

        ref_gene_info_1 = get_gene_info(F[0], F[1], ref_gene_tb) 
        ens_gene_info_1 = get_gene_info(F[0], F[1], ens_gene_tb)
        gene_info_1 = ref_gene_info_1 if len(ref_gene_info_1) > 0 else ens_gene_info_1

        ref_gene_info_2 = get_gene_info(F[3], F[4], ref_gene_tb)
        ens_gene_info_2 = get_gene_info(F[3], F[4], ens_gene_tb)
        gene_info_2 = ref_gene_info_2 if len(ref_gene_info_2) > 0 else ens_gene_info_2
        
        junc_info_1 = get_junc_info(F[0], F[1], ref_exon_tb, 5) 
        if len(junc_info_1) == 0: junc_info_1 = get_junc_info(F[0], F[1], ens_exon_tb, 5)
        
        junc_info_2 = get_junc_info(F[3], F[4], ref_exon_tb, 5) 
        if len(junc_info_2) == 0: junc_info_2 = get_junc_info(F[3], F[4], ens_exon_tb, 5)


        same_gene_flag = False        
        for g1 in ref_gene_info_1 + ens_gene_info_1:
            for g2 in ref_gene_info_2 + ens_gene_info_2:
                if g1 == g2: same_gene_flag = True

        gene_info_str_1 = "---" if len(gene_info_1) == 0 else ','.join(list(set(gene_info_1)))
        gene_info_str_2 = "---" if len(gene_info_2) == 0 else ','.join(list(set(gene_info_2)))
        junc_info_str_1 = "---" if len(junc_info_1) == 0 else ','.join(list(set(junc_info_1)))
        junc_info_str_2 = "---" if len(junc_info_2) == 0 else ','.join(list(set(junc_info_2)))


        sv_chr1, sv_pos1, sv_dir1, sv_chr2, sv_pos2, sv_dir2, sv_inseq = SV_info.split(',')

        
        if junc_info_str_1 != "---" or junc_info_str_2 != "---":
            if sv_dir1 == '-' and sv_dir2 == '+' and same_gene_flag == True:
                chimera_type = "exon_reusage"
            else:
                chimera_type = "spliced_chimera"
        elif abs(int(F[1]) - int(sv_pos1)) < 30 and abs(int(F[4]) - int(sv_pos2)) < 30:
            chimera_type = "unspliced_chimera"
        else:
            chimera_type = "putative_spliced_chimera"


        print >> hout, '\t'.join(F) + '\t' + gene_info_str_1 + '\t' + gene_info_str_2 + '\t' + \
                       junc_info_str_1 + '\t' + junc_info_str_2 + '\t' + \
                       chimera_type + '\t' + SV_info

    hin.close()
    hout.close()


    if args.debug == False:
        subprocess.call(["rm", "-rf", args.output_file + ".fusion.bedpe"])
        subprocess.call(["rm", "-rf", args.output_file + ".genomonSV.bedpe"])
        subprocess.call(["rm", "-rf", args.output_file + ".fusion_comp.bedpe"])
        subprocess.call(["rm", "-rf", args.output_file + ".refGene.bed.gz"])
        subprocess.call(["rm", "-rf", args.output_file + ".refGene.bed.gz.tbi"])
        subprocess.call(["rm", "-rf", args.output_file + ".refExon.bed.gz"])
        subprocess.call(["rm", "-rf", args.output_file + ".refExon.bed.gz.tbi"])
        subprocess.call(["rm", "-rf", args.output_file + ".ensGene.bed.gz"])
        subprocess.call(["rm", "-rf", args.output_file + ".ensGene.bed.gz.tbi"])
        subprocess.call(["rm", "-rf", args.output_file + ".ensExon.bed.gz"])
        subprocess.call(["rm", "-rf", args.output_file + ".ensExon.bed.gz.tbi"])
  

