<!-- # CoReVLA: A Dual-Stage End-to-End Autonomous Driving Framework for Long-Tail Scenarios via Collect-and-Refine -->

<div align ="center">

<img src="./assets/CoReVLA_icon.png" width="100%">

</div>



<!-- ## Introduction -->
## Abstract

Autonomous Driving (AD) systems have made notable progress, but their performance in long-tail, safety-critical scenarios remains limited. These rare cases contribute a disproportionate number of accidents. Vision-Language Action (VLA) models have strong reasoning abilities and offer a potential solution, but their effectiveness is limited by the lack of high-quality data and inefficient learning in such conditions. To address these challenges, we propose CoReVLA, a continual learning end-to-end autonomous driving framework that improves the performance in long-tail scenarios through a dual-stage process of **data Collection and behavior Refinement**. First, the model is jointly fine-tuned on a mixture of open-source driving QA datasets, allowing it to acquire a foundational understanding of driving scenarios. Next, CoReVLA is deployed within the Cave Automatic Virtual Environment (CAVE) simulation platform, where driver takeover data is collected from real-time interactions. Each takeover indicates a long-tail scenario that CoReVLA fails to handle reliably. Finally, the model is refined via Direct Preference Optimization (DPO), allowing it to learn directly from human preferences and thereby avoid reward hacking caused by manually designed rewards. Extensive open-loop and closed-loop experiments demonstrate that the proposed CoReVLA model can accurately perceive driving scenarios and make appropriate decisions. On the Bench2Drive benchmark, CoReVLA achieves a Driving Score (DS) of 72.18 and a Success Rate (SR) of 50\%, outperforming state-of-the-art methods by 7.96 DS and 15\% SR under long-tail, safety-critical scenarios. Furthermore, case studies demonstrate the model’s ability to continually improve its performance in similar failure-prone scenarios by leveraging past takeover experiences.

## Overview
<div align="center">
<img src="assets/CoReVLA_framework.png" width="1000">
</div>


## Currently Supported Features

- [x] ORION Inference Framework
- [x] Open-loop Evaluation
- [x] Close-loop Evalution
- [x] ORION Checkpoint
- [ ] Chat-B2D Dataset 
- [ ] ORION Training Framework



## Getting Started

```
git clone https://github.com/xiaomi-mlab/Orion.git
cd ./ORION
conda create -n orion python=3.8 -y
conda activate orion
pip install torch==2.4.1+cu118 torchvision==0.19.1+cu118 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu118
pip install -v -e .
pip install -r requirements.txt

```


