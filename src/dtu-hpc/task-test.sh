#!/usr/bin/env bash
#BSUB -J test
#BSUB -q hpc
#BSUB -W 8:00
#BSUB -R "span[hosts=1]"
#BSUB -n 1
#BSUB -M 2GB
#BSUB -u nevgen@dtu.dk
#BSUB -o ./output/log.out
#BSUB -e ./output/log.error

source venv/bin/activate

python3 src/main.py