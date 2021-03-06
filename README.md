
![DroneQuest Tests](https://api.travis-ci.org/DroneQuest/drone-quest.svg "Tests are passing! ... right?")

# DroneQuest

### What is DroneQuest?
DroneQuest is a collaborative project between students of Codefellows JavaScript 401 and Python 401 classes.
The Python portion of this project allows users to connect any controller they want to an API endpoint and send commands to an [AR Parrot Drone](http://www.parrot.com/usa/products/ardrone-2/).
The Javascript portion is an interactive locally hosted web page, allowing the user to control the drone and see feedback from it.
### [How do I use DroneQuest?](https://github.com/DroneQuest/drone-quest/wiki)
=======
## Core Features:
- Create a python-based API that will communicate with a front-end server
- Send useful drone information to a front-end user interface
- Create a module that anyone with a drone can pip install, then use to control their personal drone
	
## Stretch Goals:
- Connect a Leap Motion Controller to control the drone
- Send commands via the front-end web application we have created
- Use VR goggles that will connect to the drone cameras 
>>>>>>> master

Dependencies:
- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [Bottle](http://bottlepy.org/docs/dev/index.html)
- [numpy](http://www.numpy.org/)

Linux/Mac OS:
```
you@dronequest:~ $ git clone https://github.com/DroneQuest/drone-quest.git
you@dronequest:~ $ cd drone-quest
you@dronequest:~ $ python setup.py install
you@dronequest:~ $ droneserve
```

Windows Systems:
```
C:\Users\you> git clone https://github.com/DroneQuest/drone-quest.git
C:\Users\you> cd drone-quest
C:\Users\you> python setup.py install
C:\Users\you> droneserve
```

Point an http post request to [127.0.0.1:3000/do/&lt;command&gt;](http://127.0.0.1:3000/do/takeoff) to instruct the drone.
Check out our [API Endpoints Wiki Page](https://github.com/DroneQuest/drone-quest/wiki/API-Endpoints) for a list of commands.


### How did you accomplish this project?
We used Bastian Venthur's [Useful Github Repo](https://github.com/venthur/python-ardrone), which was later
improved by [Jonathan Hunt](https://github.com/jjh42/python-ardrone) and [Adrian Taylor](https://github.com/adetaylor/python-ardrone).

In addition, a very useful tutorial can be found [here](http://www.playsheep.de/drone/).

This project was built with
- Luc Ho (JavaScript)
- Kevin Sulonen (JavaScript)
- Norton Pengra (Python)
- Will Weatherford (Python)
- Munir Ibrahim (Python)

### Testing
This software was tested with the following setups:

  * Python 2.6.6
  * Python 2.7.6 (better setup)
  * Python 3.5 (only Leap Motion API is incompatible)
  * Psyco 1.6 (recommended)
  * Pygame 1.8.1 (only for the demo)
  * Unmodified AR.Drone firmware 1.5.1
  * Unmodified AR.Drone firmware 2.0


### License
This software is published under the terms of the MIT License:

  http://www.opensource.org/licenses/mit-license.php
