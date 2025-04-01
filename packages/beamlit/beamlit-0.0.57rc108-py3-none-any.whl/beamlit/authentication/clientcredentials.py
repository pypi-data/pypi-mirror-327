"""
This module provides the ClientCredentials class, which handles client credentials-based
authentication for Beamlit. It manages token refreshing and authentication flows using
client credentials and refresh tokens.
"""

import base64
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Generator, Optional

import requests
from httpx import Auth, Request, Response, post

from beamlit.common.settings import get_settings


@dataclass
class DeviceLoginFinalizeResponse:
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str


class ClientCredentials(Auth):
    """
    A provider that authenticates requests using client credentials.
    """

    def __init__(self, credentials, workspace_name: str, base_url: str):
        """
        Initializes the ClientCredentials provider with the given credentials, workspace name, and base URL.

        Parameters:
            credentials: Credentials containing access and refresh tokens.
            workspace_name (str): The name of the workspace.
            base_url (str): The base URL for authentication.
        """
        self.credentials = credentials
        self.workspace_name = workspace_name
        self.base_url = base_url

    def get_headers(self):
        """
        Retrieves the authentication headers after ensuring tokens are valid.

        Returns:
            dict: A dictionary of headers with Bearer token and workspace.

        Raises:
            Exception: If token refresh fails.
        """
        err = self.refresh_if_needed()
        if err:
            raise err

        return {
            "X-Beamlit-Authorization": f"Bearer {self.credentials.access_token}",
            "X-Beamlit-Workspace": self.workspace_name,
        }

    def refresh_if_needed(self) -> Optional[Exception]:
        """
        Checks if the access token needs to be refreshed and performs the refresh if necessary.

        Returns:
            Optional[Exception]: An exception if refreshing fails, otherwise None.
        """
        settings = get_settings()
        if self.credentials.client_credentials and not self.credentials.refresh_token:
            headers = {"Authorization": f"Basic {self.credentials.client_credentials}", "Content-Type": "application/json"}
            body = {"grant_type": "client_credentials"}
            response = requests.post(f"{settings.base_url}/oauth/token", headers=headers, json=body)
            response.raise_for_status()
            self.credentials.access_token = response.json()["access_token"]
            self.credentials.refresh_token = response.json()["refresh_token"]
            self.credentials.expires_in = response.json()["expires_in"]

        # Need to refresh token if expires in less than 10 minutes
        parts = self.credentials.access_token.split(".")
        if len(parts) != 3:
            return Exception("Invalid JWT token format")
        try:
            claims_bytes = base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4))
            claims = json.loads(claims_bytes)
        except Exception as e:
            return Exception(f"Failed to decode/parse JWT claims: {str(e)}")

        exp_time = datetime.fromtimestamp(claims["exp"])
        current_time = datetime.now()
        # Refresh if token expires in less than 10 minutes
        if current_time + timedelta(minutes=10) > exp_time:
            return self.do_refresh()

        return None

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:
        """
        Processes the authentication flow by ensuring tokens are valid and adding necessary headers.

        Parameters:
            request (Request): The HTTP request to authenticate.

        Yields:
            Request: The authenticated request.

        Raises:
            Exception: If token refresh fails.
        """
        err = self.refresh_if_needed()
        if err:
            return err

        request.headers["X-Beamlit-Authorization"] = f"Bearer {self.credentials.access_token}"
        request.headers["X-Beamlit-Workspace"] = self.workspace_name
        yield request

    def do_refresh(self) -> Optional[Exception]:
        """
        Performs the token refresh using the refresh token.

        Returns:
            Optional[Exception]: An exception if refreshing fails, otherwise None.
        """
        if not self.credentials.refresh_token:
            return Exception("No refresh token to refresh")

        url = f"{self.base_url}/oauth/token"
        refresh_data = {
            "grant_type": "refresh_token",
            "refresh_token": self.credentials.refresh_token,
            "device_code": self.credentials.device_code,
            "client_id": "beamlit",
        }

        try:
            response = post(url, json=refresh_data, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            finalize_response = DeviceLoginFinalizeResponse(**response.json())

            if not finalize_response.refresh_token:
                finalize_response.refresh_token = self.credentials.refresh_token

            from .credentials import Credentials, save_credentials

            creds = Credentials(
                access_token=finalize_response.access_token,
                refresh_token=finalize_response.refresh_token,
                expires_in=finalize_response.expires_in,
                device_code=self.credentials.device_code,
            )

            self.credentials = creds
            save_credentials(self.workspace_name, creds)
            return None

        except Exception as e:
            return Exception(f"Failed to refresh token: {str(e)}")
