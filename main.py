import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision.utils import save_image
import tqdm

from Ani_GAN.model import netD, netG
from Ani_GAN.config import opt
from Ani_GAN.Myutils import dataloader

netd = netD(opt)
netg = netG(opt)

ds, dl = dataloader()



if opt.d_save_path:
    netd.load_state_dict(torch.load(opt.d_save_path))
    print("net_D loads weight successfully......")
    print('___' * 10)
if opt.g_save_path:
    netg.load_state_dict(torch.load(opt.g_save_path))
    print("net_G loads weight successfully......")
    print('___' * 10)

optm_g = torch.optim.Adam(netg.parameters(), lr=opt.lr, betas=(opt.beta1, .99))
optm_d = torch.optim.Adam(netd.parameters(), lr=opt.lr, betas=(opt.beta1, .99))
criterion = nn.BCELoss()

true_labels = Variable(torch.ones(opt.batch_size))
fake_labels = Variable(torch.ones(opt.batch_size))
fix_noise = Variable(torch.randn(opt.batch_size, opt.noisy_dim, 1, 1))
noises = Variable(torch.randn(opt.batch_size, opt.noisy_dim, 1, 1))

device = torch.device('cuda') if opt.use_gpu else torch.device('cpu')
netg.to(device)
netg.to(device)
criterion.to(device)
true_labels = true_labels.to(device)
fake_labels = fake_labels.to(device)
fix_noise, noises = fix_noise.to(device), noises.to(device)

epochs = range(opt.max_epoch)

for epoch in epochs:
    for ii, (img, _) in tqdm.tqdm(enumerate(dl)):
        real_img = img.to(device)
        if ii % opt.d_step == 0:
            optm_d.zero_grad()
            real_outputs = netd(real_img)
            error_d_real = criterion(real_outputs, true_labels)
            error_d_real.backward()

            noises.data.copy_(torch.randn(opt.batch_size, opt.noisy_dim, 1, 1))
            fake_img = netg(noises).detach()
            fake_outputs = netd(fake_img)
            error_d_fake = criterion(fake_outputs, fake_labels)
            error_d_fake.backward()

            optm_d.step()

            error_d = error_d_fake + error_d_real

        if ii % opt.g_step == 0:
            optm_g.zero_grad()
            noises.data.copy_(torch.randn(opt.batch_size, opt.noisy_dim, 1, 1))
            fake_img = netg(noises)
            outputs = netd(fake_img)
            error_g = criterion(outputs, true_labels)
            error_g.backward()
    if (epoch + 1) % opt.save_every == 0:
        g_img = netg(fix_noise)
        save_image(g_img, '%s/%s.png' % (opt.save_path, epoch), normalize=True, range=(-1, 1))
        torch.save(netg.state_dict(), 'checkpoints/netg_%s_epoch.pth' % epoch)
        torch.save(netd.state_dict(), 'checkpoints/netd_%s_epoch.pth' % epoch)
