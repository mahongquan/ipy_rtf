# -*- coding: utf-8 -*-
import clr
import sys
clr.AddReferenceByPartialName("System.Xml")
clr.AddReferenceByPartialName("System.Data")
import  System.Xml
import System.Data
def getnode(doc,p):
    n=doc.SelectSingleNode(p);
    return(n.InnerText)
def readfn(p,fn):
    doc = System.Xml.XmlDocument()
    doc.Load(fn)
    if p.ison:
        name=getnode(doc,"/ONConfig/Name")
    else:
        name=getnode(doc,"/CSConfig/Name")
    return name
def getmethod(p,initpath):    
    return readfn(p,initpath+"/Config.xml")
def main():
    initpath=r"D:\Program Files\NCS\CS3000"
    print(readfn(initpath+"/CS/Config.xml"))
    pass
if __name__=="__main__":
    main()
