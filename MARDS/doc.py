# -*- coding: iso-8859-1 -*-
# MARDS\doc.py
#
# DOCUMENTATION GENERATION
#

from rolne import rolne

# the breakdown_rolne contains instructions on how to "break down" the files used in the final docs.
#
def generate_rst_files(schema_rolne, breakdown_rolne, dest_dir, language="en"):
    docs = {}
    # initialize with root doc
    root = breakdown_rolne["root"]
    docs[root.value] = []
    # make subs
    for sub in root.only("sub"):
        if sub.get_value("new_doc")=="true":
            docs[sub.value] = []
            current = docs[sub.value]
        else:
            current = doc[root.value]
        schema_sub = schema_rolne['name', sub.value]
        # body
        title = sub.value
        if schema_sub.has(('describe', language)):
            d = schema_sub['describe', language]
            if d.has('title'):
                title = d.get_value('title')
            current.append(title)
            current.append('====')
            current.append('')
            if d.has('abstract'):
                current.append("''''")
                current.append("Abstract")
                current.append("''''")
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
        else:
            current.append(title)
            current.append('====')
            current.append('')
        # items list
        for item in schema_sub.only('name'):
            label = str(item.value)
            if label[0:2]!="__":
                current.append(label)
    # generate everything
    for key in docs:
        fh = open(dest_dir+"/"+key+".rst", 'w')
        for line in docs[key]:
            fh.write(line)
            fh.write('\n')
        fh.close()
    return
    
# eof: MARDS\doc.py
