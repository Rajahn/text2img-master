import torch
import torch.nn.functional as F
from torch import nn


def freeze_params_(module):
    for param in module.parameters():
        param.requires_grad = False
    return module


def grad_norm(module, p=2):
    total_norm = 0
    for p in module.parameters():
        param_norm = p.grad.data.norm(2)
        total_norm += param_norm.item() ** 2
    return total_norm ** 0.5


def init_weights(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.orthogonal_(m.weight.data, 1.0)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)
    elif classname.find('Linear') != -1:
        nn.init.orthogonal_(m.weight.data, 1.0)
        if m.bias is not None:
            m.bias.data.fill_(0.0)


def rotate_tensor(t, n, dim=0):
    return torch.cat((t[-n:], t[:-n]), dim=dim)


def count_params(module):
    trainable = 0
    non_trainable = 0
    for p in module.parameters():
        if p.requires_grad:
            trainable += p.numel()
        else:
            non_trainable += p.numel()
    return trainable, non_trainable


class Interpolate(nn.Module):
    def __init__(self, scale_factor, mode):
        super().__init__()
        self.factor = scale_factor
        self.mode = mode

    def forward(self, x):
        return F.interpolate(x, scale_factor=self.factor, mode=self.mode)


def conv1x1(in_channels, out_channels):
    return nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, padding=0, bias=False)


def conv3x3(in_channels, out_channels):
    return nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False)


def upsample_block(in_channels, out_channels):
    return nn.Sequential(
        Interpolate(scale_factor=2, mode='nearest'),
        conv3x3(in_channels, out_channels * 2),
        nn.BatchNorm2d(out_channels * 2),
        nn.modules.activation.GLU(dim=1)
    )


class Residual(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.block = nn.Sequential(
            conv3x3(channels, channels * 2),
            nn.BatchNorm2d(channels * 2),
            nn.modules.activation.GLU(dim=1),
            conv3x3(channels, channels),
            nn.BatchNorm2d(channels)
        )

    def forward(self, x):
        out = self.block(x)
        out += x
        return out


def pre_json_metrics(d):
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = pre_json_metrics(v)
        elif hasattr(v, 'tolist'):
            d[k] = v.tolist()
        elif isinstance(v, list) and hasattr(v[0], 'tolist'):
            d[k] = [x.tolist() for x in v]

    return d
