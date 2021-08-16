import aiohttp
from aiohttp.client_exceptions import ClientConnectorError


class PasteBin:

    DOGBIN_URL = "https://del.dog/"
    HASTEBIN_URL = "https://hastebin.com/"
    NEKOBIN_URL = "https://nekobin.com/"
    KATBIN_URL = "https://katb.in/"
    _dkey = _hkey = _nkey = _kkey = retry = None
    service_match = {
        "-d": "dogbin",
        "-n": "nekobin",
        "-h": "hastebin",
        "-k": "katbin"}

    def __init__(self, data: str = None):
        self.http = aiohttp.ClientSession()
        self.data = data
        self.retries = 4

    def __bool__(self):
        return bool(self._dkey or self._nkey or self._hkey or self._kkey)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    async def close(self):
        await self.http.close()

    async def __call__(self, service="dogbin"):
        if service == "dogbin":
            await self._post_dogbin()
        elif service == "nekobin":
            await self._post_nekobin()
        elif service == "hastebin":
            await self._post_hastebin()
        elif service == "katbin":
            await self._post_katbin()
        else:
            raise KeyError(f"Unknown service input: {service}")

    async def _post_dogbin(self):
        if self._dkey:
            return
        try:
            async with self.http.post(
                self.DOGBIN_URL + "documents", data=self.data.encode("utf-8")
            ) as req:
                if req.status == 200:
                    res = await req.json()
                    self._dkey = res["key"]
                else:
                    self.retry = "nekobin"
        except ClientConnectorError:
            self.retry = "nekobin"

    async def _post_nekobin(self):
        if self._nkey:
            return
        try:
            async with self.http.post(
                self.NEKOBIN_URL + "api/documents", json={"content": self.data}
            ) as req:
                if req.status == 201:
                    res = await req.json()
                    self._nkey = res["result"]["key"]
                else:
                    self.retry = "hastebin"
        except ClientConnectorError:
            self.retry = "hastebin"

    async def _post_hastebin(self):
        if self._hkey:
            return
        try:
            async with self.http.post(
                self.HASTEBIN_URL + "documents", data=self.data.encode("utf-8")
            ) as req:
                if req.status == 200:
                    res = await req.json()
                    self._hkey = res["key"]
                else:
                    self.retry = "katbin"
        except ClientConnectorError:
            self.retry = "katbin"

    async def _post_katbin(self):
        if self._kkey:
            return
        try:
            async with self.http.post(
                "https://api.katb.in/api/paste", json={"content": self.data}
            ) as req:
                if req.status == 201:
                    res = await req.json()
                    self._kkey = res["paste_id"]
                else:
                    self.retry = "dogbin"
        except ClientConnectorError:
            self.retry = "dogbin"

    async def post(self, serv: str = "dogbin"):
        """Post the initialized data to the pastebin service."""
        if self.retries == 0:
            return

        await self.__call__(serv)

        if self.retry:
            self.retries -= 1
            await self.post(self.retry)
            self.retry = None

    @property
    def link(self) -> str:
        """Return the view link"""
        if self._dkey:
            return self.DOGBIN_URL + self._dkey
        if self._nkey:
            return self.NEKOBIN_URL + self._nkey
        if self._hkey:
            return self.HASTEBIN_URL + self._hkey
        if self._kkey:
            return self.KATBIN_URL + self._kkey
        return False

    @property
    def raw_link(self) -> str:
        """Return the view raw link"""
        if self._dkey:
            return self.DOGBIN_URL + "raw/" + self._dkey
        if self._nkey:
            return self.NEKOBIN_URL + "raw/" + self._nkey
        if self._hkey:
            return self.HASTEBIN_URL + "raw/" + self._hkey
        if self._kkey:
            return self.KATBIN_URL + "raw/" + self._kkey
        return False
