# ["Pong", "Breakout", "BeamRider", "Qbert", "Seaquest", "SpaceInvaders", "RoadRunner", "Enduro", "MsPacman", "Asteroids"]

nohup python train_model.py cuda:0 0 BeamRider > objk_br.log 2>&1 &
nohup python train_model.py cuda:0 0 Qbert > objk_qb.log 2>&1 &
nohup python train_model.py cuda:0 0 Seaquest > objk_sea.log 2>&1 &
nohup python train_model.py cuda:0 0 SpaceInvaders > objk_si.log 2>&1 &
nohup python train_model.py cuda:1 0 RoadRunner > objk_rr.log 2>&1 &
nohup python train_model.py cuda:1 0 Enduro > objk_end.log 2>&1 &
nohup python train_model.py cuda:1 0 MsPacman > objk_pac.log 2>&1 &
nohup python train_model.py cuda:1 0 Asteroids > objk_ast.log 2>&1 &