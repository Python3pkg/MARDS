# -*- coding: iso-8859-1 -*-
# MARDS\mards_library.py
#
# INTERNAL SUPPORT ROUTINES
#

from rolne import rolne


standard_types = '''\
#!MARDS_schema_en_1.0

define_type string
    describe en
        title "String (UTF8)"
        body "A string is any sequence of UTF8 characters. This is the default type if no other type is specified."

define_type label
    describe en
        title "Label"
        body "A UTF8 unicode string containing alphabetic characters, digits 0 to 9, underscores (\_), and periods. No other characters are permitted. Labels are generally case-sensitive."
        body ""
        body "Very explicitly: whitespace characters are forbidden (such as SPACE and TAB). Punctuation of any kind (other than underscores and periods) are forbidden."
        body ""
        body "The MARDS spec uses label rules for names in the name<space>value. However, it purposefully makes exception for labels that start with # symbol for outside-context exceptions such as for comments."
        body ""
        body "#Convention"
        body ""
        body "A label that follows the rules is ultimates a true label. However, there are conventions used in the making of the labels in English. Following these conventions makes the human interpretation of the labels much easier. They are as follows:"
        body ""
        body " *  Seperate words with underscores. Don't use CamelCase. So, instead of:"
        body ""
        body "    `OneTwoThree`"
        body ""
        body "    use:"
        body ""
        body "    `one_two_three`"
        body ""
        body " *  use all lower case letters unless called for by standard writing convention. A label is not assumed to be a sentence, so the first word should not be capitalized unless called for by other convention rules. So, instead of:"
        body ""
        body "    `Qty_Of_Johns_Boxes`"
        body ""
        body "    use:"
        body ""
        body "    `qty_of_Johns_boxes`"
        body ""
        body "    Notice that 'J' remains capitalized since 'John' is a persons name and would be capitalized by English writing convention."
        body ""
        body " *  Punctuation is 'skipped' rather than given an underscore unless such an underscore greatly adds clarity. So, instead of:"
        body ""
        body "    `qty_of_John_s_boxes`"
        body ""
        body "    use:"
        body ""
        body "    `qty_of_Johns_boxes`"
        body ""
        body " *  if the label is a schema name, imply the type of unit expected IF it aids clarity. Ideally it would be a suffix with the full type label. So, instead of:"
        body ""
        body "    `part4_twist`"
        body ""
        body "    use:"
        body ""
        body "    `part4_twist_percent`"
        body ""
        body " *  avoid the use of periods (.) for simple labels. The periods are meant to imply sectional seperation. TODO: expand this."
        body " *  reserve labels that start with an underscore for information that should be repressed from publication or normal/typical view. A single underscore implies mild suppression. A double underscore implies strong supression. The actual meaning of 'suppression' is a matter of context."
        body " *  Don't end a label with underscores or periods."

define_type price
    describe en
        title "Price"
        body "The proposed quantity of money or other compensation in exchange for a good or service. The normalization depends on the currency."
    unit USD
        describe en
            title "U.S. Dollars"
            body "A quantity of US Dollars. Precision is assumed to be to 6 decimal places. That is to say that $43.1234567 would be rounded to `43.123457 USD`. Regardless of the number, at least two decimal places are displayed. For example, $100 would normalize to `100.00 USD` but $100.932 would normalize to `100.932 USD`. But, again, the precision is to 6 decimal places regardless of display. So, $100.000000 is the same as $100. And, $100.932 is the same as $100.932000.
        default
        * "usd"
        * "us"
        * "dollars"
        prefix "$"
    unit USD-cents
        * "c"
        * "cents"
        * "pennies"
        * "¢"

define_type qty
    describe en
        title "Quantity"
        body "A positive integer representing the amount of discrete objects, items, or services contained, needed, or desired. The number range is from 0 to 9223372036854775807. Normalized to a series of decimal digits with no seperators."

define_type percent
    describe en
        title "Percentage"
        body "A fraction of unity. Normalized to a simple decimal fraction. So, nothing is '0.0' and all is '1.0'. Can alternatively represented by the '%' symbol, such as '0%' and '100.0%'. A percentage cannot be below zero, but it has no upper limit."
    unit fraction
        default
    unit percent
        * "%"

define_type check_list
    describe en
        title "Choice/Check List"
        body "A list of labels. Each label is restricted to the 'choice' elements under the 'type check_list' definition."
        body ""
        body "Each label is seperated by whitespace and/or other non-label characters."
        body ""
        body "A common convention is to use commas to visually aid in the seperation. This is not strictly required however. So, a value of `one, two, three` is the same as `one two three`. The single COMMA SPACE seperation is the normalized result."
        body ""
        body "If the schema defines the value as _required_, then the there must be at least one label selected. Otherwise, zero labels can be selected."
    name choice
        treatment unique
        value
            required
            type label

define_type radio_select
    describe en
        title "Radio Select"
        body "A selected label. The label is restricted to the 'choice' elements under the 'type radio_select' definition."
        body ""
        body "If the schema defines the value as _required_, then the there must be a label selected. Otherwise, the value can be empty."
    name choice
        treatment unique
        value
            required
            type label

define_type ignore
    describe en
        title "Ignored Value"
        body "A value with an 'ignore' type is discarded. Normalized to an empty string."

define_type unit
    describe en
        title "Desired Unit"
        body "A short sequence of characters indicating a desired or required unit of measurement. It is treated just like a 'string' type."

define_type degree
    describe en
        body "A unit of angle measurement. It is normalized to simple radians."
    unit deg
        * "°"
        * "deg"
        * "degree"
    unit rad
        default
        * "rad"
        * "radian"

define_type file
    describe en
        title "File Label"
        body "A name of a file on an storage system. The name is expected to conform to a label. As such, there might be additional information added to make it a real file name when used by the local computer."

define_type length
    describe en
        title "Length"
        body "The extent of something from end to end. Normalized to SI unit of meter (m)"
    unit m
        default
        * "m"
        * "meter"
        * "meters"
        * "metre"
        * "metres"
    unit mm
        * "mm"
        * "millimeter"
        * "millimeters"
        * "millimetre"
        * "millimetres"
    unit cm
        * "cm"
        * "centimeter"
        * "centimeters"
        * "centimetre"
        * "centimetres"
    unit dm
        * "dm"
        * "decimeter"
        * "decimeters"
        * "decimetre"
        * "decimetres"
    unit km
        * "k"
        * "km"
        * "kilometer"
        * "kilometers"
        * "kilometre"
        * "kilometres"
    unit mi
        * "mi"
        * "mile"
        * "miles"
    unit in
        * "i"
        * "in"
        * "inch"
        * "inches"
    unti ft
        * "f"
        * "ft"
        * "feet"
    unit yd
        * "y"
        * "yd"
        * "yard"
        * "yards"
define_type distance
    describe en
        title "Distance"
        body "A positive numeric measure of the how far apart two objects are. Normalized to the SI unit of meter (m). If the value is found to be negative, it is made positive."
        
define_type duration
    describe en
        title "Duration"
        body "A positive measure of time between two events. Normalized to SI unit of seconds (s)."
    unit s
        default
        * "s"
        * "sec"
        * "second"
        * "seconds"
    unit m
        * "m"
        * "min"
        * "mins"
        * "minute"
        * "minutes"
    unit h
        * "h"
        * "hr"
        * "hrs"
        * "hour"
        * "hours"
    unit d
        * "d"
        * "day"
        * "days"

define_type mass
    describe en
        title "Mass"
        body "A positive measure of the physical property of a bodies resistence to accelleration by force. At rest on a planet, weight and mass are commonly the same thing. Normalized to the SI unit of kilograme (kg)."
    unit g
        * "g"
        * "gr"
        * "gram"
        * "grams"
    unit kg
        default
        * "kg"
        * "k"
        * "kilo"
        * "kilogram"
        * "kilograms"
        * "kilograme"
        * "kilogrames"
    unit hg
        * "hg"
    unit dag
        * "dag"
    unit dg
        * "dg"
    unit cg
        * "cg"
    unit mg
        * "mg"
    unit tonne
        * "t"
        * "tonne"
        * "tonnes"
        * "metric ton"
        * "metric tons"
        * "Mg"
    unit slug
        * "sl"
        * "slug"
    unit lb
        * "lb"
        * "lbs"
        * "pound"
        * "pounds"
    unit oz
        * "oz"
        * "ounce"
        * "ounces"
        
define_type temperature
    describe en
        title "Temperature"
        body "A measure of hot and cold. Normalized to the SI unit of the Kelvin (K)".
    unit f
        * "f"
        * "°f"
        * "fahrenheit"
    unit c
        * "c"
        * "°c"
        * "celcius"
    unit k
        default
        * "k"
        * "°k"
        * "kelvin"
        
define_type luminous_intensity
    describe en
        title "Luminous Intensity"
        body "A measure of the vavelength-weighted power emitted by a light source in a particular direction per unit solid angle (see wikipedia). Normalized to the SI unit of candela (cd)."
    unit cd
        default
        * "cd"
        * "candela"

define_type current
    describe en
        title "Electrical Current"
        body "The flow of electric charge. Normalized to the SI unit of ampere (A)."
    unit a
        default
        * "a"
        * "amp"
        * "amps"
        * "ampere"
        * "amperes"
    unit ma
        * "ma"
        * "milliamp"
        * "milliamps"
        
define_type voltage
    describe en
        title "Electrical Voltage"
        body "The potential of electric force. Normalized to the SI unit of volt (V)."
    unit v
        default
        * "v"
        * "volt"
        * "volts"
    unit microvolt
        * "microvolt"
        * "microvolts"
        * "µv"
    unit millivolt
        * "millivolt"
        * "millivolts"
        * "mV"
    unit kilovolt
        * "kilovolt"
        * "kilovolts"
        * "kV"
    unit megavolt
        * "megavolt"
        * "megavolts"
        * "MV"
        
define_type frequency
    describe en
        title "Frequency"
        body "The count of events per unit of time. Normalized to the SI unit of hertz (Hz)."
    unit hz
        default
        * "hz"
        * "hertz"
        * "per second"
        * "/s"
        * "/ s"
    unit khz
        * "khz"
    unit mhz
        * "mhz"
    unit ghz
        * "ghz"
    unit invert_s
        * "s"
        * "seconds"
    unit invert_ms
        * "ms"
        * "milliseconds"

define_type boolean
    describe en
        title "Boolean"
        body "The state of either Truth (existence) or False (non-existence). Normalized to the interpretation JSON-like 'true' for true and 'false' for false."
    unit bool_true
        default
        * "true"
        * 1
        * -1
        * "good"
        * "t"
        * "correct"
        * "yes"
        * "one"
        * "yep"
        * "pass"
        * "passed"
        * "accept"
        * "accepted"
        * "consent"
        * "consented"
        * "agree"
        * "agreed"
        * "embrace"
        * "cherish"
        * "exalt"
        * "love"
        * "submit"
        * "enfold"
        * "include"
        * "bless"
        * "blessed"
        * "clean"
    unit bool_false
        * "false"
        * 0
        * "bad"
        * "f"
        * "incorrect"
        * "no"
        * "0"
        * "zero"
        * "nope"
        * "fail"
        * "failed"
        * "reject"
        * "rejected"
        * "deny"
        * "denied"
        * "decline"
        * "declined"
        * "evil"
        * "hate"
        * "hated"
        * "decry"
        * "decried"
        * "exclude"
        * "debase"
        * "debased"
        * "imprecate"
        * "curse"
        * "cursed"
        * "impure"

define_type integer
    describe en
        title "Integer (Whole Number)"
        body "A non-fractional signed number with a range of –9223372036854775808 to 9223372036854775807. Normalized to a series of decimal digits with no seperators. It is prefixed with minus (-) if the number is negative. Otherwise, there is no prefix."

define_type float
    describe en
        title "Float (Decimal Number)"
        body "A real number in specified by IEEE 754. It is normalized to standard scientific notation. For example, 123.4 is represented as `1.234x10^2`."

'''


