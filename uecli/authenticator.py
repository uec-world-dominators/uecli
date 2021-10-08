from uecauth.shibboleth import ShibbolethAuthenticator
from uecauth.password import DefaultPasswordProvider, PromptingPasswordProvider
from uecauth.mfa import AutoTOTPMFAuthCodeProvider, PromptingMFAuthCodeProvider

from campussquare.cli import Authenticator
from campussquare.util import get_flow_execution_key
from campussquare import CampusSquare
import os
import sys


class UECCampusSquareAuthenticator(Authenticator):
    def __init__(self) -> None:
        self.campusweb_do_url = 'https://campusweb.office.uec.ac.jp/campusweb/campussquare.do'
        self.campusweb_url = 'https://campusweb.office.uec.ac.jp/campusweb/ssologin.do'
        self.shibboleth_host = 'shibboleth.cc.uec.ac.jp'
        self.shibboleth_cookies_path = os.path.expanduser('~/.uecli.cookies.lwp')
        self.campussquare_credentials_path = os.path.expanduser('~/.uecli.campussquare.json')


        # Shibboleth Login
        # setup password login
        uec_username, uec_password = os.environ.get('UEC_USERNAME'), os.environ.get('UEC_PASSWORD')
        if uec_username and uec_password:
            password_provider = DefaultPasswordProvider(
                os.environ['UEC_USERNAME'],
                os.environ['UEC_PASSWORD']
            )
        else:
            password_provider = PromptingPasswordProvider()

        # setup MF Auth
        uec_mfa_secret = os.environ.get('UEC_MFA_SECRET')
        if uec_mfa_secret:
            mfa_code_provider = AutoTOTPMFAuthCodeProvider(os.environ['UEC_MFA_SECRET'])
        else:
            mfa_code_provider = PromptingMFAuthCodeProvider()

        self.shibboleth = ShibbolethAuthenticator(
            shibboleth_host=self.shibboleth_host,
            mfa_code_provider=mfa_code_provider,
            password_provider=password_provider,
            lwpcookiejar_path=self.shibboleth_cookies_path,
            debug=False,
        )

    def login(self) -> CampusSquare:
        return CampusSquare(
            self.campusweb_do_url,
            None,
            self.shibboleth.get_cookies(),
            credential_path=self.campussquare_credentials_path,
            debug=False
        )

    def refresh(self) -> CampusSquare:
        print('refreshing...', file=sys.stderr)
        res = self.shibboleth.login(self.campusweb_url)
        return CampusSquare(
            self.campusweb_do_url,
            get_flow_execution_key(res.url),
            self.shibboleth.get_cookies(),
            credential_path=self.campussquare_credentials_path,
            debug=False
        )
