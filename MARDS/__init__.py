# MARDS\__init__.py
#
# MARDS data serialization library
#
# Version 0.1.0

from rolne import rolne

import mards_library as ml

def string_to_rolne(doc=None, tab_strict=False):
    result = rolne()
    current = 0
    tab_list = [0]
    pointer_list = range(50)
    pointer_list[0]=result
    for ctr, line in enumerate(doc.split("\n")):
        (indent, key, value, error) = ml.parse_line(line, tab_list, tab_strict=tab_strict)
        if error:
            print "error in document line {c}: {e}".format(e=error, c=ctr)
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
                    print "tab error in document line {c}".format(c=ctr)
                    print indent, current
                pointer_list[indent].append(key, value)
                last_spot = pointer_list[indent][key, value]
    return result


if __name__ == "__main__":

    if True:

        my_doc = '''
item zing
    size 4
    color red
        intensity 44%
    color yellow
item womp
    size 5
    color blue
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
system_title hello'''

        recipe = '''
recipe "jim3"
id "53a8775e8c79461fe8d2cc3f"
parameter design_file
    __origin_id 53bd9ab2fbec5b433a000000
    version 0.1 mr
    name design_file
    type file
workstep default_workstep
    __origin_id 53a8775e8c79461fe8d2cc44
    version 0.1 mr
    name default_workstep
    station workbench
    command manual
    maker default_maker
    typical_cost $0.01
    file {design_file}
    output default_part final
parameter yaba_string
    __origin_id 53bee395fbec5b4f69000000
    version 0.1 mr
    name yaba_string
    type string
    default_value "mokey"
parameter how_long
    __origin_id 53bef170fbec5b66f9000000
    version 0.1 mr
    name how_long
    type length
    description "enter da longness"
    default_unit in
    default_value 0.75
parameter flap
    __origin_id 53bef19afbec5b6f8c000000
    version 0.1 mr
    name flap
    type boolean
    description "make it so"
    default_value False
parameter just_one
    __origin_id 53bef1eafbec5b03f6000000
    version 0.1 mr
    name Just_one
    type select
    description "BE PICKY"
    choices one
    choices two
    choices three
    default_value two
maker default_maker
    __origin_id 53a9b186fbec5b13b3000000
    version 0.1 mr
    name default_maker
'''
        #print my_doc
        r = string_to_rolne(recipe)
        r["maker", "default_maker"].append("one", "two")
        print r[("parameter", "flap"):("maker", "default_maker")]

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
