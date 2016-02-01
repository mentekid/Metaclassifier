import numpy as np
class MajorityVoter():
    def __init__(self):
        return
    
    def fit(self, data = None, labels = None):
        return
        
    def predict(self, data):
        """Row-wise sum and majority voting of 2 classes"""
        from scipy import stats
        win, votes = stats.mode(data, axis=1)
        return win
        #return np.array([int(float(sum(line))/len(line)>0) for line in data])
    