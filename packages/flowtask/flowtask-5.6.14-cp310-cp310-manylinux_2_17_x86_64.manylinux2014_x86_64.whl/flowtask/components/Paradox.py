import asyncio
from collections.abc import Callable
from typing import Optional, Dict, Any
import pandas as pd
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..interfaces.cache import CacheSupport
from ..exceptions import ComponentError
from ..conf import PARADOX_ACCOUNT_ID, PARADOX_API_SECRET

class Paradox(HTTPService, CacheSupport, FlowComponent):
    """
    Paradox Component

    **Overview**

    This component interacts with the Paradox API to perform various operations.
    The first step is to handle authentication and obtain an access token.
    The token is cached in Redis to avoid requesting a new one on each execution.

    .. table:: Properties
       :widths: auto

    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   Name                     | Required | Summary                                                                                      |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    |   type                     | Yes      | Type of operation to perform with the API                                                    |
    +----------------------------+----------+----------------------------------------------------------------------------------------------+
    """

    accept: str = "application/json"
    BASE_URL = "https://api.paradox.ai"
    CACHE_KEY = "_paradox_authentication"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.type: str = kwargs.get('type')
        self._access_token: Optional[str] = None
        self.max_pages: Optional[int] = kwargs.get('max_pages')
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def get_cached_token(self) -> Optional[str]:
        """
        Retrieves the cached authentication token from Redis if it exists.
        """
        try:
            async with self as cache:
                token = await cache._redis.get(self.CACHE_KEY)
                if token and isinstance(token, str) and len(token) > 10:
                    self._logger.info(f"Using cached authentication token: {token[:10]}...")
                    return token
                else:
                    self._logger.debug(f"Invalid or no token in cache: {token}")
        except Exception as e:
            self._logger.warning(f"Error getting cached token: {str(e)}")
        return None

    def set_auth_headers(self, token: str) -> None:
        """Set authentication token and headers"""
        self._access_token = token
        self.headers["Authorization"] = f"Bearer {token}"

    async def authenticate(self) -> None:
        """
        Authenticates with the Paradox API using client credentials flow.
        Stores the access token for subsequent requests.
        """
        auth_url = f"{self.BASE_URL}/api/v1/public/auth/token"

        # Prepare form data for token request
        payload = {
            'client_id': PARADOX_ACCOUNT_ID,
            'client_secret': PARADOX_API_SECRET,
            'grant_type': 'client_credentials'
        }

        # Set headers for form-urlencoded content
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json'
        }

        try:
            response = await self._post(
                url=auth_url,
                cookies=None,
                data=payload,
                headers=headers,
                follow_redirects=True,
                raise_for_status=True
            )

            result = await response.json()

            if 'access_token' not in result:
                raise ComponentError("No access token in authentication response")

            self._access_token = result['access_token']
            self.headers["Authorization"] = f"Bearer {self._access_token}"

            self._logger.info("Successfully authenticated with Paradox API")
            return result
        except Exception as e:
            raise ComponentError(f"Authentication failed: {str(e)}") from e

    async def start(self, **kwargs):
        """
        Initialize the component and authenticate with the API.
        Handles authentication flow including token caching in Redis.
        """
        if not PARADOX_ACCOUNT_ID or not PARADOX_API_SECRET:
            raise ComponentError(
                f"{__name__}: Missing required credentials: PARADOX_ACCOUNT_ID, PARADOX_API_SECRET"
            )

        if token := await self.get_cached_token():
            self.set_auth_headers(token)
            self._logger.debug("Using cached authentication token")
            return True
        try:
            result = await self.authenticate()
            token = result['access_token']
            self.set_auth_headers(token)

            async with self as cache:
                await cache.setex(
                    self.CACHE_KEY,
                    token,
                    timeout=f"{result.get('expires_in', 86400)}s"
                )

            self._logger.info("Successfully authenticated with Paradox API")
            return True

        except Exception as e:
            self._logger.error(f"Authentication failed: {str(e)}")
            raise ComponentError(f"Authentication failed: {str(e)}") from e

    async def run(self):
        """
        Execute the main component logic based on the specified type.
        Currently supports authentication as the initial implementation.
        """
        if not self._access_token or "Authorization" not in self.headers:
            self._logger.error(f"{__name__}: Not authenticated or missing Authorization header")
            raise ComponentError(f"{__name__}: Not authenticated. Call start() first")

        if not hasattr(self, self.type):
            raise ComponentError(f"{__name__}: Invalid operation type: {self.type}")

        try:
            method = getattr(self, self.type)
            result = await method()

            if isinstance(result, pd.DataFrame):
                self.add_metric("NUMROWS", len(result.index))
                self.add_metric("NUMCOLS", len(result.columns))

                if self._debug:
                    print("\n=== DataFrame Info ===")
                    print(result.head())
                    print("\n=== Column Information ===")
                    for column, dtype in result.dtypes.items():
                        print(f"{column} -> {dtype} -> {result[column].iloc[0] if not result.empty else 'N/A'}")

            self._result = result
            return self._result

        except Exception as e:
            self._logger.error(f"Error executing {self.type}: {str(e)}")
            raise

    async def close(self):
        """Cleanup any resources"""
        self._access_token = None
        return True

    async def candidates(self) -> pd.DataFrame:
        """
        Retrieves candidates from Paradox API using efficient pandas operations.
        Uses pagination to fetch all available candidates up to the maximum offset.
        Includes a delay between requests to avoid API rate limits.

        Returns:
            pd.DataFrame: DataFrame containing candidate information

        Raises:
            ComponentError: If the request fails or returns invalid data
        """
        try:
            offset = 0
            count = 0
            limit = getattr(self, 'limit', 50)
            all_candidates_data = []
            delay = 1.0
            current_page = 0
            max_retries = 3
            retry_delay = 2.0

            base_params = {
                'limit': limit,
                'note': 'true',
                'include_attributes': 'Yes'
            }

            while True:
                params = {
                    **base_params,
                    'offset': offset,
                }

                self._logger.debug(
                    f"Fetching candidates page {current_page + 1}"
                )

                # Implement retry logic
                data = None
                for retry in range(max_retries):
                    try:
                        data = await self.api_get(
                            url=self.BASE_URL + "/api/v1/public/candidates",
                            params=params,
                            headers=self.headers,
                            use_proxy=False
                        )

                        if data and 'candidates' in data:
                            break

                    except Exception as e:
                        if retry < max_retries - 1:
                            self._logger.warning(
                                f"Attempt {retry + 1} failed, retrying in {retry_delay} seconds... Error: {str(e)}"
                            )
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2  # Exponential backoff
                            continue
                        raise  # Re-raise the last exception if all retries failed

                candidates = data.get('candidates') if data else []
                if not candidates:
                    raise ComponentError(
                        "Empty response or invalid format from candidates endpoint"
                    )

                if count == 0:
                    count = data.get('count', 0)
                    max_offset = count % limit
                    self._logger.info(f"Total candidates: {count}, Max offset: {max_offset}")
                    if self.max_pages:
                        self._logger.info(f"Will retrieve maximum {self.max_pages} pages")

                all_candidates_data.extend(candidates)

                current_page += 1
                self._logger.debug(
                    f"Retrieved {len(all_candidates_data)} candidates so far (Page {current_page})"
                )

                if offset > max_offset:
                    break

                if self.max_pages and current_page >= self.max_pages:
                    self._logger.info(f"Reached configured page limit: {self.max_pages}")
                    break

                offset += 1

                # Increase delay slightly with each page to avoid rate limits
                delay = min(delay * 1.1, 3.0)  # Cap at 3 seconds

            # Convert to DataFrame and process using pandas operations
            df = pd.DataFrame(all_candidates_data)

            if df.empty:
                self._logger.warning("No candidates data found")
                return df

            # Extract nested data using pandas operations
            candidates = df['candidate'].apply(pd.Series)
            stage = df['stage'].apply(pd.Series)
            notes = df.pop('note')

            # Remove processed columns and join the extracted data
            df = df.drop(columns=['candidate', 'stage'])
            df = df.join(candidates).join(stage)
            df['notes'] = notes

            # Extract fields from attributes
            atribute = df['attributes'].apply(
                lambda x: pd.Series({
                    "first_name": x.get('first_name'),
                    "last_name": x.get('last_name'),
                    "street_address": x.get('address'),
                    "city": x.get('city'),
                    "state": x.get('state'),
                    "zip_code": x.get('zip_code'),
                    "birth_date": x.get('__birthdate')
                })
            )
            df = pd.concat([df, atribute], axis=1)

            self._logger.info(
                f"Retrieved total of {len(df)} candidates out of {count} (Pages: {current_page})"
            )
            return df

        except Exception as e:
            self._logger.error(
                f"Error fetching candidates: {str(e)}"
            )
            raise ComponentError(
                f"Failed to fetch candidates: {str(e)}"
            ) from e
