
import random
import os
import gc
import sys
import copy

class StatistcsInfo(object):
    def __init__(self,key):
        self.key = key
        self.mark = 0
        self.click = 0
        self.expo = 0
        self.rpm = 0
        self.ctr = 0
        
    def addmark(self):
        self.mark += 1
        
    def addclick(self):
        self.click += 1
        
    def addexpo(self):
        self.expo += 1
        
    def process(self,action):
        self.addexpo()
        if action == '1':
            self.addmark()
            self.addclick()
        elif action == '2':
            self.addmark()
        elif action == '3':
            self.addclick()
        
    def calculator(self):
        self.rpm = (self.mark*10000)/(self.expo+1)
        self.ctr = (self.click*10000)/(self.expo+1)

    def getinfo(self,key):
        if key == "rpm":
            return self.rpm
        elif key == "ctr":
            return self.ctr
        elif key == "expo":
            return self.expo
        else:
            return self.rpm

    def printInfo(self):
        return  str(self.key) + "," + str(self.mark)+ "," + str(self.click)+ "," + str(self.expo) + "," + str(self.ctr) + "," + str(self.rpm) + "\n"