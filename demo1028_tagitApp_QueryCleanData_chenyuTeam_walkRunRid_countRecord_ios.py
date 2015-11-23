#!/usr/bin/env python
# encoding=utf-8

"""
tagit app 
android
count the number of record for each data collector
not visualize,cleaning,store data


"""


import numpy as np
 
import cPickle,math,random 
 
from leancloud import Object
from leancloud import Query
import leancloud
import time,os


deviceId={'huawei':'ffffffff-c7a8-3cd1-ffff-ffffea16e571', 
	'xiaomi':'ffffffff-c7a7-c7d4-0000-000031a92fbe', 
	'mine':'ffffffff-c95d-196f-0000-00007e282437',
	'chenyu':'ffffffff-c43f-692d-ffff-fffff4d57110',
	'wangx':'ffffffff-c28a-1bf0-0000-00005e774605',
	'zhangx':'ffffffff-f259-8a54-0000-0000300c3e8c',
	'liyt':'ffffffff-c7a8-3c91-ffff-ffffa2dc21fc',
	'donggy':'ffffffff-c95e-eae5-ffff-ffffce758366',
	'hangwz':'ffffffff-c43f-77d4-0000-00001b78f081',
	 'wangf':'ffffffff-c7a8-3bf6-ffff-ffffb8d6d318',
	'biany':'ffffffff-c28b-7966-0000-000049d75b84',
	'liuxuan':'ffffffff-f259-8a2f-0000-0000040de9c1',
	'wangzhenfang':'00000000-53a7-c4ef-ffff-fffffd609c24',
	'cuiyajie':'ffffffff-910d-998f-0000-0000585e3d7e'
	}
sensor_list=["magneticSensor","accelerometer","proximity"]


inst_id_zhangnn_ios='L2OGFhzaHM2IbNzJ1NjEHceroElYVdk2'
inst_id_chenyu_ios='yg80UzhxQFPPcwicTtU4lDTyP9IcqDs2'
inst_id_lb_ios='G93jbBRhtiWVGFULyLR9gPHDjUkl3S3R'
inst_id_zhangnn1_ios='GsjMrEReu1OC2wtkUpM5asbWEyJ5AdQ1'
 

#######################each class generate fea
c_list=['running','walking','riding','sitting','driving']
dataPath='/home/yr/magnetic_fea/data1027/' 
test_pack=11040#01234  #012 not sure walk   |mod<15 rid  | mod>=15 walkrun|but differ between people
para_pack=0#1with liangbin riding into trainset 
class_type=c_list[1]

###########query label.data
device=deviceId['wangzhenfang'] 
sensor=sensor_list[1]
##########query log.tracer
txt_i=2
see_flag=True
inst_id=inst_id_chenyu_ios
##########

def generate_stamp(period):
	#[8,28,8,33]->[(2015, 10, 20, 22, 30, 0, 0, 0, 0),(2015, 10, 20, 22, 48, 0, 0, 0, 0)]->stamp
	dur= [(2015, period[0], period[1], period[2], period[3], 0, 0, 0, 0),\
		(2015, period[4], period[5], period[6], period[7], 0, 0, 0, 0)]
	stamp_range0=[time2stamp(dur[0]),time2stamp(dur[1])]
	stamp_range=[t*1000 for t in stamp_range0]
	return stamp_range 

def time2stamp(t):
	#t = (2015, 9, 28, 12, 36, 38, 0, 0, 0)
	stamp = int(time.mktime( t )) ;
	return stamp
def connect_db_label():#label.data
	import leancloud,cPickle
	appid = "ckjjqzf3jqwl8k1u4o10j2hqp0rm0q6ferqcfb0xpw00e8zl"
	appkey = "rn0qw8ib96xl0km63kylo6v5afuxclc8jti5ol8rx4kylqob"
	leancloud.init(appid, appkey)

def connect_db_log():##sensor.log.tracer   not label.sensor, 
	import leancloud,cPickle
	appid = "9ra69chz8rbbl77mlplnl4l2pxyaclm612khhytztl8b1f9o"
	   
	appkey = "1zohz2ihxp9dhqamhfpeaer8nh1ewqd9uephe9ztvkka544b"
	#appid = "ckjjqzf3jqwl8k1u4o10j2hqp0rm0q6ferqcfb0xpw00e8zl"
	#appkey = "rn0qw8ib96xl0km63kylo6v5afuxclc8jti5ol8rx4kylqob"
	leancloud.init(appid, appkey)


 
 


