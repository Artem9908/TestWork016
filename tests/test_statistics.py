def test_statistics(client, auth_headers):
    # Добавим несколько транзакций
    amounts = [100, 200, 300, 400, 500]
    for i, amt in enumerate(amounts):
        data = {
            "transaction_id": f"tx{i}",
            "user_id": "user_stat",
            "amount": amt,
            "currency": "USD",
            "timestamp": "2024-12-12T12:00:00"
        }
        client.post("/transactions", json=data, headers=auth_headers)
    
    # В реальности следует дождаться обработки Celery (например, sleep или мок Celery),
    # но для простоты в этом тесте можно считать, что если статистика не обновилась к моменту запроса - проверить данные "на лету".
    resp = client.get("/statistics", headers=auth_headers)
    assert resp.status_code == 200
    stats = resp.json()

    assert stats["total_transactions"] == 5

    assert abs(stats["average_transaction_amount"] - 300.0) < 1e-9

    top_amounts = [t["amount"] for t in stats["top_transactions"]]
    assert top_amounts == [500, 400, 300]
