# -*- coding: iso-8859-1 -*-
import sys, os
# the action below is a no-no in standard python, but it is done here for
# easy on-the-fly testing.

# this setup assumes that MARDS is NOT in the python library on the local
# machine, but is instead in a parrallel directory.
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..'))
#print sys.path
import MARDS

doc = '''
#!MARDS_en_1.0

blink "zippy_b.oing"
    rate 23
    abc beep beep 
        joex 44ft
        joey zed
        joeBxx 5 inches
item "broom"
    size 33
    color blue
        intensity 33%
        intensity 2
item "brush"
    size 2
zed 1.234e+2
    bob 55
'''

schema_file = "temp/simple.MARDS-schema"
with open(schema_file, "r") as fh:
    schema = fh.read()
    schema_dir = os.path.dirname(os.path.realpath(schema_file))
x,e = MARDS.ml.SCHEMA_to_rolne(doc=schema, schema_dir=schema_dir)

# x,e = MARDS.string_to_rolne(doc, schema_file="temp/simple.MARDS-schema")
#x,e = MARDS.string_to_rolne(doc)
#x,e = MARDS.compile(x, schema_file="temp/simple.MARDS-schema", renumber=True)

print "FINAL:\n"
print x._explicit()
print "ERRORS:\n"
print repr(e)
