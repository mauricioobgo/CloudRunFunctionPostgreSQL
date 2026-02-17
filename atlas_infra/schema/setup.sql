-- 1. Create the schema if it doesn't exist
-- This prevents the "schema 'app' not found" error in Docker
CREATE SCHEMA IF NOT EXISTS app;

-- 2. Ensure the search_path includes 'app' 
-- This helps Atlas map un-prefixed tables to the right place
SET search_path TO app, public;

-- 3. Grant permissions (Required if using a non-superuser, 
-- but good practice for DBAs to include)
GRANT ALL ON SCHEMA app TO postgres;