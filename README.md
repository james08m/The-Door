# The Door __[PAUSED/FINISHED]__

The Door is a __Raspberry Pi__ based project mainly developed in __Python__.

The goal of this project was to control the access of my building front door from a simple client application on my phone. To do so, I have create a __Python__ server where a client connect to and interact with a servo motor connected to a __Raspberry PI__ that have the ability to push my building front door buzzer. The server jon have the hard task to coordinate every actions between clients and the motor. Basically, it is listening on my local network on a specific port and  it waits for a any connection request from potential clients. When a connection is established, the server wait for commands from this client, check if those commands are as expected and if the client can perform the required action at this moment. If there is nothing wrong with the command received and the servo motor is not already in use, the server execute the task safely and wait for another command. 

Another import task of the server is also to make sure the motor is always put back to idle position when a client quit or when an unexpected event is happening. This is an important part, because at the end it's my building front door that can be compromise here and I don't want to be responsible of any security breahes or simply bothering my whole neighborhood with the buzzer noise when we unlock the door. 

The servo motor, in this project have a very important role in this project, it is controlling the access of my building front door by simply pressing or not pressing the little button on my wall originally made for this purpose. To control the motor I've created a __Python__ class that does the job pretty well using the __RPi.GPIO__ lib.


![alt text](https://raw.githubusercontent.com/james08m/The-Door/master/the-door.PNG)
