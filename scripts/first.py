#!/usr/bin/python

import json
import urllib
import datetime
from time import sleep

print "Content-type:application/json\n"

x = {"txt":"hello", "booll":"yes"}
h = json.dumps(x)
print h