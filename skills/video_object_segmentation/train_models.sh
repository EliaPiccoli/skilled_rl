# ["Pong", "Breakout", "BeamRider", "Qbert", "Seaquest", "SpaceInvaders", "RoadRunner", "Enduro", "MsPacman", "Asteroids"]

nohup python train_model.py cuda:2 0 BeamRider > vos_br.log 2>&1 &
nohup python train_model.py cuda:2 0 Qbert > vos_qb.log 2>&1 &
nohup python train_model.py cuda:2 0 Seaquest > vos_sea.log 2>&1 &
nohup python train_model.py cuda:2 0 SpaceInvaders > vos_si.log 2>&1 &
nohup python train_model.py cuda:3 0 RoadRunner > vos_rr.log 2>&1 &
nohup python train_model.py cuda:3 0 Enduro > vos_end.log 2>&1 &
nohup python train_model.py cuda:3 0 MsPacman > vos_pac.log 2>&1 &
nohup python train_model.py cuda:3 0 Asteroids > vos_ast.log 2>&1 &