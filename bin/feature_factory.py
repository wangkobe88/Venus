
import random
import os
import gc
import sys
import copy
from feature import *

class FeatureFactory(object):
    def createFeature(self,type_name,name,fea1,fea2,features):
        if type_name == "category":
            return CategoryFeature(name,type_name)
        elif type_name == "partation":
            return PartationFeature(name,type_name)
        elif type_name == "cross":
            return CrossFeature(name,type_name,fea1,fea2,features)