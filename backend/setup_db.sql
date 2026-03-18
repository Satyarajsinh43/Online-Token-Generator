-- Connect to PostgreSQL server (e.g., using psql or pgAdmin)
-- Run these commands to set up the database and user

-- 1. Create the database
CREATE DATABASE token_generator_db;

-- 2. Create the user (you can change the password)
CREATE USER token_user WITH PASSWORD 'secure_password';

-- 3. Configure the user settings (recommended for Django)
ALTER ROLE token_user SET client_encoding TO 'utf8';
ALTER ROLE token_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE token_user SET timezone TO 'UTC';

-- 4. Grant privileges to the user on the database
GRANT ALL PRIVILEGES ON DATABASE token_generator_db TO token_user;

-- NOTE: After running this, update your settings.py DATABASES configuration:
-- 'NAME': 'token_generator_db',
-- 'USER': 'token_user',
-- 'PASSWORD': 'secure_password',
-- 'HOST': 'localhost',
-- 'PORT': '5432',
