<!-- # CoReVLA: A Dual-Stage End-to-End Autonomous Driving Framework for Long-Tail Scenarios via Collect-and-Refine -->

<div align ="center">

<img src="./assets/CoReVLA_icon.png" width="100%">

</div>



<!-- ## Introduction -->
## Abstract

Autonomous Driving (AD) systems have made notable progress, but their performance in long-tail, safety-critical scenarios remains limited. These rare cases contribute a disproportionate number of accidents. Vision-Language Action (VLA) models have strong reasoning abilities and offer a potential solution, but their effectiveness is limited by the lack of high-quality data and inefficient learning in such conditions. To address these challenges, we propose CoReVLA, a continual learning end-to-end autonomous driving framework that improves the performance in long-tail scenarios through a dual-stage process of **data Collection and behavior Refinement**. First, the model is jointly fine-tuned on a mixture of open-source driving QA datasets, allowing it to acquire a foundational understanding of driving scenarios. Next, CoReVLA is deployed within the Cave Automatic Virtual Environment (CAVE) simulation platform, where driver takeover data is collected from real-time interactions. Each takeover indicates a long-tail scenario that CoReVLA fails to handle reliably. Finally, the model is refined via Direct Preference Optimization (DPO), allowing it to learn directly from human preferences and thereby avoid reward hacking caused by manually designed rewards. Extensive open-loop and closed-loop experiments demonstrate that the proposed CoReVLA model can accurately perceive driving scenarios and make appropriate decisions. On the Bench2Drive benchmark, CoReVLA achieves a Driving Score (DS) of 72.18 and a Success Rate (SR) of 50\%, outperforming state-of-the-art methods by 7.96 DS and 15\% SR under long-tail, safety-critical scenarios. Furthermore, case studies demonstrate the model’s ability to continually improve its performance in similar failure-prone scenarios by leveraging past takeover experiences.

---

## Highlights
<div align="center">
<img src="assets/CoReVLA_framework.png" width="1000">
</div>

* **HITL-based data collection in immersive simulation.** We collect visually grounded takeover data from the CAVE platform, enabling capture of failure cases in long-tail scenarios.
* **DPO-based behavior refinement.** We apply Direct Preference Optimization to efficiently align the model with human intent using sparse but high-quality takeover data.
  
---

## TODO List 🔨
- [x] Train and Eval Code 
- [x] DPO Dataset Part 1 (LingoQA)
- [x] Model Checkpoint before Refinement
- [ ] Model Checkpoint after Refinement 
- [ ] DPO Dataset Part 2 (Takeover in CAVE)

---

## Getting Started

### CARLA Setup

```bash
mkdir carla && cd carla
wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/CARLA_0.9.15.tar.gz
tar -xvf CARLA_0.9.15.tar.gz
cd Import
wget https://carla-releases.s3.us-east-005.backblazeb2.com/Linux/AdditionalMaps_0.9.15.tar.gz
cd .. && bash ImportAssets.sh
```

Set environment variables:

```bash
export CARLA_ROOT=YOUR_CARLA_PATH
echo "$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.15-py3.7-linux-x86_64.egg" >> YOUR_CONDA_PATH/envs/YOUR_CONDA_ENV_NAME/lib/python3.7/site-packages/carla.pth
```

#### Write `env.sh`

```bash
export CARLA_ROOT=/path/to/your/carla
export CARLA_SERVER=${CARLA_ROOT}/CarlaUE4.sh
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.15-py3.7-linux-x86_64.egg

export WORK_DIR=/path/to/this/repo
export PYTHONPATH=$PYTHONPATH:${WORK_DIR}/scenario_runner:${WORK_DIR}/leaderboard:${WORK_DIR}/B2DVL_Adapter

export SCENARIO_RUNNER_ROOT=${WORK_DIR}/scenario_runner
export LEADERBOARD_ROOT=${WORK_DIR}/leaderboard

export VQA_GEN=1
export STRICT_MODE=1
```

#### Activate Environment

```bash
source ./env.sh
```
---

### Bench2Drive Setup
```bash
git clone https://github.com/Thinklab-SJTU/Bench2Drive-VL
```




## Data Release
### STF Datasets
| Base Dataset | Instruction |      Size    |   Released  |
|:-------------:|:-----------------------:|:------------:|:----------:|
| [BDD-100k](https://bdd-data.berkeley.edu/)| Used for multi-task autonomous driving benchmarks:<br> detection, segmentation, tracking, prediction. | 100k figures with textual explanation and description | O |
| [HAD HRI](https://usa.honda-ri.com/had)  | Supports research on driver behavior, takeover intention,<br> and human-automation responsibility modeling.  | 4319 videos of 20 seconds long with textual explanation and description <br>(3926 in Train; 1123 in Val) | O |
| [LingoQA](https://github.com/wayveai/LingoQA)   | Evaluates visual-language models through question answering on images or video content. | Scenario clips with 5 seconds length and language annotations <br>(267.8k QA in Congition; 152.5 QA in Decision) | O |

Example of STF dataset format
 ```
 {
    "video_id": "test0001.mp4", 
    "QA": {
        "q": "How did the car handle the oncoming traffic before making the left turn?", 
        "a": "The ego-car detected oncoming traffic and stopped to wait until the lane was clear. It maintained the stopped position for quite some time and only proceeded to turn left when it was safe to do so. "
    }
 }
 ```



### DPO Datasets
| Base Dataset | Instruction |      Size    |   Released  |
|:-------------:|:-----------------------:|:------------:|:----------:|
| [Part1](https://bdd-data.berkeley.edu/)| Used for multi-task autonomous driving benchmarks:<br> detection, segmentation, tracking, prediction. | 9k decision preference pairs with language annotations | O |
| [Part2](https://usa.honda-ri.com/had)  | Supports research on driver behavior, takeover intention,<br> and human-automation responsibility modeling.  | Takeover data in CAVE | x |

Example of DPO dataset format
 ```
 {
    "video_id": "test0001.mp4", 
    "QA": {
        "q": "How did the car handle the oncoming traffic before making the left turn?", 
        "a": "The ego-car detected oncoming traffic and stopped to wait until the lane was clear. It maintained the stopped position for quite some time and only proceeded to turn left when it was safe to do so. "
    }
 }
 ```

## Citation
If this work is helpful for your research, please consider citing:

```

```
