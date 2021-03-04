import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision.utils import save_image
from tqdm import tqdm
import time
from model import netD, netG
from config import opt
from Myutils import dataloader

netd = netD(opt)
netg = netG(opt)

ds, dl = dataloader()

device = torch.device('cuda:0') if opt.use_gpu else torch.device('cpu')
if opt.d_save_path:
    netd.load_state_dict(torch.load(opt.d_save_path))
    print("net_D loads weight successfully......")
    print('___' * 10)
if opt.g_save_path:
    netg.load_state_dict(torch.load(opt.g_save_path))
    print("net_G loads weight successfully......")
    print('___' * 10)
netd.to(device)
netg.to(device)
optm_g = torch.optim.Adam(netg.parameters(), lr=opt.lr, betas=(opt.beta1, 0.999))
optm_d = torch.optim.Adam(netd.parameters(), lr=opt.lr, betas=(opt.beta1, 0.999))
criterion = nn.BCELoss().to(device)

true_labels = Variable(torch.ones(opt.batch_size)).to(device)
fake_labels = Variable(torch.zeros(opt.batch_size)).to(device)
fix_noise = Variable(torch.randn(opt.batch_size, opt.noisy_dim, 1, 1))
noises = Variable(torch.randn(opt.batch_size, opt.noisy_dim, 1, 1))

fix_noise, noises = fix_noise.to(device), noises.to(device)

epochs = range(opt.max_epoch)

for epoch in epochs:
    with tqdm(enumerate(dl)) as t:
        for ii, (img, _) in t:
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
                t.set_description("Epoch %s __ Batch %s" % (epoch, ii))
                t.set_postfix(loss=error_d)
                time.sleep(0.1)

            if ii % opt.g_step == 0:
                optm_g.zero_grad()
                noises.data.copy_(torch.randn(opt.batch_size, opt.noisy_dim, 1, 1))
                fake_img = netg(noises)
                outputs = netd(fake_img)
                error_g = criterion(outputs, true_labels)
                error_g.backward()
                optm_g.step()

                t.set_description("Epoch %s __ Batch %s" % (epoch, ii))
                t.set_postfix(loss=error_g)
                time.sleep(0.1)


        if (epoch + 1) % opt.save_every == 0:
            g_img = netg(fix_noise)
            save_image(g_img, '%s/%s.png' % (opt.save_path, epoch), normalize=True, range=(-1, 1))
            torch.save(netg.state_dict(), 'checkpoints/netg_epoch.pth')
            torch.save(netd.state_dict(), 'checkpoints/netd_epoch.pth')

            print('Epoch: %s, NET_G_Error: %s' % (epoch, error_g.data.item()))
