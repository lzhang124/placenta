import glob
import numpy as np
from image3d import ImageTransformer, VolSegIterator
from keras.utils.data_utils import Sequence
from process import preprocess


class AugmentGenerator(VolSegIterator):
    def __init__(self,
                 vol_files,
                 seg_files,
                 batch_size,
                 rotation_range=90.,
                 shift_range=0.1,
                 shear_range=0.2,
                 zoom_range=0.2,
                 fill_mode='nearest',
                 cval=0.,
                 flip=True,
                 save_to_dir=None):
        vol_path = vol_files.split('*/*')
        seg_path = seg_files.split('*/*')

        self.seg_files = glob.glob(seg_files)
        self.vol_files = [seg_file.replace(seg_path[0], vol_path[0])
                                  .replace(seg_path[1], vol_path[1])
                          for seg_file in self.seg_files]

        vols = np.array([preprocess(file, funcs=['resize']) for file in self.vol_files])
        segs = np.array([preprocess(file, funcs=['resize']) for file in self.seg_files])

        image_transformer = ImageTransformer(rotation_range=rotation_range,
                                             shift_range=shift_range,
                                             shear_range=shear_range,
                                             zoom_range=zoom_range,
                                             fill_mode=fill_mode,
                                             cval=cval,
                                             flip=flip)

        super(AugmentGenerator, self).__init__(vols, segs, image_transformer,
                                               batch_size=batch_size,
                                               save_to_dir=save_to_dir,
                                               x_prefix='vol',
                                               y_prefix='seg')


class VolumeGenerator(Sequence):
    def __init__(self, files, batch_size, rescale=True):
        self.files = glob.glob(files)
        self.batch_size = batch_size
        self.funcs = ['rescale', 'resize'] if rescale else ['resize']
        self.n = len(self.files)
        self.idx = 0

    def __len__(self):
        return (self.n + self.batch_size - 1) // self.batch_size

    def __getitem__(self, idx):
        batch = []
        for file in self.files[self.batch_size * idx:self.batch_size * (idx + 1)]:
            batch.append(preprocess(file, self.funcs))
        return np.array(batch)            

    def __iter__(self):
        self.idx = 0
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.idx < self.n:
            batch = []
            for self.idx in range(self.idx, min(self.idx + self.batch_size, self.n)):
                batch.append(preprocess(self.files[self.idx], self.funcs))
            self.idx += 1
            return np.array(batch)
        else:
            raise StopIteration()
