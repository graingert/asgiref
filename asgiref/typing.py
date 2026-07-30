import sys
from collections.abc import Awaitable, Callable, Iterable
from typing import Any, Literal, Protocol, TypedDict, Union

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired

__all__ = (
    "ASGIVersions",
    "HTTPScope",
    "WebSocketScope",
    "LifespanScope",
    "WWWScope",
    "Scope",
    "HTTPRequestEvent",
    "HTTPResponseStartEvent",
    "HTTPResponseBodyEvent",
    "HTTPResponseTrailersEvent",
    "HTTPResponsePathsendEvent",
    "HTTPServerPushEvent",
    "HTTPDisconnectEvent",
    "WebSocketConnectEvent",
    "WebSocketAcceptEvent",
    "WebSocketReceiveEvent",
    "WebSocketSendEvent",
    "WebSocketResponseStartEvent",
    "WebSocketResponseBodyEvent",
    "WebSocketDisconnectEvent",
    "WebSocketCloseEvent",
    "LifespanStartupEvent",
    "LifespanShutdownEvent",
    "LifespanStartupCompleteEvent",
    "LifespanStartupFailedEvent",
    "LifespanShutdownCompleteEvent",
    "LifespanShutdownFailedEvent",
    "ASGIReceiveEvent",
    "ASGISendEvent",
    "ASGIReceiveCallable",
    "ASGISendCallable",
    "ASGI2Protocol",
    "ASGI2Application",
    "ASGI3Application",
    "ASGIApplication",
)


class ASGIVersions(TypedDict):
    spec_version: NotRequired[str]
    version: NotRequired[Literal["2.0"] | Literal["3.0"]]


class HTTPScope(TypedDict):
    type: Literal["http"]
    asgi: ASGIVersions
    http_version: str
    method: str
    scheme: NotRequired[str]
    path: str
    raw_path: NotRequired[bytes]
    query_string: bytes
    root_path: NotRequired[str]
    headers: Iterable[tuple[bytes, bytes]]
    client: NotRequired[tuple[str, int] | None]
    server: NotRequired[tuple[str, int | None] | None]
    state: NotRequired[dict[str, Any]]
    extensions: dict[str, dict[object, object]] | None


class WebSocketScope(TypedDict):
    type: Literal["websocket"]
    asgi: ASGIVersions
    http_version: NotRequired[str]
    scheme: NotRequired[str]
    path: str
    raw_path: NotRequired[bytes]
    query_string: NotRequired[bytes]
    root_path: NotRequired[str]
    headers: Iterable[tuple[bytes, bytes]]
    client: NotRequired[tuple[str, int] | None]
    server: NotRequired[tuple[str, int | None] | None]
    subprotocols: NotRequired[Iterable[str]]
    state: NotRequired[dict[str, Any]]
    extensions: dict[str, dict[object, object]] | None


class LifespanScope(TypedDict):
    type: Literal["lifespan"]
    asgi: ASGIVersions
    state: NotRequired[dict[str, Any]]


WWWScope = Union[HTTPScope, WebSocketScope]
Scope = Union[HTTPScope, WebSocketScope, LifespanScope]


class HTTPRequestEvent(TypedDict):
    type: Literal["http.request"]
    body: NotRequired[bytes]
    more_body: NotRequired[bool]


class HTTPResponseDebugEvent(TypedDict):
    type: Literal["http.response.debug"]
    info: dict[str, object]


class HTTPResponseStartEvent(TypedDict):
    type: Literal["http.response.start"]
    status: int
    headers: NotRequired[Iterable[tuple[bytes, bytes]]]
    trailers: NotRequired[bool]


class HTTPResponseBodyEvent(TypedDict):
    type: Literal["http.response.body"]
    body: NotRequired[bytes]
    more_body: NotRequired[bool]


class HTTPResponseTrailersEvent(TypedDict):
    type: Literal["http.response.trailers"]
    headers: Iterable[tuple[bytes, bytes]]
    more_trailers: bool


