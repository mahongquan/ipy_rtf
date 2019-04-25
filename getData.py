# -*- coding: utf-8 -*-
import clr
import sys
import math
import getmethod
import genRtf
clr.AddReferenceByPartialName("IronPython")
#initpath=r"d:\Program Files\NCS\CS3000"
#initpath=r"C:\Program Files (x86)\NCS\ONH3000"
# initpath=r"C:\CS3000备份\CS3000_1.7.0"
initpath=r"C:\Program Files (x86)\NCS\CS3000"
# initpath=r"C:\Users\ncs\Desktop\CS3000_1.7.0"
# initpath=r"C:\Program Files (x86)\NCS"
#initpath=r"C:\CS3000备份\CS3000_1.7.0"
#initpath=r"d:\NCSONH-3000"
# initpath=r"C:\Program Files\NCS\ONH3000"
wz={
# "仪器型号":13,"仪器编号":17
# ,"调试人员":20
# ,"频率第一天":23
# ,"频率第二天":25
# ,"频率第三天":27
# ,"压差第一天":41
# ,"压差第二天":43
# ,"压差第三天":45
# ,"红外":56
# ,"马达":58
# ,"温度":60,
# "LC_L":72
# ,"LC_K":73
# ,"LC_B":74
# ,"HC_L":76
# ,"HC_K":77
# ,"HC_B":78
# ,"LS_L":80
# ,"LS_K":81
# ,"LS_B":82
# ,"HS_L":84
# ,"HS_K":85
# ,"HS_B":86
# ,".083_RSD_LC":98
# ,".083_RSD_LS":101
# ,".083_RSD_2_LC":104
# ,".083_RSD_2_LS":107
# ,"1.31RSD":115
# ,"1.31RSD_2":118
# ,"3.36RSD":126
# ,"3.36RSD_2":129
# ,"HS_NAME":130
# ,"HS_RSD":134
# ,"HS_RSD_2":137
}
sys.path.append(initpath)
clr.AddReference("NCS.exe")
clr.AddReference("NcsDbs.dll")
import NCS
import System
import raw
import getlast
import dbpath
days=7
def get(term,cfg):
    (from1,to)=nday(days)
    l=NCS.DataBase.Instance.SelectResults(from1,to,term)
    #print(l,dir(l))
    dict1={}
    for i in range(NCS.DataBase.MaxChannel):
        if (cfg.Channels[i].enable):
            dict1[cfg.Channels[i].element]=[]
    for l1 in l.GetEnumerator():
        res=recalc(l1.SampleId,cfg)
        for k in res.keys():
            dict1[k].append(res[k])
    return(dict1)
def recalc(id1,cfg):
    #DateTime id1 = (DateTime)dr[FieldNameId];
    listResults={}
    volt = NCS.VoltSignal.LoadAll(id1);
    for i in range(NCS.DataBase.MaxChannel):
        if (cfg.Channels[i].enable):
            result = cfg.Factors[i].CalculateResult(
                 volt.ListT.ToArray(), volt.ListData[i].ToArray(), 
                 volt.SampleWeight, volt.FluxWeight)
            listResults[cfg.Channels[i].element]=result
    return(listResults)
def showfactor():
    print(NCS.Devices.Current.GetConfig().Channels)
    for i in range(NCS.DataBase.MaxChannel):
        #if (NCS.Devices.Current.GetConfig().Channels[i].enable):
            c=NCS.Devices.Current.GetConfig().Channels[i]
            f=NCS.Devices.Current.GetConfig().Factors[i]
            #print(c,dir(c))
            print(c.element)
            print(c.element,c.enable,c.delay,c.comporator,c.min,c.max,c.ratio)
            print(f.Linearity, f.Calibration, f.BaseK, f.BaseB, f.Blank)
