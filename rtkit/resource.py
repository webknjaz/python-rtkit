import logging
import re
import os
import sys
from urllib2 import Request, HTTPError
from rtkit import forms, errors
from rtkit.parser import RTParser


class RTResource(object):
    """REST Resource Object"""
    def __init__(self, url, username, password, auth, **kwargs):
        """Create Connection Object

        :param url: Server URL
        :param username: RT Login
        :param password: Password
        :param auth: Instance of :py:mod:`rtkit.authenticators`
        """
        self.auth = auth(username, password, url)
        self.response_cls = kwargs.get('response_class', RTResponse)
        self.logger = logging.getLogger('rtkit')

    def get(self, path=None, headers=None):
        """GET from the server"""
        return self.request('GET', path, headers=headers)

    def post(self, path=None, payload=None, headers=None):
        """POST to the server"""
        return self.request('POST', path, payload, headers)

    def request(self, method, path=None, payload=None, headers=None):
        """Make request to server"""
        headers = headers or dict()
        headers.setdefault('Accept', 'text/plain')
        if payload:
            payload = forms.encode(payload, headers)
        self.logger.debug('{0} {1}'.format(method, path))
        self.logger.debug(headers)
        self.logger.debug('%r' % payload)
        req = Request(
            url=self.auth.url + path,
            data=payload,
            headers=headers,
        )
        try:
            response = self.auth.open(req)
        except HTTPError as e:
            response = e
        return self.response_cls(req, response)

    @classmethod
    def from_rtrc(cls, auth, filename=None, **kwargs):
        try:
            with open(filename or os.path.expanduser("~/.rtrc"), 'r') as fd:
                config = dict([re.split('\s+', line.strip(), maxsplit=1) for line in fd.readlines()])
            return cls(
                '{0}/REST/1.0/'.format(config['server']),
                config['user'],
                config['passwd'],
                auth,
                **kwargs
            )
        except (KeyError, IOError):
            raise errors.RTBadConfiguration


class RTResponse(object):
    """Represents the REST response from server"""
    def __init__(self, request, response):
        self.headers = response.headers
        """Headers as dict"""

        self.body = response.read()
        """Request Body"""

        if sys.version_info > (2,7):
            self.body = self.body.decode()

        self.status_int = response.code
        """Status Code"""

        self.status = '{0} {1}'.format(response.code, response.msg)
        """Status String"""

        self.logger = logging.getLogger('rtkit')
        """Logger"""

        self.logger.info(request.get_method())
        self.logger.info(request.get_full_url())
        self.logger.debug('HTTP_STATUS: {0}'.format(self.status))
        r = RTParser.HEADER.match(self.body)
        if r:
            self.status = r.group('s')
            self.status_int = int(r.group('i'))
        else:
            self.logger.error('"{0}" is not valid'.format(self.body))
            self.status = self.body
            self.status_int = 500
        self.logger.debug('%r' % self.body)

        self.parsed = None
        """A List of Tuples of  data"""
        try:
            decoder = RTParser.decode
            if self.status_int == 409:
                decoder = RTParser.decode_comment
            self.parsed = RTParser.parse(self.body, decoder)
        except errors.RTResourceError as e:
            self.parsed = []
            self.status_int = e.status_int
            self.status = '{0} {1}'.format(e.status_int, e.msg)
        self.logger.debug('RESOURCE_STATUS: {0}'.format(self.status))
        self.logger.info(self.parsed)
