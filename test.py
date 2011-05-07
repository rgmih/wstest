'''
Created on May 7, 2011

@author: gleb.rybakov
'''
from wstest import WSTest

def test_example():
    wst = WSTest()
    wst.nsmapping['soap'] = 'http://www.w3.org/2003/05/soap-envelope'
    wst.nsmapping['wsa']  = 'http://www.w3.org/2005/08/addressing'

    response = wst.on(
        "http://localhost:6500/onvif/device/",
        headers = {'Content-Type':'application/soap+xml'}
    ).post(
        wst.file('1.soap').using(
            consumer = 'http://localhost:8080/server/services/NotificationConsumer/'
        )
    )
    assert response.at('/soap:Envelope/soap:Body/d:GetDeviceInformationResponse/d:Manufacturer',{
        'd':'http://www.onvif.org/ver10/device/wsdl'
    }) == 'ITRIUM-SPb'