def main():
    p=dbpath.P()
    p.init(initpath)
    print(p.dbpath)
    cfg=loadmethod(p)
    elements=[]
    for i in range(NCS.DataBase.MaxChannel):
        c=cfg.Channels[i]
        f=cfg.Factors[i]
        if not cfg.Channels[i].enable:
            continue
        elements.append(c.element)
    print(elements)
    if not raw.checkdayct(p,elements):
        raw_input("个数错误")
    else:
        raw_input("个数ok")
    NCS.DataBase.Instance.InitDB(p.dbpath+r"\data.db")
    if p.ison:
        if p.l==3 or p.l==5:
            #r112=get("112%",cfg)
            #checkrr(cfg,".0112",r112,{"低氧":1.5,"低氮":1.8},{"低氧":(.0112,0.0003),"低氮":(.0084,0.003)})
            # r112=get("38%",cfg)
            # checkrrNew(cfg,".0038",r112,{"低氧":[0.00015,"sd"],"低氮":1.8},{"低氧":(.0038,0.0003),"低氮":(.0820,0.0003)})
            r120=get("120%",cfg)
            checkrrNew(cfg,".0120",r120,{"低氧":1.5,"低氮":[0.00018,"sd"]}
                ,{"低氧":(.0120,0.0003),"低氮":(.0019,0.0003)})            

        else:
            r135=get("135%",cfg)
            checkrr(cfg,".0135",r135,{"低氧":1.5},{"低氧":(.0135,0.0003)})
    else:
        for e in elements:
            print(e)
        ############
        if "高碳" in elements:
            r336=get("3.36%",cfg)
            r131=get("1.31%",cfg)
        if "高硫" in elements:
            r39=get("39.52%",cfg)
        r083=get(".083%",cfg)
        #############
        if len(r083)==0:
            r083=get("0.083%",cfg)
        if "高碳" in elements:
            checkrr(cfg,"3.36",r336,{"高碳":0.5,"低硫":2},{"高碳":(3.36,0.03)})
            checkrr(cfg,"1.31",r131,{"高碳":0.5,"低硫":2},{"高碳":(1.31,0.03)})
        checkrr(cfg,".083",r083,{"低碳":0.8,"低硫":2},{"低碳":(.083,0.003),"低硫":(0.031,0.003)})
        if "高硫" in elements:
            checkr(cfg,"39.52",r39,{"高硫":2},{"高硫":(39.52,0.4)})
    checkline(cfg)
    genRtf.change(wz)
    raw_input("pause")
def checkr(cfg,term,r336,rsds,dvs):
    #print(r336)
    for i in range(NCS.DataBase.MaxChannel):
        
        if (not cfg.Channels[i].enable):
            continue
        c=cfg.Channels[i]
        print(c.element)
        rsd=rsds.get(c.element)
        dv=dvs.get(c.element)
        if rsd!=None:
            data=r336[c.element]
            print(term+" "+c.element)
            data=data[-7:]
            print(pjrsd(data,dv,rsd))
def checkrrNew(cfg,term,r336,rsds,dvs):
    #print(r336)
    for i in range(NCS.DataBase.MaxChannel):
        if (not cfg.Channels[i].enable):
            continue
        c=cfg.Channels[i]
        rsd=rsds.get(c.element)
        dv=dvs.get(c.element)
        if rsd!=None:
            data=r336[c.element]
            print(term+" "+c.element)
            if term==".083":
                data=data[-25:]
                print(pjrsd(data,dv,rsd))
                data0=data[:7]
                print(pjrsd(data0,dv,rsd))
                data1=data[7:14]
                print(pjrsd(data1,dv,rsd))
                data2=data[14:]
                print(pjrsd(data2,dv,rsd))
            else:

                data=data[-21:]
                data0=data[:7]
                data1=data[7:14]
                data2=data[14:]
                if rsd.__class__==list:
                    sd=rsd[0]
                    print(pjSd(data,dv,sd))
                    print(pjSd(data0,dv,sd))
                    print(pjSd(data1,dv,sd))
                    print(pjSd(data2,dv,sd))

                else:
                    print(pjrsd(data,dv,rsd))
                    print(pjrsd(data0,dv,rsd))
                    print(pjrsd(data1,dv,rsd))
                    print(pjrsd(data2,dv,rsd))

