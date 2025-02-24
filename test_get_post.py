from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from get_post import (get_post_by_id, get_post_by_id_with_validation,
                      get_posts_by_user_id)

mock_post = {
    'userId': 1,
    'id': 1,
    'title': 'Test Post',
    'body': 'Test post body.',
}

mock_posts_list = [
    {
        'userId': 1,
        'id': 1,
        'title': 'First Post',
        'body': 'First post body.'},
    {
        'userId': 1,
        'id': 2, 'title': 'Second Post',
        'body': 'Second post body.'
    },
]


@pytest.fixture
def mock_http_get():
    with patch('get_post.http_get') as mock_get:
        yield mock_get


def test_get_post_by_id(mock_http_get):
    mock_http_get.return_value.json.return_value = mock_post
    assert get_post_by_id(1) == mock_post


def test_get_posts_by_user_id(mock_http_get):
    mock_http_get.return_value.json.return_value = mock_posts_list
    assert get_posts_by_user_id(1) == mock_posts_list


def test_get_post_by_id_with_validation(mock_http_get):
    mock_http_get.return_value.json.return_value = mock_post
    assert get_post_by_id_with_validation(1) == mock_post


def test_get_post_by_id_http_error(mock_http_get):
    mock_http_get.side_effect = HTTPError()
    assert get_post_by_id(1) is None


def test_get_posts_by_user_id_http_error(mock_http_get):
    mock_http_get.side_effect = HTTPError()
    assert get_posts_by_user_id(1) is None


def test_get_post_by_id_with_validation_http_error(mock_http_get):
    mock_http_get.side_effect = HTTPError()
    assert get_post_by_id_with_validation(1) is None


def test_get_post_by_id_with_validation_invalid_post_id():
    with pytest.raises(ValueError, match='post_id must be greater than 0'):
        get_post_by_id_with_validation(0)
