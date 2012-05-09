from __future__ import with_statement
import re
import os.path
import mimetypes
import getpass
from distutils.core import Command
from distutils.errors import DistutilsOptionError

__author__ = 'Hong Minhee'
__email__ = 'minhee' '@' 'dahlia.kr'
__copyright__ = 'Copyright 2012, Hong Minhee'
__license__ = 'Public Domain'
__version__ = '0.1.1'


class BitbucketClient(object):
    """Minimal Bitbucket that signs in and uploads files."""

    def __init__(self, username, password, repository):
        import requests  # IF YOU SEE ImportError, DO `easy_install requests`
        self.session = requests.session(
        )  # IF YOU SEE AttributeError, DO `easy_install -U request`
        self.signin(username, password)
        self.repository = repository

    def signin(self, username, password):
        url = 'https://bitbucket.org/account/signin/'
        form = self.session.get(url)
        token = self._find_field(form.content, 'csrfmiddlewaretoken')
        data = {'username': username, 'password': password,
                'csrfmiddlewaretoken': token}
        login = self.session.post(url, data=data, cookies=form.cookies,
                                  headers={'Referer': url})
        self.cookies = login.cookies

    def upload(self, filename):
        try:
            from collections import OrderedDict as odict
        except ImportError:
            from odict \
            import odict  # IF YOU SEE ImportError, DO `easy_install odict`
        url = 'https://bitbucket.org/' + self.repository + '/downloads'
        s3_url = 'https://bbuseruploads.s3.amazonaws.com/'
        fields = ('acl', 'success_action_redirect', 'AWSAccessKeyId',
                  'Policy', 'Signature', 'Content-Type', 'key')
        form = self.session.get(url, cookies=self.cookies)
        data = odict((f, self._find_field(form.content, f)) for f in fields)
        basename = os.path.basename(filename)
        data['Content-Type'] = mimetypes.guess_type(filename)[0]
        data['key'] += basename
        class FoolishHack(object):
            """requests doesn't maintain form fields' order, so we have to
            do workaround it.  Works with requests==0.10.8"""
            def __init__(self, odict):
                self.odict = odict
            def copy(self):
                return self.odict
        with open(filename, 'rb') as fp:
            files = {'file': (basename, fp)}
            response = self.session.post(s3_url, data=FoolishHack(data),
                                         files=files)
        if 300 <= response.status_code < 400 and 'location' in response.headers:
            response = self.session.get(response.headers['location'])
        return url + '/' + basename

    def _find_field(self, form_string, name):
        pattern = (r'<input\s[^<>]*name=[\'"]' + re.escape(name) +
                   r'[\'"]\s[^>]*>')
        tag = re.search(pattern, form_string)
        token = re.search(r'value=[\'"]([^\'"]+)[\'"]', tag.group(0))
        return token.group(1)


class UploadCommand(Command):
    """Upload package to Bitbucket."""

    description = __doc__
    user_options = [
        ('bb-repository=', 'R', 'Bitbucket repository name e.g. user/reponame'),
        ('bb-username=', 'u', 'Bitbucket username'),
        ('bb-password=', 'p', 'Bitbucket password')
    ]

    def initialize_options(self):
        self.bb_repository = ''
        self.bb_username = ''
        self.bb_password = ''
        self.bb_password_prompt = False

    def finalize_options(self):
        if not self.bb_username:
            self.bb_username = raw_input('Bitbucket username: ')
        if not self.bb_password:
            self.bb_password = getpass.getpass('Bitbucket password: ')
        if not re.match(r'^[-_.a-z]+/[-_.a-z]+$', self.bb_repository):
            raise DistutilsOptionError('-R/--bb-repository option is incorrect')

    def run(self):
        if not self.distribution.dist_files:
            raise DistutilsOptionError(
                'No dist file created in earlier command'
            )
        bb = BitbucketClient(self.bb_username,
                             self.bb_password,
                             self.bb_repository)
        sdist_url = None
        for command, pyversion, filename in self.distribution.dist_files:
            url = bb.upload(filename)
            if command == 'sdist':
                sdist_url = url
        if sdist_url:
            url = sdist_url
        self.distribution.metadata.download_url = url


upload = UploadCommand
commands = {'upload': upload}