def checkrr(cfg,term,r336,rsds,dvs):
    #print(r336)
    global wz
    for i in range(NCS.DataBase.MaxChannel):
        if (not cfg.Channels[i].enable):
            continue
        c=cfg.Channels[i]
        rsd=rsds.get(c.element)
        dv=dvs.get(c.element)
        if rsd!=None:
            data=r336[c.element]
            print(term+" "+c.element)
            if term==".083":
                data=data[-25:]
                r_change=pjrsd(data,dv,rsd)
                data0=data[:7]
                r_1=pjrsd(data0,dv,rsd)
                data1=data[7:14]
                r_2=pjrsd(data1,dv,rsd)
                data2=data[14:]
                r_3=pjrsd(data2,dv,rsd)
            else:
                data=data[-21:]
                r_change=pjrsd(data,dv,rsd)
                data0=data[:7]
                r_1=pjrsd(data0,dv,rsd)
                data1=data[7:14]
                r_2=pjrsd(data1,dv,rsd)
                data2=data[14:]
                r_3=pjrsd(data2,dv,rsd)
            if term=="1.31" and c.element=="高碳":
                wz["1.31RSD"]=r_3[1]
                wz["1.31RSD_2"]=r_change[1]
            if term=="3.36" and c.element=="高碳":
                wz["3.36RSD"]=r_3[1]
                wz["3.36RSD_2"]=r_change[1]
            if term==".083" and c.element=="低碳":
                wz[".083_RSD_LC"]=r_3[1]
                wz[".083_RSD_2_LC"]=r_change[1]
            if term==".083" and c.element=="低硫":
                wz[".083_RSD_LS"]=r_3[1]
                wz[".083_RSD_2_LS"]=r_change[1]
def pjSd(data,dv,rsd1):
    #print(data)
    t=0.0
    for one in data:
        t=t+one
    pj=t/len(data)
    rsd=0.0
    for one in data:
        #print(one)
        rsd+=(one-pj)*(one-pj)
    rsd=rsd/(len(data)-1)
    rsd=math.sqrt(rsd)
    #rsd=rsd/pj*100
    if dv!=None:
        if len(data)>12:#长期
            p1=rsd<rsd1*2
        else:
            p1=rsd<rsd1
        p2=(math.fabs(pj-dv[0])<dv[1])
        data=("%0.5f" % pj, "%0.5f%%" % rsd,len(data), "%0.5f" % (pj-dv[0]),p1,p2)
        if p1==False or p2==False:
            r="""============not pass======================================================
                %s
==========================================================================""" % str(data)
            return r
        else:
            return str(data)
    else:
        data =("%0.5f" % pj,"%0.5f%%" % rsd,len(data),None)
        return str(data)

def pjrsd(data,dv,rsd1):
    #print(data)
    t=0.0
    for one in data:
        t=t+one
    pj=t/len(data)
    rsd=0.0
    for one in data:
        #print(one)
        rsd+=(one-pj)*(one-pj)
    rsd=rsd/(len(data)-1)
    rsd=math.sqrt(rsd)
    rsd=rsd/pj*100
    if dv!=None:
        if len(data)>12:#长期
            p1=rsd<rsd1*2
        else:
            p1=rsd<rsd1
        p2=(math.fabs(pj-dv[0])<dv[1])
        data=("%0.5f" % pj, "%0.2f%%" % rsd,len(data), "%0.4f" % (pj-dv[0]),p1,p2)
        if p1==False or p2==False:
            r="""============not pass======================================================
                %s
==========================================================================""" % str(data)
            print r
            return data
        else:
            print(str(data))
            return data
    else:
        data =("%0.5f" % pj,"%0.2f%%" % rsd,len(data),None)
        print(str(data))
        return data
