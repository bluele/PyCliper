# -*- coding: utf-8 -*-
'''
License: http://techno-st.net/2009/11/07/python-html.html
'''

def handler(string):
    import re
    import htmlentitydefs
    amp = string.find('&')
    if amp == -1:
        return string

    entity = re.compile("&([A-Za-z]+);")
    entity_match = entity.findall(string)

    for name in entity_match:
        try:
            c = htmlentitydefs.name2codepoint[name]
        except KeyError:
            continue

        string = string.replace("&%s;" % name, unichr(c))
        
    return string
