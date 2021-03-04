import torch.nn as nn


class netG(nn.Module):
    def __init__(self, opt):
        super(netG, self).__init__()
        feature_map = opt.ngf
        self.layer = nn.Sequential(
            # (100,1,1) to (800, 4,4)
            nn.ConvTranspose2d(opt.noisy_dim, opt.ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(opt.ngf * 8),
            nn.ReLU(inplace=True),

            # (400, 12, 12)
            nn.ConvTranspose2d(opt.ngf * 8, opt.ngf * 4, 6, 2, 0, bias=False),
            nn.BatchNorm2d(opt.ngf * 4),
            nn.ReLU(inplace=True),

            # (200, 25, 25)
            nn.ConvTranspose2d(opt.ngf * 4, opt.ngf * 2, 5, 2, 1),
            nn.BatchNorm2d(opt.ngf * 2),
            nn.ReLU(inplace=True),

            # (100, 50, 50)
            nn.ConvTranspose2d(opt.ngf * 2, opt.ngf, 4, 2, 1),
            nn.BatchNorm2d(opt.ngf),
            nn.ReLU(inplace=True),

            # (100, 150, 150)
            nn.ConvTranspose2d(opt.ngf, 3, 5, 3, 1),
            nn.Tanh()
        )

    def forward(self, x):
        return self.layer(x)


class netD(nn.Module):
    def __init__(self, opt):
        super(netD, self).__init__()
        self.layer = nn.Sequential(
            # input = (3, 150, 150)
            nn.Conv2d(3, opt.ndf, 5, 3, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(opt.ndf, opt.ndf * 2, 4, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(opt.ndf * 2, opt.ndf * 4, 5, 2, 1, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(opt.ndf * 4, opt.ndf * 8, 6, 2, 0, bias=False),
            nn.LeakyReLU(0.2, inplace=True),

            nn.Conv2d(opt.ndf * 8, 1, 4, 1, 0, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.layer(x).view(-1)
