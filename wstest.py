'''
Created on May 6, 2011

@author: gleb.rybakov
'''

import urllib2
import libxml2

class Request():
    def __init__(self,text):
        self.__text = text
    def using(self,**kwargs):
        return Request(self.__text.format(**kwargs))
    def text(self):
        return self.__text

class Response():
    def __init__(self,wst,text):
        self.__wst  = wst
        self.__text = text
    def at(self,path,nsmapping={}):
        doc = libxml2.parseDoc(self.__text)
        xp = doc.xpathNewContext()
        for (prefix,ns) in dict(self.__wst.nsmapping, **nsmapping).iteritems():
            xp.xpathRegisterNs(prefix,ns)
        a = xp.xpathEval(path)
        if len(a) == 0:
            return None
        elif len(a) == 1:
            return a[0].content
        else:
            return a
    def text(self):
        return self.__text

class HTTPResponse(Response):
    def __init__(self,wst,url):
        self.url = url
        Response.__init__(self,wst,url.read())
        self.url.close()
    
    def header(self,name):
        return self.url.info().getheader(name)

class HTTPEndpoint():
    def __init__(self,wst,url,**kwargs):
        self.__wst = wst
        self.url = url
        self.headers = kwargs.get('headers',{})
        # split parameters from URL ?
        pass
    def post(self,request,header={},param=[]):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        http_request = urllib2.Request(self.url,data=request.text(),headers=self.headers)
        url = opener.open(http_request)
        return HTTPResponse(self.__wst,url)
    
    def get(self,header={},param=[]):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        http_request = urllib2.Request(self.url,headers=self.headers)
        url = opener.open(http_request)
        return HTTPResponse(self.__wst,url)

class WSTest():
    
    def __init__(self):
        self.nsmapping = {}
    def on(self,uri,**kwargs):
        # different protocol bindings may be added
        return HTTPEndpoint(self,uri,**kwargs)
    
    def file(self,path):
        f = open(path)
        return Request(f.read())
