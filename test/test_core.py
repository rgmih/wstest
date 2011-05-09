from wstest.core import WSTest, Request
import os

def test_soap():
    wst = WSTest()
    
    response = wst.on(
        'http://www.w3schools.com/webservices/tempconvert.asmx',
        headers = {'Content-Type':'application/soap+xml'}
    ).post(wst.file('{0}/test_core.soap12'.format(os.path.dirname(__file__))))
    
    assert response.at('/tmp:CelsiusToFahrenheitResponse/tmp:CelsiusToFahrenheitResult',{
        'tmp': 'http://tempuri.org/'
    }) == '-4.9'
    
def test_xml():
    wst = WSTest()
    
    response = wst.on(
        'http://www.w3schools.com/webservices/tempconvert.asmx/CelsiusToFahrenheit',
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    ).post(Request('Celsius=-40'))
    
    assert response.at('/tmp:string',{
        'tmp': 'http://tempuri.org/'
    }) == '-40'
    
def test_json():
    wst = WSTest()
    response = wst.on('http://api.geonames.org/citiesJSON?north=44.1&south=-9.9&east=-22.4&west=55.2&lang=de&username=demo').get()
    assert response.at('/geonames[1]/name') == 'Mexico City'
    