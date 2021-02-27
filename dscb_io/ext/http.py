import aiohttp
import urllib.parse
from quart import request
from .exceptions import *
from .base import *
import json
from .models.user import User
from .models.guild import Guild
from quart import session
import asyncio
from authlib.integrations.httpx_client import AsyncOAuth2Client


class AioClient:
    def __init__(self, app):
        self.client_id = app.config['DISCORD_CLIENT_ID']
        self.client_secret = app.config['DISCORD_CLIENT_SECRET']
        self.scopes = app.config['SCOPES']
        self.redirect_url = app.config['DISCORD_REDIRECT_URI']
        self.discord_bot_token = app.config['DISCORD_BOT_TOKEN']
        self.token_url = 'https://discordapp.com/api/oauth2/token'
        # base_redirect = 'https://discord.com/api/oauth2/authorize?'
        # url_variables = {'client_id': self.client_id, 'redirect_url': self.redirect_url,
        #                  'response_type': 'code'}
        # self.redirect_url = base_redirect + urllib.parse.urlencode(url_variables)
        # if self.scopes:
        #     self.redirect_url += ('&scope=' + '%20'.join(self.scopes))

    @staticmethod
    def token_updater(token):
        session["DISCORD_OAUTH2_TOKEN"] = token

    @staticmethod
    def token_remover():
        session["DISCORD_OAUTH2_TOKEN"] = None

    @staticmethod
    async def _request(**kwargs):
        try:
            async with aiohttp.ClientSession(read_timeout=5) as res:
                _method = getattr(res, kwargs.pop('type'))
                return await _method(**kwargs)
        except asyncio.TimeoutError:
            raise Unauthorized

    async def _make_session(self, token=None, scope=None, state=None):
        if scope is None:
            scope = self.scopes or ['identify', 'guilds']
        return AsyncOAuth2Client(client_id=self.client_id,
                                 client_secret=self.client_secret,
                                 scope=scope,
                                 state=state or session.get("DISCORD_OAUTH2_STATE"),
                                 token=token or session.get("DISCORD_OAUTH2_TOKEN"),
                                 redirect_uri=self.redirect_url,
                                 auto_refresh_kwargs={
                                     'client_id': self.client_id,
                                     'client_secret': self.client_secret,
                                 },
                                 auto_refresh_url=self.token_url)

    # async def callback(self):
    #     code = request.args.get('code')
    #     payload = {
    #         'client_id': self.client_id,
    #         'client_secret': self.client_secret,
    #         'grant_type': 'authorization_code',
    #         'code': code,
    #         'redirect_url': self.redirect_url,
    #         'scope': '%20'.join(self.scopes)
    #     }
    #
    #     headers = {
    #         'Content-type': 'application/x-www-form-urlencoded'
    #     }
    #     access_token = await self._request(type='post', url=self.token_url, data=payload, headers=headers)
    #     if access_token.status != 200:
    #         raise Unauthorized
    #     return await access_token.json()

    async def fetch_user(self):
        discord = await self._make_session()
        response = await discord.request('get', DISCORD_API_BASE_URL + "/users/@me")
        if response.status_code == 401:
            raise Unauthorized
        elif response.status_code == 429:
            raise Ratelimited
        elif response.status_code != 200:
            raise OAuthError
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = response.text
        return User(data)
        # access_token = session.get('DISCORD_OAUTH2_TOKEN')
        # url = DISCORD_API_BASE_URL + '/users/@me'
        # headers = {
        #     "Authorization": "Bearer {}".format(access_token)
        # }
        # data = await AioClient._request(type='get', url=url, headers=headers)
        # if data.status == 401:
        #     raise Unauthorized
        # try:
        #     response = await data.json()
        # except json.decoder.JSONDecodeError:
        #     response = await data.text()
        # return User(response)

    async def fetch_guilds(self):
        discord = await self._make_session()
        response = await discord.request('get', DISCORD_API_BASE_URL+ '/users/@me/guilds')
        if response.status_code == 401:
            raise Unauthorized
        elif response.status_code == 429:
            raise Ratelimited
        elif response.status_code != 200:
            raise OAuthError
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = response.text
        return [Guild(datum) for datum in data]
        # access_token = session.get('DISCORD_OAUTH2_TOKEN')
        # url = DISCORD_API_BASE_URL + '/users/@me/guilds'
        # headers = {
        #     "Authorization": "Bearer {}".format(access_token)
        # }
        # data = await AioClient._request(type='get', url=url, headers=headers)
        # if data.status == 401:
        #     raise Unauthorized
        # try:
        #     response = await data.json()
        # except json.decoder.JSONDecodeError:
        #     response = await data.text()
        # list_ = []
        # for res in response:
        #     list_.append(Guild(res))
        # return list_

