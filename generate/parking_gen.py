import json, threading, time, requests, random, csv, os

# from kafka import Producer

class parking(object):
	
	def __init__(self):
		self.lat=""
		self.long=""
		self.pID=""

	def __repr__(self):
		return str(self)

listdat=[]

def return_random_state():
	rand=random.randint(1,10000)
	rand=rand%2
	
	if rand==0:
		state=-1
	if rand==1: 
		state=1

	return state



def make_initial_data():

	with open('../data/parking_data.json') as data_file:
		data = json.load(data_file)
	#	print data[u'san_francisco'].keys()
		garages=data[u'san_francisco'][u'garages'].keys()
	
		print garages		

random_locs=[]
files=[]
def make_initial_spots():


	path='../data/taxicab/'
	files=os.listdir('../data/taxicab/')

	pid=0
	for fs in files:
		
		filepath=path+fs 
		with open(filepath,"r") as f:
			
			data=f.readlines()
			
			ran=random.randint(45,50)
			count=random.randint(1,10)
			for line in data:
				count+=1
				
				if count%ran==0 and pid <1000:

					pid+=1	
				
					words=line.split()
					loc={}
					loc['lon']=words[0]	
					loc['lat']=words[1]
					loc['pID']=str(pid)	
					loc['state']=str(return_random_state())

					random_locs.append(loc)
				

	with open('../data/pID_data.json','wb') as pout:
		json.dump(random_locs,pout)
	pout.close	


def random_time_parking_data():
	
	line={}
	newdata=[]
	
	with open('../data/pID_data.json','r') as pID_in:
		data=json.load(pID_in)


		for ii in range(1,1000000):
		
			index=random.randint(1,999)
			state=data[index][u'state'].encode('utf-8')
		

			if state=="1":
				newstate=str(-1).decode('utf-8')
				data[index][u'state']=newstate
				newdata.append(data[index])
			if state=="-1":
				newstate=str(1).decode('utf-8')
				data[index][u'state']=newstate
				line=data[index]
				newdata.append(data[index])
		

		with open("file_out.txt","w") as output:
			output.write(str(newdata))



def main():
	make_initial_spots()

	random_time_parking_data()

if __name__=="__main__":
	
	main()
