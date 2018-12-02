# The Door
The Door is a __Raspberry Pi__ based project mainly developed in __Python__.

The core function of this project is to control the access of my building front door from a simple client application on my phone.

To do so, I've elaborated a __Python__ server interacting in between a client appication and a servo motor connected to the Raspberry PI.

The server, acting as clients/requests handler, is listening on my local nework and wait for a any connection request from potential clients.

When a connection is established, the server now wait for commands from the client and check if the commands are as expected and if the client can do it at the moment. If there is nothing wrong, the server execute  it safely . 

The server job is also to make sure the motor is always put back into idle position when a client leave or when an unexpected event happen. This is an important part, because at the end it's my building front door that can be compromise here.

The servo motor role is to control the access to my building front door by simply pressing or not pressing the little button on my wall originally made for this task. To control the motor I've created a __Python__ class that does the job pretty well using the __RPi.GPIO__ lib.