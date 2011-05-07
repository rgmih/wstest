'''
Created on May 6, 2011

@author: gleb.rybakov
'''

import urllib2

class Request():
    def __init__(self,text):
        self.__text = text
    def using(self,**kwargs):
        return Request(self.__text.format(**kwargs))
    def text(self):
        return self.__text

class Response():
    def __init__(self,text):
        self.__text = text
    def at(self,path):
        pass
    def text(self):
        return self.__text

class HTTPResponse(Response):
    def __init__(self,url):
        self.url = url
        Response.__init__(self, url.read())
        self.url.close()
    
    def header(self,name):
        return self.url.info().getheader(name)

class HTTPEndpoint():
    def __init__(self,url,**kwargs):
        self.url = url
        self.headers = kwargs.get('headers',{})
        # split parameters from URL ?
        pass
    def post(self,request,header={},param=[]):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        http_request = urllib2.Request(self.url, data=request.text(), headers=self.headers)
        url = opener.open(http_request)
        return HTTPResponse(url)
    
    def get(self,header={},param=[]):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        http_request = urllib2.Request(self.url, headers=self.headers)
        url = opener.open(http_request)
        return HTTPResponse(url)

class WSTest():
    
    def on(self,uri,**kwargs):
        # different protocol bindings may be added
        return HTTPEndpoint(uri,**kwargs)
    
    def file(self,path):
        f = open(path)
        return Request(f.read())
