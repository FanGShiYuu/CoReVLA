<!-- # CoReVLA: A Dual-Stage End-to-End Autonomous Driving Framework for Long-Tail Scenarios via Collect-and-Refine -->

<div align ="center">

<img src="./assets/CoReVLA_icon.png" width="100%">

</div>



<!-- ## Introduction -->
## Abstract

Autonomous Driving (AD) systems have made notable progress, but their performance in long-tail, safety-critical scenarios remains limited. These rare cases contribute a disproportionate number of accidents. Vision-Language Action (VLA) models have strong reasoning abilities and offer a potential solution, but their effectiveness is limited by the lack of high-quality data and inefficient learning in such conditions. To address these challenges, we propose CoReVLA, a continual learning end-to-end autonomous driving framework that improves the performance in long-tail scenarios through a dual-stage process of **data Collection and behavior Refinement**. First, the model is jointly fine-tuned on a mixture of open-source driving QA datasets, allowing it to acquire a foundational understanding of driving scenarios. Next, CoReVLA is deployed within the Cave Automatic Virtual Environment (CAVE) simulation platform, where driver takeover data is collected from real-time interactions. Each takeover indicates a long-tail scenario that CoReVLA fails to handle reliably. Finally, the model is refined via Direct Preference Optimization (DPO), allowing it to learn directly from human preferences and thereby avoid reward hacking caused by manually designed rewards. Extensive open-loop and closed-loop experiments demonstrate that the proposed CoReVLA model can accurately perceive driving scenarios and make appropriate decisions. On the Bench2Drive benchmark, CoReVLA achieves a Driving Score (DS) of 72.18 and a Success Rate (SR) of 50\%, outperforming state-of-the-art methods by 7.96 DS and 15\% SR under long-tail, safety-critical scenarios. Furthermore, case studies demonstrate the model’s ability to continually improve its performance in similar failure-prone scenarios by leveraging past takeover experiences.

## Highlights
<div align="center">
<img src="assets/CoReVLA_framework.png" width="1000">
</div>


## TODO List 🔨
- [x] Train and Eval Code 
- [x] DPO Dataset Part 1 (LingoQA)
- [x] Model Checkpoint before Refinement
- [ ] Model Checkpoint after Refinement 
- [ ] DPO Dataset Part 2 (Takeover in CAVE)



## Getting Started

### STF datasets

```
git clone https://github.com/xiaomi-mlab/Orion.git
cd ./ORION
conda create -n orion python=3.8 -y
conda activate orion
pip install torch==2.4.1+cu118 torchvision==0.19.1+cu118 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu118
pip install -v -e .
pip install -r requirements.txt

```

### Carla prepare



## Results



## Citation
If this work is helpful for your research, please consider citing:

```

```
