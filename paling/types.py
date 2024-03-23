from typing import Union, Dict, List, Tuple, Callable, Optional, Any, TYPE_CHECKING

# This business is slightly awkward, but needed for backward compatibility,
# because Python < 3.7 doesn't have __future__/annotations, and <3.10 doesn't
# support TypeAlias.
if TYPE_CHECKING:
    from jinja2 import Environment
    try:
        from typing import TypeAlias # Introduced in Python 3.10
        JinjaEnvironmentT: TypeAlias = Environment
    except ImportError:
        JinjaEnvironmentT = Environment # type: ignore
    from geventwebsocket.websocket import WebSocket
    WebSocketT = WebSocket
else:
    JinjaEnvironmentT = None
    WebSocketT = Any

OptionsDictT = Dict[
        str,
        Optional[
            Union[
                str, bool, int, float,
                List[str], Tuple[int, int], Dict[str, Tuple[int, int]],
                Callable[..., Any], JinjaEnvironmentT
            ]
        ]
    ]
