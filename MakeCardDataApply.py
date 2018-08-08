#coding:utf-8
# @Time    :2018-8-8 14:55
# @Author  :David
# @Mail    :xxx@yyy.com
# @Function:PBOSS_MakeCardData_AutoTest
import requests
from time import *
import random
import os,sys
import ftplib # FTP操作
import requests

'''01-生成并发送制卡申请报文'''
print u"请输入制卡省份,制卡数量,制卡号段,卡商,申请人,申请原因,申请人联系方式,以空格分开\n"
print u"模板:250 10 1722220 2 David MakeCardData 13512345678\n"

bipcode ='BIP2B950'

FourteenTime = strftime('%Y%m%d%H%M%S', localtime(time()))

provid,number,MsisdnSection,CardMfrs,Applicant,ApplyReason,ApplicantPhone =\
	raw_input("provid,number,MsisdnSection,CardMfrs,Applicant,ApplyReason,ApplicantPhone:\n").split()
			  
Appcode = provid + '1' +bipcode+ FourteenTime + str(random.randint(000000, 999999)).zfill(6)

OprNum = Appcode[:-6]+str(random.randint(000000, 999999)).zfill(6)
print u"生成的制卡订单号Appcode: \n%s" % Appcode	
print u"生成的制卡操作流水号OprNum: \n%s" % OprNum

def xmlheader(FourteenTime,provid):
    xml_request='''<?xml version="1.0" encoding="UTF-8"?>
<InterBOSS>
    <Version>0100</Version>
    <TestFlag>0</TestFlag>
    <BIPType>
        <BIPCode>BIP2B950</BIPCode>
        <ActivityCode>T2140950</ActivityCode>
        <ActionCode>0</ActionCode>
    </BIPType>
    <RoutingInfo>
        <OrigDomain>BOSS</OrigDomain>
        <RouteType>00</RouteType>
        <Routing>
            <HomeDomain>PBSS</HomeDomain>
            <RouteValue>997</RouteValue>
        </Routing>
    </RoutingInfo>
    <TransInfo>
        <SessionID>2017070511031010</SessionID>
        <TransIDO>2017070511031010</TransIDO>
        <TransIDOTime>%s</TransIDOTime>
	</TransInfo>
	<SNReserve> 
		<TransIDC>2017070511031010</TransIDC>
		<ConvID>2017070511031010</ConvID>
		<CutOffDay>%s</CutOffDay>
		<OSNTime>%s</OSNTime>
		<OSNDUNS>%s0</OSNDUNS>
		<HSNDUNS>9970</HSNDUNS>
		<MsgSender>%s1</MsgSender>
		<MsgReceiver>0600</MsgReceiver>
		<Priority>90</Priority>
		<ServiceLevel>55</ServiceLevel>
		<SvcContType>01</SvcContType>
	</SNReserve>  
</InterBOSS>'''%(FourteenTime[:],FourteenTime[:8],FourteenTime[:],provid,provid)
    return xml_request
    
def xmlbody(Appcode,provid,Applicant,ApplicantPhone,FourteenTime,ApplyReason,MsisdnSection,number):
    xml_request='''<?xml version="1.0" encoding="UTF-8"?>
<InterBOSS>
<SvcCont><![CDATA[<?xml version="1.0" encoding="UTF-8"?>
<SyncInfo>
    <Queryinfo>
        <OprNum>%s</OprNum>
        <QueryOprNum>%s</QueryOprNum>
        <CardMfrs>2</CardMfrs>     --2：武汉天喻
        <ProvinceID>%s</ProvinceID>
        <Applicant>%s</Applicant>
        <ApplicantPhone>%s</ApplicantPhone>
        <ApplyDate>%s</ApplyDate>
        <ApplyReason>%s</ApplyReason>
        <FileReceiver>1</FileReceiver>
          <MsisdnSectionInfo>        
            <MsisdnSection>%s</MsisdnSection> 
            <MsisdnSectionNum>%s</MsisdnSectionNum> 
        </MsisdnSectionInfo>
    </Queryinfo>
</SyncInfo>]]>
</SvcCont>
</InterBOSS>'''%(OprNum,Appcode,provid,Applicant,ApplicantPhone,FourteenTime[:8],ApplyReason,MsisdnSection,number)
    return xml_request

 
