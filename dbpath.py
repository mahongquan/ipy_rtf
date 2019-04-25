# -*- coding: utf-8 -*-
import getlast
class P:
    ison=False
    dbpath=""
    def init(self,initpath):
        self.initpath=initpath
        if "ONH" in initpath:
            self.ison=True
        else:
            self.ison=False
        if self.ison:
            l=getlast.getLast(initpath)
            if l==0:
                self.dbpath=initpath+r"\O"
            elif l==1:
                self.dbpath=initpath+r"\N"
            elif l==2:
                self.dbpath=initpath+r"\H"
            elif l==3:
                self.dbpath=initpath+r"\ON"
            elif l==4:
                self.dbpath=initpath+r"\OH"
            elif l==5:
                self.dbpath=initpath+r"\ONH"
            self.l=l
        else:
            self.dbpath=initpath+r"\CS"
if __name__=="__main__":
    p=P()
    p.init(r"C:\Users\Administrator\Desktop\ONH3000 2.1.33")
    print(p.ison,p.dbpath)
    
