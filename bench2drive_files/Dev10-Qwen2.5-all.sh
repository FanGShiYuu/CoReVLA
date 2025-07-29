#!/bin/bash
#SBATCH --job-name=carla-vlm-run
#SBATCH --comment="VLM service + Carla closed-loop testing"
#SBATCH --partition=L40
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=7
#SBATCH --gres=gpu:l40:1
#SBATCH --time=48:00:00
#SBATCH -o /share/home/u22537/data/FSY/Bench2Drive/outs/%j.out
#SBATCH -e /share/home/u22537/data/FSY/Bench2Drive/outs/%j.err

source /share/apps/miniconda3/etc/profile.d/conda.sh
module load cuda/12.1

# ---------- Launch VLM service ----------
echo "[VLM] Launching VLM web service..."
(
    conda activate b2d-vlm
    cd ../Bench2Drive/B2DVL
    python ../Bench2Drive/B2DVL/Bench2Drive-VL-main/B2DVL_Adapter/web_interact_app.py \
        --config ./vlm_config_all.json
) &

# ---------- Wait for VLM service to be up ----------
# Assuming the web service listens on port 7023 (change if needed)
VLM_PORT=7023
MAX_WAIT=300     # Maximum wait time in seconds
INTERVAL=5       # Check interval

echo "[VLM] Waiting for VLM service to start on port :$VLM_PORT (max wait ${MAX_WAIT}s)..."
SECONDS_WAITED=0
until nc -z localhost $VLM_PORT; do
    sleep $INTERVAL
    SECONDS_WAITED=$((SECONDS_WAITED + INTERVAL))
    echo "[VLM] Port $VLM_PORT not yet available, waited ${SECONDS_WAITED}s..."
    if [ $SECONDS_WAITED -ge $MAX_WAIT ]; then
        echo "[ERROR] Timeout: VLM service failed to start within ${MAX_WAIT}s"
        exit 1
    fi
done

echo "[VLM] VLM service is ready. Launching Carla experiments..."

# ---------- Launch Carla closed-loop task ----------
(
    conda activate b2d-carla
    cd ../Bench2Drive/B2DVL/Bench2Drive-VL-main
    source ../Bench2Drive/B2DVL/env.sh
    bash startup_closeloop_all.sh
) &

# ---------- Wait for both subprocesses ----------
wait
echo "[DONE] VLM and Carla have both completed execution."
