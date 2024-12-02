#!/usr/bin/env bash
#SBATCH --job-name=code-server
# --ntasks=1
# --ntasks-per-node=32
#SBATCH --cpus-per-task=64
#SBATCH --mem-per-cpu=2G
# Time format: d-hh:mm:ss
#SBATCH --time=4:00:00
#SBATCH --partition=es_biol
#SBATCH --account=es_biol
# --gpus=1
source ~/.bashrc
module load eth_proxy
module load stack/2024-06
#module load python/3.11.6_cuda
module load code-server
VSC_IP_REMOTE="$(hostname -i)"
echo $VSC_IP_REMOTE
code-server --bind-addr=${VSC_IP_REMOTE}:8898