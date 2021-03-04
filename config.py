class Config(object):
    data_path = 'data/'
    num_works = 0
    img_size = 150

    # train cofig
    batch_size = 64
    max_epoch = 100
    lr = 2e-4
    beta1 = 0.5
    use_gpu = False
    save_every = 5

    # G and D config
    noisy_dim = 100
    ngf = 64
    ndf = 64

    save_path = 'imgs/'

    # G and D Updating Frequency
    d_step = 1
    g_step = 5

    d_save_path = None
    g_save_path = None


opt = Config()
