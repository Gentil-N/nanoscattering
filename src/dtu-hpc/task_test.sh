#!/usr/bin/env bash
#BSUB -J Test
#BSUB -q hpc
#BSUB -W 8:00
#BSUB -R "span[hosts=1]"
#BSUB -n 1
#BSUB -M 2GB
#BSUB -u nevgen@dtu.dk
#BSUB -o ./output/log_test.out
#BSUB -e ./output/log_test.error

module load python3

source venv/bin/activate

python3 src/main.py