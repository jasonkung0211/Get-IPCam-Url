#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from WSDiscovery import WSDiscovery, QName
from urllib.parse import urlparse
from onvif import ONVIFCamera, ONVIFError

import logging
logging.getLogger("requests").setLevel(logging.WARNING)  # disable log messages from the Requests


ONVIF_TYPE = QName('http://www.onvif.org/ver10/network/wsdl', 'NetworkVideoTransmitter')

try_auth = [
    ('admin', 'pass'),  # Lilin
    ('admin', 'dh123456'),  # Dahua
]


def discovery():
    ret = []
    for service in wsd.searchServices(types=[ONVIF_TYPE]):
        url = urlparse(service.getXAddrs()[0])
        scopes = service.getScopes()
        print(" Scopes:")
        for scope in scopes:
            print("  {})".format(repr(scope)))
        ret.append(url)

    return ret


if __name__ == "__main__":
    wsd = WSDiscovery()
    wsd.start()
    all_ipc = discovery()
    started = time.time()
    for cam in all_ipc:
        if cam.port is None:
            port = 80
        else:
            port = cam.netloc.split(':')[1]

        for auth_info in try_auth:
            try:
                IP_cam = ONVIFCamera(cam.hostname, port, auth_info[0], auth_info[1], '/home/jk/.local/lib/python3.5/site-packages/onvif/wsdl')
            except ONVIFError as e:
                # print("ONVIFCamera Got error {}".format(e))
                continue

            try:
                media_service = IP_cam.create_media_service()
                profiles = media_service.GetProfiles()
            except ONVIFError as e:
                # print("GetProfiles Got error {}".format(e))
                continue

            print(" Streams:")

            for profile in profiles:
                try:
                    obj = media_service.create_type('GetStreamUri')
                    obj.ProfileToken = profile.token
                    obj.StreamSetup = {'Stream': 'RTP-Unicast', 'Transport': {'Protocol': 'RTSP'}}
                    resp = media_service.GetStreamUri(obj)
                    print("  {}".format(resp.Uri))
                except ONVIFError as e:
                    print("Got error {} from GetStreamUri({})".format(e, obj))
                    continue
    wsd.stop()
