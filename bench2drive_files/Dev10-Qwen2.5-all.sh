#!/bin/bash
#SBATCH --job-name=carla-vlm-run
#SBATCH --comment="VLM服务 + Carla闭环测试"
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

# ---------- 启动 VLM 服务 ----------
echo "[VLM] 启动 VLM Web 服务中..."
(
    conda activate b2d-vlm
    cd /share/home/u22537/data/FSY/Bench2Drive/B2DVL
    python /share/home/u22537/data/FSY/Bench2Drive/B2DVL/Bench2Drive-VL-main/B2DVL_Adapter/web_interact_app.py \
        --config ./vlm_config_all.json
) &

# ---------- 等待 VLM 服务启动 ----------
# 假设 Web 服务监听 7023 端口（你可修改成实际端口）
VLM_PORT=7023
MAX_WAIT=300     # 最长等待时间（秒）
INTERVAL=5       # 检测间隔

echo "[VLM] 等待 VLM 服务端口 :$VLM_PORT 启动中（最多等待 ${MAX_WAIT}s）..."
SECONDS_WAITED=0
until nc -z localhost $VLM_PORT; do
    sleep $INTERVAL
    SECONDS_WAITED=$((SECONDS_WAITED + INTERVAL))
    echo "[VLM] 仍未检测到端口 $VLM_PORT 开启，已等待 ${SECONDS_WAITED}s..."
    if [ $SECONDS_WAITED -ge $MAX_WAIT ]; then
        echo "[ERROR] 等待超时：VLM 服务未能在 ${MAX_WAIT}s 内启动"
        exit 1
    fi
done

echo "[VLM] VLM 服务已就绪，启动 Carla 实验..."

# ---------- 启动 Carla 闭环任务 ----------
(
    conda activate b2d-carla
    cd /share/home/u22537/data/FSY/Bench2Drive/B2DVL/Bench2Drive-VL-main
    source /share/home/u22537/data/FSY/Bench2Drive/B2DVL/env.sh
    bash startup_closeloop_all.sh
) &

# ---------- 等待两个子进程 ----------
wait
echo "[DONE] VLM 与 Carla 均已完成运行。"