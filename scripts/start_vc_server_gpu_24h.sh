#!/usr/bin/env bash
#SBATCH --job-name=code-server
#SBTACH --ntasks=1
# --ntasks-per-node=32
#SBATCH --cpus-per-task=8
#SBATCH --mem-per-cpu=16G
# Time format: d-hh:mm:ss
#SBATCH --time=8:00:00
# --partition=es_biol
#SBATCH --account=es_biol
#SBATCH --gpus=1
source ~/.bashrc
module load eth_proxy
module load stack/2024-06
#module load python_cuda/3.11.6
module load code-server
VSC_IP_REMOTE="$(hostname -i)"
echo $VSC_IP_REMOTE
code-server --bind-addr=${VSC_IP_REMOTE}:8898