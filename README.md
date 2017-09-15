# Insight-Data-Engineering-Project

Parking meter reservation system for San Francisco; using availability sensors integrated into the currently existing parking 
meters in the city.

The idea is to develop a mobile application in which a user could search a location where they would like to find parking.
The application would then query a database of parking meters in the vicinity of the location (within a certain radius, 
let's say 0.5 mi) and return the number of available and unavailable parking meters within the radius. 

As the user approaches the location, and is within a certain radius (e.g. 1 mi), the user may then reserve the meter for a 
premium price (for example 3x the price of the meter, or flat rate $5) for 5 minutes.  The reservation would then trigger an 
indicator on the meter that would indicate it is unavailable for use and is no longer registered as available on the app. 

When the user approaches the meter, they can then continue the transaction into a parking transaction at the given parking 
meter rate. This would limit the case in which a user tries to cheat the system by claiming they are parking in the spot 
via the application, without paying the more expensive reservation price. Also, the higher price for reserving the spot
discourages people from reserving a spot and then parking elsewhere. 


Interface:

1.) Would be a mobile app; when user pulls up the application, they should be able to drop a pin on a map, or enter a 
 destination location. The application should display the available and unavailable parking meters in the region of 
 the destination location.
 - parking events don't need to be continuously streaming; only when a spot becomes reserved, occupied, or unoccupied.  
 
 2.) If the user is within a certain radius of the meter, they should be able to reserve the meter by one click. They 
 should be able to select the "closest meter" or the "cheapest rate" and select it.
  - The app will be receiving streaming data from the user as they travel toward the parking meter location. (1 events/sec?).
    How many users to simulate?
    - This needs to be an atomic process. The meter should immediately become "reserved" instead of "available" and block
    other users from seeing the meter as available.
 
 3.) 
 
 

