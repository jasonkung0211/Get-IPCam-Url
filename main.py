#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
from WSDiscovery import WSDiscovery
from urlparse import urlparse, parse_qs
#from urllib.parse import urlparse, parse_qs

from onvif import ONVIFCamera

def Onvifdiscovery(retries=3):
    wsd = WSDiscovery()
    wsd.start()
    resp = []
    ipclist = []
    a = 0
    while not resp and a < retries:
        ret = wsd.searchServices()
        wsd._sendProbe()
        a = a + 1
        for service in ret:
            tmp = urlparse(service.getXAddrs()[0])
            if (tmp.path.find("/onvif/device_service")) >= 0:
                resp.append(service.getXAddrs()[0])

    if len(resp) > 1:
        for camera in resp:
            selected = urlparse(camera)
            ipclist.append(selected.netloc)

    return resp


if __name__ == "__main__":
    IPC = []
    token = ''
    IPC = Onvifdiscovery()

    if len(IPC) < 1:
        pass
    else:
        #print IPC
        for camera in IPC:
            selected = urlparse(camera)
            try:
                mycam = ONVIFCamera(selected.netloc, 80, 'user', '12345678')
            except:
                continue
            media_service = mycam.create_media_service()
            profiles = media_service.GetProfiles()
            token = profiles[0]._token
            uri = media_service.GetStreamUri()

            print (uri.Uri).replace("rtsp://", "rtsp://" + "user" + ":" + "12345678" + "@")
