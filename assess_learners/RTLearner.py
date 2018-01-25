"""
Decision Tree learner
"""

import numpy as np


class RTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size

    def author(self):
        return 'ywan43'

    def build_tree(self, train_x, train_y):
        if train_y.shape[0] <= self.leaf_size:
            return np.array([[0, train_y.mean(), 0, 0, 0]])
        else:
            i = np.random.randint(train_x.shape[1], size=1)[0]
            split_val = np.median(train_x[:, i])
            left_data = train_x[train_x[:, i] <= split_val, :]
            right_data = train_x[train_x[:, i] > split_val, :]
            left_y = train_y[train_x[:, i] <= split_val]
            right_y = train_y[train_x[:, i] > split_val]
            if left_data.shape[0] == train_x.shape[0] or right_data.shape[0] == train_x.shape[0]:
                return np.array([[0, train_y.mean(), 0, 0, 0]])
            else:
                left_tree = self.build_tree(left_data, left_y)
                right_tree = self.build_tree(right_data, right_y)
                root = np.array([[1, i, split_val, 1, left_tree.shape[0] + 1]])
                return np.concatenate((root, left_tree, right_tree), axis=0)

    def go_tree(self, i, observ):
        i = int(i)
        if self.tree[i, 0] == 0:
            return self.tree[i, 1]
        else:
            split_val = self.tree[i, 2]
            col = self.tree[i, 1]
            if observ[int(col)] > split_val:
                return self.go_tree(i + self.tree[i, 4], observ)
            else:
                return self.go_tree(i + self.tree[i, 3], observ)

    def addEvidence(self, train_x, train_y):
        self.tree = self.build_tree(train_x, train_y)

    def query(self, data_x):
        prediction = np.zeros([data_x.shape[0]])
        for i in range(0, data_x.shape[0]): prediction[i] = self.go_tree(0, data_x[i])
        return prediction

