# -*- coding: utf-8 -*-
import clr
import sys
clr.AddReferenceByPartialName("System.Data")
import System.Data
clr.AddReferenceByPartialName("IronPython")
# initpath=r"e:\test"#D:\CS3000 19"
# sys.path.append(initpath)
# clr.AddReference("NCS.exe")
# clr.AddReference("NcsDbs.dll")
import NCS
import System
p=None
days=7
def checkOne(term):
    b =NCS.DataBase.Instance.InitDB(p.dbpath+r"\data.db")
    print(b)
    session=NCS.DataBase.Instance.GetSession()
    c=session.Connection
    print(dir(c))
    print(c.ConnectionString)
    cmd=c.CreateCommand()
    (fromd, tod)=ndaystr(days)
    ct="select strftime('%Y-%m-%d',sampleid) as day,SampleName,SampleNum from Result where SampleName like '"+term+"%' and SampleId between '" +fromd+"' and '"+tod+"'"
    #print(fromd,tod)
    #ct="select * from result"
    cmd.CommandText=ct
    rs=cmd.ExecuteReader()
    r=rs.Read()
    data=[]
    while(r):
        vs=rs.GetValues()
        one={}
        for k in vs.Keys:
            #print(k,vs.Get(k))
            one[k]=vs.Get(k)
        data.append(one)
        r=rs.Read()
    print(data)
    data=data[-7:]
    if len(data)!=7:
        print(term,len(data))
        raw_input("总数量不是7个数量错误")
    data0=data[:7]
    print(term)
    return(checkoneday(data0))
def check(term):
    b =NCS.DataBase.Instance.InitDB(p.dbpath+r"\data.db")
    print(b)
    session=NCS.DataBase.Instance.GetSession()
    c=session.Connection
    print(dir(c))
    print(c.ConnectionString)
    cmd=c.CreateCommand()
    (fromd, tod)=ndaystr(days)
    ct="select strftime('%Y-%m-%d',sampleid) as day,SampleName,SampleNum from Result where SampleName like '"+term+"%' and SampleId between '" +fromd+"' and '"+tod+"'"
    #print(fromd,tod)
    #ct="select * from result"
    cmd.CommandText=ct
    rs=cmd.ExecuteReader()
    r=rs.Read()
    data=[]
    while(r):
        vs=rs.GetValues()
        one={}
        for k in vs.Keys:
            #print(k,vs.Get(k))
            one[k]=vs.Get(k)
        data.append(one)
        r=rs.Read()
    print("========================")
    for one in data:
        print(one)
    if term==".083":
        data=data[-25:]
        if len(data)!=25:
            print(term,len(data))
            raw_input("总数量不是25个数量错误")
        data0=data[:7]
        data1=data[7:14]
        data2=data[14:]
        if len(data2)!=11:
            print(term)
            raw_input("第三天数量不是11个数量错误")
    else:
        data=data[-21:]
        if len(data)!=21:
            print(term,len(data))
            raw_input("总数量不是21个数量错误")
        data0=data[:7]
        data1=data[7:14]
        data2=data[14:]
        if len(data2)!=7:
            print(term)
            raw_input("第三天数量不是7个错误")
    print(term)
    return(checkoneday(data0) and checkoneday(data1) and checkoneday(data2))
def checkoneday(data):
    print(data)
    first=data[0]
    n=first["SampleNum"]
    day=first["day"]
    for one in data[1:]:
        print(one)
        n1=one["SampleNum"]
        day1=one["day"]
        if int(n1)-int(n)==1 and day1==day:
            n=n1
        else:
            print(n,n1)
            raw_input("序号不连续错误")
            return False
    return True
def nday(days):
    to=System.DateTime.Now
    from1=System.DateTime.Now
    #print(dir(from1))
    from1=from1.AddDays(-days)
    return(from1,to)
def ndaystr(days):
    (from1,to)=nday(days)
    return(from1.ToString("yyyy-MM-dd HH:mm:ss"),to.ToString("yyyy-MM-dd HH:mm:ss"))
def checkdayct(p1,elements):
    global p
    p=p1
    if p.ison:
        if p.l==3 or p.l==5:
            # a=check("38")
            a=check("120")
            return a
        else:
            a=check("135")
            return a
    else:
        r=True
        if "高碳" in elements:
            r=r and check("3.36")
            r=r and check("1.31")
        if  "低碳" in elements:
            r= r and check(".083")
        # if  "高硫" in elements:
        #     r= r and checkOne("39.52")
        return r
