# MODEL PATHS
# model_paths = {}
# ---------------------------------------------------------------------------------------------------------------
## PONG

# # ### state
# model_paths["pong_state_rep_uns_path"] = "skills/models/pong-state-rep.pt"
# model_paths["pong_state_ae_path"] = "skills/models/pong-state-rep-ae.pt"
#
# # ### denoise-ae
# model_paths["pong_denoise_ae_path"] = "skills/models/pong-denoise-ae.pt"
#
# # ### object-keypoints
# model_paths["pong_obj_key_path"] = "skills/models/pong-obj-key.pt"
# model_paths["pong_obj_key_adapt_enc_path"] = "skills/models/pong-obj-key-enc-ae.pt"
# model_paths["pong_obj_key_adapt_keynet_path"] = "skills/models/pong-obj-key-keynet-ae.pt"
#
# # ### video-segmentation
# model_paths["pong_vid_obj_seg_path"] = "skills/models/pong-vid-obj-seg.pt"
# model_paths["pong_vid_obj_seg_adapt_path"] = "skills/models/pong-vid-obj-seg-ae.pt"
#
# # ---------------------------------------------------------------------------------------------------------------
# ## BREAKOUT
#
# # ### state
# model_paths["breakout_state_rep_uns_path"] = "skills/models/breakout-state-rep.pt"
# model_paths["breakout_state_ae_path"] = "skills/models/breakout-state-rep-ae.pt"
#
# # ### denoise-ae
# model_paths["breakout_denoise_ae_path"] = "skills/models/breakout-denoise-ae.pt"
#
# # ### object-keypoints
# model_paths["breakout_obj_key_path"] = "skills/models/breakout-obj-key.pt"
# model_paths["breakout_obj_key_adapt_enc_path"] = "skills/models/breakout-obj-key-enc-ae.pt"
# model_paths["breakout_obj_key_adapt_keynet_path"] = "skills/models/breakout-obj-key-keynet-ae.pt"
#
# # ### video-segmentation
# model_paths["breakout_vid_obj_seg_path"] = "skills/models/breakout-vid-obj-seg.pt"
# model_paths["breakout_vid_obj_seg_adapt_path"] = "skills/models/breakout-vid-obj-seg-ae.pt"

# ---------------------------------------------------------------------------------------------------------------

import sys

sys.path.append('skills/autoencoders/src')
sys.path.append('skills')

import torch
import torch.nn.functional as F
from torch import Tensor
from collections import namedtuple
from argparse import Namespace
# from atariari.methods.encoders import NatureCNN
from state_representation.encoder import NatureCNN
# from autoencoders import DeepConvAutoencoder
from object_keypoints.model import Encoder, KeyNet, RefineNet, Transporter
from video_object_segmentation.model import VideoObjectSegmentationModel
from autoencoders.model import Autoencoder

# TODO: Eventually can become: Skill(input_model, input_output, skill_model, skill_output, adapter_model, adapter_output)
Skill = namedtuple('Skill', ['name', 'input_adapter', 'skill_model', 'skill_output', 'skill_adapter'])


def model_forward(model, x):
    return model(x)


def state_rep_input_trans(x: Tensor):
    x = x.float()
    return F.interpolate(x, (160, 210), mode='bilinear', align_corners=True)


def get_state_rep_uns(game, device):
    input_transformation_function = state_rep_input_trans
    model_path = "skills/models/" + game.lower() + "-state-rep.pt"
    # n = Namespace()
    # setattr(n, 'feature_size', 512)
    # setattr(n, 'no_downsample', True)
    # setattr(n, 'end_with_relu', False)
    model = NatureCNN(4, 512)
    model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
    model.eval()
    model.to(device)
    adapter = None

    return Skill("state_rep_uns", input_transformation_function, model, model_forward, adapter)



def autoencoder_input_trans(x: Tensor):
    # al momento l'autoencoder prende solo l'ultimo frame, fare un autoencoder su tutti e 4 i frame?

    # x is of shape 32x4x84x84, because there are 4 frame stacked, pick only the last frame and return a tensor of shape 32x1x84x84
    x = x[:, -1:, :, :]
    return x.float()
def get_autoencoder(game, device):
    model_path = "skills/models/" + game.lower() + "-nature-encoder.pt"
    model = Autoencoder().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
    model.eval()
    adapter = None
    input_transformation_function = autoencoder_input_trans
    return Skill("autoencoder", input_transformation_function, model.encoder, model_forward, adapter)


def ae_input_trans(x: Tensor):
    return x.float()


def get_state_ae(game, device):
    input_transformation_function = ae_input_trans
    model_path = "skills/models/" + game.lower() + "-state-rep-ae.pt"
    model = DeepConvAutoencoder(
        inp_side_len=84,
        dims=(4, 16, 32),
        kernel_sizes=3,
        central_dim=512)
    model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
    model.eval()
    model.to(device)
    adapter = None

    return Skill("state_ae", input_transformation_function, model.encoder, model_forward, adapter)


