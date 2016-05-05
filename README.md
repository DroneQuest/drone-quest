
![DroneQuest Tests](https://api.travis-ci.org/DroneQuest/drone-quest.svg "Tests are passing! ... right?")


# DroneQuest

### What is DroneQuest?
DroneQuest is a collaborative project between students of Codefellows JavaScript 401 and Python 401 classes.
The Python portion of this project allows users to connect any controller they want to an API endpoint and send commands to an
[AR Parrot Drone](http://www.parrot.com/usa/products/ardrone-2/).

### How do I use DroneQuest?

Dependencies:
- [Python 2.7](https://www.python.org/download/releases/2.7/)
- [Bottlepy](http://bottlepy.org/docs/dev/index.html)
- [numpy](http://www.numpy.org/)

Unix Systems:
```
you@dronequest:~ $ git clone https://github.com/DroneQuest/drone-quest.git
you@dronequest:~ $ cd drone-quest
you@dronequest:~ $ python setup.py install
you@dronequest:~ $ ./runapp.sh
```

Windows Systems:
```
C:\Users\you> git clone https://github.com/DroneQuest/drone-quest.git
C:\Users\you> cd drone-quest
C:\Users\you> python setup.py install
C:\Users\you> runapp.bat
```

Point an http post request to [127.0.0.1:3000/do/<command>](http://127.0.0.1:3000/do/takeoff) to instruct the drone.

### Cool, what are your API endpoints?
Check out our [API Endpoints Wiki Page](https://github.com/DroneQuest/drone-quest/wiki/API-Endpoints)


### How did you accomplish this project?
We used Bastian Venthur's [Useful Github Repo](https://github.com/venthur/python-ardrone), which was later
improved by [Jonathan Hunt](https://github.com/jjh42/python-ardrone).

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
  * Psyco 1.6 (recommended)
  * Pygame 1.8.1 (only for the demo)
  * Unmodified AR.Drone firmware 1.5.1

  * Python 2.7.6 (better setup)
  * Unmodified AR.Drone firmware 2.0

### License
This software is published under the terms of the MIT License:

  http://www.opensource.org/licenses/mit-license.php
