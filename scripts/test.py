#!/usr/bin/python

print "Content-type: application/json\n\n"

import operations

operations.init("information.shelve")

print operations.convert_json()

operations.close()
