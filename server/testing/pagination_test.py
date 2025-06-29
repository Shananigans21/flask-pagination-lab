import os
import pytest
from config import create_app, db
from models import Book

@pytest.fixture
def test_client():
    app = create_app("test")
    # Register your resources explicitly here (since api.init_app only initializes Api, doesn't add routes)
    from app import BookResource, Books
    api.add_resource(BookResource, '/book/<int:book_id>', endpoint='book')
    api.add_resource(Books, '/books', endpoint='books')

    with app.test_client() as client:
        with app.app_context():
            yield client


def seed_test_data():
    """Seed the in-memory test database with dummy books."""
    for i in range(1, 21):  # 20 books
        db.session.add(Book(title=f"Book {i}", author="Flatiron School"))
    db.session.commit()


def test_default_pagination(test_client):
    """Should return page 1 with default per_page (5)."""
    response = test_client.get("/books")
    data = response.get_json()

    assert response.status_code == 200
    assert data["page"] == 1
    assert data["per_page"] == 5
    assert len(data["items"]) == 5
    assert data["total"] == 20
    assert data["total_pages"] == 4


def test_specific_page_and_per_page(test_client):
    """Should return the correct page and number of records."""
    response = test_client.get("/books?page=2&per_page=3")
    data = response.get_json()

    assert response.status_code == 200
    assert data["page"] == 2
    assert data["per_page"] == 3
    assert len(data["items"]) == 3
    assert data["items"][0]["title"] == "Book 4"


def test_last_page_has_remaining_items(test_client):
    """The last page may return fewer than per_page if uneven total."""
    response = test_client.get("/books?page=4&per_page=6")
    data = response.get_json()

    assert response.status_code == 200
    assert data["page"] == 4
    assert len(data["items"]) == 2  # 6*3 = 18, 20-18 = 2 left


def test_empty_results_when_page_exceeds_total(test_client):
    """Should return an empty list but not crash if page exceeds total."""
    response = test_client.get("/books?page=99")
    data = response.get_json()

    assert response.status_code == 200
    assert data["items"] == []
    assert data["page"] == 99
    assert data["total"] == 20
    assert data["total_pages"] >= 1


def test_missing_params_fallback_to_defaults(test_client):
    """Requesting without query parameters should still work."""
    response = test_client.get("/books")
    data = response.get_json()

    assert response.status_code == 200
    assert data["page"] == 1
    assert data["per_page"] == 5
    assert len(data["items"]) == 5
