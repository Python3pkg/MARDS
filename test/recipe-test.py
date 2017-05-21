import sys, os
# the action below is a no-no in standard python, but it is done here for
# easy on-the-fly testing.

# this setup assumes that MARDS is NOT in the python library on the local
# machine, but is instead in a parrallel directory.
sys.path.append(os.path.join(os.path.dirname(sys.argv[0]), '..'))
#print sys.path
import MARDS



with open("Bling.MARDS", 'r') as docfile:
    doc = docfile.read()
with open("mr recipe.MARDS-schema", 'r') as schemafile:
    schema = schemafile.read()

#x,e = MARDS.ml._SCHEMA_to_rolne(schema)
x,e = MARDS.string_to_rolne(doc, schema)
print("FINAL:\n")
print(x._explicit())
print("ERRORS:\n")
print(repr(e))
