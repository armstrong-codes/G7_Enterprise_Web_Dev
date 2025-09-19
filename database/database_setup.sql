DROP DATABASE IF EXISTS momo_db;
CREATE DATABASE momo_db;
USE momo_db;

CREATE TABLE User (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each user',
    first_name VARCHAR(50) NOT NULL COMMENT 'User first name',
    last_name VARCHAR(50) NOT NULL COMMENT 'User last name',
    email VARCHAR(100) UNIQUE NOT NULL COMMENT 'Unique email address',
    phone_number VARCHAR(20) UNIQUE COMMENT 'User phone number',
    address VARCHAR(255) COMMENT 'User address',
    account_number VARCHAR(20) UNIQUE NOT NULL COMMENT 'Unique account number for transactions',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation time',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Record last update time',
    INDEX idx_users_email (email),
    INDEX idx_users_account (account_number)
);

CREATE TABLE Transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique category id',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Transaction type',
    description VARCHAR(255) COMMENT 'Category description'
);

CREATE TABLE Transaction (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique transaction id',
    sender_id INT NOT NULL COMMENT 'User who initiates the transaction',
    receiver_id INT NOT NULL COMMENT 'User who receives the transaction',
    category_id INT NOT NULL COMMENT 'Transaction category',
    amount DECIMAL(12,2) NOT NULL COMMENT 'Transaction amount',
    currency VARCHAR(10) DEFAULT 'USD' COMMENT 'Currency code',
    status ENUM('pending','completed','failed') NOT NULL DEFAULT 'pending' COMMENT 'Transaction status',
    transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When the transaction occurred',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Record creation time',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Record update time',

    CONSTRAINT fk_transactions_sender FOREIGN KEY (sender_id) REFERENCES User(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_transactions_receiver FOREIGN KEY (receiver_id) REFERENCES User(user_id) ON DELETE CASCADE,
    CONSTRAINT fk_transactions_category FOREIGN KEY (category_id) REFERENCES Transaction_categories(category_id) ON DELETE RESTRICT,

    CHECK (amount > 0),

    INDEX idx_transactions_sender (sender_id),
    INDEX idx_transactions_receiver (receiver_id),
    INDEX idx_transactions_category (category_id),
    INDEX idx_transactions_date (transaction_date)
);

CREATE TABLE System_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique log id',
    user_id INT NULL COMMENT 'User associated with the action',
    transaction_id INT NULL COMMENT 'Related transaction if any',
    action VARCHAR(50) NOT NULL COMMENT 'Performed action',
    log_message VARCHAR(255) COMMENT 'Detailed log message',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'When log entry was created',

    CONSTRAINT fk_logs_user FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE SET NULL,
    CONSTRAINT fk_logs_transaction FOREIGN KEY (transaction_id) REFERENCES Transaction(transaction_id) ON DELETE SET NULL,

    INDEX idx_logs_user (user_id),
    INDEX idx_logs_transaction (transaction_id),
    INDEX idx_logs_action (action)
);

INSERT INTO User (first_name, last_name, email, phone_number, address, account_number)
VALUES
('Alice', 'Smith', 'alice@example.com', '+250788111111', 'Kigali, Rwanda', 'ACC1001'),
('Bob', 'Johnson', 'bob@example.com', '+250788222222', 'Nairobi, Kenya', 'ACC1002'),
('Charlie', 'Brown', 'charlie@example.com', '+250788333333', 'Kampala, Uganda', 'ACC1003'),
('David', 'Lee', 'david@example.com', '+250788444444', 'Dar es Salaam, Tanzania', 'ACC1004'),
('Eva', 'Green', 'eva@example.com', '+250788555555', 'Lagos, Nigeria', 'ACC1005');

INSERT INTO Transaction_categories (category_name, description)
VALUES
('Deposit', 'Funds added to an account'),
('Withdrawal', 'Funds withdrawn from an account'),
('Transfer', 'Funds sent between users'),
('Bill Payment', 'Payments for services'),
('Purchase', 'Purchases from merchants');

INSERT INTO Transaction (sender_id, receiver_id, category_id, amount, currency, status)
VALUES
(1, 2, 3, 150.00, 'USD', 'completed'),
(2, 3, 1, 200.00, 'USD', 'completed'),
(3, 4, 2, 50.00, 'USD', 'pending'),
(4, 5, 4, 100.00, 'USD', 'completed'),
(5, 1, 5, 75.50, 'USD', 'failed');

INSERT INTO System_Log (user_id, transaction_id, action, log_message)
VALUES
(1, 1, 'CREATE', 'Alice initiated a transfer to Bob'),
(2, 1, 'RECEIVE', 'Bob received transfer from Alice'),
(3, 2, 'DEPOSIT', 'Charlie deposited funds'),
(4, 3, 'WITHDRAWAL', 'David withdrawal pending approval'),
(5, 5, 'PURCHASE', 'Eva purchase failed due to insufficient funds');

SELECT * FROM Transaction WHERE status = 'completed';

UPDATE Transaction SET status = 'completed' WHERE transaction_id = 3;

DELETE FROM System_Log WHERE log_id = 5;

INSERT INTO User (first_name, last_name, email, phone_number, address, account_number)
VALUES ('Frank', 'Miller', 'frank@example.com', '+250788666666', 'Accra, Ghana', 'ACC1006');
