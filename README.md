# Insight-Data-Engineering-Project

Parking meter reservation system for San Francisco; using availability sensors integrated into the currently existing parking 
meters in the city.

The idea is to develop a mobile application in which a user could search a location where they would like to find parking.
The application would then query a database of parking meters in the vicinity of the location (within a radius of 0.25 mi) 
and return the number of available and unavailable parking meters within the radius. 

As the user approaches the location, and is within a certain radius (0.5 mi), the user may then reserve the meter for a 
premium price (for example 3x the price of the meter, or flat rate $5) for 5 minutes.  The reservation would then trigger an 
indicator on the meter that would indicate it is unavailable for use and is no longer registered as available on the app. 

When the user approaches the meter, they can then continue the transaction into a parking transaction at the given parking 
meter rate. This would limit the case in which a user tries to cheat the system by claiming they are parking in the spot 
via the application, without paying the more expensive reservation price. Also, the higher price for reserving the spot
discourages people from reserving a spot and then parking elsewhere. 

Technologies:


Kafka:
Produce data using Kafka; One producer node streaming the user GPS data
3 Kafka Brokers to act as the message queue
Consumers on HDFS and Redis nodes

HDFS:
Acts as source of truth
Stores all parking meter data

Redis:
Database to query the nearby parking meter locations
Returns available parking meters
Allows for expiration of key



Directory Structure


src
|
|--kafka_consumer
|     |
|     |-kafka_consumer.py
|     
|--kafka_producer
|     |
|     |-kafka_producer.py **
|     
|--HDFS
|     |
|     |-kafka_to_hdfs.py *******
| 
|
|--redis
|
|
|--data
|    |
|    |--taxis
|    |
|    |--user_gps
|    |
|    |--reservation
|
|--frontend


