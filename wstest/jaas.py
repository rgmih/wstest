"""This module provides Java Authentication and Authorization
Service (JAAS) related utility functions.
"""

import urllib2
import urllib
import re

def do_login(url, username, password):
    """Performs login to URL protected with JAAS"""
    
    def parse_jsessionid(response):
        """Parses cookie string and returns JAAS session identifier."""
        cookie = response.info().getheader('Set-Cookie')
        return re.match(r'JSESSIONID=(\w*)', cookie).group(1)
    
    # GET
    response = urllib2.urlopen(url)
    jsessionid = parse_jsessionid(response)
    
    # POST j_username, j_password
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    request = urllib2.Request(url + 'j_security_check',
        urllib.urlencode({
            'j_username': username,
            'j_password': password                    
        }),
        {'Cookie': 'JSESSIONID={0};'.format(jsessionid)}
    )
    response = opener.open(request)
    return parse_jsessionid(response)