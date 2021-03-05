class Config(object):
    data_path = 'data/'
    num_works = 0
    img_size = 150

    # train cofig
    batch_size = 64
    max_epoch = 200
    lr = 3e-4
    beta1 = 0.5
    use_gpu = True
    save_every = 5

    # G and D config
    noisy_dim = 100
    ngf = 64
    ndf = 64

    save_path = 'imgs/'

    # G and D Updating Frequency
    d_step = 1
    g_step = 2
    #
    d_save_path = None
    g_save_path = None
    # d_save_path = 'checkpoints/netd_epoch_2.pth'
    # g_save_path = 'checkpoints/netg_epoch_2.pth'


opt = Config()
