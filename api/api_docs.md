# api_server.py — API Documentation

Base URL: http://localhost:8000  
Authentication: HTTP Basic (USERNAME="admin", PASSWORD="password")  
Authorization header example: Authorization: Basic YWRtaW46cGFzc3dvcmQ= (admin:password)

---

## GET /transactions
- Description: Return all transactions.
- Request example (curl):
  ```bash
  curl -u admin:password http://localhost:8000/transactions
  ```
- Response example (200 OK, application/json):
  ```json
  [
    {
        "id": "1715351451000",
        "sender": "M-Money",
        "receiver_name": null,
        "receiver_phone": null,
        "amount": 2000.0,
        "type": "received",
        "timestamp": "1715351458724",
        "body": "You have received 2000 RWF from Jane Smith (*********013) on your mobile money account at 2024-05-10 16:30:51. Message from sender: . Your new balance:2000 RWF. Financial Transaction Id: 76662021700."
    },
    {
        "id": "1715351498000",
        "sender": "M-Money",
        "receiver_name": "Jane Smith",
        "receiver_phone": null,
        "amount": 1000.0,
        "type": "payment",
        "timestamp": "1715351506754",
        "body": "TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith 12845 has been completed at 2024-05-10 16:31:39. Your new balance: 1,000 RWF. Fee was 0 RWF.Kanda*182*16# wiyandikishe muri poromosiyo ya BivaMoMotima, ugire amahirwe yo gutsindira ibihembo bishimishije."
    }
  ]
  ```
- Here's the related screenshot: [GET & Confirm AUTH](</screenshots/get_auth.png>)
---

## GET /transactions/{id}
- Description: Return a single transaction by id.
- Request example:
  ```bash
  curl -u admin:password http://localhost:8000/transactions/1715351498000
  ```
- Response example (200 OK):
  ```json
  {
    "id": "1715351498000",
    "sender": "M-Money",
    "receiver_name": "Jane Smith",
    "receiver_phone": null,
    "amount": 1000.0,
    "type": "payment",
    "timestamp": "1715351506754",
    "body": "TxId: 73214484437. Your payment of 1,000 RWF to Jane Smith 12845 has been completed at 2024-05-10 16:31:39. Your new balance: 1,000 RWF. Fee was 0 RWF.Kanda*182*16# wiyandikishe muri poromosiyo ya BivaMoMotima, ugire amahirwe yo gutsindira ibihembo bishimishije."
  }
  ```
- Errors:
  - 401 Unauthorized — missing/invalid Basic auth
  - 404 Not Found — no transaction with the given id
    
- Here's the related screenshot: [GET By Id](</screenshots/get_byID.png>)
---

## POST /transactions
- Description: Create/add a new transaction. The server expects a JSON object. The implementation requires an `id` field (used as key).
- Request example:
  ```bash
  curl -u admin:password -X POST \
    -H "Content-Type: application/json" \
    -d '{"id": "13443", "sender": "M-Money", "receiver_name": "Semana", "receiver_phone": null, "amount": 600000.0, "type": "payment", "timestamp": "1715369560245", "body": "TxId: 51732411227. Your payment of 600000 RWF to Samuel Carter 95464 has been completed at 2024-05-10 21:32:32. Your new balance: 987400 RWF. Fee was 0 RWF.Kanda*182*16# wiyandikishe muri poromosiyo ya BivaMoMotima, ugire amahirwe yo gutsindira ibihembo bishimishije."}' \
    http://localhost:8000/transactions
  ```
- Response example (201 Created):
  ```json
  {
    "id": "13443",
    "sender": "M-Money",
    "receiver_name": "Semana",
    "receiver_phone": null,
    "amount": 600000.0,
    "type": "payment",
    "timestamp": "1715369560245",
    "body": "TxId: 51732411227. Your payment of 600000 RWF to Samuel Carter 95464 has been completed at 2024-05-10 21:32:32. Your new balance: 987400 RWF. Fee was 0 RWF.Kanda*182*16# wiyandikishe muri poromosiyo ya BivaMoMotima, ugire amahirwe yo gutsindira ibihembo bishimishije."
  }
  ```
- Notes:
  - The server stores the provided JSON in memory (transactions_dict). Data is not persisted to disk by the current implementation.
- Errors:
  - 401 Unauthorized — missing/invalid Basic auth
  - 400 Bad Request — malformed JSON (not explicitly handled in code, may raise server error)
    
- Here's the related screenshot: [Creating New Transaction](</screenshots/post.png>)
---

## PUT /transactions/{id}
- Description: Replace/update the transaction with the given id. The request must contain the full JSON for the updated transaction.
- Request example:
  ```bash
  curl -u admin:password -X PUT \
    -H "Content-Type: application/json" \
    -d '{"id": "13443", "sender": "M-Money", "receiver_name": "John Doe", "receiver_phone": null, "amount": 600000.0}' \
    http://localhost:8000/transactions/123
  ```
- Response example (200 OK):
  ```json
  { 
    "id": "13443",
     "sender": "M-Money",
     "receiver_name": "John Doe",
     "receiver_phone": null,
    "amount": 600000.0
  }
  ```
- Errors:
  - 401 Unauthorized — missing/invalid Basic auth
  - 404 Not Found — no transaction with the given id
  - 400 Bad Request — malformed JSON
    
- Here's the related screenshot: [Updating By Id](</screenshots/put.png>)
---

## DELETE /transactions/{id}
- Description: Delete the transaction with the given id and return the deleted object.
- Request example:
  ```bash
  curl -u admin:password -X DELETE http://localhost:8000/transactions/13443
  ```
- Response example (200 OK):
  ```json
  {
    "id": "13443",
    "sender": "M-Money",
    "receiver_name": "John Doe",
    "receiver_phone": null,
    "amount": 600000.0
  }
  ```
- Errors:
  - 401 Unauthorized — missing/invalid Basic auth
  - 404 Not Found — no transaction with the given id
 
- Here's the related screenshot: [Deleting By Id](</screenshots/delete.png>)


## Implementation notes / caveats
- Authentication is basic and uses hardcoded credentials — change before production.
- Transactions are loaded from `./modified_sms_v2.xml` at server start (via dsa.parse_sms.parse_sms_xml) and held in memory. Changes are not persisted.
- The server does not validate transaction fields beyond JSON parsing and uses the provided `id` as the key.
- Content-Type for JSON responses is `application/json`. Unauthorized responses write a short plain body and set WWW-Authenticate.

