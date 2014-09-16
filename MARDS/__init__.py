# MARDS\__init__.py
#
# MARDS data serialization library
#
# Version 0.1.2

from rolne import rolne
import os

import standard_types as st
import mards_library as ml

def string_to_rolne(string, schema=None, schema_file=None):
    schema_dir = os.getcwd()
    if schema_file:
        with open(schema_file, "r") as fh:
            schema = fh.read()
            schema_dir = os.path.dirname(os.path.realpath(schema_file))
    if not schema:
        schema = "#!MARDS_schema_en_1.0\n    exclusive false\n"
    result, error_list =  ml.MARDS_to_rolne(doc=string, schema=schema, schema_dir=schema_dir)
    return result, error_list

def string_to_python(doc=None, schema=None, context="doc", tab_strict=False):
    r, error_list = MARDS_to_rolne(doc, schema, context=context, tab_strict=tab_strict)
    if schema:
        schema, schema_errors = MARDS_to_rolne(schema, context="schema")
        error_list.extend(schema_errors)
        result = ml.sub_convert_python(r, schema)
    else:
        result = r.dump()
    return result, error_list

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

    print "TBD"