header=xmlheader(FourteenTime,provid)
body=xmlbody(Appcode,provid,Applicant,ApplicantPhone,FourteenTime,ApplyReason,MsisdnSection,number)

print u"生成的报文头:\n"
print header

print u"生成的报文体:\n"
print body

requestXml = header+body

a=body.find('<QueryOprNum>')
b=body.find('</QueryOprNum>')

Appcode_new=body[a+13:b]
print Appcode_new

print (Appcode == Appcode_new)
 


url=u'http://192.168.127.110:9083/huawei-test3/http/tsn_boss_call_pboss/send.jsp'
data = {'serviceUrl':'http://192.168.127.110:9080/interface4boss/bossTSNActionServlet','requestHeaderXml': header,'requestBodyXml':body,'responseXml':''}
r = requests.post(url,data=data)
x=r.text.find("<Response>")
y=r.text.find("</Response>")
print(r.text[x:y+11])

 

print u"制卡订单已生成，请手动去CSP前台进行审批，谢谢！"

sleep(60)#去审批

answer = raw_input(u'是否已经申请通过？y/n \n')
if answer == 'y':
    pass
if answer == 'n':
    sleep(60)
    print "再等待1分钟..."

'''02-生成握奇模拟卡数据文件及密钥索引文件'''
    
#起始IMSI,起始ICCID需要去CSP前台审批后获取
print u"请依次输入起始IMSI,起始ICCID,以空格分开\n"
print u"模板:460072200000959 898602F2131820000959\n"
 
IMSIStart,ICCIDStart = raw_input("IMSIStart,ICCIDStart:\n").split()
	
print "当前工作目录为：%s" % os.getcwd()


if os.getcwd() != 'C:/Users/Administrator/Desktop/woqi':
        if os.path.exists('C:/Users/Administrator/Desktop/woqi') == True:
            os.chdir('C:/Users/Administrator/Desktop/woqi')
        else:
            os.makedirs('C:/Users/Administrator/Desktop/woqi')
            os.chdir('C:/Users/Administrator/Desktop/woqi')
else:
    pass
    
filename0 = 'KeyData_'+Appcode+'_'+CardMfrs+'_'+Appcode[0:3]+'_1_'+\
           Appcode[12:26]+'.IDX'
		   
filename = 'MW_USimMS_'+Appcode+'_'+CardMfrs+'_'+Appcode[0:3]+'_1_'+\
           Appcode[12:26]+'.dat'
           
filename_jiami = 'USimMS_'+Appcode+'_'+CardMfrs+'_'+Appcode[0:3]+'_1_'+\
           Appcode[12:26]+'.dat'           

		   
print filename0
print filename
print filename_jiami

fp=open(filename0,'w')
print u"开始写入秘钥索引文件内容..."
fp.write('001|002\n')
fp.close()
fp=open(filename0,'r')
print u"生成的秘钥索引文件内容为：\n %s" % fp.read()
fp.close()

#sleep(5)
fp=open(filename,'w')#打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
print u"开始写入卡数据文件头..."
 
fp.write(Appcode+'|'+CardMfrs+'|'+Appcode[0:3]+'|'+Applicant+'|'+ApplicantPhone+'|'+\
	Appcode[12:20]+'|'+ApplyReason+'|'+MsisdnSection+'|'+number+'|2~'+str(int(number)+1)+'\n')
fp.close()
fp=open(filename,'r')
print u"生成的制卡模拟文件头为：\n %s" % fp.read()
fp.close()

#sleep(5)
print u"开始写入卡数据文件体..."
fp=open(filename,'a')#打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
 
