import limedio.cli
import campussquare
from limedio.limedio import LimedioLibrary
from uecauth.shibboleth import ShibbolethAuthenticator
from uecauth.password import DefaultPasswordProvider, PromptingPasswordProvider
from uecauth.mfa import AutoTOTPMFAuthCodeProvider, PromptingMFAuthCodeProvider

import campussquare.cli
from campussquare.util import get_flow_execution_key
from campussquare import CampusSquare

import os
import sys


def shibboleth_login(url: str) -> None:
    shibboleth_host = 'shibboleth.cc.uec.ac.jp'
    shibboleth_cookies_path = os.path.expanduser('~/.uecli.cookies.lwp')

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

    return ShibbolethAuthenticator(
        shibboleth_host=shibboleth_host,
        mfa_code_provider=mfa_code_provider,
        password_provider=password_provider,
        lwpcookiejar_path=shibboleth_cookies_path,
        debug=False,
    )


class UECCampusSquareAuthenticator(campussquare.cli.Authenticator):
    def __init__(self) -> None:
        self.campusweb_url = 'https://campusweb.office.uec.ac.jp/campusweb/ssologin.do'
        self.campusweb_do_url = 'https://campusweb.office.uec.ac.jp/campusweb/campussquare.do'
        self.campussquare_credentials_path = os.path.expanduser('~/.uecli.campussquare.json')
        self.shibboleth = shibboleth_login(self.campusweb_url)

    def login(self) -> CampusSquare:
        return CampusSquare(
            self.campusweb_do_url,
            None,
            self.shibboleth.get_cookies(),
            credential_path=self.campussquare_credentials_path,
            debug=False
        )

    def refresh(self) -> CampusSquare:
        print('認証情報を更新しています...', file=sys.stderr)
        try:
            res = self.shibboleth.login(self.campusweb_url)
        except Exception as e:
            print(f'認証に失敗しました: {e}', file=sys.stderr)
            exit(1)

        return CampusSquare(
            self.campusweb_do_url,
            get_flow_execution_key(res.url),
            self.shibboleth.get_cookies(),
            credential_path=self.campussquare_credentials_path,
            debug=False
        )


class UECLibraryAuthenticator(limedio.cli.Authenticator):
    def __init__(self) -> None:
        self.url = 'https://www.lib.uec.ac.jp/opac/user/top'
        self.shibboleth = shibboleth_login(self.url)
        self.prefix = 'https://www.lib.uec.ac.jp'

    def login(self) -> LimedioLibrary:
        return LimedioLibrary(
            self.prefix,
            cookies=self.shibboleth.get_cookies()
        )

    def refresh(self) -> LimedioLibrary:
        print('認証情報を更新しています...', file=sys.stderr)
        try:
            self.shibboleth.login(self.url)
        except Exception as e:
            print(f'認証に失敗しました: {e}', file=sys.stderr)
            exit(1)

        return LimedioLibrary(
            self.prefix,
            cookies=self.shibboleth.get_cookies()
        )
