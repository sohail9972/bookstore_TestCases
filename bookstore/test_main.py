
import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database import get_db,Base
from main import app
import random as rand


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL,
                       connect_args={"check_same_thread": False,}
                       ,poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)

def override_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db



@classmethod
def setUpClass(cls):
    cls.client = TestClient(app)
    response = cls.client.post('/token', data={
        'username': 'test',
        'password': 'test'
    })
    cls.token = response.json()['access_token']
    print(cls.token)

def setup():
    Base.metadata.create_all(bind=engine)

def teardown():
    Base.metadata.drop_all(bind=engine)

def test_read_root():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "up"}

def headers():
    return {
        'Authorization': f'Bearer eyJhbGciOiJIUzI1NiJ9.e30.6VYvcIrLY3hHCSzcr32Vnom21nnhMWQfhVpsqNT27Ro',
        'Content-Type': 'application/json'
    }

def create_payload():
    book_id = rand.randrange(10,500000,2)
    unique_id = uuid.uuid4().hex

    return {
        "id": book_id,
        "name": f"string_test_{unique_id}",
        "author": f"string_test_author_{unique_id}",
        "published_year": 2023,
        "book_summary": f"string_summary_{unique_id}"
}


def updated_payload(book_id):
    unique_id = uuid.uuid4().hex
    return {
        "id": book_id,
        "name": f"string_test_{unique_id}",
        "author": f"string_test_author_{unique_id}",
        "published_year": 2023,  # Replace with the actual year
        "book_summary": f"string_summary_{unique_id}"
    }

def validation_payload():
    book_id = rand.randrange(10,50000,2)
    unique_id = uuid.uuid4().hex
    return {
        "detail": [
            {
                "loc": [
                    f"string_test_{unique_id}",
                    book_id
                ],
                "msg": f"string_msg_test_{unique_id}",
                "type": f"string_type_test_{unique_id}"
            }
        ]
    }
# Validation Method Calls
def final_post_validation():
    return client.post("/books", headers=headers(), json=validation_payload())

def final_put_validation(book_id):
    return client.put(f"/books/{book_id}",headers=headers(),json=validation_payload())

def final_get_validation(book_id):
    return client.get(f'/books/{book_id}', headers=headers())

def final_delete_validation(book_id):
    return client.delete(f"/books/{book_id}",headers=headers())

def final_post():
    return client.post("/books", headers=headers(), json=create_payload())

def final_put_EndToEnd(book_id):
    return client.put(f"/books/{book_id}",headers=headers(),json=updated_payload(book_id))
def final_put(book_id,from_post_payload):
    return client.put(f"/books/{book_id}",headers=headers(),json=from_post_payload)

def final_get(book_id):
    return client.get(f'/books/{book_id}', headers=headers())

def final_delete(book_id):
    return client.delete(f"/books/{book_id}",headers=headers())


def test_user_login_Operation():
    user_id = rand.randrange(1000, 100000, 10)
    unique_id = uuid.uuid4().hex
    payload = {
        "id": user_id,
        "email": f"string_test_{unique_id}@example.com",  # Ensure a valid email format
        "password": f"string_test_{unique_id}"
    }
    user_response = client.post("/signup", headers=headers(), json=payload)
    assert user_response.status_code == 200
    login_response = client.post("/login", headers=headers(), json=payload)
    assert login_response.status_code == 200
    return (login_response.json()["access_token"])

# print(acess_token())

def test_get_sample_book():
    response = client.get('/books', headers=headers())
    # Assert the response status code is 200 OK
    assert response.status_code==200
    response.json()
    # print(data)

# Both Post and Put chaining main part of the Test

def test_create_update_get_delete_EndToEnd_boook():
    create_response_book=final_post()
    assert create_response_book.status_code==200
    print(create_response_book.json())
    book_id=create_response_book.json()["id"]

    # updating the created book
    creating_put_response = final_put_EndToEnd(book_id)
    assert creating_put_response.status_code==200
    print(creating_put_response.json())

    # fetching the Updated book
    get_response = final_get(book_id)
    assert get_response.status_code == 200
    assert get_response.json()["id"]==creating_put_response.json()["id"]
    # delete the Added book
    delete_response = final_delete(book_id)
    assert delete_response.status_code == 200
    print(delete_response.json())

def test_individual_create_post():
    create_book_response = final_post()
    assert create_book_response.status_code ==200
    assert create_book_response.json()["id"]
    assert create_book_response.json()["name"]
    assert create_book_response.json()["author"]
    assert create_book_response.json()["book_summary"]
    assert create_book_response.json()["published_year"]
    new_payload = {
        "id": create_book_response.json()["id"],
        "name": create_book_response.json()["name"],
        "author": create_book_response.json()["author"],
        "published_year": create_book_response.json()["published_year"],  # Replace with the actual year
        "book_summary": create_book_response.json()["book_summary"]
    }
    return new_payload

def test_indvidual_update_book():
    from_post_payload = test_individual_create_post()
    book_id = from_post_payload["id"]
    individual_put_response= final_put(book_id,from_post_payload)
    assert individual_put_response.status_code==200
    assert individual_put_response.json()["id"]==from_post_payload["id"]
    assert individual_put_response.json()["name"]==from_post_payload["name"]
    assert individual_put_response.json()["author"] == from_post_payload["author"]
    assert individual_put_response.json()["published_year"] == from_post_payload["published_year"]
    assert individual_put_response.json()["book_summary"] == from_post_payload["book_summary"]
    return book_id

def test_individual_get_book_id():
    get_payload_book_id = test_indvidual_update_book()
    print(get_payload_book_id)
    book_id=get_payload_book_id
    get_response_book_id = final_get(book_id)
    assert get_response_book_id .status_code == 200
    assert get_response_book_id.json()["id"]==get_payload_book_id

def test_delete_book():
    book_id_to_delete=test_indvidual_update_book()
    delete_response=final_delete(book_id_to_delete)
    assert delete_response.status_code==200
    print(delete_response.json())

# validation tests

# def test_validation_error_response():
#     validation_response = final_post_validation()
#     assert validation_response.status_code == 422