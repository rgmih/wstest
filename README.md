wstest
======

You may use this compact framework to create web-service unit tests quickly and easily.

Example
-------

Less words, more examples.

```python
from wstest.core import WSTest, Request
import os

def test_soap():
    wst = WSTest()
    
    response = wst.on(
        'http://www.w3schools.com/webservices/tempconvert.asmx',
        headers = {'Content-Type':'application/soap+xml'}
    ).post(wst.file('test_core.soap12').using(celsius=-20.5))
    
    assert response.at('/tmp:CelsiusToFahrenheitResponse/tmp:CelsiusToFahrenheitResult',{
        'tmp': 'http://tempuri.org/'
    }) == '-4.9'
```