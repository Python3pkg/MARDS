# MARDS\mards_library.py
#
# INTERNAL SUPPORT ROUTINES
#
    
def parse_line(line, tab_list, tab_strict=False):
    indent = None
    key = None
    value = None
    error = None
    space_ctr = 0
    # mode: 0=beginning, 1=key, 2=pre-value, 3=value
    mode = 0 # beginning
    for c in line:
        if mode==0: # beginning
            if c==" ":
                space_ctr += 1
            elif c=="\n":
                return (indent, key, value, error) # skip line if all whitespaces
            elif c=="#":
                return (indent, key, value, error) # skip line if starts with # comment symbol
            elif len(c.strip())==0:
                return (indent, key, value, "non-space whitespace character found before key")
            else:
                key=c
                mode = 1 # key
        elif mode==1: # key
            if c==" ":
                mode = 2 # pre-value
            elif len(c.strip())==0:
                return (indent, key, value, "non-space whitespace character found inside key")
            else:
                key += c
        elif mode==2: # pre-value
            if c==" ":
                pass
            else:
                value=c
                mode = 3 # value
        elif mode==3: # value
            value += c
        else:
            raise
    if value is not None and len(value.strip())>=2:
        if value[0]=='"':
            if value.rstrip()[-1]=='"':
                value=value.rstrip()[1:-1]
    #
    # calculate indent
    #
    if tab_strict:
        indent = int(space_ctr / 4)
        if space_ctr % 4 != 0:
            return (indent, key, value, "indent found that is not a multiple of 4 spaces")
    else:
        indent = 0
        #print key, value, space_ctr, repr(tab_list)
        match_found = False
        for spot, x in enumerate(tab_list):
            if space_ctr<x:
                # spot found, but at a new 'tab'. aka the 'slide to the left'
                indent = spot
                break
            elif space_ctr==x:
                indent = spot
                match_found = True
                break
            elif space_ctr>x:
                indent = spot
        else:
            # new 'biggest' number found
            tab_list.append(space_ctr)
            indent += 1
            match_found = True
        #print indent, match_found
        if not match_found:
            tab_list[indent] = space_ctr
        if len(tab_list)>(indent+1):
            del tab_list[indent+1:]
    #
    # done
    #
    return (indent, key, value, error)

def rolne_to_dict(rolne):
    d = {}
    for entry in rolne:
        (key, value, new_rolne) = entry
        if new_rolne:
            if key in d:
                d[key].append(rolne_to_dict(new_rolne))
            else:
                d[key] = [rolne_to_dict(new_rolne)]
        if value is not None:
            if key in d:
                d[key].append(value)
            else:
                d[key] = [value]
    return d

def render_mards_target(target, indent=0, quote_method='all'):
    result = ""
    if type(target) is dict:
        for key in target:
            # turn everything back into list of things
            if type(target[key]) is list:
                value_list = target[key]
            elif type(target[key]) is dict:
                value_list = [None]
            else:
                value_list = [target[key]]
            for value in value_list:
                result += " "*(indent*4)
                result += str(key)
                if value:
                    result += value_output(value, quote_method=quote_method)
                result += "\n"
            if type(target[key]) is dict:
                result += render_mards_target(target[key], indent=indent+1, quote_method=quote_method)
    return result
    
def delist(target):
    ''' for any "list" found, replace with a single entry if the list has exactly one entry '''
    result = target
    if type(target) is dict:
        for key in target:
            target[key] = delist(target[key])
    if type(target) is list:
        if len(target)==0:
            result = None
        elif len(target)==1:
            result = delist(target[0])
        else:
            result = [delist(e) for e in target]
    return result

