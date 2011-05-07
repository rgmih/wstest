'''
Created on May 7, 2011

@author: gleb
'''
from wstest import WSTest

if __name__ == '__main__':
    wst = WSTest()
    # response = wst.on("http://google.com/").get();
    response = wst.on(
        "http://localhost:6500/event/NotificationProducer/",
        headers = {'Content-Type':'application/soap+xml'}
    ).post(
        wst.request('1.soap').using(
            consumer = 'http://localhost:8080/server/services/NotificationConsumer/'
        )
    )
    print response.text()