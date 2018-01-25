"""
Decision Tree learner
"""

import numpy as np
#import DTLearner as dtl
#import RTLearner as rt
#import LinRegLearner as lr

#############
#Implemented by
#Name: Yun Wan
#GTID: ywan43
#############

class DTLearner(object):
    def __init__(self, leaf_size=1, verbose=False):
        self.leaf_size = leaf_size

    def author(self):
        return 'ywan43'

    def build_tree(self, train_x, train_y):
        if train_y.shape[0] <= self.leaf_size:
            return np.array([[0, train_y.mean(), 0, 0, 0]])
        else:
            i = np.abs(np.corrcoef(train_x, train_y, rowvar=False)[:-1, -1]).argmax()
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


class BagLearner(object):
      def __init__(self, learner=DTLearner,kwargs={}, bags=20, boost=False ,verbose=False):
          # self.model_list=bags*[learner(**kwargs)]
           self.model_list=[]
           for  i in range(0, bags):
                self.model_list =self.model_list + [learner(**kwargs)]




      def author(self):
          return 'ywan43'




      def addEvidence(self, train_x, train_y):

          for i in range(0, len(self.model_list)):
              sub = np.random.choice(train_x.shape[0], train_x.shape[0])
              sub_x = train_x[sub,]
              sub_y = train_y[sub,]
              self.model_list[i].addEvidence(sub_x,sub_y)

      def query(self, data_x):

          pred_list=[]

          for i in range(0, len(self.model_list)):
              pred_list=pred_list + [self.model_list[i].query(data_x)]

              pred_array=np.asarray(pred_list).T
          return np.mean(pred_array,axis=1)
