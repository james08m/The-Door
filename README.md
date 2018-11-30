# The Door
The Door is a Raspberry Pi based project mainly developped in python. 
The core function of this project is to control the access of my building front door.
A python server act as a clients and requests handler listening on the local network
for any connections requests from a client application. After a connection established,
the server manage the access between any clients and the servo motor connected to the
Raspbery Pi. This motor, interfaced with a custom python class, control le the access
to the building front door by pressing or not a button on my wall.
