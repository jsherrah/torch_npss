import os
import os.path
import math
import threading
import torch
import torch.utils.data
import numpy as np
import librosa as lr
import bisect


class NpssDataset(torch.utils.data.Dataset):
    def __init__(self,
                 dataset_file,
                 condition_file,
                 receptive_field,
                 target_length,
                 train=True):

        #           |----receptive_field----|
        # example:  | | | | | | | | | | | | | | | | | | | | |
        # target:                             | | | | | | | | |
        self.dataset_file = dataset_file
        self._receptive_field = receptive_field
        self.target_length = target_length
        self.item_length = self._receptive_field+self.target_length

        self.data = np.load(self.dataset_file)


        self.conditon = np.load(condition_file).astype(np.float)


        self._length = 0
        self.calculate_length()
        self.train = train



    def calculate_length(self):

        available_length = self.data.shape[0] - self._receptive_field
        self._length = math.floor(available_length / self.target_length)


    def __getitem__(self, idx):

        sample_index = idx * self.target_length

        sample = self.data[sample_index:sample_index+self.item_length, :]

        item_condition = np.transpose(self.conditon[sample_index+self.item_length-1:sample_index+self.item_length, :])

        example = torch.from_numpy(sample)

        item = example[:self._receptive_field].transpose(0, 1)
        target = example[-self.target_length:].transpose(0, 1)
        return (item, item_condition), target

    def __len__(self):

        return self._length


