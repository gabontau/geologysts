#!/usr/bin/env python

import sys
from omniORB import CORBA, PortableServer

import _GlobalIDL, _GlobalIDL__POA

class Echo_i (_GlobalIDL__POA.Echo):
    def echoString(self, mesg):
        print "Client called with message:", mesg
        return mesg

orb = CORBA.ORB_init(sys.argv, CORBA.ORB_ID)

poa = orb.resolve_initial_references("RootPOA")

ei = Echo_i()

eo = ei._this()

with open("D:\ior.txt","w") as f:
    f.write(orb.object_to_string(eo))

#print orb.object_to_string(eo)

poaManager = poa._get_the_POAManager()
poaManager.activate()

orb.run()