def checkline(cfg):
    for i in range(NCS.DataBase.MaxChannel):
        c=cfg.Channels[i]
        f=cfg.Factors[i]
        if not cfg.Channels[i].enable:
            continue
        if "碳" in c.element:
            if f.BaseR>=0.9999:
                print(c.element+" "+f.BaseR.ToString()+" ok")
            else:
                print(c.element+" "+f.BaseR.ToString()+"  ========================not ok")
            print(f.Linearity,f.BaseK,f.BaseB)
        elif "硫" in c.element:
            if f.BaseR>=0.9995:
                print(c.element+" "+f.BaseR.ToString()+" ok")
            else:
                print(c.element+" "+f.BaseR.ToString()+"  ========================not ok")
            print(f.Linearity,f.BaseK,f.BaseB)
        if "氧" in c.element:
            if f.BaseR>=0.9995:
                print(c.element+" "+f.BaseR.ToString()+" ok")
            else:
                print(c.element+" "+f.BaseR.ToString()+"  ========================not ok")
            print(f.Linearity,f.BaseK,f.BaseB)
        elif "氮" in c.element:
            if f.BaseR>=0.995:
                print(c.element+" "+f.BaseR.ToString()+" ok")
            else:
                print(c.element+" "+f.BaseR.ToString()+"  ========================not ok")
            print(f.Linearity,f.BaseK,f.BaseB)
        if c.element=="低碳":
            wz["LC_L"]="%0.5f" % f.Linearity
            wz["LC_K"]="%0.5f" % f.BaseK
            wz["LC_B"]="%0.5f" % f.BaseB
        if c.element=="低硫":
            wz["LS_L"]="%0.5f" % f.Linearity
            wz["LS_K"]="%0.5f" % f.BaseK
            wz["LS_B"]="%0.5f" % f.BaseB
        if c.element=="高碳":
            wz["HC_L"]="%0.5f" % f.Linearity
            wz["HC_K"]="%0.5f" % f.BaseK
            wz["HC_B"]="%0.5f" % f.BaseB
        if c.element=="高硫":
            wz["HS_L"]="%0.5f" % f.Linearity
            wz["HS_K"]="%0.5f" % f.BaseK
            wz["HS_B"]="%0.5f" % f.BaseB
def loadmethod(p):
    if p.ison:
        if p.l==3 :
            f=getmethod.getmethod(p,p.initpath+"\\ON")
            f=p.initpath+"\\ON\\"+f+".ini"
        elif p.l==5:
            f=getmethod.getmethod(p,p.initpath+"\\ONH")
            f=p.initpath+"\\ONH\\"+f+".ini"
        elif p.l==4:
            f=getmethod.getmethod(p,p.initpath+"\\OH")
            f=p.initpath+"\\OH\\"+f+".ini"
        else:
            f=getmethod.getmethod(p,p.initpath+"\\O")
            f=p.initpath+"\\O\\"+f+".ini"
    else:
        f=getmethod.getmethod(p,p.initpath+"\\CS")
        f=p.initpath+"\\CS\\"+f+".ini"
    print(f)
    print(dir(NCS.NcsSerialize))
    print(NCS.Devices.Current.GetConfig().GetType())
    cfg=NCS.NcsSerialize.Deserialize(f, NCS.Devices.Current.GetConfig().GetType())
    print("cfg="+str(cfg))
    return cfg
    # e=NCS.ConfigBase.Enumerate(initpath+"\\CS",NCS.Devices.Current.GetConfig().GetType())
    # for f in e:
    #     if f!="Default":
    #         if ison:
    #             f=initpath+"\\O\\"+f+".ini"
    #         else:
    #             f=initpath+"\\CS\\"+f+".ini"
    #         cfg=NCS.NcsSerialize.Deserialize(f, NCS.Devices.Current.GetConfig().GetType())
    #         # for c in cfg.Channels:
    #             # print(c.element,c.enable,c.delay,c.comporator,c.min,c.max,c.ratio)
    #         break
    # return cfg
def nday(days):
    to=System.DateTime.Now
    from1=System.DateTime.Now
    #print(dir(from1))
    from1=from1.AddDays(-days)
    return(from1,to)
if __name__=="__main__":
    main()
