from http import HTTPStatus

import pytest as pytest

from backend.tests.functional.testdata import counter, films, jwt

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': True}
        ),
        (
                {'film_id': films[1]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': True}
        ),
        (
                {'film_id': films[2]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': True}
        ),
        (
                {'film_id': films[3]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': True}
        ),
    ]
)
@pytestmark
async def test_add_review(
        make_post_request, mongo_delete_data, mongo_write_data, query_data,
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
        "review": query_data["review"]
    }
    # Act
    response = await make_post_request(
        "reviews", params=body, headers=headers
    )
    # Assert
    assert response['body']['status'] == expected_answer['status']
    assert response['body']['review_id'] is not None


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.CONFLICT}
        ),
        (
                {'film_id': films[1]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.CONFLICT}
        ),
        (
                {'film_id': films[2]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.CONFLICT}
        ),
        (
                {'film_id': films[3]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.CONFLICT}
        ),
    ]
)
@pytestmark
async def test_add_double_review(
        make_post_request, mongo_delete_data, mongo_write_data, query_data,
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
        "review": query_data["review"]
    }
    _ = await make_post_request(
        "reviews", params=body, headers=headers
    )
    # Act
    response = await make_post_request(
        "reviews", params=body, headers=headers
    )
    # Assert
    assert response['status'] == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я",
                 "update": "Или не я"},
                {'status': True}
        ),
        (
                {'film_id': films[1]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я",
                 "update": "Или все же я"},
                {'status': True}
        ),
        (
                {'film_id': films[2]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я",
                 "update": "Нет не я"},
                {'status': True}
        ),
        (
                {'film_id': films[3]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я",
                 "update": "Я это я"},
                {'status': True}
        ),
    ]
)
@pytestmark
async def test_put_review(
        make_post_request, make_put_request, mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    body_1 = {
        "film_id": query_data["film_id"],
        "review": query_data["review"]
    }
    body_2 = {
        "film_id": query_data["film_id"],
        "review": query_data["update"]
    }
    # Act
    response_1 = await make_post_request(
        "reviews", params=body_1, headers=headers
    )
    response_2 = await make_put_request(
        "reviews", params=body_2, headers=headers
    )
    # Assert
    assert response_1['body']['status'] == expected_answer['status']
    assert response_1['body']['review_id'] is not None
    assert response_2['body']['status'] == expected_answer['status']
    assert response_2['body']['review_id'] is not None
    assert response_2['body']['review_id'] == response_1['body']['review_id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'], },
                {'reviews': counter}
        ),
        (
                {'film_id': films[1]['film_id']},
                {'reviews': counter}
        ),
        (
                {'film_id': films[2]['film_id']},
                {'reviews': counter}
        ),
        (
                {'film_id': films[3]['film_id']},
                {'reviews': counter}
        ),
    ]
)
@pytestmark
async def test_get_reviews(
        make_get_request, mongo_delete_data, mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    params = {
        'page': 1,
        'size': 10,
    }
    status = True
    count_reviews = 0
    # Act
    while status:
        response = await make_get_request(f"reviews/{query_data['film_id']}",
                                          params=params)
        if response['status'] == HTTPStatus.OK:
            params['page'] += 1
            count_reviews += len(response['body']['reviews'])
        else:
            status = False
    # Assert
    assert count_reviews == expected_answer['reviews']


@pytest.mark.parametrize(
    'query_data',
    [
        (
                {'film_id': films[0]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"}
        ),
        (
                {'film_id': films[1]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"}
        ),
        (
                {'film_id': films[2]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"}
        ),
        (
                {'film_id': films[3]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"}
        ),
    ]
)
@pytestmark
async def test_del_review(
        make_post_request, make_get_request, make_delete_request,
        mongo_delete_data,
        mongo_write_data, query_data):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    body_1 = {
        "film_id": query_data["film_id"],
        "review": query_data["review"]
    }
    body_2 = {
        "film_id": query_data["film_id"]
    }
    params = {
        'page': 1,
        'size': 10,
    }
    # Act
    response_1 = await make_post_request(
        "reviews", params=body_1, headers=headers
    )
    response_2 = await make_get_request(f"reviews/{query_data['film_id']}",
                                        params=params, headers=headers)
    response_3 = await make_delete_request(
        "reviews", params=body_2, headers=headers
    )
    response_4 = await make_get_request(f"reviews/{query_data['film_id']}",
                                        params=params, headers=headers)
    # Assert
    assert response_1['body']['review_id'] == response_2['body'][
        'user_review_id']
    assert response_2['body']['user_review_id'] == response_3['body'][
        'review_id']
    assert response_3['body']['review_id'] != response_4['body'][
        'user_review_id']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[1]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[2]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[3]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
    ]
)
@pytestmark
async def test_bad_add_review(
        make_post_request, mongo_delete_data, mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    body = {
        "film_id": query_data["film_id"],
        "review": query_data["review"]
    }
    # Act
    response = await make_post_request(
        "reviews", params=body
    )
    # Assert
    assert response['status'] == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я",
                 "update": "Или не я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[1]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я",
                 "update": "Или все же я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[2]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я",
                 "update": "Нет не я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[3]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я",
                 "update": "Я это я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
    ]
)
@pytestmark
async def test_bad_put_review(
        make_post_request, make_put_request, mongo_delete_data,
        mongo_write_data, query_data,
        expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    body_1 = {
        "film_id": query_data["film_id"],
        "review": query_data["review"]
    }
    body_2 = {
        "film_id": query_data["film_id"],
        "review": query_data["update"]
    }
    # Act
    _ = await make_post_request(
        "reviews", params=body_1, headers=headers
    )
    response_2 = await make_put_request(
        "reviews", params=body_2
    )
    # Assert
    assert response_2['status'] == expected_answer['status']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        (
                {'film_id': films[0]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[1]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[2]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
        (
                {'film_id': films[3]['film_id'],
                 "review": "Райан Гослинг в этом фильме буквально я"},
                {'status': HTTPStatus.UNAUTHORIZED}
        ),
    ]
)
@pytestmark
async def test_no_token_del_review(
        make_post_request, make_get_request, make_delete_request,
        mongo_delete_data,
        mongo_write_data, query_data, expected_answer):
    # Arrange
    await mongo_delete_data()
    await mongo_write_data()
    headers = {
        "Authorization": f"Bearer {jwt}",
        "Content-Type": "application/json",
    }
    body_1 = {
        "film_id": query_data["film_id"],
        "review": query_data["review"]
    }
    body_2 = {
        "film_id": query_data["film_id"]
    }
    params = {
        'page': 1,
        'size': 10,
    }
    # Act
    response_1 = await make_post_request(
        "reviews", params=body_1, headers=headers
    )
    response_2 = await make_get_request(f"reviews/{query_data['film_id']}",
                                        params=params, headers=headers)
    response_3 = await make_delete_request(
        "reviews", params=body_2
    )
    response_4 = await make_get_request(f"reviews/{query_data['film_id']}",
                                        params=params, headers=headers)
    # Assert
    assert response_1['body']['review_id'] == response_2['body'][
        'user_review_id']
    assert response_3['status'] == expected_answer['status']
    assert response_2['body']['user_review_id'] == response_4['body'][
        'user_review_id']
