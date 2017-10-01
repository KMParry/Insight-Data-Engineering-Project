import redis, operator


def main():

	with open('input.txt') as file_in:
		data=file_in.read().strip('\n')
	lng,lat=data.split(',')

	meters={}
	states={}
	
	temp=redis.StrictRedis(host="localhost",port=6379,db=0)
	temp.geoadd("sanfran",float(lng),float(lat),"tmp")
	
	#get meters within the given radius
	rlocs=redis.StrictRedis(host="localhost",port=6379,db=0)
	meters=rlocs.georadiusbymember("sanfran", "tmp",100,"mi")

	#get the states of the returned meters
	rstates=redis.StrictRedis(host="localhost",port=6379,db=0)
	states=rstates.get(meters)

	met_str=[]
	pos=redis.StrictRedis(host="localhost",port=6379,db=0)
	for ii in meters:
		locs=pos.geopos("sanfran", ii)
		met_str.append(locs)	
	
	met_str_new=reduce(operator.concat, met_str)
		
	file_out=open("output.txt","w")
	file_out.write(str(met_str_new))	


if __name__=="__main__":
	main()