for i in range(int(number)):
	#IMSI = str(4600722000000)+str(i).zfill(2)#如果制卡数量小于等于99张就得补1位，完整是2位
	IMSI = str(int(IMSIStart)+i)
	ICCID = ICCIDStart[:-5]+str(int(ICCIDStart[-5:])+i).zfill(5)
	fp.write(IMSI+'|'+ICCID+'|0C3B713EAF0CD3BC63BA5ABC6C9475EF|679A21DDBB73C82E593B2B17B1000000|11111111|22222222|0123|4567|1A2B3C4D|'+\
                 IMSI[-1]+'|13800100569\n')
				 
fp.close()
 

print u"生成的制卡握奇模拟卡数据文件和密钥索引文件见：\n C:/Users/Administrator/Desktop/woqi: \n %s \n %s" % (filename0,filename)

'''03-加密握奇模拟卡数据文件'''

#切换到EncryptCardFile.jar包所在路径--桌面
if os.getcwd() != 'C:/Users/Administrator/Desktop':
        os.chdir('C:/Users/Administrator/Desktop')
        
print  "当前工作目录为：%s" % os.getcwd()        

#对握奇加密，要把EncryptCardFile.jar包放到握奇卡数据同一个目录（此处密钥为001|002 只用到001）
filepath = 'C:\Users\Administrator\Desktop\woqi\\'+filename

Encrypt_filepath = 'C:\Users\Administrator\Desktop\woqi\\'+filename_jiami
#必须在EncryptCardFile.jar包所在路径执行java -jar 加密才能成功
#java -jar EncryptCardFile.jar 1的密钥 0的密钥 源文件 加密后的文件（记得带上路径，不然覆盖了原文件）

#判断目录是否存在，若不存在，创建目录
# if os.path.exists('C:/Users/Administrator/Desktop/woqi/jiami') == False:
    # os.makedirs('C:/Users/Administrator/Desktop/woqi/jiami')
# else:
    # pass
    

def EncryptCardFile(filepath,Encrypt_filepath):
    cmd_command = 'java -jar EncryptCardFile.jar E4B044E830559B337AD15F2151A05AE8 B9A8C2FDA2378AA4A8EA9D028064FB3B'+' '+filepath+' '+Encrypt_filepath
    print u"加密命令：%s" % cmd_command
    os.system(cmd_command)
   
EncryptCardFile(filepath,Encrypt_filepath)

print u"加密后的制卡握奇模拟文件和密钥索引文件见：\n C:/Users/Administrator/Desktop/woqi: \n %s \n %s" % (filename0,filename_jiami)


'''04-通过FTP上传握奇模拟卡数据文件(加密的)及密钥索引文件'''

host = '192.168.127.111'
username = 'pboss'
password = 'P_BOSS$2017'
file = '1.txt'

f = ftplib.FTP(host)  # 实例化FTP对象
f.login(username, password)  # 登录

# 获取当前路径
pwd_path = f.pwd()
#print(u"FTP当前路径:", pwd_path)
print u"FTP当前路径:%s" % pwd_path

# 逐行读取ftp文本文件
# f.retrlines('RETR %s' % file)


def ftp_upload_miyao():
    '''以二进制形式上传文件'''
    file_remote = '/home/pboss/file/pboss/cardinfo/'+filename0
    print file_remote
    #file_local = 'D:\\test_data\\ftp_upload.txt'
    file_local = 'C:\\Users\\Administrator\\Desktop\\woqi\\'+filename0
    print file_local
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'rb')
    f.storbinary('STOR ' + file_remote, fp, bufsize)
    fp.close()

def ftp_upload_kashuju():
    '''以二进制形式上传文件'''
    file_remote = '/home/pboss/file/pboss/cardinfo/'+filename_jiami
    print file_remote
    #file_local = 'D:\\test_data\\ftp_upload.txt'
    file_local = Encrypt_filepath
    print file_local
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'rb')
    f.storbinary('STOR ' + file_remote, fp, bufsize)
    fp.close()

#ftp_download()
ftp_upload_miyao()
ftp_upload_kashuju()
f.quit()


