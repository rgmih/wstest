from xml.etree.cElementTree import Element, tostring
import json

def to_xml(text):
    jsondata = json.loads(text)
    xmlroot = Element('json')
    __serialize(xmlroot, jsondata)
    return '<?xml version="1.0" encoding="UTF-8" standalone="no"?>' + \
            tostring(xmlroot, 'utf-8')

def __serialize(parent_elem, data):
    if isinstance(data, (list, tuple)):
        __serialize_list(parent_elem, data, 'item')
    elif isinstance(data, dict):
        __serialize_dict(parent_elem, data)
    else:
        parent_elem.text = unicode(data)

def __serialize_list(parent_elem, data_list, key):
    for i in data_list:
        item_elem = Element(key)
        parent_elem.append(item_elem)
        __serialize(item_elem, i)

def __serialize_dict(parent_elem, data_dict):
    for k, v in data_dict.iteritems():
        if isinstance(v, (list, tuple)):
            __serialize_list(parent_elem, v, k)
        else:
            key_elem = Element(k)
            parent_elem.append(key_elem)
            __serialize(key_elem, v)

