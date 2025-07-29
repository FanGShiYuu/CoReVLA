---
library_name: peft
license: other
base_model: /share/home/u22537/data/FSY/LLaMA-Factory/models/qwen2.5/Qwen/Qwen2.5-VL-7B-Instruct
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: 20250712-all
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# 20250712-all

This model is a fine-tuned version of [/share/home/u22537/data/FSY/LLaMA-Factory/models/qwen2.5/Qwen/Qwen2.5-VL-7B-Instruct](https://huggingface.co//share/home/u22537/data/FSY/LLaMA-Factory/models/qwen2.5/Qwen/Qwen2.5-VL-7B-Instruct) on the HAD_train, the BDD_train and the lingoqa_action datasets.

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 0.0001
- train_batch_size: 2
- eval_batch_size: 8
- seed: 42
- distributed_type: multi-GPU
- num_devices: 7
- gradient_accumulation_steps: 8
- total_train_batch_size: 112
- total_eval_batch_size: 56
- optimizer: Use adamw_torch with betas=(0.9,0.999) and epsilon=1e-08 and optimizer_args=No additional optimizer arguments
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 3.0

### Training results



### Framework versions

- PEFT 0.12.0
- Transformers 4.49.0
- Pytorch 2.6.0+cu124
- Datasets 3.3.2
- Tokenizers 0.21.0