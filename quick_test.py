import MARDS


schema = '''
#!MARDS_schema_en_1.0 blah
    import sub
        local "test/sub.MARDS-schema"

ordered False
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
        extend xx
name zoom_flag
    treatment one
    value
        required
        default True
    name color
name boing
    required
    value
        required
        default joejoe
    recurse boing
        limit 3
name code_seq
    value
        ordered False
    ordered False
    treatment sum
    name *
name system_title
'''

#print my_doc
#print schema
x,e = MARDS._SCHEMA_to_rolne(schema)
#x,e = MARDS_to_rolne(my_doc, schema, tab_strict=True)
#y,e = MARDS_to_rolne(my_doc, schema, tab_strict=True)
#x,e = MARDS_to_python(my_doc, schema)
#for ctr, line in enumerate(my_doc.split("\n")):
#    print ctr, line
print "FINAL:\n"
print x._explicit()
print "ERRORS:\n"
print repr(e)
