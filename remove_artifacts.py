from process import remove_artifacts
import constants
import glob
import os
import numpy as np
import util

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('model', type=str)
options = parser.parse_args()


def dice_coef(true, pred):
    true_f = true.flatten()
    pred_f = pred.flatten()
    intersection = np.sum(true_f * pred_f)
    return (2. * intersection) / (np.sum(true_f) + np.sum(pred_f))

def main(model):
    old_metrics = {}
    new_metrics = {}

    for file in glob.glob('data/predict/{}/*_0000.nii.gz'.format(model)):
        sample = os.path.basename(file).split('_')[0]
        header = util.header(file)
        volume = util.read_vol(file)
        label = util.read_vol(glob.glob('data/labels/{}/{}_0_all_brains.nii.gz'.format(sample, sample))[0])

        old_metrics[sample] = dice_coef(label, volume)

        n = 2 if sample in constants.TWINS else 1
        volume = remove_artifacts(volume, n)

        new_metrics[sample] = dice_coef(label, volume)

        os.makedirs('data/predict_cleaned/{}/'.format(model), exist_ok=True)
        util.save_vol(volume, 'data/predict_cleaned/{}/{}_0000.nii.gz'.format(model, sample), header)

    print('before: ', old_metrics)
    print('after: ', new_metrics)


if __name__ == '__main__':
    main(options.model)
