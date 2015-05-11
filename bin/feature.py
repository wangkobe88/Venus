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
    
    def getPoints(self):
        pass

    def clear(self):
        self.x_values = []

class CategoryFeature(Feature):
    def __init__(self,name,type):
        Feature.__init__(self,name,type)
        self.categories = []
        self.category_statistics = {}

    def getPoints(self):
        return self.category_statistics
    
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

    def getPartationPoint(self,key):
        for i in range(0,len(self.categories)):
            if self.categories[i] == key:
                return i

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
    
    def getPoints(self):
        return self.partation_points

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

class CrossFeature(Feature):
    def __init__(self,name,type,fea1,fea2,features):
        Feature.__init__(self,name,type)
        self.feature1_index = fea1
        self.feature2_index = fea2
    
        self.feature1 = features[fea1]
        self.feature2 = features[fea2]
        
        self.points_statistics = {}
    
    def hash_code(self,fea1_index,fea2_index):
        return fea1_index + 100*fea2_index
    
    def getStatistics(self):
        #print len(self.feature1.x_values)
        #print len(self.feature1.y_values)
        
        for i in range(0,len(self.feature1.getPoints())):
            for j in range(0,len(self.feature2.getPoints())):
                hashcode = self.hash_code(i,j)
                #print hashcode
                if hashcode not in self.points_statistics:
                    self.points_statistics[hashcode] = StatistcsInfo(hashcode)
        #self.points_statistics[hashcode].process(self.y_values[i])
        print "-----------------------"
        for i in range(0,len(self.feature1.x_values)):
            fea1_index = self.feature1.getPartationPoint(self.feature1.x_values[i])
            fea2_index = self.feature2.getPartationPoint(self.feature2.x_values[i])
            hashcode = self.hash_code(fea1_index,fea2_index)
            #print hashcode
            self.points_statistics[hashcode].process(self.feature1.y_values[i])

        for i in range(0,len(self.feature1.getPoints())):
            for j in range(0,len(self.feature2.getPoints())):
                hashcode = self.hash_code(i,j)
                if hashcode in self.points_statistics:
                    self.points_statistics[hashcode].calculator()

    def printInfo(self,report_file):
        report_file.write("------" + self.name + "------" + self.type + "------" + "\n")
        for key in self.points_statistics.keys():
            report_file.write(self.points_statistics[key].printInfo())
                
    def plotall(self,dataset_name):
        for obj in ("rpm","ctr","expo"):
            self.plot(dataset_name,obj)
    
    def plot(self,dataset_name,obj):
        from numpy import *
        import pylab as py
        import mpl_toolkits.mplot3d.axes3d as p3
        x = []

        for i in range(len(self.feature1.getPoints())):
            x.append([])
            for j in range(len(self.feature2.getPoints())):
                x[i].append(i)

        y = []
        for i in range(len(self.feature1.getPoints())):
            y.append([])
            for j in range(len(self.feature2.getPoints())):
                y[i].append(j)

        #print x
        #print y
        z = []
        for i in range(len(self.feature1.getPoints())):
            z.append([])
            for j in range(len(self.feature2.getPoints())):
                z[i].append(self.points_statistics[self.hash_code(i,j)].getinfo(obj))

        fig = py.figure()
        ax = p3.Axes3D(fig)
        ax.plot_wireframe(x,y,z)
        ax.set_xlabel(self.feature1.name)
        ax.set_ylabel(self.feature2.name)
        ax.set_zlabel(obj)
#py.show()
    
        if not os.path.isdir("../pics/"+self.name+"/"):
            os.mkdir("../pics/"+self.name+"/")
        
        py.savefig("../pics/"+self.name+"/"+dataset_name+"_"+obj+".png")
        #show()
        py.clf()

