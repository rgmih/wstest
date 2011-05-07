'''
Created on May 7, 2011

@author: gleb.rybakov
'''
from wstest import WSTest

def test_json():
    wst = WSTest()
    response = wst.on('http://api.geonames.org/citiesJSON?north=44.1&south=-9.9&east=-22.4&west=55.2&lang=de&username=demo').get()
    assert response.at('/geonames[0]/name') == 'Mexico City'
    
def test_soap():
    wst = WSTest()
    wst.nsmapping['soap'] = 'http://www.w3.org/2003/05/soap-envelope'
    wst.nsmapping['wsa']  = 'http://www.w3.org/2005/08/addressing'
    
    response = wst.on(
        "http://localhost:6500/onvif/device/",
        headers = {'Content-Type':'application/soap+xml'}
    ).post(wst.file('1.soap'))
    
    assert response.at('/soap:Envelope/soap:Body/d:GetDeviceInformationResponse/d:Manufacturer',{
        'd':'http://www.onvif.org/ver10/device/wsdl'
    }) == 'ITRIUM-SPb'
    
def test_xml():
    wst = WSTest()

    response = wst.on('http://api.geonames.org/cities?north=44.1&south=-9.9&east=-22.4&west=55.2&username=demo').get()
    assert response.at('/geonames/geoname[1]/name') == 'Mexico City'