# G7 Enterprise Web DEv

### Project description:
This project is about creating MOMO app. Which will be used to receive and process the inserted data for providing the required information.

### Members list:
> Gakwaya Ineza Ketia (Group leader)

> Rwakunda Kaliza Sheila Milena

> Hirwa Armstrong



This is Draw.io link: https://drive.google.com/file/d/1T7GoRHwGNc2ddbfRLX7-H-Gn9S0lQ0fy/view?usp=sharing 

### Database documentation:
In this step, we designed database with ERD(Entity Relational Diagram) and then implemented it using SQL(Structured Query Language) so that we can create the exact database when we are done designing the front-end part.

We first identified what entities we will need and after we designed a diagram to represent those entities and the atrributes each holds and also the relationship they have between themselves which includes 1 to many, etc...

After drawing the ERD, we applied the diagram into SQL so that we can turn our diagram into a real database using sql language. That is where we created our file and called it database_setup with sql extension that it can be ran whenever we need to use it. 

Within this file, is where the magic was done. This is where we created our database called "momo_db" which will hold all the entities and data that will be inserted into these entities. After creating the database, i created user table with multiple attributes for holding all user's data that will be required by the system. Those attributes are userId which will uniquely identify a user from other users, firstName and lastName, email, phoneNumber, accountNumber, creationDate and updationDate. This was the same process for other tables/entities which are transaction, transactionCategories and systemLog with their respective attributes.

Afterwards, i did serialization shifting SQL file to a JSON file. I got the SQL structure and rewrote it in JSON structure where tables are curly braces, attributes are keys and data are values. And all of them are inside a square bracket which represent the database in this case.

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