def MARDS_to_rolne(doc=None, schema=None, context="doc", tab_strict=False, key_open=False, prefix=""):
    result = rolne()
    error_list = []
    if doc is None:
        return result, error_list
    if schema:
        schema, schema_errors = _SCHEMA_to_rolne(schema)
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
        (indent, key, value, error) = parse_line(line, tab_list, tab_strict=tab_strict, key_open=key_open)
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
                index = pointer_list[indent].append_index(key, value, seq=prefix+str(ctr))
                last_spot = pointer_list[indent][key, value, index]
                last_nvi[indent]=(key, value, index)
                #for r in range(indent+1):
                #    line_tracker[ctr].append(last_nvi[r])
    if schema:
        result, schema_errors = schema_rolne_check(result, schema)
        error_list.extend(schema_errors)
    return result, error_list

    
def parse_line(line, tab_list, tab_strict=False, key_open=False):
    indent = None
    key = None
    value = None
    error = None
    space_ctr = 0
    if len(line.strip())==0: #skip completely whitespace lines
        return (indent, key, value, error)
    # mode: 0=beginning, 1=key, 2=pre-value, 3=value
    mode = 0 # beginning
    for c in line:
        if mode==0: # beginning
            if c==" ":
                space_ctr += 1
            elif c=="\n":
                return (indent, key, value, error) # skip line if all whitespaces
            elif c=="#" and key_open==False:
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
    if value is not None:
        value = value.strip()
        if len(value)>=2:
            if value[0]==value[-1]=='"':
                value=value.rstrip()[1:-1]
            elif value[0]==value[-1]=="'":
                value=value.rstrip()[1:-1]
    #
    # calculate indent
    #
    if tab_strict:
        indent = int(space_ctr / 4)
        if space_ctr % 4 != 0:
            snap = line.strip()[:20]
            return (indent, key, value, "indent found that is not a multiple of 4 spaces: '{}'".format(snap))
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

    
standard_type_rolne = MARDS_to_rolne(standard_types)
    
