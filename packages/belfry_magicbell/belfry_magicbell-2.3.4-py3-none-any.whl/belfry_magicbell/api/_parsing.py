import typing

import httpx
import orjson
from pydantic import BaseModel

from belfry_magicbell import errors
from belfry_magicbell.model import Response, ResponseBodyT


def check_response(response: httpx.Response) -> None:
    if response.is_client_error:
        raise errors.MagicBellHTTPClientError(response)
    elif response.is_server_error:
        raise errors.MagicBellHTTPServerError(response)
    elif not response.is_success:
        raise errors.MagicBellHTTPError(response)


def build_response(
    *,
    response: httpx.Response,
    out_type: typing.Optional[typing.Type[ResponseBodyT]],
    content_override: str | None = None
) -> Response[ResponseBodyT]:
    """Transform an `httpx.Response` into a `Response`.

    Raises an error if the response is not successful.
    """

    check_response(response)

    response_content = response.content if content_override is None else content_override

    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=out_type.model_validate_json(response_content) if out_type else None,
    )


def build_request_content(
    content: typing.Union[BaseModel, typing.Dict]
) -> typing.Union[str, bytes]:
    """Transform a `BaseModel` or a `dict` into a `str` or `bytes` for use with an http request."""
    if isinstance(content, BaseModel):
        return content.model_dump_json(exclude_unset=True)
    return orjson.dumps(content)
