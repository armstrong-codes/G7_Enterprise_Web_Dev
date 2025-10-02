# G7 Enterprise Web Dev

### Project description:
This project is about creating MOMO app. Which will be used to receive and process the inserted data for providing the required information.

### Members list:
> Gakwaya Ineza Ketia (Group leader)

> Rwakunda Kaliza Sheila Milena

> Hirwa Armstrong



This is Draw.io link: https://drive.google.com/file/d/1T7GoRHwGNc2ddbfRLX7-H-Gn9S0lQ0fy/view?usp=sharing 

### Database documentation:
In this step, we designed database with ERD(Entity Relational Diagram) and then implemented it using SQL(Structured Query Language) so that we can create the exact database when we are done designing the front-end part.

We first identified what entities we need and after we designed a diagram to represent those entities and the atrributes each holds and also the relationship they have between themselves which includes 1 to many, etc...

Then we designed them according to how the system flows, We imagined how we want our system to work and from there we got what entities needed for our system to work as intended. Here is where we found that we need users table, transaction table to hold transactions and all of the other tables/entities that will help the system to store data effectively and efficientlt using their respective attributes which enhance the accuracy and integrity of the stored data by storing them in the related column names and assigning them with effective constraint for more data security.

After drawing the ERD, we applied the diagram into SQL so that we can turn our diagram into a real database using sql language. That is where we created our file and called it database_setup with sql extension that it can be ran whenever we need to use it. 

Within this file, is where the magic was done. This is where we created our database called "momo_db" which will hold all the entities and data that will be inserted into these entities. After creating the database, i created user table with multiple attributes for holding all user's data that will be required by the system. Those attributes are userId which will uniquely identify a user from other users, firstName and lastName, email, phoneNumber, accountNumber, creationDate and updationDate. This was the same process for other tables/entities which are transaction, transactionCategories and systemLog with their respective attributes.

Afterwards, i did serialization shifting SQL file to a JSON file. I got the SQL structure and rewrote it in JSON structure where tables are curly braces, attributes are keys and data are values. And all of them are inside a square bracket which represent the database in this case.

This below is the mapping of SQL to JSON:

| SQL Table / Column                         | JSON Representation                   |
| ------------------------------------------ | ------------------------------------- |
| **User.user\_id**                         | `user_id`                             |
| **User.first\_name, last\_name**          | `first_name`, `last_name`             |
| **User.email, phone\_number**             | `email`, `phone_number`               |
| **User.account\_number**                  | `account_number`                      |
| **Transaction.transaction\_id**           | `transaction_id`                      |
| **Transaction.sender\_id**                | Nested in `sender` object             |
| **Transaction.receiver\_id**              | Nested in `receiver` object           |
| **Transaction.category\_id**              | Nested in `category` object           |
| **Transaction.amount**                    | `amount`                              |
| **Transaction.currency**                  | `currency`                            |
| **Transaction.status**                    | `status`                              |
| **Transaction.transaction\_date**         | `transaction_date`                    |
| **Transaction\_categories.category\_name** | `category.category_name`              |
| **System\_Log.action, log\_message**      | `log[].action`, `log[].log_message` |
| **System\_Log.timestamp**                 | `log[].timestamp`                    |

## REST API Implementation

The project now includes a **secure REST API** for programmatic access to transactions:

**Endpoints:**

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| /transactions | GET | Retrieve all transactions | Yes |
| /transactions/<id> | GET | Retrieve a specific transaction | Yes |
| /transactions | POST | Add a new transaction | Yes |
| /transactions/<id> | PUT | Update a transaction | Yes |
| /transactions/<id> | DELETE | Delete a transaction | Yes |

**Authentication & Security:**

* Basic Authentication is implemented for all endpoints.  
* Demo credentials for testing:  
  - Admin: `admin` / `password`  
* Unauthorized access returns `401 Unauthorized`.  
* Reflection: Basic Auth is simple but weak for production; stronger alternatives include **JWT**, **OAuth2**, and **API keys over HTTPS**.

**Why Basic Auth is Weak:**

* Credentials are sent with every request, often only base64-encoded, making them vulnerable if intercepted.  
* Without HTTPS, attackers can easily capture usernames and passwords.  
* No token expiration means compromised credentials remain valid until manually changed.  
* Lacks fine-grained access control and revocation capabilities.  
* Recommended alternatives include OAuth2, JWT tokens, and API keys with HTTPS to improve security and control.

**Request Examples (curl):**

```bash
# List all transactions
curl -u admin:password http://localhost:8080/transactions

# Get transaction by ID
curl -u admin:password http://localhost:8080/transactions/1

# Add new transaction
curl -u admin:password -X POST -H "Content-Type: application/json" \
    -d '{"id": "13443", "sender": "M-Money", "receiver_name": "Semana", "receiver_phone": null, "amount": 600000.0, "type": "payment", "timestamp": "1715369560245", "body": "TxId: 51732411227. Your payment of 600000 RWF to Samuel Carter 95464 has been completed at 2024-05-10 21:32:32. Your new balance: 987400 RWF. Fee was 0 RWF.Kanda*182*16# wiyandikishe muri poromosiyo ya BivaMoMotima, ugire amahirwe yo gutsindira ibihembo bishimishije."}' \
    http://localhost:8080/transactions
```

---

## Data Structures & Algorithms (DSA Integration)

To demonstrate efficient searching:

* **Linear Search**: Scans the transaction list sequentially to find a record by ID (O(n)).  
* **Dictionary Lookup**: Uses a dictionary index (`id → transaction`) for O(1) average-time lookup.  
* **Comparison Results (1000*20 searches)**:
  - Linear search total time: 2.882248 seconds  
  - Dictionary lookup total time: 0.032148 seconds  
  - Average linear per lookup: 0.000144112 seconds  
  - Average dict per lookup: 0.000001607 seconds  
* **Analysis**: Dictionary lookup is faster because it uses O(1) average-time hashing lookup, while linear search is O(n).  

This demonstrates the importance of selecting proper data structures for performance-critical operations in APIs.

---

## Setup and Usage

1. **Clone the Repository**:

```bash
git clone <https://github.com/armstrong-codes/G7_Enterprise_Web_Dev.git >
cd G7_Enterprise_Web_Dev 
```

2. **Set Up the Database**:

* Navigate to the `/database` folder.  
* Run the SQL scripts to create the database and tables:

```sql
source database_setup.sql;
```

* Update configuration files with your database credentials.

3. **Run the REST API**:

```bash
python api/api_server.py
```

* Access endpoints via curl or Postman (see Authentication & Security section).  

4. **Testing & Validation**:

* Test endpoints for GET, POST, PUT, DELETE.