def schema_rolne_check(doc, schema):
    error_list = []
    #
    # PASS ONE: FORWARD CHECK OF DOC
    #
    # this pass verifies that each entry in the document
    # has a corresponding entry in the schema
    #
    el = check_schema_coverage(doc, schema)
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

def check_schema_coverage(doc, schema):
    '''
    FORWARD CHECK OF DOCUMENT
    
    This routine looks at each element in the doc, and makes sure there
    is a matching 'name' in the schema at that level.
    '''
    error_list = []
    for entry in doc.dump_list( (), name=True, value=True, index=True, seq=True):
        (name, value, index, seq) = entry
        temp_schema = schema_match_up(doc, schema)
        if not name in temp_schema.list_values("name"):
            error_list.append( ("doc", seq, "a name of '{}' not found in schema".format(name)) )
        else:
            # check subs
            el = check_schema_coverage(doc[name, value, index], temp_schema["name", name])
            error_list.extend(el)
    return error_list

def schema_match_up(doc, schema):
    '''
    SCHEMA mini-recompile for SEARCH and MATCH functions
    
    given the doc, it returns a schema copy that implements the match
    '''
    search_list = schema.list_values("search")  #TODO have earlier scan remove duplicate searches (e.g. 'search color' and 'search color' in same layer/context)
    if search_list:
        copy = schema.copy(seq_prefix="match_", seq_suffix="")
        for target_name in search_list:
            target_value = doc.value(target_name)
            if target_value:
                match_list = copy["search", target_name].list_values("match")
                if target_value in match_list:
                    copy.extend(copy["search", target_name]["match", target_value])
                    del copy["search", target_name]
                    copy = schema_match_up(doc, copy)
        return copy
    return schema
    
