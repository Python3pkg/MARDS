# MARDS\__init__.py
#
# MARDS data serialization library
#
# Version 0.1.0

from rolne import rolne

import mards_library as ml

def string_to_rolne(doc=None):
    result = rolne()
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
        system_title hello
        '''
        print string_to_rolne(my_doc)

    else:
        print "==================================="
        print
        import doctest
        print "Testing begins. Errors found:"
