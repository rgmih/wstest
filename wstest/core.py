'''
Created on May 6, 2011

@author: gleb.rybakov
'''

import urllib2
import libxml2
import json2xml

class Request():
    def __init__(self, text):
        self.__text = text
    def using(self, **kwargs):
        return Request(self.__text.format(**kwargs))
    def text(self):
        return self.__text

class DynamicObject:
    pass

def xml_to_object(node):
    
    result = DynamicObject()
    count = 0
    for child in node.children:
        if child.type == "element":
            setattr(result, child.name, xml_to_object(child))
            count += 1
    if count == 0:
        return child.content
    else:
        return result

def evaluate_xpath(text, path, nsmapping):
    doc = libxml2.parseDoc(text)
    xpc = doc.xpathNewContext()
    try:
        for (prefix, namespace) in nsmapping.iteritems():
            xpc.xpathRegisterNs(prefix, namespace)
        nodes = xpc.xpathEval(path)
        print(path)
        print(len(nodes))
        if len(nodes) == 0:
            root = doc.getRootElement()
            if root.name == 'Envelope' and \
                    root.ns().content == 'http://www.w3.org/2003/05/soap-envelope':
                # try starting from /envelope/body
                xpc.xpathRegisterNs('soap12','http://www.w3.org/2003/05/soap-envelope')
                nodes = xpc.xpathEval('/soap12:Envelope/soap12:Body')
                if len(nodes) > 0:
                    xpc.setContextNode(nodes[0])
                    nodes = xpc.xpathEval(path[1:]) # make path relative
        if len(nodes) == 0:
            return None
        elif len(nodes) == 1:
            return xml_to_object(nodes[0])
        else:
            result = []
            for node in nodes:
                result.append(xml_to_object(node))
            return result
    finally:
        xpc.xpathFreeContext()
        doc.freeDoc()

class Response():
    def __init__(self, wst, text):
        self.__wst  = wst
        self.__text = text
        
    def at(self, path, nsmapping={}):
        if self.__text.strip().startswith('<'): # XML
            full_nsmapping = dict(self.__wst.nsmapping, **nsmapping)
            return evaluate_xpath(self.__text, path, full_nsmapping)
        else: # JSON
            xml = json2xml.to_xml(self.__text)
            return evaluate_xpath(xml, '/json/' + path, nsmapping)
            
    def text(self):
        return self.__text

class HTTPResponse(Response):
    def __init__(self, wst, url):
        self.url = url
        Response.__init__(self, wst, url.read())
        self.url.close()
    
    def header(self, name):
        return self.url.info().getheader(name)

class HTTPEndpoint():
    def __init__(self, wst, url, **kwargs):
        self.__wst = wst
        self.url = url
        self.headers = kwargs.get('headers', {})
        # split parameters from URL ?
        pass
    def post(self, request, header={}, param=[]):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        http_request = urllib2.Request(self.url, request.text(), self.headers)
        url = opener.open(http_request)
        return HTTPResponse(self.__wst, url)
    
    def get(self, header={}, param=[]):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        http_request = urllib2.Request(self.url, headers=self.headers)
        url = opener.open(http_request)
        return HTTPResponse(self.__wst, url)

class WSTest():
    
    def __init__(self):
        self.nsmapping = {}
    def on(self, uri, **kwargs):
        # different protocol bindings may be added
        return HTTPEndpoint(self, uri, **kwargs)
    
    def file(self, path):
        f = open(path)
        return Request(f.read())