def sub_schema_treatments(doc, orig_schema):
    schema = schema_match_up(doc, orig_schema)
    error_list = []
    for target in schema.list_values("name"):
        pointer = schema["name", target]
        treatment = pointer.value("treatment")
        if not treatment:
            treatment = "list"
        if treatment=="list":
            pass # there are no checks needed for list
        elif treatment=="unique":
            first_line = {}
            delete_list=[]
            for entry in doc.dump_list((target), name=True, value=True, index=True, seq=True):
                (en, ev, ei, es) = entry
                if ei==0:
                    first_line[ev] = es
                else:
                    delete_list.append((en, ev, ei))
                    error_list.append( ("doc", es, "'{}' entries should be unique, but this line is a duplicate of line {}.".format(target, first_line[ev])) )
            for tup in reversed(delete_list):  # the items must be deleted in reverse to avoid index numbering problems
                del doc[tup]
        elif treatment=="sum":
            pass
        elif treatment=="average":
            pass
        elif treatment=="one":
            entry_list = doc.dump_list((target), name=True, value=True, index=True, seq=True)
            if len(entry_list)>1:
                first_line = entry_list[0][3]
                del entry_list[0]
                for (en, ev, ei, es) in entry_list:
                    error_list.append( ("doc", es, "only one '{}' entry should exist, but this line is in addition to line {}.".format(target, first_line)) )
                for (en, ev, ei, es) in reversed(entry_list):
                    del doc[en, ev, ei]
        else:
            pass
        # check subs
        for key in doc.keys(target):
            el = sub_schema_treatments(doc[key],schema["name", target])
            error_list.extend(el)
    return error_list

