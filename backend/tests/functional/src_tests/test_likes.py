import pytest as pytest

from backend.tests.functional.testdata import films, counter, jwt
from http import HTTPStatus

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id']},
                {'likes': counter,
                 'dislikes': counter}
        ),
        (
                {'film_id': films[1]['film_id']},
                {'likes': counter,
                 'dislikes': counter}
        ),
        (
                {'film_id': films[2]['film_id']},
                {'likes': counter,
                 'dislikes': counter}
        ),
        (
                {'film_id': films[3]['film_id']},
                {'likes': counter,
                 'dislikes': counter}
        ),
    ]
)
@pytestmark
async def test_count_likes(
        make_get_request, mongo_delete_data, mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    # Act
    response = await make_get_request(f"likes/{query_data['film_id']}")
    # Assert
    assert response['body']['likes'] == expected_answer['likes']
    assert response['body']['dislikes'] == expected_answer['dislikes']
    assert response['body']['user_like'] is None


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 'value': 1},
                {'status': True}
        ),
        (
                {'film_id': films[1]['film_id'],
                 'value': 0},
                {'status': True}
        ),
        (
                {'film_id': films[2]['film_id'],
                 'value': 1},
                {'status': True}
        ),
        (
                {'film_id': films[3]['film_id'],
                 'value': 0},
                {'status': True}
        ),
    ]
)
@pytestmark
async def test_add_likes(
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
        "value": query_data["value"]
    }
    # Act
    response = await make_post_request(
        "likes", params=body, headers=headers
    )
    # Assert
    assert response['body']['status'] == expected_answer['status']
    assert response['body']['like_id'] is not None


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 'value': 1},
                {'status': True}
        ),
        (
                {'film_id': films[1]['film_id'],
                 'value': 0},
                {'status': True}
        ),
        (
                {'film_id': films[2]['film_id'],
                 'value': 1},
                {'status': True}
        ),
        (
                {'film_id': films[3]['film_id'],
                 'value': 0},
                {'status': True}
        ),
    ]
)
@pytestmark
async def test_del_likes(
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
        "value": query_data["value"]
    }
    _ = await make_post_request(
        "likes", params=body, headers=headers
    )
    # Act
    response = await make_post_request(
        "likes", params=body, headers=headers
    )
    # Assert
    assert response['body']['status'] == expected_answer['status']
    assert response['body']['like_id'] is None


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 'value': 1},
                {'likes': counter + 1,
                 'dislikes': counter}
        ),
        (
                {'film_id': films[1]['film_id'],
                 'value': 0},
                {'likes': counter,
                 'dislikes': counter + 1}
        ),
        (
                {'film_id': films[2]['film_id'],
                 'value': 1},
                {'likes': counter + 1,
                 'dislikes': counter}
        ),
        (
                {'film_id': films[3]['film_id'],
                 'value': 0},
                {'likes': counter,
                 'dislikes': counter + 1}
        ),
    ]
)
@pytestmark
async def test_count_before_add_likes(
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
        "value": query_data["value"]
    }
    _ = await make_post_request(
        "likes", params=body, headers=headers
    )
    # Act
    response = await make_get_request(f"likes/{query_data['film_id']}",
                                      headers=headers)
    # Assert
    assert response['body']['likes'] == expected_answer['likes']
    assert response['body']['dislikes'] == expected_answer['dislikes']
    assert response['body']['user_like'] is not None


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 'value': 100},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                {'film_id': films[1]['film_id'],
                 'value': ''},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        ),
        (
                {'film_id': films[2]['film_id'],
                 'value': 'fdsfsd'},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        )
        ,
        (
                {'film_id': 'dsda',
                 'value': 0},
                {'status': HTTPStatus.UNPROCESSABLE_ENTITY}
        )
    ]
)
@pytestmark
async def test_bad_add_likes(
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
        "value": query_data["value"]
    }
    # Act
    response = await make_post_request(
        "likes", params=body, headers=headers
    )
    # Assert
    assert response['status'] == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 'value': 1},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[1]['film_id'],
                 'value': 0},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[2]['film_id'],
                 'value': 1},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[3]['film_id'],
                 'value': 0},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
    ]
)
@pytestmark
async def test_no_token_add_likes(
        make_get_request, make_post_request, mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    body = {
        "film_id": query_data["film_id"],
        "value": query_data["value"]
    }
    # Act
    response = await make_post_request(
        "likes", params=body
    )
    # Assert
    assert response['status'] == expected_answer['status']