'''05-模拟握奇发送反馈报文通知PBOSS'''

sleep(30)
# print u"请确认是否已经上传加密的握奇卡数据文件及密钥索引到指定目录？\n"
# a =  raw_input("：YES or NOT?\n"))

print u"开始模拟握奇发送反馈报文通知PBOSS..."

def WoqiXml(Appcode,filename_jiami,filename0):
    xml_request='''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pbos="http://www.chinamobile.com/PBOSS/">
<soapenv:Header/>
<soapenv:Body>
        <pbos:CardApplyResultNoticeRequest>
               <Queryinfo>
                      <OprNum>%s</OprNum>
					  <QueryOprNum>%s</QueryOprNum>
					  <Result>01</Result>
                      <ResultDesc></ResultDesc>
                      <DataFile>%s</DataFile>
                      <KeyIdxFile>%s</KeyIdxFile>
               </Queryinfo>
        </pbos:CardApplyResultNoticeRequest>
</soapenv:Body>
</soapenv:Envelope>''' % (OprNum,Appcode,filename_jiami,filename0)
    return xml_request
    

    
woqixml=WoqiXml(Appcode,filename_jiami,filename0)
print woqixml

url=u'http://192.168.127.110:9083/huawei-test3/http/soap/send.jsp'
data = {'serviceUrl':'http://192.168.127.110:9080/interface4cdcs/services/PBOSSCardApplyResultNotice','requestXml':woqixml,'responseXml':''}
r = requests.post(url,data=data)
#<RspCode>0000</RspCode>
x=r.text.find("<RspCode>")
y=r.text.find("</RspCode>")

print u"\n查看反馈结果报文返回码...\n"
print(r.text[x:y+9])

'''06-模拟写卡平台生成卡数据及密钥索引文件'''

#131802FFFFF120000000需要去后台日志查询获取
print u"请输入EIDStart,以空格分开\n"
print u"模板:131802FFFFF120000000\n"
	
EIDStart = raw_input(u"EIDStart:\n")


EIDEnd=EIDStart[:-7]+str(int(EIDStart[-7:])+int(number)-1).zfill(7)

print "EIDEnd：%s" % EIDEnd
#print u"制卡订单号appcode为: %s" % Appcode
print "当前工作目录为：%s" % os.getcwd()
 

if os.getcwd() != 'C:/Users/Administrator/Desktop/wcp':
        if os.path.exists('C:/Users/Administrator/Desktop/wcp') == True:
            os.chdir('C:/Users/Administrator/Desktop/wcp')
        else:
            os.makedirs('C:/Users/Administrator/Desktop/wcp')
            os.chdir('C:/Users/Administrator/Desktop/wcp')
else:
    pass
 
 
filename0_wcp = 'KeyData_'+Appcode+'_2_'+Appcode[0:3]+'_'+Appcode[12:26]+'.IDX'
		   
filename_wcp = 'MW_USimMS_UpdateKey_'+Appcode+'_2_'+Appcode[0:3]+'_'+Appcode[12:26]+'.dat'

filename_wcp_jiami = 'USimMS_UpdateKey_'+Appcode+'_2_'+Appcode[0:3]+'_'+Appcode[12:26]+'.dat'
		   
print filename0_wcp
print filename_wcp

fp=open(filename0_wcp,'w')
print u"开始写入秘钥索引文件内容..."
fp.write('001|002\n')
fp.close()
fp=open(filename0_wcp,'r')
print u"生成的秘钥索引文件内容为：\n %s" % fp.read()
fp.close()

#sleep(5)
fp=open(filename_wcp,'w')#打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
print u"开始写入卡数据文件头..."
 
fp.write(Appcode+'|2|'+Appcode[0:3]+'|David|13612345678|'+\
	Appcode[12:26]+'|MakeCardData|'+EIDStart+'|'+EIDEnd+'\n')
fp.close()
fp=open(filename_wcp,'r')
print u"生成的制卡模拟文件头为：\n %s" % fp.read()
fp.close()