def get_denoise_ae(game, device):
    input_transformation_function = ae_input_trans
    model_path = "skills/models/" + game.lower() + "-denoise-ae.pt"
    model = DeepConvAutoencoder(
        inp_side_len=84,
        dims=(4, 16, 16),
        kernel_sizes=3,
        central_dim=512)
    model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
    model.eval()
    model.to(device)
    adapter = None

    return Skill("denoise_ae", input_transformation_function, model.encoder, model_forward, adapter)


def obj_key_input_trans(x: Tensor):
    x = x.float()
    x = x[:, -1, ...]
    return x.unsqueeze(1)


def get_object_keypoints_encoder(game, device, load_only_model=False):
    input_transformation_function = obj_key_input_trans
    model_path = "skills/models/" + game.lower() + "-obj-key.pt"
    e = Encoder(1)
    k = KeyNet(1, 4)
    r = RefineNet(1)
    model = Transporter(e, k, r)
    model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
    model.eval()
    model.to(device)

    if not load_only_model:
        adapter_path = "skills/models/" + game.lower() + "-obj-key-adapt-enc-ae.pt"
        adapter = DeepConvAutoencoder(
            inp_side_len=21,
            dims=(128, 64, 64),
            kernel_sizes=3,
            central_dim=512)
        adapter.load_state_dict(torch.load(adapter_path, map_location=device), strict=True)
        adapter.eval()
        adapter.to(device)
    else:
        adapter = None

    return Skill("obj_key_enc", input_transformation_function, model.encoder, model_forward,
                 adapter.encoder if adapter else None)


def get_object_keypoints_keynet(game, device, load_only_model=False):
    input_transformation_function = obj_key_input_trans
    model_path = "skills/models/" + game.lower() + "-obj-key.pt"
    e = Encoder(1)
    k = KeyNet(1, 4)
    r = RefineNet(1)
    model = Transporter(e, k, r)
    model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
    model.eval()
    model.to(device)

    if not load_only_model:
        adapter_path = "skills/models/" + game.lower() + "-obj-key-keynet-ae.pt"
        adapter = DeepConvAutoencoder(
            inp_side_len=21,
            dims=(4, 32, 64),
            kernel_sizes=3,
            central_dim=512)
        adapter.load_state_dict(torch.load(adapter_path, map_location=device), strict=True)
        adapter.eval()
        adapter.to(device)
    else:
        adapter = None

    return Skill("obj_key_key", input_transformation_function, model.key_net, model_forward,
                 adapter.encoder if adapter else None)


def vos_output_masks(model: VideoObjectSegmentationModel, x):
    return model.compute_masks(x)


def vid_obj_seg_input_trans(x: Tensor):
    x = x.float()
    first_frames = torch.mean(x[:, :2, ...], 1)
    second_frames = torch.mean(x[:, 2:, ...], 1)
    s = torch.stack([first_frames, second_frames])
    norm_s = s / 255.
    return norm_s.permute(1, 0, 2, 3)


def get_video_object_segmentation(game, device, load_only_model=False):
    model_path = "skills/models/" + game.lower() + "-vid-obj-seg.pt"
    model = VideoObjectSegmentationModel(device)
    model.load_state_dict(torch.load(model_path, map_location=device), strict=True)
    model.eval()
    model.to(device)

    if not load_only_model:
        adapter_path = "skills/models/" + game.lower() + "-vid-obj-seg-ae.pt"
        adapter = DeepConvAutoencoder(
            inp_side_len=84,
            dims=(20, 16, 32),
            kernel_sizes=3,
            central_dim=512)
        adapter.load_state_dict(torch.load(adapter_path, map_location=device), strict=True)
        adapter.eval()
        adapter.to(device)
    else:
        adapter = None

    return Skill("vid_obj_seg", vid_obj_seg_input_trans, model, vos_output_masks, adapter.encoder if adapter else None)


if __name__ == "__main__":
    a = get_state_rep_uns("pong", "cuda:0")
    b = get_state_rep_uns("breakout", "cuda:0")
    print("state_rep_uns:\t OK")

    c = get_state_ae("pong", "cuda:0")
    d = get_state_ae("breakout", "cuda:0")
    print("state_ae:\t OK")

    e = get_denoise_ae("pong", "cuda:0")
    f = get_denoise_ae("breakout", "cuda:0")
    print("denoise_ae:\t OK")

    g = get_object_keypoints_encoder("pong", "cuda:0")
    h = get_object_keypoints_encoder("breakout", "cuda:0")
    print("object_keypoints_encoder:\t OK")

    i = get_object_keypoints_keynet("pong", "cuda:0")
    j = get_object_keypoints_keynet("breakout", "cuda:0")
    print("object_keypoints_keynet:\t OK")

    k = get_video_object_segmentation("pong", "cuda:0")
    l = get_video_object_segmentation("breakout", "cuda:0")
    print("video_object_segmentation:\t OK")