def value_output(value, quote_method='all', none_handle='strict'):
    '''
    Format types:
    'all'.
       (default) everything is embraced with quotes
    'needed'.
       Quote only if needed. Values are on placed in quotes if:
       a. the value contains a quote
       b. there is whitespace at the beginning or end of string
    'none'.
       Quote nothing.
    '''
    p = str(value)
    if value is None:
        if none_handle=='strict':
            return ""
        elif none_handle=='empty':
            return ' ""'
        elif none_handle=='None':
            p = "None"
        else:
            raise "none handler "+str(none_handle)+" not recognized"
    if quote_method=='all':
        return ' "'+p+'"'
    elif quote_method=='by_need':
        if len(p)!=len(p.strip()):
            return ' "'+p+'"'
        if '"' in p:
            return ' "'+p+'"'
        return " "+p
    elif quote_method=='none':
        return " "+p
    else:
        raise "quote method "+str(quote_method)+" not recognized"
    return

def schema_rolne_check(doc, schema):
    error_list = []
    #
    # PASS ONE: FORWARD CHECK OF DOC
    #
    # this pass verifies that each entry in the document
    # has a corresponding entry in the schema
    #
    el = sub_schema_coverage(doc, schema)
    error_list.extend(el)
    #
    # PASS TWO: REQUIREMENTS CHECK OF SCHEMA
    #
    # this pass verifies that any 'required' entries in the
    # schema are met. If auto-inserts if allowed. Otherwise,
    # it adds an error.
    el = sub_schema_requirements(doc, schema)
    error_list.extend(el)
    #
    # PASS THREE: TREATMENT CHECKS
    #
    el = sub_schema_treatments(doc, schema)
    error_list.extend(el)
    return doc, error_list

def sub_schema_coverage(doc, schema):
    error_list = []
    for entry in doc.dump():
        (name, value, index, seq) = entry
        if not name in schema.get_list("name"):
            error_list.append( ("doc", seq, "a name of '{}' not found in schema context".format(name)) )
        else:
            # check subs
            el = sub_schema_coverage(doc[name, value, index], schema["name", name])
            error_list.extend(el)
    return error_list

def sub_schema_treatments(doc, schema):
    error_list = []
    for target in schema.get_list("name"):
        pointer = schema["name", target]
        treatment = pointer.value("treatment")
        if not treatment:
            treatment = "list"
        if treatment=="list":
            pass # there are no checks needed for list
        elif treatment=="unique":
            first_line = {}
            for entry in doc.dump(target):
                (en, ev, ei, es) = entry
                if ei==0:
                    first_line[ev] = es
                else:
                    error_list.append( ("doc", es, "'{}' entries should be unique, but this line is a duplicate of line {}.".format(target, first_line[ev])) )
        elif treatment=="sum":
            pass
        elif treatment=="average":
            pass
        elif treatment=="one":
            entry_list = doc.dump(target)
            if len(entry_list)>1:
                first_line = entry_list[0][3]
                del entry_list[0]
                for (en, ev, ei, es) in entry_list:
                    error_list.append( ("doc", es, "only one '{}' entry should exist, but this line is in addition to line {}.".format(target, first_line)) )
        else:
            pass
        # check subs
        for key in doc.keys(target):
            el = sub_schema_treatments(doc[key],schema["name", target])
            error_list.extend(el)
    return error_list

req_ctr = 0

def sub_schema_requirements(doc, schema):
    global req_ctr
    error_list = []
    for target in schema.get_list("name"):
        pointer = schema["name", target]
        # check for missing target
        if pointer.get_list("required", None):
            if doc.get_list(target):
                pass
            else:
                if pointer.get_list("value", None):
                    doc.append(target, pointer["value", None].value("default"), seq='auto'+str(req_ctr))
                else:
                    doc.append(target, None, seq="auto"+str(req_ctr))
                req_ctr += 1
        # check 'value' (if exists)
        if pointer.get_list("value", None):
            value_parms = pointer["value", None]
            if value_parms.get_list("required", None):
                for name,value,index,seq in doc.dump(target):
                    #key_list = [(name, value, index)]
                    #line_number = find_rolne_line(line_keys, key_list)
                    if value is None:
                        if value_parms.value("default"):
                            doc[target, value, 0]=value_parms.value("default")
                        else:
                            error_list.append( ("schema", seq, "value is required for '{}'.".format(target)) )
        # check subs
        for key in doc.keys(target):
            el = sub_schema_requirements(doc[key], pointer)
            error_list.extend(el)
    return error_list

# eof: MARDS\mards_library.py