#####################
def get_content(results):#result is from find() 
 	 
	obs={}; 
	r=results
	for i in range(1):
		#print type(r.get("events")) 
		if len(r.get("events"))>=1:
			 
			print r.get("motion"),r.get("events").__len__()
			ll=r.get("events") #ll=[ {},{}...]
			for dic in ll[:]:#dic={timestamp:xxxx,value:[1,2,3]...}
			
			#print dic["timestamp"],' ',dic["values"][0],' ',dic["values"][1],' ',dic["values"][2]
				if dic["timestamp"] not in obs.keys():
					obs[ dic["timestamp"] ]=[r.get("motion"),\
					dic["values"][0],dic["values"][1],dic["values"][2]  ]
				###data form: {timestamp:[obs],...}  [obs]=[motion,x,y,z]
		 
	###########################
	"""
	for k,v in obs.items():
		print k,' ',v
	"""
	print 'final',obs.__len__()

	

	#print 'i',i,count  #query-has-limit100,real-count=320
	###################3
	return obs 
	
	 


def get_all(query,skip,result):
	limit=500
	query.limit(limit)
	query.skip(skip)
	found=query.find()
	if found and len(found)>0:
		result.extend(found)
		print 'av_utils get all,now result len:',len(result),'skip',skip
		return get_all(query,skip+limit,result)
	else:
		return result
	


def save2pickle(c,name):
    write_file=open(dataPath+str(name),'wb')
    cPickle.dump(c,write_file,-1)#[ (timestamp,[motion,x,y,z]),...]
    write_file.close()
 
def load_pickle(path_i):
    f=open(path_i,'rb')
    data=cPickle.load(f)#[ [time,[xyz],y] ,[],[]...]
    f.close()
    #print data.__len__(),data[0]
    return data	


def see_record_num(period_label_dic):
	valid_num=0 
	####init
	connect_db_log()
	log = leancloud.Object.extend('Log')
	log_query = leancloud.Query(log)
	#print 'all',log_query.count()##error
	inst_query = leancloud.Query(leancloud.Installation)
	#print 'install',inst_query.count()#2335
	inst = inst_query.equal_to('objectId', inst_id).find();#print '1',inst[0]
	#
	
	
	 
	
	 
	for label,periods in period_label_dic.items():
	
		for period in periods:
			stamp_range=generate_stamp(period)
	 		#################each period
			log_query.equal_to('installation', inst[0]).equal_to("type",'sensor').\
			less_than("timestamp", stamp_range[1]).greater_than("timestamp",stamp_range[0])
			print label,period,'count',log_query.count()
                        if log_query.count()>0:valid_num+=log_query.count()

        print 'total valid count',valid_num
                        


def remove_punct(line):	
	for punct in ['.','-',':','/','\\']:
		if punct in line:line=line.replace(punct,' ')
	return line
	
	

############3
if __name__=="__main__":
	txt_path='/home/yr/magnetic_fea/txt_1123/'
	period_label={};
	for filename in os.listdir(txt_path)[txt_i:txt_i+1]:
		print 'file '+filename
		inpath=txt_path+filename
		content=open(inpath,'r')
		line=content.readline().strip('\n').strip('\r').strip(' ')
		#period=[0,0,0,0,0,0,0,0]#month day minu sec ....
		while line:
			line=remove_punct(line)
			line=line.split(' ');print line
			
			period=[int(line[0]),int(line[1]),int(line[2]),int(line[3]),\
				int(line[0]),int(line[1]),int(line[4]),int(line[5])]
			 
			label=line[-1]
			if label not in period_label:
				period_label[label]=[period]
			elif label in period_label:
				period_label[label].append(period)
			#####next
			line=content.readline().strip('\n').strip('\r').strip(' ')
		###################
		for k,v in period_label.items():#{label:[period,p,...],label:{}...
			print k,v.__len__()
	#########see valid record
	if see_flag==True : see_record_num(period_label)
	elif see_flag==False:print 'file '+filename	
			
			
		

	
	

 	 
		
    
 
	
		
	
   		 



