import random
import os
import gc
import sys
import random

from sklearn import linear_model
from matplotlib import pylab
from sklearn.metrics import precision_recall_curve, roc_curve, auc
from sklearn.metrics import classification_report

from utilitis import *
from feature_factory import *
from feature import *

class Trainer(object):
    def __init__(self,log_filename,conf_filename,dis_filename):
        self.log_filename = log_filename
        self.conf_filename = conf_filename
        self.dis_filename = dis_filename
        
        self.feature_count = 0
        self.dataX = []
        self.dataY = []
        self.dataI = []
        self.confInfo = []
        self.features = {}
    
        self.features_indexs = {}

    def plot_pr(self, auc_score, precision, recall, label=None):
        pylab.figure(num = None, figsize=(6, 5))
        pylab.xlim([0.0, 1.0])
        pylab.ylim([0.0, 1.0])
        pylab.xlabel('Recall')
        pylab.ylabel('Precision')
        pylab.title('P/R (AUC=%0.2f) / %s' % (auc_score, label))
        pylab.fill_between(recall, precision, alpha=0.5)
        pylab.grid(True, linestyle='-', color='0.75')
        pylab.plot(recall, precision, lw=1)
        pylab.show()

    def plot_auc(self, auc_score, tpr, fpr, label=None):
        pylab.figure(num = None, figsize=(6, 5))
        pylab.xlim([0.0, 1.0])
        pylab.ylim([0.0, 1.0])
        pylab.xlabel('False Positive Rate')
        pylab.ylabel('True Positive Rate')
        pylab.title('ROC (AUC=%0.2f) / %s' % (auc_score, label))
        pylab.fill_between(fpr, tpr, alpha=0.5)
        pylab.grid(True, linestyle='-', color='0.75')
        pylab.plot(fpr, tpr, lw=1)
        pylab.show()

    def processLog(self,line,count):
        x_value = []
        y_value = 0
        i_value = 0
        line = line.strip().split(' ')

        if int(line[0]) > 0:
            y_value = 1

        if not (count%13 == 0 or y_value == 1):
                return
    
        for i in range(1,len(line)):
            feature_count = 0
            if isinstance(self.features[i],PartationFeature):
                feature_count = len(self.features[i].partation_points)
            else:
                feature_count = len(self.features[i].categories)
            
            for j in range(0,feature_count):
                if j == int(line[i]):
                    x_value.append(1)
                else:
                    x_value.append(0)
            i_value = random.randint(0,6)

        self.dataX.append(x_value)
        self.dataY.append(y_value)
        self.dataI.append(i_value)

    def get_feature_count(self):
        for i in self.features.keys():
            
            if isinstance(self.features[i],PartationFeature):
                feature_count = len(self.features[i].partation_points)
            else:
                feature_count = len(self.features[i].categories)

            for j in range(0,feature_count):
                self.features_indexs[self.feature_count + j] = i

            self.feature_count += feature_count

    
    def loadData(self):
        log_file = open(self.log_filename,'r')
        line = log_file.readline()
        count = 0
        while line:
            if count%100000 == 0 and count > 1:
                print "data loaded",count
                print self.dataX[-1]
                print self.dataY[-1]
                print self.dataI[-1]
            count += 1
            """
            if not count%33 == 0:
                line = log_file.readline()
                continue
            """
            self.processLog(line,count)
                
            line = log_file.readline()
        log_file.close()

    def loadConf(self):
        conf_file = open(self.conf_filename,'r')
        line = conf_file.readline()
        while line:
            line = line.strip().split(' ')
            if len(line) < 3:
                break
            name = line[0]
            pos = int(line[1])
            type = line[2]
            
            self.confInfo.append(ConfInfo(name,pos,type))
            line = conf_file.readline()
        conf_file.close()

    def buildFeatures(self):
        feature_factory = FeatureFactory()
        for info in self.confInfo:
            self.features[info.pos] = feature_factory.createFeature(info.type,info.name)
    #print self.features

    def init_point(self):
        dis_file = open(self.dis_filename,'r')
        line = dis_file.readline()
        while line:
            line = line.strip().split(' ')
            if len(line) < 2:
                break
            key = int(line[0])
            self.features[key].partation_points = []
            for i in range(1,len(line)):
                self.features[key].partation_points.append(int(line[i]))
            line = dis_file.readline()
        dis_file.close()

    def training(self,test_index = 6):
        training_set_x = []
        training_set_y = []
        test_set_x = []
        test_set_y = []
        
        for i in range(0,len(self.dataI)):
            if self.dataI[i] == test_index:
                test_set_x.append(self.dataX[i])
                test_set_y.append(self.dataY[i])
            else:
                training_set_x.append(self.dataX[i])
                training_set_y.append(self.dataY[i])
                    
        clf = linear_model.LogisticRegression(C=1.0, penalty='l1', tol=1e-10)
        clf.fit(training_set_x, training_set_y)
        #print clf.coef_
        #print clf.predict(test_set_x[i]),test_set_y[i]

        answer = clf.predict_proba(test_set_x)[:,1]
        report = answer > 0.03
        
        for i in range(0,len(test_set_y)):
            if i%10000 == 0:
                print test_set_y[i], answer[i]
        precision, recall, thresholds = precision_recall_curve(test_set_y, answer)
        fpr, tpr, thresholds_auc = roc_curve(test_set_y, answer)
        roc_auc = auc(fpr, tpr)
        print(classification_report(test_set_y, report, target_names = ['neg', 'pos']))

        #self.plot_pr(0.5, precision, recall, "pos")
        print test_index,"'th cv,auc:",roc_auc
