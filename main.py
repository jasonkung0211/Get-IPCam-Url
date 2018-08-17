#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from WSDiscovery import WSDiscovery
from urlparse import urlparse
import subprocess


def getMACaddrFromIP(ip=""):
    # nmap -sP 192.168.*.*
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
    a = 0
    while not resp and a < retries:
        ret = wsd.searchServices()
        wsd._sendProbe()
        a = a + 1
        for service in ret:
            tmp = urlparse(service.getXAddrs()[0])
            if (tmp.path.find("/onvif/device_service")) >= 0:
                resp.append(service.getXAddrs()[0])

    return resp


if __name__ == "__main__":
    IPC = Onvifdiscovery()
    if len(IPC) >= 1:
        for camera in IPC:
            selected = urlparse(camera)
            IP = str(selected.netloc).replace(":80", "")
            # print IP and MAC
            print IP, str(getMACaddrFromIP(IP)).replace(":", "")