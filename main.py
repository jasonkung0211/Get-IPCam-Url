#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import argparse
from WSDiscovery import WSDiscovery
from urlparse import urlparse
import subprocess
from onvif import ONVIFCamera


# def getStreamUriFromIP(ip=""):
#     try:
#         mycam = ONVIFCamera(IP, 80, 'user', '12345678')
#     except:
#         return None
#     media_service = mycam.create_media_service()
#     #profiles = media_service.GetProfiles()
#     #token = profiles[0]._token
#     uri = media_service.GetStreamUri()
#
#     return (uri.Uri).replace("rtsp://", "rtsp://" + "user" + ":" + "12345678" + "@")

def getMACaddrFromIP(ip=""):
    p = subprocess.Popen(['arp', '-n'], stdout=subprocess.PIPE)
    out = p.communicate()[0]
    try:
        arp = [x for x in out.split('\n') if ip in x][0]
        return ' '.join(arp.split()).split()[2]
    except IndexError:
        return None


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
        for camera in IPC:
            selected = urlparse(camera)
            IP = str(selected.netloc).replace(":80", "")
            # print IP and MAC
            print IP
            print str(getMACaddrFromIP(IP)).replace(":", "-")
