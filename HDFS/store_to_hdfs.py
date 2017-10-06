import json, os, time
from confluent_kafka import Consumer, KafkaError


class Consumer_HDFS(object):
	
	def __init__(self,conf,addr,topic,group):
		
		print 'Initiated a kafka consumer for HDFS...'
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
				self.flush_to_hdfs(output_dir)
			elif message.error() !=KafkaError._PARTITION_EOF:
				print(message.error())
				running = False

		#for ii in range(0,2):
		#	try:
				#########################3
				###messages=self.consumer.get_messages(count=1000, block=False)
		#		messages=self.consumer.poll(timeout=3.0)

		#	print messages
			#	for message in messages:
			#		self.temp_file.write(message.message.value + "\n")

			#	if self.temp_file.tell() > 20000000:
			#		self.flush_to_hdfs(output_dir)
			
			#	self.consumer.commit()

			#except:
			#	self.consumer.seek(0,2)
		


	def flush_to_hdfs(self, output_dir):

		print 'testing flush to hdfs function...'
		self.temp_file.close()
		timestamp = time.strftime('%Y%m%d%H%M%S')
	
		hadoop_fullpath="%s/%s_%s_%s.dat" %(self.hadoop_path, 
					self.group, self.topic, timestamp)

		#print "Block {}:Flushing 20MB file to HDFS => {}".format(str(self.block_cnt),hadoop_fullpath)

		self.block_cnt += 1
		
		print("hdfs dfs -put %s hdfs:%s" %(self.temp_file_path,
								output_dir))
		os.system("hdfs dfs -put %s hdfs:%s" %(self.temp_file_path,
								output_dir))
		
		##################################
		# os.remove(self.temp_file_path)
		
		# timestamp = time.strftime('%Y%m%d%H%M%S')

		#self.temp_file_path="%s/kafka_%s_%s_%s.dat" % (output_dir,
		#					self.topic,
		#					self.group,
		#					timestamp)

		#self.temp_file=open(self.temp_file_path, "w")


def main():

	print "\nTesting HDFS consumer..."
	
	conf={'bootstrap.servers':'ec2-35-166-130-18.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-35-160-85-146.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-34-214-129-134.us-west-2.compute.amazonaws.com:9092','group.id':'my_group'}
	kafka_brokers={'bootstrap.servers':'ec2-35-166-130-18.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-35-160-85-146.us-west-2.compute.amazonaws.com:9092','bootstrap.servers':'ec2-34-214-129-134.us-west-2.compute.amazonaws.com:9092'}
	parking_meters='parking_meter_topic'
        group='my_group'


	cons=Consumer_HDFS(conf,kafka_brokers,parking_meters,group)
	cons.consume_topic("/home/ubuntu/py-kafka-hdfs")

if __name__=='__main__':

	main()

	#cons_gps=Consumer_HDFS(kafka_brokers,group='my-group', topic='user-gps-topic')
	#cons_gps.consume_topic("/home/ubuntu/py-kafka-hdfs/")
	#cons_gps.flush_to_hdfs("/user_gps/")