req_ctr = 0

def sub_schema_requirements(doc, orig_schema):
    schema = schema_match_up(doc, orig_schema)
    global req_ctr
    error_list = []
    for target in schema.list_values("name"):
        pointer = schema["name", target]
        # check for missing target
        if pointer.list_values("required", None):
            if doc.list_values(target):
                pass
            else:
                if pointer.list_values("value", None):
                    doc.append(target, pointer["value", None].value("default"), seq='auto'+str(req_ctr))
                else:
                    doc.append(target, None, seq="auto"+str(req_ctr))
                req_ctr += 1
        # check 'value' (if exists)
        if pointer.list_values("value", None):
            value_parms = pointer["value", None]
            if value_parms.list_values("required", None):
                for name,value,index,seq in doc.dump_list((target), name=True, value=True, index=True, seq=True):
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
    for entry in doc.dump_list( (), name=True, value=True, index=True, seq=True):
        (en, ev, ei, es) = entry
        treatment = schema["name", en].value("treatment")
        if schema["name", en].value("ordered")=="False":
            value_ordered_flag = False
        else:
            value_ordered_flag = True
        if schema["name", en].list_values("name"):
            has_subs = True
        else:
            has_subs = False
        name_count = len(doc.list_values(en))
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

def _SCHEMA_to_rolne(doc=None, prefix=""):
    ################################
    # CONVERT TO A ROLNE
    ################################
    schema, error_list = MARDS_to_rolne(doc, context="schema", tab_strict=True, key_open=True, prefix=prefix)
    ################################
    #  FIRST PASS SYNTAX CHECKING
    #
    # build a list of names from the document and their corresponding locations
    # mark as False if the key is seen twice
    # also do basic syntax checking
    ################################
    for key in schema.flattened_list( (), name=True, value=True, seq=True):
        (en, ev, es) = key
        if en in ["name", "template"]:
            pass
        elif en in ["#!MARDS_schema_en_1.0", "import", "local"]:
            pass
        elif en in ["##"]:
            schema.seq_delete(es)
        elif en in ["limit"]:
            # TODO: check that parent is 'recurse'
            parent_es = schema.seq_parent(es)
            if schema.at_seq(parent_es).name()!='recurse':
                error_list.append( ("schema", es, "the 'limit' element may only be applied to a 'recurse'") )
                schema.seq_delete(es)
            else:
                if ev.isdigit():
                    if int(ev)<1 or int(ev)>20:
                        error_list.append( ("schema", es, "the 'limit' should have a integer value between 1 and 20") )
                        schema.seq_delete(es)
                else:
                    error_list.append( ("schema", es, "the 'limit' should have a integer value between 1 and 20") )
                    schema.seq_delete(es)
        elif en in ["treatment", "value", "required", "default", "ordered"]:
            pass
        elif en in ["insert", "recurse", "extend", "from"]:
            pass
        elif en in ["describe", "title", "abstract", "body", "reference", "author", 'title', 'url', 'journal', 'book', 'date_written', 'date_retreived', 'pages', 'paragraphs', 'copyright_message', 'publisher']:
            pass
        elif en in ["match", "search"]:
            pass
        elif en in ["type", "choice", "search", "min"]:  ## TODO: Type stuff
            pass
        else:
            t = ("schema", es, "'{}' not a recognized schema element name".format(en))
            error_list.append(t)
            schema.seq_delete(es)
    #################################
    #
    # IMPLEMENT Header and imports
    #
    #################################
    schema_list = schema.flattened_list(("#!MARDS_schema_en_1.0"), value=True, seq=True)
    for (ev, es) in schema_list:
        header = schema.at_seq(es)
        import_list = header.flattened_list(("import"), value=True, seq=True)
        for (iev, ies) in import_list:
            i = header.at_seq(ies)
            if iev:
                prx = iev+"/"
            else:
                prx = "./"
            if i.name("local"):
                file_loc = i.value("local")
                if file_loc is None:
                    file_loc = iev+".MARDS-schema"
                try:
                    with open(file_loc, 'r') as file:
                        subdata = file.read()
                except IOError, e: 
                    error_list.append ( ("schema", ies, str(e)) )
                    subdata = None
                if subdata:
                    sr,e = _SCHEMA_to_rolne(subdata, prefix=prx)
                    schema.extend(sr)  #TODO: 'prepend' rather than 'extend'?
                    # TODO: convince rolne to retain line numbering in sr
                    error_list.extend(e)
            else:
                error_list.append( ("schema", ies, "unable to locate import for '{}'".format(iev)) )
        schema.seq_delete(es)  #TODO: verify rolne .seq_delete also deletes children
    #################################
    #
    # MAKE A COPY AND BUILD INDEX
    #
    # copy used by other functions for internal insertions, etc.
    #################################
    copy = schema.copy(seq_prefix="", seq_suffix="")
    name_seq = {}
    name_recurs = {}
    for key in schema.flattened_list( (), name=True, value=True, seq=True):
        (en, ev, es) = key
        if en in ["name", "template"]:
            if ev in name_seq:
                name_seq[ev]=False
            else:
                name_seq[ev]=es
    #################################
    # IMPLEMENT 'template'
    #
    # This is done oddly: now that 'copy' has been made, we simply
    # delete the templates from the  active rolne and rename 'template' to
    # 'name' in the copy.
    #################################

    schema_list = schema.flattened_list(("template"), value=True, seq=True)
    for (ev, es) in schema_list:
        if not prefix:
            schema.seq_delete(es)
        copy.at_seq(es).set_name("name")
    #print "jschema",prefix,schema
    #print "jcopy",copy
    #################################
    #
    # IMPLEMENT 'insert'
    #
    #################################
    schema_list = schema.flattened_list(("insert"), value=True, seq=True)
    safety_ctr=0
    while schema_list and safety_ctr<20:
        for (ev, es) in schema_list:
            if ev in name_seq:
                if name_seq[ev] is False:
                    t = ("schema", es, "'name {}' found in schema multiple times".format(ev))
                    error_list.append(t)
                    schema.seq_delete(es)
                else:
                    src = name_seq[ev]
                    depth_desired = 1
                    line = schema.seq_lineage(es)
                    new_depth = len(line) 
                    prx = src+".i"+str(new_depth)+"."
                    if name_seq[ev] in line:
                        error_list.append(("schema", es, "'insert {}' ends up forming a loop. See lines {}. ".format(ev, ",".join(line))))
                        schema.seq_delete(es)
                    else:
                        schema.seq_replace(es, copy.ptr_to_seq(src), prx)
            else:
                t = ("schema", es, "'name {}' not found in schema".format(ev))
                error_list.append(t)
                schema.seq_delete(es)
        schema_list = schema.flattened_list(("insert"), value=True, seq=True)
        safety_ctr += 1
    #################################
    #
    # IMPLEMENT 'extend'
    #
    #################################
    schema_list = schema.flattened_list(("extend"), value=True, seq=True)
    safety_ctr=0
    while schema_list and safety_ctr<20:
        for (ev, es) in schema_list:
            if ev in name_seq:
                if name_seq[ev] is False:
                    t = ("schema", es, "'name {}' found in schema multiple times".format(ev))
                    error_list.append(t)
                    schema.seq_delete(es)
                else:
                    src = name_seq[ev]
                    depth_desired = 1
                    line = schema.seq_lineage(es)
                    new_depth = len(line) 
                    prx = src+".e"+str(new_depth)+"."
                    if name_seq[ev] in line:
                        error_list.append(("schema", es, "'extend {}' ends up forming a loop. See lines {}. ".format(ev, ",".join(line))))
                        schema.seq_delete(es)
                    else:
                        parent = schema.at_seq(schema.seq_parent(es))
                        children = copy.at_seq(src)
                        parent.extend(children, prefix=prx)
                        schema.seq_delete(es)
            else:
                t = ("schema", es, "'name {}' not found in schema".format(ev))
                error_list.append(t)
                schema.seq_delete(es)
        schema_list = schema.flattened_list(("extend"), value=True, seq=True)
        safety_ctr += 1
    #################################
    #
    # IMPLEMENT 'resurse' recursion
    #
    #################################
    schema_list = schema.flattened_list(("recurse"), value=True, seq=True)
    safety_ctr=0
    while schema_list and safety_ctr<20:
        for (ev, es) in schema_list:
            if ev in name_seq:
                if name_seq[ev] is False:
                    t = ("schema", es, "'name {}' found in schema multiple times".format(ev))
                    error_list.append(t)
                    schema.seq_delete(es)
                else:
                    src = name_seq[ev]
                    depth_desired = schema.at_seq(es).value("limit")
                    if depth_desired is None:
                        depth_desired = 2
                    else:
                        depth_desired = int(depth_desired)
                    line = schema.seq_lineage(es)
                    new_depth = len(line)-1 
                    prx = src+".r"+str(new_depth)+"."
                    if name_seq[ev] in line:
                        if new_depth<=depth_desired:
                            schema.seq_replace(es, copy.ptr_to_seq(src), prx)
                        else:
                            schema.seq_delete(es)
                    else:
                        error_list.append(("schema", es, "'recurse {}' is not recursive".format(ev)))
                        schema.seq_delete(es)
            else:
                t = ("schema", es, "'name {}' not found in schema".format(ev))
                error_list.append(t)
                schema.seq_delete(es)
        schema_list = schema.flattened_list(("recurse"), value=True, seq=True)
        safety_ctr += 1
    ########################
    #   DONE
    ########################
    return schema, error_list

    
    
# eof: MARDS\mards_library.py
