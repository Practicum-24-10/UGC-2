import asyncio
from typing import Any, Generator

import aiohttp
import motor.motor_asyncio
import pytest

from backend.tests.functional.settings import test_settings
from backend.tests.functional.testdata import collections
from backend.tests.functional.utils.generator import GeneratorMongo


@pytest.fixture(scope='session')
async def mongo_client():
    client = motor.motor_asyncio.AsyncIOMotorClient(
        f"mongodb://{test_settings.mongo_host}:{test_settings.mongo_port}"
    )["movies"]
    yield client
    for collection in collections:
        await client[collection].delete_many({})


@pytest.fixture(scope="session", name="event_loop")
def fixture_event_loop() -> Generator[asyncio.AbstractEventLoop, Any, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mongo_write_data(mongo_client):
    async def inner():
        for docs in GeneratorMongo().harvest():
            await mongo_client[docs[0].collection].insert_many(
                [doc.dict(exclude={'collection'}) for doc
                 in docs])

    return inner


@pytest.fixture
def mongo_delete_data(mongo_client):
    async def inner():
        for collection in collections:
            await mongo_client[collection].delete_many({})
    return inner


@pytest.fixture
async def make_get_request():
    async with aiohttp.ClientSession() as session:
        async def _make_get_request(
                endpoint: str, params: dict | None = None,
                headers: dict | None = None
        ):
            url = test_settings.service_url + endpoint
            params = params if params else {}
            async with session.get(url, params=params,
                                   headers=headers) as response:
                body = await response.json()
                status = response.status
            return {"status": status, "body": body}

        yield _make_get_request


@pytest.fixture
async def make_post_request():
    async with aiohttp.ClientSession() as session:
        async def _make_post_request(
                endpoint: str, params: dict | None = None,
                headers: dict | None = None
        ):
            url = test_settings.service_url + endpoint
            params = params or {}
            async with session.post(url, json=params,
                                    headers=headers) as response:
                status = response.status
                body = await response.json()
            return {"status": status, "body": body}

        yield _make_post_request


@pytest.fixture
async def make_delete_request():
    async with aiohttp.ClientSession() as session:
        async def _make_delete_request(
                endpoint: str, params: dict | None = None,
                headers: dict | None = None
        ):
            url = test_settings.service_url + endpoint
            params = params or {}
            async with session.delete(url, json=params,
                                      headers=headers) as response:
                status = response.status
                body = await response.json()
            return {"status": status, "body": body}

        yield _make_delete_request


@pytest.fixture
async def make_update_request():
    async with aiohttp.ClientSession() as session:
        async def _make_update_request(
                endpoint: str, params: dict | None = None,
                headers: dict | None = None
        ):
            url = test_settings.service_url + endpoint
            params = params or {}
            async with session.patch(url, json=params,
                                     headers=headers) as response:
                status = response.status
                body = await response.json()
            return {"status": status, "body": body}

        yield _make_update_request


@pytest.fixture
async def make_put_request():
    async with aiohttp.ClientSession() as session:
        async def _make_put_request(
                endpoint: str, params: dict | None = None,
                headers: dict | None = None
        ):
            url = test_settings.service_url + endpoint
            params = params or {}
            async with session.put(url, json=params,
                                   headers=headers) as response:
                status = response.status
                body = await response.json()
            return {"status": status, "body": body}

        yield _make_put_request