#sleep(5)
print u"开始写入卡数据文件体..."
fp=open(filename_wcp,'a')#打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。

# EIDStart[:-7]+str(int(EIDStart[-7:])+int(i)).zfill(7)
for i in range(int(number)):
	fp.write(EIDStart[:-7]+str(int(EIDStart[-7:])+int(i)).zfill(7)+'|'+'3467012345abcde0456783232809'+str(i).zfill(4)+'|3467012345abcde0456873232809'+str(i).zfill(4)+'|3467012345abcde0457683232809'+str(i).zfill(4)+'\n')
				 
fp.close()
 

print u"生成的制卡写卡平台模拟文件和卡数据文件见：\n C:/Users/Administrator/Desktop/wcp: \n %s \n %s，请查收！" % (filename0_wcp,filename_wcp)



'''07-加密写卡平台模拟卡数据文件'''

#切换到EncryptCardFile.jar包所在路径--桌面
if os.getcwd() != 'C:/Users/Administrator/Desktop':
        os.chdir('C:/Users/Administrator/Desktop')
        
print  "当前工作目录为：%s" % os.getcwd()        

filepath_wcp = 'C:\Users\Administrator\Desktop\wcp\\'+filename_wcp
#Encrypt_filepath = 'C:\Users\Administrator\Desktop\woqi\jiami\\'+filename_jiami
Encrypt_filepath_wcp = 'C:\Users\Administrator\Desktop\wcp\\'+filename_wcp_jiami
 
   
EncryptCardFile(filepath_wcp,Encrypt_filepath_wcp)

print u"加密后的制卡写卡平台模拟文件和密钥索引文件见：\n C:/Users/Administrator/Desktop/wcp: \n %s \n %s" % (filename0_wcp,filename_wcp_jiami)


'''08-通过FTP上传写卡平台模拟卡数据文件(加密的)及密钥索引文件'''

host = '192.168.127.111'
username = 'pboss'
password = 'P_BOSS$2017'
file = '1.txt'

f = ftplib.FTP(host)  # 实例化FTP对象
f.login(username, password)  # 登录

# 获取当前路径
pwd_path = f.pwd()
#print(u"FTP当前路径:", pwd_path)
print u"FTP当前路径:%s" % pwd_path


def ftp_upload_miyao_wcp():
    '''以二进制形式上传文件'''
    file_remote = '/home/pboss/file/ftp/cardkiinfo/'+filename0_wcp
    print file_remote
    #file_local = 'D:\\test_data\\ftp_upload.txt'
    file_local = 'C:\\Users\\Administrator\\Desktop\\wcp\\'+filename0_wcp
    print file_local
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'rb')
    f.storbinary('STOR ' + file_remote, fp, bufsize)
    fp.close()

def ftp_upload_kashuju_wcp():
    '''以二进制形式上传文件'''
    file_remote = '/home/pboss/file/ftp/cardkiinfo/'+filename_wcp_jiami
    print file_remote
    #file_local = 'D:\\test_data\\ftp_upload.txt'
    file_local = Encrypt_filepath_wcp
    print file_local
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'rb')
    f.storbinary('STOR ' + file_remote, fp, bufsize)
    fp.close()

#ftp_download()
ftp_upload_miyao_wcp()
ftp_upload_kashuju_wcp()

f.quit()


'''09-模拟写卡平台发送反馈报文通知PBOSS'''

sleep(30)
# print u"请确认是否已经上传加密的握奇卡数据文件及密钥索引到指定目录？\n"
# a =  raw_input("：YES or NOT?\n"))

print u"开始模拟写卡平台发送反馈报文通知PBOSS..."


