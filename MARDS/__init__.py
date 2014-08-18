# MARDS\__init__.py
#
# MARDS data serialization library
#
# Version 0.1.0

from rolne import rolne

import mards_library as ml

schema_schema = '''
ordered false
name ordered
    treatment one
    required
    value
        type boolean
        required
        default True
name name
    treatment unique
    value
        type label
        required
    name ordered
        treatment one
        required
        value
            type boolean
            required
            default True
    name required
        treatment one
        required
        value
            type boolean
            required
            default False
    name treatment
        value
        type label
    name value
        name type
        name required
        name default
    name name
        treatment unique
        value
            type label
            required
        name ordered
            treatment one
            required
            value
                type boolean
                required
                default True
        name required
            treatment one
            required
            value
                type boolean
                required
                default False
        name treatment
            value
            type label
        name value
            name type
            name required
            name default
        name name
            treatment unique
            value
                type label
                required
            name ordered
                treatment one
                required
                value
                    type boolean
                    required
                    default True
            name required
                treatment one
                required
                value
                    type boolean
                    required
                    default False
            name treatment
                value
                type label
            name value
                name type
                name required
                name default
'''



def MARDS_to_rolne(doc=None, schema=None, context="doc", tab_strict=False):
    result = rolne()
    error_list = []
    if doc is None:
        return result, error_list
    if schema:
        schema, schema_errors = MARDS_to_rolne(schema, context="schema")
        error_list.extend(schema_errors)
    current = 0
    tab_list = [0]
    pointer_list = range(50)
    pointer_list[0]=result
    last_spot = pointer_list[0]
    #line_tracker = []
    last_nvi = range(50)
    for ctr, line in enumerate(doc.split("\n")):
        #line_tracker.append([])
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
                index = pointer_list[indent].append_index(key, value, seq=str(ctr))
                last_spot = pointer_list[indent][key, value, index]
                last_nvi[indent]=(key, value, index)
                #for r in range(indent+1):
                #    line_tracker[ctr].append(last_nvi[r])
    if schema:
        result, schema_errors = ml.schema_rolne_check(result, schema)
        error_list.extend(schema_errors)
    return result, error_list

def MARDS_to_python(doc=None, schema=None, context="doc", tab_strict=False):
    r, error_list = MARDS_to_rolne(doc, schema, context=context, tab_strict=tab_strict)
    if schema:
        schema, schema_errors = MARDS_to_rolne(schema, context="schema")
        error_list.extend(schema_errors)
        result = sub_convert_python(r, schema)
    else:
        result = sub_generate_tuple_list_simple(r)
    return result, error_list

#TODO: make this part of rolne
def sub_generate_tuple_list_simple(doc):
    result = []
    for entry in doc.dump():
        (en, ev, ei, es) = entry
        tup = (en, ev, sub_generate_tuple_list_simple(doc[en, ev, ei]))
        result.append(tup)
    return result

def sub_convert_python(doc, schema):
    #print "jj", doc, schema
    if schema.value("ordered")=="False":
        name_ordered_flag = False
    else:
        name_ordered_flag = True
    # create the 'structure' whatever it is
    if name_ordered_flag:
        result = []
    else:
        result = {}
    delete_list = {}
    # parse each entry
    for entry in doc.dump():
        (en, ev, ei, es) = entry
        treatment = schema["name", en].value("treatment")
        if schema["name", en].value("ordered")=="False":
            value_ordered_flag = False
        else:
            value_ordered_flag = True
        if schema["name", en].get_list("name"):
            has_subs = True
        else:
            has_subs = False
        name_count = len(doc.get_list(en))
        sub_list = sub_convert_python(doc[en, ev, ei], schema["name", en])
        # create an item for the structure
        if name_ordered_flag:
            if value_ordered_flag:
                if has_subs:
                    item = (en, ev, sub_list)
                else:
                    item = (en, ev)
            else:
                if has_subs:
                    item = (en, ev, sub_list)
                else:
                    item = (en, ev)
            result.append(item)
        else:
            if value_ordered_flag:
                if has_subs:
                    if ev:
                        item = (ev, sub_list)
                    else:
                        item = sub_list
                else:
                    item = ev
            else:
                if has_subs:
                    item = {ev: sub_list}
                else:
                    item = ev
            if treatment=='one':
                if not en in result:
                    result[en] = item # only set if the first found
            elif treatment=='sum':
                if value_ordered_flag:
                    if not en in result:
                        result[en] = (ev, sub_list)
                    else:
                        result[en] = (type_aware_sum_value(result[en][0], ev), type_aware_sum_sub(result[en][1], sub_list))
                else:
                    #print "jj", en
                    if not en in result:
                        result[en] = {ev: sub_list}
                        if not en in delete_list:
                            delete_list[en] = [ev]
                    else:
                        dv = delete_list[en][-1]
                        delete_list[en].append(ev)
                        new_key = type_aware_sum_value(dv, ev)
                        #print "new_key", new_key
                        result[en][new_key] = type_aware_sum_sub(result[en][dv], sub_list)
            else: #anything else is a list
                if not en in result:
                    result[en] = []
                result[en].append(item)
        # cleanup of deleted keys from sub operation
        for name in delete_list:
            print "del", name, delete_list[name]
            # TODO: leave this in here or handle summing in rolne?
    return result


def type_aware_sum_sub(item_a, item_b, item_type=None):
    if type(item_a) is list:
        result = item_a
        if type(item_b) is list:
            result.extend(item_b)
        else:
            result.append(item_b)
    elif type(item_a) is dict:
        result = {}
        for key in item_a:
            if key in item_b:
                if type(item_a[key]) is list:
                    value = item_a[key] + item_b[key]
                else:
                    value = str(item_a[key])+str(item_b[key])
                result[key] = value
            else:
                result[key] = item_a[key] 
        #dict(item_a.items() + item_b.items())
    else:
        result = "fail"
    return result

def type_aware_sum_value(item_a, item_b, item_type=None):
    if item_a is None:
        if item_b is None:
            result = None
        else:
            result = item_b
    else:
        if item_b is None:
            result = item_a
        else:
            result = str(item_a)+str(item_b)
    return result


def rolne_to_MARDS(r, tab_size=4, quote_all=True):
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
code_seq a
    * r9
    * r3
    * r2
    * r3
code_seq b
    * a
    * b
    * c
    * d
system_title hello
zoom_flag False'''

        schema = '''
ordered False
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
    value
        ordered False
    ordered False
    treatment sum
    name *
name system_title
'''

        #print my_doc
        print schema
        #x,e = MARDS_to_rolne(schema, schema_schema)
        #r,e = MARDS_to_rolne(my_doc, schema, tab_strict=True)
        x,e = MARDS_to_python(my_doc, schema)
        for ctr, line in enumerate(my_doc.split("\n")):
            print ctr, line
        #for ctr, line in enumerate(schema.split("\n")):
        #    print ctr, line
        print "FINAL:\n"
        print str(x)
        print "ERRORS:\n"
        print repr(e)

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
