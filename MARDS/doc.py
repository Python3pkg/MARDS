# -*- coding: iso-8859-1 -*-
# MARDS\doc.py
#
# DOCUMENTATION GENERATION
#

from rolne import rolne
from MARDS import st

# the breakdown_rolne contains instructions on how to "break down" the files used in the final docs.
#
def generate_rst_files(schema_rolne, breakdown_rolne, dest_dir, language="en"):
    docs = {}
    # initialize with root doc
    root = breakdown_rolne["root"]
    docs[root.value] = []
    # make subs
    parse_rst(root, schema_rolne, docs, language)
    # generate everything
    for key in docs:
        fh = open(dest_dir+"/"+key+".rst", 'w')
        for line in docs[key]:
            fh.write(line)
            fh.write('\n')
        fh.close()
    return

def parse_rst(breakdown, schema_rolne, docs, language):
    for sub in breakdown.only('sub'):
        docs[sub.value] = []
        current = docs[sub.value]
        schema_sub = schema_rolne['name', sub.value]
        # body
        if schema_sub.has([('describe', language),('title')]):
            title = schema_sub['describe', language].get_value('title')
        else:
            title = sub.value
        current.append(title)
        current.append('='*len(title))
        current.append('')
        if schema_sub.has([('value'),('type')]):
            type = schema_sub['value'].get_value('type')
        else:
            type = 'string'
        if type!='ignore':
            current.append("''''''")
            current.append("Format")
            current.append("''''''")
            current.append('')
            current.append(sub.value+' *'+type+'*')
            current.append('')
        if schema_sub.has(('describe', language)):
            d = schema_sub['describe', language]
            if d.has('abstract'):
                current.append("''''''''")
                current.append("Abstract")
                current.append("''''''''")
                current.append('')
                current.append(d.get_value('abstract'))
                current.append('')
            if d.has('body'):
                current.append("''''")
                current.append("Body")
                current.append("''''")
                current.append('')
                current.append(d.get_value('body'))
                current.append('')
        # items list
        if len(schema_sub.only('name')):
            current.append("''''''''''")
            current.append("Attributes")
            current.append("''''''''''")
            current.append('')
            current.extend(rst_list_attributes_recursive(schema_sub.only('name'), language))
        #if len(schema_sub.only('sub')):
        #    for subsub in schema_sub.only('sub'):
        #        parse_rst(subsub, schema_sub, docs, language)
    return

def rst_list_attributes_recursive(schema, language):
    result = []
    for item in schema:
        if str(item.value)[0:2]!="__":
            if item.has([('value'),('type')]):
                type = item['value'].get_value('type')
            else:
                type = 'string'
            result.append(str(item.value)+' : '+type)
            if item.has('value'):
                temp_list = st.rst(item['value'])
                for line in temp_list:
                    result.append('    '+line)
            if item.has(('describe', language)):
                d = item['describe', language]
                if d.has('title'):
                    result.append('    title: '+d.get_value('title'))
                    result.append('    ')
                if d.has('abstract'):
                    result.append('    abstract: '+d.get_value('abstract'))
                    result.append('    ')
                if d.has('body'):
                    result.append('    body: '+d.get_value('body'))
                    result.append('    ')
            if item.has('name'):
                temp_list = rst_list_attributes_recursive(item.only('name'), language)
                result.append('    The following items can be below this attribute:')
                result.append('    ')
                for line in temp_list:
                    result.append('    '+line)
                result.append('    ')
            result.append('    ')
    return result
    
# eof: MARDS\doc.py
