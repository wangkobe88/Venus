
class LogInfo(object):
    def __init__(self,line):
        line = line.strip().split(' ')
        self.x = line[1:]
        self.y = line[0]

class ConfInfo(object):
    def __init__(self,name,pos,type,feature1,feature2):
        self.name = name
        self.pos = pos
        self.type = type
        self.feature1 = feature1
        self.feature2 = feature2