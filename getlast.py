# -*- coding: utf-8 -*-
import clr
import sys
import math
import getmethod
clr.AddReferenceByPartialName("IronPython")
initpath=r"D:\ma\ONHCS1014\ONH3000\ONHCS\bin\Debug"
sys.path.append(initpath)
clr.AddReference("NCS.exe")
clr.AddReference("NcsDbs.dll")
import NCS
import System
import NCS.ConfigDB
def getLast(initpath):
    r=NCS.ConfigDB.Instance.Init(initpath+"\\Configs.db")
    u=NCS.ConfigDB.Instance.LoadLastUser()
    print(u,dir(u))
    if u.Count>0:
        u=u[0]
        print(dir(u))
        return u.lastDevice
    return None
if __name__=="__main__":
    main()
