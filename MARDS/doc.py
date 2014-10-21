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
    title = root.value
    if root.has("title"):
        title = str(root.get_value("title"))
    docs[root.value].append("="*len(title))
    docs[root.value].append(title)
    docs[root.value].append("="*len(title))
    docs[root.value].append('')
    for sub in root.only('sub'):
        docs[root.value].append('* :doc:`'+sub.value+'`')
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
        if schema_rolne.has(('name', sub.value)):
            schema_sub = schema_rolne['name', sub.value]
        else:
            match = sub.value.split(".")[-1]
            if schema_rolne.has(('match', match)):
                schema_sub = schema_rolne['match', match]
            else:
                continue
        docs[sub.value] = []
        current = docs[sub.value]
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
            current.append('``'+sub.value+'`` *'+type+'*')
            current.append('')
        if schema_sub.has(('describe', language)):
            d = schema_sub['describe', language]
            if d.has('abstract'):
                temp = ""
                for paragraph in d.list_values('abstract'):
                    temp += paragraph + " "
                current.append('*'+temp.strip()+'*')
                current.append('')
            if d.has('body'):
                for paragraph in d.list_values('body'):
                    current.append(paragraph)
                    current.append('')
        # items list
        if len(schema_sub.only('search')):
            current.append("''''''''''")
            current.append("Variations")
            current.append("''''''''''")
            current.append('')
            for v in schema_sub.only('search'):
                current.append('There are additional attributes based on **'+v.value+'** :')
                current.append('')
                for m in v.only('match'):
                    # head = sub.value.split(".")[0]
                    doc_name = sub.value+"."+v.value+'.'+m.value
                    current.append('  * :doc:`'+doc_name+'`')
                    sub.append("sub", doc_name)
                    sub["sub", doc_name].append("new_doc", "true")
                parse_rst(sub, v, docs, language)
        if len(schema_sub.only('name')):
            current.append("''''''''''")
            current.append("Attributes")
            current.append("''''''''''")
            current.append('')
            current.extend(rst_list_attributes_recursive(schema_sub, language, sub.value))
    return

def rst_list_attributes_recursive(schema, language, head):
    result = []
    for item in schema.only('name'):
        if str(item.value)[0:2]!="__":
            val_type = item['value'].get_value('type')
            if val_type=='ignore':
                result.append(str(item.value))
            else:
                # TODO: add a hyperlink for val_type as gen'd by from st module
                result.append('``'+str(item.value)+'`` *'+val_type+'*')
                result.append('')
                # if val_type!='radio_select':
                #    temp_list = st.rst(item['value'])
                #    for line in temp_list:
                #        result.append('    '+line)
            if item['value']['type'].has('choice'):
                match_list = []
                if schema.has(('search', item.value)):
                    match_list = schema['search', item.value].list_values('match')
                    result.append('    The choice selected adds additional attributes. Click above to see them.')
                result.append('    choices:')
                result.append('    ')
                for choice in item['value']['type'].only("choice"):
                    if choice.value in match_list:
                        result.append('      * ``'+choice.value.strip()+'`` - :doc:`'+head+"."+item.value+'.'+choice.value+'`')
                    else:
                        result.append('      * ``'+choice.value.strip()+'``')
                    result.append('    ')
                    if choice.has('name'):
                        temp_list = rst_list_attributes_recursive(choice, language, head)
                        result.append('        The following can further define this choice:')
                        result.append('        ')
                        for line in temp_list:
                            result.append('        '+line)
                        result.append('        ')
                result.append('    ')
            if item.has(('describe', language)):
                d = item['describe', language]
                if d.has('abstract'):
                    temp = ""
                    for paragraph in d.list_values('abstract'):
                        temp += paragraph + " "
                    result.append('    *'+temp.strip()+'*')
                    result.append('    ')
                if d.has('body'):
                    for paragraph in d.list_values('body'):
                        result.append('    '+paragraph)
                        result.append('    ')
            if item.has('name'):
                temp_list = rst_list_attributes_recursive(item.only('name'), language, head)
                result.append('    The following can further define this attribute:')
                result.append('    ')
                for line in temp_list:
                    result.append('        '+line)
                result.append('    ')
            result.append('    ')
    return result
    
# eof: MARDS\doc.py
