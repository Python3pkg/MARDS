# MARDS\__init__.py
#
# MARDS data serialization library
#
# Version 0.1.0

from rolne import rolne

import mards_library as ml

def string_to_rolne(doc=None, schema=None, context="doc", tab_strict=False):
    result = rolne()
    error_list = []
    if doc is None:
        return result, error_list
    if schema:
        schema, schema_errors = string_to_rolne(schema, context="schema")
        error_list.extend(schema_errors)
    current = 0
    tab_list = [0]
    pointer_list = range(50)
    pointer_list[0]=result
    last_spot = pointer_list[0]
    line_tracker = []
    last_nvi = range(50)
    for ctr, line in enumerate(doc.split("\n")):
        line_tracker.append([])
        (indent, key, value, error) = ml.parse_line(line, tab_list, tab_strict=tab_strict)
        if error:
            t = (context, ctr, error)
            error_list.append(t)
        else:
            if key:
                if indent<current:
                    current = indent
                elif indent==current:
                    pass # do nothing, the operational default works
                elif indent==(current+1):
                    pointer_list[indent] = last_spot
                    current = indent
                else:
                    t = (context, ctr, "tab stop jumped ahead too far")
                    error_list.append(t)
                index = pointer_list[indent].append_index(key, value)
                last_spot = pointer_list[indent][key, value, index]
                last_nvi[indent]=(key, value, index)
                for r in range(indent+1):
                    line_tracker[ctr].append(last_nvi[r])
    if schema:
        result, schema_errors = schema_rolne_check(result, schema, line_tracker)
        error_list.extend(schema_errors)
    return result, error_list

def schema_rolne_check(doc, schema, line_keys):
    # TODO: move to library
    #the line_key list a (name, value, index) tuple in the original source text
    #
    # PASS ONE: FORWARD CHECK OF DOC
    #
    error_list = []
    for ctr, tuple_list in enumerate(line_keys):
        indent = len(tuple_list) - 1
        if indent<0: # this can happen on an empty line or a comment line
            continue
        pointer = schema
        for tup in tuple_list:
            name, value, index = tup
            if ("name", name) in pointer.get_tuples():
                pointer = pointer["name", name]
            else:
                error_list.append( ("doc", ctr, "a name of '{}' not found in schema context".format(name)) )
                continue
    #
    # PASS TWO: REQUIREMENTS CHECK OF SCHEMA
    #
    el = sub_schema_requirements(doc, schema, line_keys)
    error_list.extend(el)
    #
    # PASS THREE: TREATMENT CHECKS
    #
    el = sub_schema_treatments(doc, schema, line_keys)
    error_list.extend(el)
    return doc, error_list

def sub_schema_treatments(doc, schema, line_keys):
    error_list = []
    for target in schema.get_list("name"):
        pointer = schema["name", target]
        treatment = pointer.value("treatment")
        if not treatment:
            treatment = "list"
        if treatment=="list":
            pass # there are no checks needed for list
        elif treatment=="unique":
            value_list = doc.get_list(target)
            short_list = set(value_list)
            if not len(short_list)==len(value_list):
                ctr = {}
                for value in short_list:
                    ctr[value] = 0
                for value in value_list:
                    ctr[value] += 1
                for value in ctr:
                    for i in range(ctr[value]):
                        key_list = [(target, value, i)]
                        line_number = find_rolne_line(line_keys, key_list)
                        if i==0:
                            first_line = line_number
                        else:
                            error_list.append( ("doc", line_number, "'{}' entries should be unique, but this line is a duplicate of line {}.".format(target,str(first_line))) )
        elif treatment=="sum":
            pass
        elif treatment=="average":
            pass
        elif treatment=="one":
            value_list = doc.keys(target)
            if len(value_list)>1:
                key_list = [value_list[0]]
                first_line = find_rolne_line(line_keys, key_list)
                print "jj",key_list
                del value_list[0]
                for tup in value_list:
                    key_list = [tup]
                    line_number = find_rolne_line(line_keys, key_list)
                    error_list.append( ("doc", line_number, "only one '{}' entry should exist, but this line is in addition to line {}.".format(target,str(first_line))) )
        else:
            pass
        # check subs
        #for sub in doc.get_list(target):
        #    el = sub_schema_requirements(doc[target,sub],pointer,line_keys)
        #    error_list.extend(el)
    return error_list

def sub_schema_requirements(doc, schema, line_keys):
    error_list = []
    for target in schema.get_list("name"):
        pointer = schema["name", target]
        # check for missing target
        if pointer.get_list("required", None):
            if doc.get_list(target):
                pass
            else:
                if pointer.get_list("value", None):
                    doc.append(target, pointer["value", None].value("default"))
                else:
                    doc.append(target, None)
        # check 'value' (if exists)
        if pointer.get_list("value", None):
            value_parms = pointer["value", None]
            if value_parms.get_list("required", None):
                for name,value,index in doc.keys(target):
                    key_list = [(name, value, index)]
                    line_number = find_rolne_line(line_keys, key_list)
                    if value is None:
                        if value_parms.value("default"):
                            doc[target, value, 0]=value_parms.value("default")
                        else:
                            error_list.append( ("schema", line_number, "value is required for '{}'.".format(target)) )
        # check subs
        for key in doc.keys(target):
            el = sub_schema_requirements(doc[key],pointer,line_keys)
            error_list.extend(el)
    return error_list


def find_rolne_line(line_keys, key_list):
    for ctr, entry in enumerate(line_keys):
        if key_list==entry:
            return ctr
    return -1

def rolne_to_string(r, tab_size=4, quote_all=True):
    result = ""
    #print r.data
    if r:
        for (rn, rv, rl) in r.data:
            result += rn
            if rv is not None:
                printable = str(rv)
                quote_flag = False
                if '"' in printable:
                    quote_flag = True
                if len(printable) != len(printable.strip()):
                    quote_flag = True
                if quote_flag or quote_all:
                    result += " "+'"'+rv+'"'
                else:
                    result += " "+rv
            result += "\n"
            if rl:
                temp = rolne_to_string(rolne(in_list=rl), tab_size=tab_size, quote_all=quote_all)
                for line in temp.split("\n"):
                    if line:
                        result += " "*tab_size+line
                        result += "\n"
    return result

if __name__ == "__main__":

    if True:

        my_doc = '''
item zing
    size 4
    color red
        intensity 44%
    color yellow
    size 2
item womp
    size 5
    color blue
item bam
item bam
item broom
    size 7
    title "The "big" thing"
zoom_flag
code_seq
    * r9
    * r3
    * r2
    * r3
system_title hello
zoom_flag False'''

        schema = '''
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
name zoom_flag
    treatment one
    value
        required
        default True
name boing
    required
    value
        required
        default joejoe
name code_seq
    name *
name system_title
'''

        #print my_doc
        print schema
        r,e = string_to_rolne(my_doc, schema, tab_strict=True)
        #r = string_to_python(my_doc, schema)
        for ctr, line in enumerate(my_doc.split("\n")):
            print ctr, line
        print "FINAL:\n"
        print str(r)
        print "ERRORS:\n"
        print repr(e)

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
