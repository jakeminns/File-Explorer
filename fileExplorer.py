from os.path import expanduser#import the os
import tkinter as tk
from pathlib import Path
import numbers    

class pathHistory:
    
    def __init__(self, path):
        self.pathList = []
        self.pathListIndex = 0
        
    def addNewPath(self,path):
        self.pathListIndex = self.pathListIndex + 1
        self.pathList.append(path)
        
    def resetPathListIndex(self):
        self.pathListIndex = 0
        
    def backButtonPressed(self):
        if self.backCheck():
            self.pathListIndex = self.pathListIndex - 1
            
    def forwardButtonPressed(self):
        if self.forwardCheck():
            self.pathListIndex = self.pathListIndex + 1
    
    def forwardCheck(self):
        if self.pathListIndex < len(self.pathList):
            return True
        else:
            return False
    def backCheck(self):
        if self.pathListIndex >1:
            return True
        else:
            return False  
    def newPathOpenedCutList(self):
        self.pathList = self.pathList[0:self.pathListIndex]          
class MainGui:
    
    def __init__(self,master, path):
        self.master=master
        self.path =  path
        master.title("File Explorer")
        
        #Path History Object
        self.pathList = pathHistory(path)
        
        #Path Text Vairable
        self.entry_path_text = tk.StringVar()
        
        #Path Contents
        self.path_contents = tk.Listbox(master, selectmode=tk.SINGLE)   
        self.path_contents.bind("<Double-1>",self.updatePathOnItemDoubleClick)
        
        #Path Text Entry Object
        self.entry_path = tk.Entry(master)
        self.updatePath(str(self.path),"o")   
 
        #File Contents Window
        self.file_contents = tk.Text(master)
    #    self.image_contents = tk.Image(master)
    
        #Go to Path Button
        self.goto_button = tk.Button(master, text="Open", command=lambda: self.updatePath(self.entry_path.get(),"f"))
        self.back_button = tk.Button(master, text="<-", command=lambda: self.backToPreviousPath())
        self.forward_button = tk.Button(master, text="->",command=lambda: self.forwardToPreviousPath() )
        self.up_button = tk.Button(master, text="^",command=lambda:self.upToPath())
        
        #Layout
        self.back_button.grid(row=0, column=0)
        self.forward_button.grid(row=0,column=1)
        self.up_button.grid(row=0,column=2)
        self.entry_path.grid(row=0,column=3,columnspan=2,sticky=tk.N+tk.E+tk.S+tk.W)
        self.goto_button.grid(row=0,column=5)
        self.path_contents.grid(row=1,column=0,rowspan=2,columnspan=4,sticky=tk.N+tk.E+tk.S+tk.W)
        self.file_contents.grid(row=1,column=4, columnspan=2)
     #   self.image_contents.grid(row=2,column=4)
        
    def upToPath(self):
        
        p = len(str(self.path))

        for i in range(len(str(self.path))):
            if str(self.path)[p-1] == "\\":
                self.updatePath(str(self.path)[0:p-1],"f")
                break
            else:
                p=p-1
        
    def backToPreviousPath(self):
        
        if self.pathList.backCheck():
            self.pathList.backButtonPressed()
            self.updatePath(self.pathList.pathList[self.pathList.pathListIndex-1],"b") 

    def forwardToPreviousPath(self):
        
        if self.pathList.forwardCheck():
            self.pathList.forwardButtonPressed()
            self.updatePath(self.pathList.pathList[self.pathList.pathListIndex-1],"f") #pathList -1 because pathListIndex starts count at 1
        
    def displayPathContents(self):
        
        contents = self.getFolderContentsList(self.path)
        self.path_contents.delete(0, tk.END)
        for i in contents:
            content_label = str(self.path)
            i = i[len(content_label):len(i)]
            self.path_contents.insert(tk.END, i)
        
    def updatePath(self,newPath,backForwardOpen):
        
        self.path = Path(newPath)
        self.entry_path_text.set(self.path)
        self.entry_path.delete(0,tk.END)
        self.entry_path.insert(0,self.entry_path_text.get())
        
        if backForwardOpen == "b":
            pass
        elif backForwardOpen=="f":
            pass
        elif backForwardOpen == "o":
            self.pathList.newPathOpenedCutList()
            self.pathList.addNewPath(self.path)
            
        self.displayPathContents()

    def updatePathOnItemDoubleClick(self, index):
        
        contentIndex = self.path_contents.curselection()
        contents = self.getFolderContentsList(self.path)
        path = contents[contentIndex[0]]
        if isinstance(contentIndex[0],numbers.Number):
            if Path(path).is_file():
                print("file", self.path)
                file = open(Path(path),"r")
                lines = file.readlines()
                print(file.readlines())
                self.file_contents.delete(1.0,tk.END)
                for line in lines:
                    self.file_contents.insert(tk.END,line)
            else:
                print("folder")
                self.updatePath(path,"o")
            
    def pathItemClick(self, index):
        
        contentIndex = self.path_contents.curselection()
        print("cont",contentIndex)
        if isinstance(contentIndex[0],numbers.Number):
            contents = self.getFolderContentsList(self.path)
            print("Click",contents[contentIndex[0]])
            
        
    def getFolderContentsList(self, path):
        contents = []
        contents.clear()
        for x in path.iterdir():
           # if x.is_dir():
           contents.append(str(x))
                
        return contents

root = tk.Tk()

the_gui = MainGui(root, Path.home())


root.mainloop()
