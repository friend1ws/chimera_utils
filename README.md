# chimera_utils

## Introduction 

This is a suite of tools for processing chimeric reads generated at a STAR alignment step (Chimeric.out.sam files).

## Dependency

### Python
Python (>= 2.7), `pysam (>= 0.8.1)`

### Software
[hstlib](http://www.htslib.org)


## Install

```
git clone https://github.com/friend1ws/chimera_utils.git
cd chimera_utils
python setup.py build install
```
For the last command, you may need to add --user if using a shared computing cluster.

## Commands

### count
Count supporting read pairs for each chimera junction

```
chimera_utils count [-h] [--abnormal_insert_size ABNORMAL_INSERT_SIZE]
                          [--min_major_clipping_size MIN_MAJOR_CLIPPING_SIZE]
                          [--min_read_pair_num MIN_READ_PAIR_NUM]
                          [--min_cover_size MIN_COVER_SIZE]
                          [--anchor_size_thres ANCHOR_SIZE_THRES]
                          [--min_chimeric_size MIN_CHIMERIC_SIZE] [--debug]
                          Chimeric.out.sam output_file
```

### merge_control
Merge chimeric junction cout file (generated by `count` command) of control data (typically) for later filtering

```
chimera_utils merge_control [-h] chimeric_count_list.txt output_file
```
