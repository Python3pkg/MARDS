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
    abc
        joex 44
item "broom"
    size 33
    color blue
        intensity 33%
item "brush"
    size 2
zed 1.234e+2
'''

schema = '''
#!MARDS_schema_en_1.0 blah

##    import sub
##        local "sub.MARDS-schema"

name blink
    value
        type label
        required
    name rate
    insert abc
template abc
    name joex
        required
    name joey
name zed
    value
        type float
name item
    treatment unique
    value
        type label
        required
    name size
        treatment one
    name color
        treatment unique
        name intensity
    name title
        required
        treatment concat
        value
            default "unknown"
'''

#x,e = MARDS.ml._SCHEMA_to_rolne(MARDS.ml.standard_types)
x,e = MARDS.string_to_rolne(doc, schema)
print "FINAL:\n"
print x._explicit()
print "ERRORS:\n"
print repr(e)
