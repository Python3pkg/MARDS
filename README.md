MARDS
=====

Data Serialization Based on Rolne Data Type

This is a Library of functions usefull for the interpretation of MARDS data serialization format.

This Library is dependent on the 'rolne' datatype class.

Usage
-----

Simply import the library:

    import MARDS
    
One can then convert a MARDS document into a rolne data type:

    >>> my_doc = '''
    >>> item zing
    >>>     size 4
    >>>     color red
    >>>         intensity 44%
    >>>     color yellow
    >>> item womp
    >>>     size 5
    >>>     color blue
    >>> item bam
    >>> item broom
    >>>     size 7
    >>>     title "The "big" thing"
    >>> zoom_flag
    >>> system_title hello
    >>> '''
    >>> result = MARDS.string_to_rolne(my_doc)
    >>> print result.get_list("items")
    ["zing", "womp", "bam", "broom"]
    
And, in reverse, one can create a MARDS document:

    >>> my_doc = MARDS.rolne_to_string(result)
    >>> print my_doc
    x
    
For now, that is pretty much it. For manipulation of the rolne variable, please view the 'rolne' documentation.
