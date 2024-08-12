#/!/bin/bash
nohup python train_agent.py --env Seaquest --device 0 --use-skill True --debug False --extractor lin_concat_ext > si_lin.log 2>&1 &
nohup python train_agent.py --env Seaquest --device 0 --use-skill True --debug False --extractor cnn_concat_ext > si_cnn.log 2>&1 &
nohup python train_agent.py --env Seaquest --device 1 --use-skill True --debug False --extractor combine_ext > si_cmb.log 2>&1 &
nohup python train_agent.py --env Seaquest --device 1 --use-skill True --debug False --extractor self_attention_ext > si_att.log 2>&1 &
nohup python train_agent.py --env Seaquest --device 2 --use-skill True --debug False --extractor reservoir_concat_ext > si_res.log 2>&1 &
