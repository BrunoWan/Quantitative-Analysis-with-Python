import numpy as np
import BagLearner as bl
import LinRegLearner as lr
class InsaneLearner(object):
    def __init__(self, learner=bl.BagLearner,bags=20, boost=False, verbose=False):
        self.bglearner_list=[]
        for i in range(0, bags):
            self.bglearner_list=self.bglearner_list+[learner(learner=lr.LinRegLearner,bags=20)]
    def author(self):
        return 'ywan43'
    def addEvidence(self, train_x, train_y):
        for bag_model in self.bglearner_list:
            sub=np.random.choice(train_x.shape[0],train_x.shape[0])
            bag_model.addEvidence(train_x[sub,], train_y[sub,])
    def query(self,data_x):
        pred_list=[]
        for bag_model in self.bglearner_list:
            pred_list=pred_list+[bag_model.query(data_x)]
            pred_array=np.asarray(pred_list).T
        return np.mean(pred_array, axis=1)