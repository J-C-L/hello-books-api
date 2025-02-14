def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []
    
def test_get_all_books_with_records(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == [
        {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
        },
        {
        "id": 2,
        "title": "Mountain Book",
        "description": "i luv 2 climb rocks"
        } 
    ]   

def test_create_new_book(client):
    # Act
    response = client.post("/books", 
        json={
        "title" : "Happy Book",
        "description" : "shiny happy people"
        }
        )
    response_text = response.get_data(as_text=True)

    # Assert
    assert response.status_code == 201
    assert response_text == "Book Happy Book successfully created with id 1"

    
    
def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
       "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }
    
def test_get_one_book_no_data(client):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
