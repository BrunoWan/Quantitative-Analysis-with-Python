"""
Decision Tree learner
"""

import numpy as np
import DTLearner as dt
import RTLearner as rt
import LinRegLearner as lr


class BagLearner(object):
      def __init__(self, learner=dt.DTLearner,kwargs={}, bags=20, boost=False ,verbose=False):
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

