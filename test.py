'''
Created on May 7, 2011

@author: gleb.rybakov
'''
from wstest import WSTest

if __name__ == '__main__':
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
    # print response.text()
    print response.at('/soap:Envelope/soap:Header/wsa:Action1')