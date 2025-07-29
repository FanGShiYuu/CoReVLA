#!/bin/bash
BASE_PORT=20082 # CARLA port
BASE_TM_PORT=50000 # CARLA traffic manager port
BASE_ROUTES=./leaderboard/data/drivetransformer_bench2drive_dev10  # path to your route xml /leaderboard/data/drivetransformer_bench2drive_dev10   bench2drive220
TEAM_AGENT=leaderboard/team_code/data_agent.py # path to your agent, in B2DVL, the agent is fixed, so don't modify this
BASE_CHECKPOINT_ENDPOINT=./checkpoint_DEV10_Qwen2.5-all-0716 # path to the checkpoint file with saves sceanario running process and results. 
# If not exist, it will be automatically created.
SAVE_PATH=./eval_v1/ # the directory where seonsor data is saved.
GPU_RANK=0 # the gpu carla runs on
VLM_CONFIG=../vlm_config_short.json # your config json
PORT=$BASE_PORT
TM_PORT=$BASE_TM_PORT
ROUTES="${BASE_ROUTES}.xml"
CHECKPOINT_ENDPOINT="${BASE_CHECKPOINT_ENDPOINT}.json"
export MINIMAL=0 # if MINIMAL > 0, DriveCommenter takes control of the ego vehicle,
# and vlm server is not needed
bash leaderboard/scripts/run_evaluation.sh $PORT $TM_PORT 1 $ROUTES $TEAM_AGENT "." $CHECKPOINT_ENDPOINT $SAVE_PATH "null" $GPU_RANK $VLM_CONFIG
