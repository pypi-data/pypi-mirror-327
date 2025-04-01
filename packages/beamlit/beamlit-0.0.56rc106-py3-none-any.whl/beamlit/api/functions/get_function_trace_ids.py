from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.trace_ids_response import TraceIdsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    function_name: str,
    *,
    environment: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["environment"] = environment

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/functions/{function_name}/traces",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[TraceIdsResponse]:
    if response.status_code == 200:
        response_200 = TraceIdsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TraceIdsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    function_name: str,
    *,
    client: AuthenticatedClient,
    environment: Union[Unset, str] = UNSET,
) -> Response[TraceIdsResponse]:
    """Get function trace IDs

    Args:
        function_name (str):
        environment (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TraceIdsResponse]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
        environment=environment,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    function_name: str,
    *,
    client: AuthenticatedClient,
    environment: Union[Unset, str] = UNSET,
) -> Optional[TraceIdsResponse]:
    """Get function trace IDs

    Args:
        function_name (str):
        environment (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TraceIdsResponse
    """

    return sync_detailed(
        function_name=function_name,
        client=client,
        environment=environment,
    ).parsed


async def asyncio_detailed(
    function_name: str,
    *,
    client: AuthenticatedClient,
    environment: Union[Unset, str] = UNSET,
) -> Response[TraceIdsResponse]:
    """Get function trace IDs

    Args:
        function_name (str):
        environment (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TraceIdsResponse]
    """

    kwargs = _get_kwargs(
        function_name=function_name,
        environment=environment,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    function_name: str,
    *,
    client: AuthenticatedClient,
    environment: Union[Unset, str] = UNSET,
) -> Optional[TraceIdsResponse]:
    """Get function trace IDs

    Args:
        function_name (str):
        environment (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TraceIdsResponse
    """

    return (
        await asyncio_detailed(
            function_name=function_name,
            client=client,
            environment=environment,
        )
    ).parsed
