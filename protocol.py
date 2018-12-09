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


# Not implemented in the server yet...
class PROTOCOL():
    ## ACTIONS
    CONNECT = "!1"
    DISCONNECT = "!2"
    IDLE = "!3"
    PSH = "!4"
    RST = "!5"

    ## STATUS
    ACK = "?1"
    DENY = "?2"
    IGN = "?3"
    ERR = "?4"

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
    print PROTOCOL().CONVERT("!1")
    print PROTOCOL().CONVERT("!2")
    print PROTOCOL().CONVERT("!3")
    print PROTOCOL().CONVERT("!4")
    print PROTOCOL().CONVERT("!5")
    print "\n"
    print PROTOCOL().CONVERT("?1")
    print PROTOCOL().CONVERT("?2")
    print PROTOCOL().CONVERT("?3")
    print PROTOCOL().CONVERT("?4")
    print "\n"
    print PROTOCOL().CONNECT
    print PROTOCOL().DISCONNECT
    print PROTOCOL().IDLE
    print PROTOCOL().PSH
    print PROTOCOL().RST
    print "\n"
    print PROTOCOL().ACK
    print PROTOCOL().DENY
    print PROTOCOL().IGN
    print PROTOCOL().ERR
