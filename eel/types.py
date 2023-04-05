from __future__ import annotations
from typing import Union, Dict, List, Tuple, Callable, Optional, Any, TYPE_CHECKING
from typing_extensions import Literal, TypedDict, TypeAlias
from bottle import Bottle

# This business is slightly awkward, but needed for backward compatibility,
# because Python <3.10 doesn't support TypeAlias, jinja2 may not be available
# at runtime, and geventwebsocket.websocket doesn't have type annotations so
# that direct imports will raise an error.
if TYPE_CHECKING:
    from jinja2 import Environment
    JinjaEnvironmentT: TypeAlias = Environment
    from geventwebsocket.websocket import WebSocket
    WebSocketT: TypeAlias = WebSocket
else:
    JinjaEnvironmentT: TypeAlias = Any
    WebSocketT: TypeAlias = Any

OptionsDictT = TypedDict(
    'OptionsDictT',
    {
        'mode': Optional[Union[str, Literal[False]]],
        'host': str,
        'port': int,
        'block': bool,
        'jinja_templates': Optional[str],
        'cmdline_args': List[str],
        'size': Optional[Tuple[int, int]],
        'position': Optional[Tuple[int, int]],
        'geometry': Dict[str, Tuple[int, int]],
        'close_callback': Optional[Callable[..., Any]],
        'app_mode': bool,
        'all_interfaces': bool,
        'disable_cache': bool,
        'default_path': str,
        'app': Bottle,
        'shutdown_delay': float,
        'suppress_error': bool,
        'jinja_env': JinjaEnvironmentT,
    },
    total=False
)