## Preperation
You can refer to [here](https://github.com/Thinklab-SJTU/Bench2DriveZoo/blob/uniad/vad/docs/DATA_PREP.md) to prepare the Bench2drive dataset.

ORION uses the pretrained [2D llm weights](https://huggingface.co/exiawsh/pretrain_qformer/) and [vision encoder + projector weights](https://github.com/NVlabs/OmniDrive/releases/download/v1.0/eva02_petr_proj.pth) provided by [Omnidrive](https://github.com/NVlabs/OmniDrive/tree/main)
```
cd /path/to/OmniDrive
mkdir ckpts
```
The vision encoder + projector weights are extracted from ckpts/pretrain_qformer/, which is pretrained by using llava data.


## Open-loop evaluation

You can perform an open-loop evaluation of ORION with the following command

``` 
./adzoo/orion/orion_dist_eval.sh adzoo/orion/configs/orion_stage3.py [--PATH_CHECKPOINTS] 1
```

You also can perform a CoT inference of ORION with (this might be quite slow)

``` 
./adzoo/orion/orion_dist_eval.sh adzoo/orion/configs/orion_stage3_cot.py [--PATH_CHECKPOINTS] 1
```

We recommend inference for ORION on an NVIDIA A100 or other GPUs with more than **32GB** of memory (inference in **FP32**, as default).

Meanwhile, Orion can also perform **FP16** inference and achieve almost the same performance. We recommend fp16 inference on a GPU with more than **17GB** of memory.

``` 
./adzoo/orion/orion_dist_eval.sh adzoo/orion/configs/orion_stage3_fp16.py [--PATH_CHECKPOINTS] 1
```

## Close-loop evaluation

You can refer to [here](https://github.com/Thinklab-SJTU/Bench2Drive) to clone Bench2Drive evaluation tools and prepare CARLA for it.

Follow [here](https://github.com/Thinklab-SJTU/Bench2Drive?tab=readme-ov-file#eval-tools) to use evaluation tools of Bench2Drive.

Note that you may first verify the correctness of the team agent， you need to set GPU_RANK, TEAM_AGENT, TEAM_CONFIG in the eval scripts.

You can set as following for close-loop evaluation 
```
TEAM_CONFIG=adzoo/orion/configs/orion_stage3_agent.py+[CHECKPOINT_PATH]
```

## Results and Checkpoints

### Orion and other baselines
The results of UniAD & VAD are refer to the official results of [Bench2DriveZoo](https://github.com/Thinklab-SJTU/Bench2DriveZoo)

| Method | L2 (m) 2s | Driving Score | Success Rate(%) | Config | Download | Eval Json|
| :---: | :---: | :---: | :---: |  :---: | :---: | :---: |
| UniAD-Tiny |0.80 | 40.73 |  13.18 | [config](https://github.com/Thinklab-SJTU/Bench2DriveZoo/tree/uniad/vad/adzoo/uniad/configs/stage2_e2e/base_e2e_b2d.py) | [Hugging Face](https://huggingface.co/rethinklab/Bench2DriveZoo/blob/main/uniad_tiny_b2d.pth)/[Baidu Cloud](https://pan.baidu.com/s/1psr7AKYHD7CitZ30Bz-9sA?pwd=1234 )| [Json](assets/results/UniAD-Tiny.json) |
| UniAD-Base |0.73 | 45.81  |  16.36 | [config](https://github.com/Thinklab-SJTU/Bench2DriveZoo/tree/uniad/vad/adzoo/uniad/configs/stage2_e2e/tiny_e2e_b2d.py) | [Hugging Face](https://huggingface.co/rethinklab/Bench2DriveZoo/blob/main/uniad_base_b2d.pth)/[Baidu Cloud](https://pan.baidu.com/s/11p9IUGqTax1f4W_qsdLCRw?pwd=1234) | [Json](assets/results/UniAD-Base.json) |
| VAD        |0.91 | 42.35  | 15.00 | [config](https://github.com/Thinklab-SJTU/Bench2DriveZoo/tree/uniad/vad/adzoo/vad/configs/VAD/VAD_base_e2e_b2d.py) | [Hugging Face](https://huggingface.co/rethinklab/Bench2DriveZoo/blob/main/vad_b2d_base.pth)/[Baidu Cloud](https://pan.baidu.com/s/1rK7Z_D-JsA7kBJmEUcMMyg?pwd=1234) | [Json](assets/results/VAD.json) |
| ORION       |0.68 | 77.74  | 54.62 | [config](adzoo/orion/configs/orion_stage3.py) | [Hugging Face](https://huggingface.co/poleyzdk/Orion/blob/main/Orion.pth)| [Json](assets/results/ORION.json) |


## Qalitative visualization & Analysis
We provide some visualization videos and qualitatively analysis for Orion and compared them with TCP-traj, UniAD-Base, VAD-Base at [here](docs/analysis.md). 


## Citation
If this work is helpful for your research, please consider citing:

```
@article{fu2025orion,
  title={ORION: A Holistic End-to-End Autonomous Driving Framework by Vision-Language Instructed Action Generation},
  author={Haoyu Fu and Diankun Zhang and Zongchuang Zhao and Jianfeng Cui and Dingkang Liang and Chong Zhang and Dingyuan Zhang and Hongwei Xie and Bing Wang and Xiang Bai},
  journal={arXiv:2503.19755},
  year={2025}
}
```
