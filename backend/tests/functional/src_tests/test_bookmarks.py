import pytest as pytest

from backend.tests.functional.testdata import films, counter, jwt
from http import HTTPStatus

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 'value': 1},
                {'status': True,
                 'film_id': films[0]['film_id']}
        ),
        (
                {'film_id': films[1]['film_id'],
                 'value': 0},
                {'status': True,
                 'film_id': films[1]['film_id']}
        ),
        (
                {'film_id': films[2]['film_id'],
                 'value': 1},
                {'status': True,
                 'film_id': films[2]['film_id']}
        ),
        (
                {'film_id': films[3]['film_id'],
                 'value': 0},
                {'status': True,
                 'film_id': films[3]['film_id']}
        ),
    ]
)
@pytestmark
async def test_add_bookmark(
        make_get_request, make_post_request, mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    body = {
        "film_id": query_data["film_id"],
    }
    # Act
    response = await make_post_request(
        "bookmarks", params=body, headers=headers
    )
    # Assert
    assert response['body']['status'] == expected_answer['status']
    assert response['body']['film_id'] == expected_answer['film_id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id']},
                {'status': True,
                 'film_id': films[0]['film_id']}
        ),
        (
                {'film_id': films[1]['film_id']},
                {'status': True,
                 'film_id': films[1]['film_id']}
        ),
        (
                {'film_id': films[2]['film_id']},
                {'status': True,
                 'film_id': films[2]['film_id']}
        ),
        (
                {'film_id': films[3]['film_id']},
                {'status': True,
                 'film_id': films[3]['film_id']}
        ),
    ]
)
@pytestmark
async def test_del_bookmark(
        make_get_request, make_post_request, make_delete_request,
        mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    body = {
        "film_id": query_data["film_id"],
    }
    _ = await make_post_request(
        "bookmarks", params=body, headers=headers
    )
    # Act
    response = await make_delete_request(
        "bookmarks", params=body, headers=headers
    )
    # Assert
    assert response['body']['status'] == expected_answer['status']
    assert response['body']['film_id'] == expected_answer['film_id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id']},
                {'status': HTTPStatus.NOT_FOUND}
        ),
        (
                {'film_id': films[1]['film_id']},
                {'status': HTTPStatus.NOT_FOUND}
        ),
        (
                {'film_id': films[2]['film_id']},
                {'status': HTTPStatus.NOT_FOUND}
        ),
        (
                {'film_id': films[3]['film_id']},
                {'status': HTTPStatus.NOT_FOUND}
        ),
    ]
)
@pytestmark
async def test_del_not_found_bookmark(
        make_get_request, make_post_request, make_delete_request,
        mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    body = {
        "film_id": query_data["film_id"],
    }
    # Act
    response = await make_delete_request(
        "bookmarks", params=body, headers=headers
    )
    # Assert
    assert response['status'] == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id']},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[1]['film_id']},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[2]['film_id']},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[3]['film_id']},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
    ]
)
@pytestmark
async def test_bad_add_bookmark(
        make_get_request, make_post_request, mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    body = {
        "film_id": query_data["film_id"],
    }
    # Act
    response = await make_post_request(
        "bookmarks", params=body
    )
    # Assert
    assert response['status'] == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id']},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[1]['film_id']},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[2]['film_id']},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[3]['film_id']},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
    ]
)
@pytestmark
async def test_no_token_del_bookmark(
        make_get_request, make_post_request, make_delete_request,
        mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    body = {
        "film_id": query_data["film_id"],
    }
    _ = await make_post_request(
        "bookmarks", params=body, headers=headers
    )
    # Act
    response = await make_delete_request(
        "bookmarks", params=body
    )
    # Assert
    assert response['status'] == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'films': films},
                {'films': films}
        )
    ]
)
@pytestmark
async def test_get_bookmarks(
        make_get_request, make_post_request, mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    for film in query_data['films']:
        _ = await make_post_request(
            "bookmarks", params=film, headers=headers
        )
    # Act
    response = await make_get_request("bookmarks", headers=headers)
    # Assert
    assert response['body']['bookmarks'] == expected_answer['films']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'films': films},
                {'status': HTTPStatus.UNAUTHORIZED}
        )
    ]
)
@pytestmark
async def test_bad_get_bookmarks(
        make_get_request, make_post_request, mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    for film in query_data['films']:
        _ = await make_post_request(
            "bookmarks", params=film, headers=headers
        )
    # Act
    response = await make_get_request("bookmarks")
    # Assert
    assert response['status'] == expected_answer['status']
