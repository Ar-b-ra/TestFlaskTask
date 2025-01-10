import os
from pathlib import Path
from src.db_worker import DatabaseWorker
from http import HTTPStatus

URL = "/execute"


def test_get_db_path():
    db_number = 1
    expected_path = os.path.join("databases", "database_1.db")
    assert DatabaseWorker.get_db_by_name(db_number) == Path(expected_path)


def test_execute_query_create_table(client):
    response = client.post(
        URL,
        json={
            "db_number": 1,
            "query": "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"message": "Query executed successfully"}


def test_execute_query_insert_data(client):
    response = client.post(
        URL, json={"db_number": 1, "query": 'INSERT INTO test (name) VALUES ("Alice")'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"message": "Query executed successfully"}


def test_execute_query_select_data(client):
    # Сначала вставляем данные
    client.post(
        URL, json={"db_number": 1, "query": 'INSERT INTO test (name) VALUES ("Alice")'}
    )

    # Затем выбираем данные
    response = client.post(URL, json={"db_number": 1, "query": "SELECT * FROM test"})
    assert response.status_code == HTTPStatus.OK
    assert response.json == [[1, "Alice"]]


def test_execute_query_invalid_sql(client):
    response = client.post(URL, json={"db_number": 1, "query": "INVALID SQL"})
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "error" in response.json


def test_execute_query_missing_fields(client):
    response = client.post(URL, json={})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_execute_query_multiple_databases(client):
    # Создаем таблицу в базе данных 1
    client.post(
        URL,
        json={
            "db_number": 1,
            "query": "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)",
        },
    )

    # Вставляем данные в базу данных 1
    client.post(
        URL, json={"db_number": 1, "query": 'INSERT INTO test (name) VALUES ("Alice")'}
    )

    # Создаем таблицу в базе данных 2
    client.post(
        URL,
        json={
            "db_number": 2,
            "query": "CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)",
        },
    )

    # Вставляем данные в базу данных 2
    client.post(
        URL, json={"db_number": 2, "query": 'INSERT INTO test (name) VALUES ("Bob")'}
    )

    # Проверяем данные в базе данных 1
    response = client.post(URL, json={"db_number": 1, "query": "SELECT * FROM test"})
    assert response.status_code == HTTPStatus.OK
    assert response.json == [[1, "Alice"]]

    # Проверяем данные в базе данных 2
    response = client.post(URL, json={"db_number": 2, "query": "SELECT * FROM test"})
    assert response.status_code == HTTPStatus.OK
    assert response.json == [[1, "Bob"]]


def test_cleanup():
    for db_number in [1, 2]:
        db_path = DatabaseWorker.get_db_by_name(db_number)
        if os.path.exists(db_path):
            os.remove(db_path)