class HTTPResponsePathsendEvent(TypedDict):
    type: Literal["http.response.pathsend"]
    path: str


class HTTPServerPushEvent(TypedDict):
    type: Literal["http.response.push"]
    path: str
    headers: Iterable[tuple[bytes, bytes]]


class HTTPDisconnectEvent(TypedDict):
    type: Literal["http.disconnect"]


class WebSocketConnectEvent(TypedDict):
    type: Literal["websocket.connect"]


class WebSocketAcceptEvent(TypedDict):
    type: Literal["websocket.accept"]
    subprotocol: NotRequired[str | None]
    headers: NotRequired[Iterable[tuple[bytes, bytes]]]


class WebSocketReceiveEvent(TypedDict):
    type: Literal["websocket.receive"]
    bytes: NotRequired[bytes | None]
    text: NotRequired[str | None]


class WebSocketSendEvent(TypedDict):
    type: Literal["websocket.send"]
    bytes: NotRequired[bytes | None]
    text: NotRequired[str | None]


class WebSocketResponseStartEvent(TypedDict):
    type: Literal["websocket.http.response.start"]
    status: int
    headers: Iterable[tuple[bytes, bytes]]


class WebSocketResponseBodyEvent(TypedDict):
    type: Literal["websocket.http.response.body"]
    body: bytes
    more_body: bool


class WebSocketDisconnectEvent(TypedDict):
    type: Literal["websocket.disconnect"]
    code: int
    reason: NotRequired[str | None]


class WebSocketCloseEvent(TypedDict):
    type: Literal["websocket.close"]
    code: NotRequired[int]
    reason: NotRequired[str | None]


class LifespanStartupEvent(TypedDict):
    type: Literal["lifespan.startup"]


class LifespanShutdownEvent(TypedDict):
    type: Literal["lifespan.shutdown"]


class LifespanStartupCompleteEvent(TypedDict):
    type: Literal["lifespan.startup.complete"]


class LifespanStartupFailedEvent(TypedDict):
    type: Literal["lifespan.startup.failed"]
    message: NotRequired[str]


class LifespanShutdownCompleteEvent(TypedDict):
    type: Literal["lifespan.shutdown.complete"]


class LifespanShutdownFailedEvent(TypedDict):
    type: Literal["lifespan.shutdown.failed"]
    message: NotRequired[str]


ASGIReceiveEvent = Union[
    HTTPRequestEvent,
    HTTPDisconnectEvent,
    WebSocketConnectEvent,
    WebSocketReceiveEvent,
    WebSocketDisconnectEvent,
    LifespanStartupEvent,
    LifespanShutdownEvent,
]


ASGISendEvent = Union[
    HTTPResponseStartEvent,
    HTTPResponseBodyEvent,
    HTTPResponseTrailersEvent,
    HTTPServerPushEvent,
    HTTPDisconnectEvent,
    WebSocketAcceptEvent,
    WebSocketSendEvent,
    WebSocketResponseStartEvent,
    WebSocketResponseBodyEvent,
    WebSocketCloseEvent,
    LifespanStartupCompleteEvent,
    LifespanStartupFailedEvent,
    LifespanShutdownCompleteEvent,
    LifespanShutdownFailedEvent,
]


ASGIReceiveCallable = Callable[[], Awaitable[ASGIReceiveEvent]]
ASGISendCallable = Callable[[ASGISendEvent], Awaitable[None]]


class ASGI2Protocol(Protocol):
    def __init__(self, scope: Scope) -> None: ...

    async def __call__(
        self,
        receive: ASGIReceiveCallable,
        send: ASGISendCallable,
    ) -> None: ...


ASGI2Application = type[ASGI2Protocol]
ASGI3Application = Callable[
    [
        Scope,
        ASGIReceiveCallable,
        ASGISendCallable,
    ],
    Awaitable[None],
]
ASGIApplication = Union[ASGI2Application, ASGI3Application]
