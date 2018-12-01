#! /usr/bin/env/ python

###########################
#!#  Protocol : actions #!#
###########################
## CONNECT		!1
## DISCONNECT	!2
## IDLE			!3
## PSH			!4
## RST			!5

###########################
#!#  Protocol : status  #!#
###########################
## ACK	?1
## DENY	?2
## IGN	?3
## ERR	?4

###########################
#!#  Protocol : exemple #!#
###########################
## Client > !1 	(Client connect request)
## Server > !1?1	(Server acknowledge client request)



class Protocol():

	def __init__(self):
	
		## ACTIONS
		self.CONNECT 	= "!1"
		self.DISCONNECT = "!2"
		self.IDLE 		= "!3"
		self.PSH 		= "!4"
		self.RST 		= "!5"
		
		## STATUS
		self.ACK	= "?1"
		self.DENY 	= "?2"
		self.IGN 	= "?3"
		self.ERR 	= "?4"
		
	def toString(self, cmd):
		if cmd[0] == '!': ## COMMAND
			if cmd[1] == '1':
				return "CONNECT"
			elif cmd[1] == '2':
				return "DISCONNECT"
			elif cmd[1] == '3':
				return "IDLE"
			elif cmd[1] == '4':
				return "PSH"
			elif cmd[1] == '5':
				return "RST"
			else:
				return "0"
		elif cmd[0] == '?': ## STATUS
			if cmd[1] == '1':
				return "ACK"
			elif cmd[1] == '2':
				return "DENY"
			elif cmd[1] == '3':
				return "IGN"
			elif cmd[1] == '4':
				return "ERR"
			else:
				return "0"			
		else:
			return "0"
	