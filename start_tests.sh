#/!/bin/bash
nohup python train_agent.py --env MsPacman --device 0 --use-skill True --debug False --extractor lin_concat_ext > ast_lin.log 2>&1 &
nohup python train_agent.py --env MsPacman --device 0 --use-skill True --debug False --extractor cnn_concat_ext > ast_cnn.log 2>&1 &
nohup python train_agent.py --env MsPacman --device 0 --use-skill True --debug False --extractor combine_ext > ast_cmb.log 2>&1 &
nohup python train_agent.py --env MsPacman --device 0 --use-skill True --debug False --extractor self_attention_ext > ast_att.log 2>&1 &
nohup python train_agent.py --env MsPacman --device 0 --use-skill True --debug False --extractor reservoir_concat_ext > ast_res.log 2>&1 &