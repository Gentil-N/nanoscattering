#!/usr/bin/env bash
#BSUB -J ComputeSurface
#BSUB -q hpc
#BSUB -W 8:00
#BSUB -R "span[hosts=1]"
#BSUB -n 8
#BSUB -M 2GB
#BSUB -u nevgen@dtu.dk
#BSUB -o ./output/log_computesurface.out
#BSUB -e ./output/log_computesurface.error

module load python3

source venv/bin/activate

python3 src/computesurface.py