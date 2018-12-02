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
    ## ACTIONS
    CONNECT 	= "!1"
    DISCONNECT = "!2"
    IDLE 		= "!3"
    PSH 		= "!4"
    RST 		= "!5"

    ## STATUS
    ACK 	= "?1"
    DENY 	= "?2"
    IGN 	= "?3"
    ERR 	= "?4"
    
    @staticmethod
    def CONVERT(cmd):
        if cmd[0] == '!':  # COMMAND
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
        elif cmd[0] == '?':  # STATUS
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

########################
#!# Run Main Program #!#
########################

if __name__ == "__main__":

	print Protocol().CONVERT("!1")
	print Protocol().CONVERT("!2")
	print Protocol().CONVERT("!3")
	print Protocol().CONVERT("!4")
	print Protocol().CONVERT("!5")
	print "\n"
	print Protocol().CONVERT("?1")
	print Protocol().CONVERT("?2")
	print Protocol().CONVERT("?3")
	print Protocol().CONVERT("?4")
	print "\n"
	print Protocol().CONNECT
	print Protocol().DISCONNECT
	print Protocol().IDLE
	print Protocol().PSH
	print Protocol().RST
	print "\r"
	print Protocol().ACK
	print Protocol().DENY
	print Protocol().IGN
	print Protocol().ERR

