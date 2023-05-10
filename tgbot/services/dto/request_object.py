import copy
from dataclasses import dataclass
from typing import Optional, Mapping, Any

from aiohttp.typedefs import StrOrURL, LooseCookies, LooseHeaders


@dataclass
class RequestObject:
    method: str
    url: StrOrURL
    timeout: int = None
    params: Optional[Mapping[str, Any]] = None
    data: Any = None
    json: Any = None
    cookies: Optional[LooseCookies] = None
    headers: Optional[LooseHeaders] = None
    proxy: str = None

    def copy(self):
        return copy.deepcopy(self)