def WcpXml(Appcode,filename_wcp_jiami,filename0_wcp):
    xml_request=u'''<?xml version"1.0" encoding="UTF-8" standalone="no"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns1="http://www.chinamobile.com/PBOSS/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<SOAP-ENV:Header>
<ns1:Address>http://172.16.122.39:8080/interface4iomp/iompActionServlet</ns1:Address>
<ns1:Username>1</ns1:Username>
<ns1:Password>1</ns1:Password>
<ns1:BIPCode>WIP1A001</ns1:BIPCode>
<ns1:BIPVer>0100</ns1:BIPVer>
<ns1:ActivityCode>T1000002</ns1:ActivityCode>
<ns1:ProcID>20130923104514153</ns1:ProcID>
<ns1:TransIDO>0634TTM2P00920140923104514002010</ns1:TransIDO>
<ns1:TransIDH/>
<ns1:ProcessTime>20130923104514</ns1:ProcessTime>
<ns1:TestFlag>0</ns1:TestFlag>
<ns1:SvcConVer>0100</ns1:SvcConVer>
</SOAP-ENV:Header>
<SOAP-ENV:Body>
<SimKeyInfoSynNoticeRequest>
<OprSeq>%s</OprSeq>
<QueryOprNum>%s</QueryOprNum>       
<DataFileName>%s</DataFileName>
<KeyFileName>%s</KeyFileName>
<Retcode>0000</Retcode>
<RetMsg>成功</RetMsg>
</SimKeyInfoSynNoticeRequest>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>''' % (OprNum,Appcode,filename_wcp_jiami,filename0_wcp)
    return xml_request

 
#woqixml=WoqiXml(OprNum,Appcode,filename,filename0)
wcpxml=WcpXml(Appcode,filename_wcp_jiami,filename0_wcp)
print wcpxml

url=u'http://192.168.127.110:9083/huawei-test3/http/soap/send.jsp'
data = {'serviceUrl':'http://192.168.127.110:9080/interface4wcp/wcpActionServlet','requestXml':wcpxml,'responseXml':''}
r = requests.post(url,data=data)
#<RspCode>0000</RspCode>

# </SOAP-ENV:Header> 
# <SOAP-ENV:Body> 
# <SimKeyInfoSynNoticeResponse>
    # <Retcode>0000</Retcode>
    # <RetMsg>成功</RetMsg>
# </SimKeyInfoSynNoticeResponse>
# </SOAP-ENV:Body> 


x=r.text.find("<SimKeyInfoSynNoticeResponse>")
y=r.text.find("</SimKeyInfoSynNoticeResponse>")

print u"\n查看反馈返回信息...\n"
print(r.text[x:y+30])
 

sleep(120)
print u"准备下载下发给BOSS的个人化卡数据和密钥索引..."

'''10-下载下发给BOSS的个人化卡数据和密钥索引'''

host = '192.168.127.111'
username = 'pboss'
password = 'P_BOSS$2017'
file = '1.txt'

f = ftplib.FTP(host)  # 实例化FTP对象
f.login(username, password)  # 登录

# 获取当前路径
pwd_path = f.pwd()
#print(u"FTP当前路径:", pwd_path)
print u"FTP当前路径:%s" % pwd_path

if os.path.exists('C:/Users/Administrator/Desktop/boss') == False:
    os.makedirs('C:/Users/Administrator/Desktop/boss')
    
def ftp_download_boss_carddata():
    '''以二进制形式下载文件'''
    file_remote = '/home/pboss/file/pboss/cardinfo/'+filename_jiami
    file_local = 'C:\\Users\\Administrator\\Desktop\\boss\\'+filename_jiami
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'wb')
    f.retrbinary('RETR %s' % file_remote, fp.write, bufsize)
    fp.close()

def ftp_download_boss_index():
    '''以二进制形式下载文件'''
    file_remote = '/home/pboss/file/pboss/cardinfo/'+filename0
    file_local = 'C:\\Users\\Administrator\\Desktop\\boss\\'+filename0
    bufsize = 1024  # 设置缓冲器大小
    fp = open(file_local, 'wb')
    f.retrbinary('RETR %s' % file_remote, fp.write, bufsize)
    fp.close()
	
# ftp_download()
ftp_download_boss_carddata()
ftp_download_boss_index()
f.quit()