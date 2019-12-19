import maya.cmds as cmds
import os
import json

libraryPath = r"C:\Users\PAV-15\Desktop\REVIEW\library"

class Library():
    
	
    def __initi__(self):
    		
        self.library = None
        self.folders = None
        self.length = None
        self.totalAssets = None
        
		
    def setPath(self, libraryPath):
    
        if os.path.isdir(libraryPath):
        	self.library = libraryPath
        	self.folders  = os.listdir(libraryPath)
        	self.length = len(self.folders )
        	print self.length, "aasv",  self.folders 
        else:
        	cmds.warning("path DOES NOT Exist!")


    def category(self):
        print self.folders 
    
	
    def index(self):
        
        if self.length > 0:
            f = open(libraryPath+"\\assetDictionary.json", "w+")
            self.index = {}
            for folder in self.folders:
                self.index[folder] =  os.listdir(self.library+"\\"+folder)
            json.dump(self.index, f)
            f.close()
				
	def tag(self, tag, assets):
	f = open(libraryPath+"\\assetTag.json", "w+")		
		if len(assets) > 0:
			for asset in assets:
				
'''
tagDic = {}
tag = "pine"
asset  = "\tree\treePine01.ma"
asset2  = "\tree\treePine01.png"
assets = ["\tree\treePine01.png", "\tree\treePine01.ma"]
tagDic[tag] = [asset2]

print tagDic
for asset in assets:
    if asset not in tagDic[tag]:
        tagDic[tag].append(asset)	
'''
		