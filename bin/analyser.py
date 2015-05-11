import random
import os
import gc
import sys

from utilitis import *
from feature_factory import *
from feature import *

class DataSet(object):
    def __init__(self,logs_path,log_name,conf_filename):
        self.logs_path = logs_path
        self.log_name = log_name
        self.conf_filename = conf_filename
        self.logsInfo = []
        self.confInfo = []
        self.features = {}

    def loadData(self):
        logs_file = open(logs_path + logname,'r')
        line = logs_file.readline()
        count = 0
        while line:
            if count%100000 == 0:
                print "data loaded",count
            #sampling 1/5 data
            count += 1
            
            self.logsInfo.append(LogInfo(line))
            line = logs_file.readline()
        logs_file.close()

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

            feature1 = 0
            feature2 = 0

            if len(line) > 3:
                feature1 = int(line[3])
                feature2 = int(line[4])
            
            self.confInfo.append(ConfInfo(name,pos,type,feature1,feature2))
            line = conf_file.readline()
        conf_file.close()

    def buildFeatures(self):
        feature_factory = FeatureFactory()
        for info in self.confInfo:
            self.features[info.pos] = feature_factory.createFeature(info.type,info.name,info.feature1,info.feature2,self.features)
        #print self.features

    def analysis(self):
        for loginfo in self.logsInfo:
            for i in range(0,len(loginfo.x)):
                if (i+1) in self.features.keys():
                    if not loginfo.x[i] == 'NULL':
                        self.features[i+1].addData(int(float(loginfo.x[i])),loginfo.y)
                    else:
                        self.features[i+1].addData(-1,loginfo.y)
    
        for key in self.features.keys():
            self.features[key].getStatistics()

    def clear(self):
        for key in self.features.keys():
            self.features[key].clear()
    
    def write_points(self,dis_file):
        for key in self.features.keys():
            if isinstance(self.features[key],PartationFeature):
                point = " "
                for value in self.features[key].partation_points:
                    point =  point + str(value) + " "
                
                dis_file.write(str(key) + point + "\n")

    def generate_pics(self):
        for key in self.features.keys():
            self.features[key].plotall(self.log_name)
    
    def generate_report(self,report_file):
        for key in self.features.keys():
            self.features[key].printInfo(report_file)

if __name__ ==  "__main__":
    logs_path = sys.argv[1]
    conf_filename = sys.argv[2]
    report_filename = sys.argv[3]
    
    report_file = open(report_filename,'w')
    
    print logs_path,conf_filename,report_filename

    logs_filenames = os.listdir(logs_path)
    print logs_filenames
    for logname in logs_filenames:
        if not "dat" in logname:
            continue

        dataset = DataSet(logs_path,logname,conf_filename)
        dataset.loadConf()
        dataset.loadData()
        dataset.buildFeatures()
        dataset.analysis()
        dataset.clear()
#dataset.write_points(dis_file)
        dataset.generate_pics()
        dataset.generate_report(report_file)
