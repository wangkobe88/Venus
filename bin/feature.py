import random
import os
import gc
import sys
import copy
from statistcs_info import *

class Feature(object):
    def __init__(self,name,type):
        self.name = name
        self.type = type
        self.y_values = []
        self.x_values = []

    def addData(self,x,y):
        self.x_values.append(x)
        self.y_values.append(y)

    def getStatistics(self):
        print "datasize:",len(self.x_values)

    def plot(self):
        pass

    def clear(self):
        self.x_values = []

class CategoryFeature(Feature):
    def __init__(self,name,type):
        Feature.__init__(self,name,type)
        self.categories = []
        self.category_statistics = {}
    
    def getStatistics(self):
        for i in range(len(self.x_values)):
            category = self.x_values[i]
            if category not in self.category_statistics.keys():
                self.categories.append(category)
                self.category_statistics[category] = StatistcsInfo(category)
            self.category_statistics[category].process(self.y_values[i])
        
        for key in self.category_statistics.keys():
            self.category_statistics[key].calculator()

    def printInfo(self,report_file):
        report_file.write("------" + self.name + "------" + self.type + "------" + "\n")
        for key in self.category_statistics.keys():
            report_file.write(self.category_statistics[key].printInfo())

    def plotall(self,dataset_name):
        for obj in ("rpm","ctr","expo"):
            self.plot(dataset_name,obj)

    def plot(self,dataset_name,obj):
        from pylab import *
        x = []
        xlabels = []
        for i in range(0,len(self.categories)):
            x.append(i+0.2)
        y = []
        for category in self.category_statistics.keys():
            y.append(self.category_statistics[category].getinfo(obj))
        #print x
        #print y
        bar(x, y, 0.4, alpha=0.4, color='r')
        xticks(x, self.categories)
        title("Feature: "+self.name)
        xlabel('Category Index')
        ylabel('RPM Mean')
        if not os.path.isdir("../pics/"+self.name+"/"):
            os.mkdir("../pics/"+self.name+"/")
        
        savefig("../pics/"+self.name+"/"+dataset_name+"_"+obj+".png")
        #show()
        clf()

class PartationFeature(Feature):
    def __init__(self,name,type):
        Feature.__init__(self,name,type)
        self.partation_points = []
        self.partation_statistics = {}

    def getPartationPoint(self,key):
        low = 0
        high = len(self.partation_points)-1
        mid = (low+high)/2
        while low <= high:
            mid = (low+high)/2
            if key == self.partation_points[mid]:
                return mid
            if key > self.partation_points[mid]:
                low = mid+1
            else:
                high = mid-1
        return high

    def calPartationPoints(self):
        x_values_copy = copy.deepcopy(self.x_values)
        x_values_copy.sort()
        N = 10
        length = len(x_values_copy)
        """
        for i in range(0,N):
            self.partation_points.append(x_values_copy[length*i/N])
            self.partation_statistics[i] = StatistcsInfo(x_values_copy[length*i/N])
        """
        pre_point = -2
        cur_index = 0
        for i in range(0,N):
            if not pre_point == x_values_copy[length*i/N]:
                pre_point = x_values_copy[length*i/N]
                self.partation_points.append(x_values_copy[length*i/N])
                self.partation_statistics[cur_index] = StatistcsInfo(x_values_copy[length*i/N])
                cur_index = cur_index + 1
            else:
                continue
        #print self.partation_points
        #print self.partation_statistics

    def getStatistics(self):
        #Feature.getStatistics()
        
        self.calPartationPoints()
        
        for i in range(len(self.x_values)):
            partation_point = self.getPartationPoint(self.x_values[i])
            self.partation_statistics[partation_point].process(self.y_values[i])

        for key in self.partation_statistics.keys():
            self.partation_statistics[key].calculator()
            #print self.partation_statistics[key].printInfo()

    def printInfo(self,report_file):
        report_file.write("------" + self.name + "------" + self.type + "------"+"\n")
        for key in self.partation_statistics.keys():
            report_file.write(self.partation_statistics[key].printInfo())

    def plotall(self,dataset_name):
        for obj in ("rpm","ctr","expo"):
            self.plot(dataset_name,obj)

    def plot(self,dataset_name,obj):
        from pylab import *
        x = range(0,len(self.partation_points),1)
        #print x
        y = []
        for key in x:
            y.append(self.partation_statistics[key].getinfo(obj))
        #print y
        plot(x, y)
        xticks(x, self.partation_points)
        title("Feature: "+self.name)
        xlabel('Partation Index')
        ylabel('RPM Mean')
        grid(True)
        if not os.path.isdir("../pics/"+self.name+"/"):
            os.mkdir("../pics/"+self.name+"/")
        savefig("../pics/"+self.name+"/"+dataset_name+"_"+obj+".png")
        #savefig("../pics/"+self.name+"/"+dataset_name+".png")
        #show()
        clf()
