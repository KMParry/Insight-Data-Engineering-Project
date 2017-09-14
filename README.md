# Insight-Data-Engineering-Project

Parking meter reservation system for San Francisco; using availability sensors integrated into the currently existing parking 
meters in the city.

The idea is to develop a mobile application in which a user could search a location where they would like to find parking.
The application would then query a database of parking meters in the vicinity of the location (within a certain radius, 
let's say 0.5 mi) and return the number of available and unavailable parking meters within the radius. 

As the user approaches the location, and is within a certain radius (e.g. 1 mi), the user may then reserve the meter for a 
premium price (for example 3x the price of the meter, or flat rate $5) for 5 minutes.  The reservation would then trigger an 
indicator on meter that would indicate it is unavailable for use and is no longer registered as available on the app. 

When the user approaches the meter, they can then continue the transaction into a parking transaction at the given parking 
meter rate. This would limit the case in which a user tries to cheat the system by claiming they are parking in the spot 
via the application, without paying the more expensive reservation price. Also, the higher price for reserving the spot
discourages people from reserving a spot and then parking elsewhere. 

