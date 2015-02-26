#!/usr/bin/env python
"""fritz box api calls for python"""
import requests
import md5
import xml.etree.ElementTree as ET
import re
import logging


PASSWORD = 'secret Password'


class Frytz(object):
    """class for interaction with the FRITZ!Box(R)"""

    def __init__(self, domain='fritz.box', password=''):
        self.domain = 'http://' + domain
        self.base = '{}/cgi-bin/webcm'.format(self.domain)
        self.post_base = "getpage=../html/de/menus/menu2.html&var:lang=de"
        self.headers = {'content-type': "application/x-www-form-urlencoded"}
        self.password = password
        self.sid = self._get_sid()

    def _get_sid(self):
        """
        gets a sesion id

        see [1] for details

        [1] http://www.avm.de/de/Extern/files/session_id/AVM_Technical_Note_-_Session_ID.pdf
        """
        response = requests.get('{}/login_sid.lua'.format(self.domain))
        tree = ET.fromstring(response.content)
        for one in tree.findall('Challenge'):
            challenge = one.text
        md5sum = md5.new((challenge + "-" + self.password).encode('utf-16LE'))
        md5sum = md5sum.hexdigest()
        fresponse = challenge + '-' + md5sum
        #parameter = "&login:command/response={}".format(fresponse)
        response = requests.get(
            '{}/login_sid.lua?username=&response={}'.format(self.domain, fresponse),
            headers=self.headers
        )
        # we are looking for something like this:
        # <SID>0123456789abcdef</SID>
        match = re.search(r'\<SID\>([^<]+)\</SID\>', response.text)
        if match:
            sid = match.groups()[0]
        else:
            logging.error('could not get sid')
            logging.error('response was:')
            logging.error(response.content)
            raise Exception('could not get sid')
        return sid

    def dial(self, number):
        """dial number

        pick up the default phone
        """
        url = self.base
        data = ('{post_base}&sid={sid}&telcfg:settings/UseClickToDial=1&'
                'telcfg:command/Dial={number}')
        data = data.format(post_base=self.post_base, number=number, sid=self.sid)
        response = requests.post(url, data=data, headers=self.headers)
        if response.text != u'':
            logging.error(response.text)

    def get_wanip(self):
        """getting the external IP of the FritzBox"""
        # XXX does not work
        service_type = 'urn:schemas-upnp-org:service:WANIPConnection:1'
        name = 'GetStatusInfo'
        headers = {'soapaction': '',
                   'content-type': 'text/xml',
                   'charset': 'utf-8',
                   }
        template = """
            <?xml version="1.0" encoding="utf-8"?>
            <s:Envelope s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
                        xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
            <s:Body>
            <u:{service_type} xmlns:u="{name}" />
            </s:Body>
            </s:Envelope>
            """
        headers['soapaction'] = '%s#%s' % (service_type, name)
        data = template.format(name=name, service_type=service_type)
        response = requests.post(self.domain, data=data, headers=headers)
        return response


if __name__ == '__main__':
    import sys
    frytz = Frytz(password=PASSWORD)
    if sys.argv[1].startswith('-'):
        print('usage: frytz.py +492219876543')
    else:
        frytz.dial(sys.argv[1])
