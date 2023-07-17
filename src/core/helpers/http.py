""" (module)

This module contains several functions to make HTTP requests
"""

from typing import Optional

import aiohttp

from core.helpers.exceptions import FailedToFetchError


async def get_url_json(url, data: Optional[dict] = None):
    """
    This function makes a GET request to a url and returns the json

    Parameters:
        url (str) : The url to make a request to
        data (Optional[dict]) : This is a dictionary of any extra params to send the request

    Returns:
        dict | list: The json response
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, data=data) as resp:
            try:
                response = await resp.json()
            except Exception as err:
                raise FailedToFetchError(url) from err
    return response


async def get_url_image(url, data: Optional[dict] = None):
    """
    This function makes a get request to a url and returns the image

    Parameters:
        url (str) : The url to make a request to
        data (Optional[dict]) : This is a dictionary of any extra params to send the request

    Returns:
        bytes: The bytes data response
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, data=data) as resp:
                resp = await resp.read()
        except Exception as err:
            raise FailedToFetchError(url) from err
    return resp
