import cv2
import sys
import os.path
import logging
from tqdm import tqdm
import os
import argparse
import copy


def detect(opt):
    indir, cascade_file, outdir = opt.indir, opt.weights, opt.outdir
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)
    if not os.path.exists(outdir.strip()):
        logging.error('outdir direction does not exist')
        choice = input('create a new direction by outdir (N/Y)')
        if choice == 'Y':
            os.makedirs(outdir)
        else:
            raise Exception('direction %s not found' % outdir.strip())
    cascade = cv2.CascadeClassifier(cascade_file)
    logging.info('weight loading finish...')

    file_list = os.listdir(indir)
    bar = tqdm(file_list)
    for file in bar:
        filename = os.path.join(indir, file)
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = cascade.detectMultiScale(gray,
                                         # detector options
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(24, 24))
        if not isinstance(faces, tuple):
            for (x, y, w, h) in faces:
                try:
                    if opt.save:
                        if not image[y:y + h, x:x + w].size == 0:
                            cv2.imwrite(os.path.join(outdir, file), image[y:y + h, x:x + w])
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    if opt.view:
                        cv2.imshow("image", image)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                    image = image[y:y + h, x:x + w]

                    bar.set_description("Processing %s" % filename)
                except Exception as e:
                    logging.error(e)


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Do face detection')
    parse.add_argument('--indir', default='images', help='choose the in-dir of images')
    parse.add_argument('--outdir', default='data/output', help='the dir result will save')
    parse.add_argument('-weights', default='lbpcascade_animeface.xml')
    parse.add_argument('--view', action='store_true', help='show the crop box')
    parse.add_argument('--save', action='store_false', help='save or not')
    opt = parse.parse_args()
    detect(opt)
# detect('/Users/macintosh/Documents/Prgramming/Python/PyTorchLearning/Ani_GAN/data/images', 'output')
