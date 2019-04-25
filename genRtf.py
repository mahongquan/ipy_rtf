# -*- coding: utf-8 -*-
import clr
import sys
# import math
import getpath
drv=getpath.getpath().split("\\")[0]
clr.AddReferenceByPartialName("IronPython")
initpath=drv+r"\soft\rtf1\RtfConverter_v1.7.0\bin\Release"
sys.path.append(initpath)
clr.AddReference("Itenso.Rtf.Parser.dll")
# import Itenso.Rtf
from Itenso.Rtf.Parser import RtfParserListenerStructureBuilder,RtfParser
from Itenso.Rtf.Support import RtfSource
from Itenso.Rtf.Model import RtfElementCollection,RtfTag,RtfGroup,RtfText
# import System
# from System.IO import *
import codecs
wz={"仪器型号":13,"仪器编号":17
,"调试人员":20
,"频率第一天":23
,"频率第二天":25
,"频率第三天":27
,"压差第一天":41
,"压差第二天":43
,"压差第三天":45
,"红外":56
,"马达":58
,"温度":60
,"LC_L":72
,"LC_K":73
,"LC_B":74
,"HC_L":76
,"HC_K":77
,"HC_B":78
,"LS_L":80
,"LS_K":81
,"LS_B":82
,"HS_L":84
,"HS_K":85
,"HS_B":86
,".083_RSD_LC":98
,".083_RSD_LS":101
,".083_RSD_2_LC":104
,".083_RSD_2_LS":107
,"1.31RSD":115
,"1.31RSD_2":118
,"3.36RSD":126
,"3.36RSD_2":129
,"HS_NAME":130
,"HS_RSD":134
,"HS_RSD_2":137
}
# newValues=wz
wz1={
17:"仪器编号",
20:"调试人员",126:'3.36RSD',129:'3.36RSD_2',130:'HS_NAME',134:'HS_RSD',137:'HS_RSD_2'
,13:'仪器型号',23:'频率第一天',25:'频率第二天',27:'频率第三天'
,41:'压差第一天',43:'压差第二天',45:'压差第三天'
,56:"红外",58:"马达",60:"温度"
,72:'LC_L'
,73:'LC_K',74:'LC_B',76:'HC_L',77:'HC_K',78:'HC_B',80:'LS_L'
,81:'LS_K',82:'LS_B',84:'HS_L',85:'HS_K',86:'HS_B',98:'.083_RSD_LC',101:'.083_RSD_LS'
,104:'.083_RSD_2_LC',107:'.083_RSD_2_LS',115:'1.31RSD',118:'1.31RSD_2'}
count=0
def encodeText(Text):
    if Text == None or len(Text) == 0:
        return 
    res=' ';
    for  iCount in range(len(Text)):
        c = Text[iCount ];
        if c == '\t':
            res+=r'\tab '
        elif  ord(c) < 256:
            if ord(c) > 32 or ord(c) < 127:
                #出现特殊字符，需要斜线转义
                if c == '\\' or c == '{' or c == '}':
                    res+='\\'
                res+=c
            else:
                res+="\\\'"
                res+=c #( byte ) c );
        else:
            bs = c.encode("gb18030")
            iCount2 = 0
            while iCount2 < bs.Length: 
                res+="\\\'"
                res+=hex(ord(bs[iCount2]))[2:]
                iCount2 +=1
    return res
def MyStr(c,newValues):
    global count
    if type(c)==RtfTag:
        return c.ToString()
    elif type(c)==RtfElementCollection:
        r=""
        for one in c:
            r+=MyStr(one,newValues)
        return r
    elif type(c)==RtfGroup:
        r="{"
        for one in c.Contents:
            r+=MyStr(one,newValues)
        return r+"}"
    elif type(c)==RtfText:
        print(count,c)
        r=""
        if count in  wz1.keys():
            print "in"
            if newValues.get(wz1[count])!=None:
                newv=str(newValues[wz1[count]])
                r=encodeText(newv)
            else:
                r=encodeText(c.ToString())    
        else:
            r=encodeText(c.ToString())
        count+=1
        return r
    else:
        print("===not treat=====================")
        print(type(c))
        return ""
def  change(newValues):
    testRes=codecs.open("CS.rtf","r","cp1252").read()
    if ord(testRes[-1])==0:#remove 0 at file tail
        testRes=testRes[:-1]
    structureBuilder = RtfParserListenerStructureBuilder()
    parser =  RtfParser();
    parser.AddParserListener( structureBuilder )
    parser.Parse(RtfSource( testRes ) )
    rt = structureBuilder.StructureRoot
    new=MyStr(rt,newValues)
    f=codecs.open("CS调试记录.rtf","w","cp1252")        
    f.write(new)
    f.close()
if __name__=="__main__":
    change({})
# k=wz.keys()
# v=wz.values()
# d={}
# i=0
# for v1 in v:
#     d[v1]=k[i]
#     i+=1
# print(d)
# r=""
# for d1 in d:
#     r+=str(d1)+":'"+d[d1]+"',"
# print(r)