#self.plot_auc(roc_auc,tpr,fpr, "pos")
        return roc_auc

    def training_with_cv(self):
        total_score = 0.0
        for i in range(0,6):
            total_score += self.training(i)
        print "mean_score:" + str(float(total_score/6))
    
    ##------------------

    def filter_data(self,data,feature_subset,search_index):
        newdata = []
        for i in feature_subset:
            newdata.append(data[i])
        newdata.append(data[search_index])
        return newdata
    
    def training_subset(self,test_index,feature_subset,search_index):
        training_set_x = []
        training_set_y = []
        test_set_x = []
        test_set_y = []
        
        for i in range(0,len(self.dataI)):
            if self.dataI[i] == test_index:
                test_set_x.append(self.filter_data(self.dataX[i],feature_subset,search_index))
                test_set_y.append(self.dataY[i])
            else:
                training_set_x.append(self.filter_data(self.dataX[i],feature_subset,search_index))
                training_set_y.append(self.dataY[i])
    
        clf = linear_model.LogisticRegression(C=1.0, penalty='l1', tol=1e-10)
        clf.fit(training_set_x, training_set_y)
        
        answer = clf.predict_proba(test_set_x)[:,1]
        report = answer > 0.03
        
        for i in range(0,len(test_set_y)):
            if i%1000000 == 0:
                pass
        #print test_set_y[i], answer[i]
        precision, recall, thresholds = precision_recall_curve(test_set_y, answer)
        fpr, tpr, thresholds_auc = roc_curve(test_set_y, answer)
        roc_auc = auc(fpr, tpr)
#print(classification_report(test_set_y, report, target_names = ['neg', 'pos']))

#print test_index,"'th cv,auc:",roc_auc

        return roc_auc
        #self.plot_auc(roc_auc,tpr,fpr, "pos")
            
    def training_subset_with_cv(self,feature_subset,search_index):
        total_score = 0.0
        for i in range(0,6):
            total_score += self.training_subset(i,feature_subset,search_index)
        return total_score/6

    def forward_search(self):
        feature_indexs = {}
        iteration_scores = []
        for i in range(0,self.feature_count):
            max_score = 0.0
            current_feature = -1
            for j in range(0,self.feature_count):
                if feature_indexs.has_key(j):
                    continue
                current_score = self.training_subset_with_cv(feature_indexs,j)
                if current_score > max_score:
                    max_score = current_score
                    current_feature = j

            feature_indexs[current_feature] = 1
            iteration_scores.append(max_score)

            print "iter:",str(i)
            print feature_indexs.keys()
            print iteration_scores
            for key in feature_indexs.keys():
                print key,self.features_indexs[key]
            
            if i > 1 and (iteration_scores[-1] - iteration_scores[-2]) < 0.0003:
                break

"""
    def backward_search(self):
        feature_indexs = {}
        deleted_indexs = []
        for i in range(0,self.feature_count):
            feature_indexs[i] = 1
        iteration_scores = []
        
        for i in range(0,self.feature_count):
            max_score = 0.0
            current_feature = -1
            for j in range(0,self.feature_count):
                if not feature_indexs.has_key(j):
                    continue
                current_score = self.training_subset_with_cv2(feature_indexs,j)
                if current_score > max_score:
                    max_score = current_score
                    current_feature = j
        
            feature_indexs.pop(current_feature)
            deleted_indexs.append(current_feature)
            iteration_scores.append(max_score)
            
            print "iter:",str(i)
            print feature_indexs.keys()
            print iteration_scores
"""


if __name__ ==  "__main__":
    log_filename = sys.argv[1]
    conf_filename = sys.argv[2]
    dis_filename = sys.argv[3]
    
    print log_filename,conf_filename,dis_filename

    trainer = Trainer(log_filename,conf_filename,dis_filename)
    trainer.loadConf()
    trainer.buildFeatures()
    trainer.init_point()
    trainer.loadData()
    trainer.get_feature_count()
    trainer.forward_search()

#trainer.training_with_cv()

    #dataset.generate_pics()
    #dataset.generate_report(report_file)
