import os
import re

import requests
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.datasets import ImageFolder

from config import opt


def dataloader():
    transf = transforms.Compose([
        transforms.Resize(opt.img_size),
        transforms.CenterCrop(opt.img_size),
        transforms.ToTensor(),
        transforms.Normalize((.5, .5, .5), (.5, .5, .5))
    ])

    dataset = ImageFolder('data/', transform=transf)
    dl = DataLoader(dataset=dataset, batch_size=opt.batch_size, num_workers=opt.num_works, drop_last=True,
                    shuffle=True)
    return dataset, dl
