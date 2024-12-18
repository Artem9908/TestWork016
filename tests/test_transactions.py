def test_add_transaction(client, auth_headers):
    data = {
        "transaction_id": "test123",
        "user_id": "user_001",
        "amount": 100.0,
        "currency": "USD",
        "timestamp": "2024-12-12T12:00:00"
    }
    resp = client.post("/transactions", json=data, headers=auth_headers)
    assert resp.status_code == 200
    assert "task_id" in resp.json()

def test_delete_transactions(client, auth_headers):
    # Добавим транзакцию
    data = {
        "transaction_id": "todelete",
        "user_id": "user_002",
        "amount": 200.0,
        "currency": "USD",
        "timestamp": "2024-12-12T13:00:00"
    }
    client.post("/transactions", json=data, headers=auth_headers)
    # Теперь удалим все
    resp = client.delete("/transactions", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "All transactions deleted"
