
class LogInfo(object):
    def __init__(self,line):
        line = line.strip().split(' ')
        self.x = line[1:]
        self.y = line[0]

class ConfInfo(object):
    def __init__(self,name,pos,type):
        self.name = name
        self.pos = pos
        self.type = type