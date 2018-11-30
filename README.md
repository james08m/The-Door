# The Door
The Door is a Raspberry Pi based project mainly developped in python. 
The core function of this project is to control the access of my building front door.
A python server, acting as clients/requests handler, is listening on the local network
for connections request from a client application. When a connection is established with
a new client, the server manage the access between clients and a servo motor connected
to a Raspbery Pi. This servo motor, interfaced with a custom python class of mine, control
the access to my building front door by pressing or not the little button on my wall
originally made dor this task.
