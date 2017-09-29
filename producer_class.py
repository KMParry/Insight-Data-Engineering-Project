import json, os, time,random
from confluent_kafka import Producer

class Producer_Custom(object):


	def __init__(self, addr,group,topic):
	
		print 'Initiatied kafka producer ...'
		
		self.address=addr
		self.topic=topic
		self.group=group
		self.producer=Producer(self.address)
		
	def produce_topic(self,datafile):
	
		#timestamp=time.strftime('%Y%m%d%H%M%S')
		#print timestamp
		print 'testing'
		self.producer.produce(self.topic,datafile)
		self.producer.flush()

	#	print('testing print function..., at%s' %(timestamp))

def main():
	
	kafka_brokers={'bootstrap.servers':'ec2-35-166-130-18.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-35-160-85-146.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-34-214-129-134.us-west-2.compute.amazonaws.com:9092'}

	parking_meters='parking_meter_topic'
	group='my_group'

	p=Producer_Custom(kafka_brokers,group,parking_meters)
	
	for ii in range(1,10):
		p.produce_topic("../data/pID_data.json")

if __name__=="__main__":

	main()
