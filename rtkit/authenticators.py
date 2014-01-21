"""Connect to an RT server using various authentication techniques

* The :py:class:`~rtkit.authenticators.AbstractAuthenticator` contains the base methods
* And the current implementations are:
    * :py:class:`~rtkit.authenticators.BasicAuthenticator`
    * :py:class:`~rtkit.authenticators.CookieAuthenticator`
    * :py:class:`~rtkit.authenticators.KerberosAuthenticator`

.. seealso::

    :py:mod:`rtkit.resource` for usage


"""
import os
import sys
import urllib
import urllib2
import cookielib

__all__ = [
    'BasicAuthenticator',
    'CookieAuthenticator',
    'KerberosAuthenticator',
]
if os.environ.get('__GEN_DOCS__', None):
    __all__.insert(0, "AbstractAuthenticator")


class AbstractAuthenticator(object):
    """Abstract Base Authenticator"""
    def __init__(self, username, password, url, *handlers):
        """
        :param username: The RT Login
        :param password: Plain Text Password
        :param url: the url ?
        :param *handlers: todo
        """
        self.opener = urllib2.build_opener(*handlers)
        self.username = username
        self.password = password
        self.url = url
        self._logged = True

    def login(self):
        """Login to server, unless already logged in"""
        if self._logged:
            return
        self._login()
        self._logged = True

    def _login(self):
        raise NotImplementedError

    def open(self, request):
        """Open connection to server"""
        self.login()
        return self.opener.open(request)


class BasicAuthenticator(AbstractAuthenticator):
    """Basic Authenticator

    .. doctest::

        from rtkit.resource import RTResource
        from rtkit.authenticators import BasicAuthenticator
        from rtkit.errors import RTResourceError

        from rtkit import set_logging
        import logging
        set_logging('debug')
        logger = logging.getLogger('rtkit')

        resource = RTResource('http://<HOST>/REST/1.0/', '<USER>', '<PWD>', BasicAuthenticator)
    """
    def __init__(self, username, password, url):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, username, password)
        super(BasicAuthenticator, self).__init__(
            username, password, url,
            urllib2.HTTPBasicAuthHandler(passman)
        )


class CookieAuthenticator(AbstractAuthenticator):
    """Authenticate against server using a cookie

    .. doctest::

        from rtkit.resource import RTResource
        from rtkit.authenticators import CookieAuthenticator
        from rtkit.errors import RTResourceError

        from rtkit import set_logging
        import logging
        set_logging('debug')
        logger = logging.getLogger('rtkit')

        resource = RTResource('http://<HOST>/REST/1.0/', '<USER>', '<PWD>', CookieAuthenticator)
    """
    def __init__(self, username, password, url):
        super(CookieAuthenticator, self).__init__(
            username, password, url,
            urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar())
        )
        self._logged = False

    def _login(self):
        data = {'user': self.username, 'pass': self.password}

        urlencoded_data = urllib.urlencode(data)
        if sys.version_info > (2,7):
            urlencoded_data = urlencoded_data.encode()

        self.opener.open(
            urllib2.Request(self.url, urlencoded_data)
        )


class KerberosAuthenticator(AbstractAuthenticator):
    """Authenticate using Kerberos

    .. warning::

        * Requires the urllib2_kerberos
        * http://pypi.python.org/pypi/urllib2_kerberos/
        * sudo easy_install urllib2_kerberos

    .. doctest::

        from rtkit.resource import RTResource
        from rtkit.authenticators import KerberosAuthenticator
        from rtkit.errors import RTResourceError

        from rtkit import set_logging
        import logging
        set_logging('debug')
        logger = logging.getLogger('rtkit')

        resource = RTResource(url, None, None, KerberosAuthenticator)
    """
    def __init__(self, username, password, url):
        try:
            from urllib2_kerberos import HTTPKerberosAuthHandler
        except ImportError:
            raise ImportError('You need urllib2_kerberos, try: pip install urllib2_kerberos')

        super(KerberosAuthenticator, self).__init__(
            username, password, url,
            HTTPKerberosAuthHandler()
        )
