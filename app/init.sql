CREATE TABLE IF NOT EXISTS events (
    event_id UUID PRIMARY KEY,
    user_id INT NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    event_time TIMESTAMP NOT NULL,
    page_url VARCHAR(255),
    product_id VARCHAR(50),
    amount NUMERIC(10, 2),
    error_code VARCHAR(50)
);