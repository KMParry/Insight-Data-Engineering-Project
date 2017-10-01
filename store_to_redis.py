import json, os, random,time
from confluent_kafka import Consumer, KafkaError
import redis

class Consumer_redis(object):
	
	def __init__(self,conf,addr,topic,group):
		
		print 'Initiated a kafka consumer for REDIS...'
		self.conf=conf
		self.address=addr	
		self.topic=topic
		self.group=group
		self.consumer=Consumer(conf)
		self.consumer.subscribe([topic])

		self.temp_file_path=None
		self.temp_file = None
		self.block_cnt=0
		self.hadoop_path="/home/ubuntu"

	def consume_topic(self,output_dir):
		
		timestamp=time.strftime('%Y%m%d%H%M%S')
	
		self.temp_file_path="%s/kafka_%s_%s_%s.dat" % (output_dir,
								self.topic,
								self.group,
								timestamp)
		print self.temp_file_path

		self.temp_file=open(self.temp_file_path,"w")
	
		running = True

		while running:
			message = self.consumer.poll()
			if not message.error():
				print ('Received message %s' % (message.value().decode('utf-8')))
				self.store_to_redis(output_dir)
			elif message.error() !=KafkaError._PARTITION_EOF:
				print(message.error())
				running = False

		
	def store_to_redis(self,output_dir):
		
		print 'testing store_to_redis function'

		r=redis.StrictRedis(host="localhost",port=6379,db=0)
		lon=random.uniform(-121.0, -120.0)
		lat=random.uniform(37.0, 38.0)
		pid=str(random.randint(1,100))
		print 'pid is %s'%pid		

		r.geoadd("sanfran", lon,lat,pid)

		r.set(pid,0)



	#def flush_to_hdfs(self, output_dir):

	#	print 'testing flush to hdfs function...'
	#	self.temp_file.close()
	#	timestamp = time.strftime('%Y%m%d%H%M%S')
	
	#	hadoop_fullpath="%s/%s_%s_%s.dat" %(self.hadoop_path, 
		#			self.group, self.topic, timestamp)


	#	self.block_cnt += 1
		
	#	print("hdfs dfs -put %s hdfs:%s" %(self.temp_file_path,
		#						output_dir))
	#	os.system("hdfs dfs -put %s hdfs:%s" %(self.temp_file_path,
	#							output_dir))
		
		##################################
		# os.remove(self.temp_file_path)
		
		# timestamp = time.strftime('%Y%m%d%H%M%S')

		#self.temp_file_path="%s/kafka_%s_%s_%s.dat" % (output_dir,
		#					self.topic,
		#					self.group,
		#					timestamp)

		#self.temp_file=open(self.temp_file_path, "w")



def main():

	print "\nTesting redis consumer..."
	
	conf={'bootstrap.servers':'ec2-35-166-130-18.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-35-160-85-146.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-34-214-129-134.us-west-2.compute.amazonaws.com:9092','group.id':'my_group'}
	kafka_brokers={'bootstrap.servers':'ec2-35-166-130-18.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-35-160-85-146.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-34-214-129-134.us-west-2.compute.amazonaws.com:9092'}
	parking_meters='parking_meter_topic'
        group='my_group'


	cons=Consumer_redis(conf,kafka_brokers,parking_meters,group)
	cons.consume_topic("/home/ubuntu")

	#cons.get_in_rad("3",0.5)
if __name__=='__main__':

	main()
 
