-- Fix users table schema to match SQLAlchemy model
-- This script adds missing columns and renames full_name to company_name

-- Add missing columns
ALTER TABLE users ADD COLUMN IF NOT EXISTS company_name VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS company_size VARCHAR(50);
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_plan VARCHAR(50) DEFAULT 'trial';
ALTER TABLE users ADD COLUMN IF NOT EXISTS subscription_status VARCHAR(50) DEFAULT 'active';
ALTER TABLE users ADD COLUMN IF NOT EXISTS stripe_customer_id VARCHAR(255);
ALTER TABLE users ADD COLUMN IF NOT EXISTS is_onboarded BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMPTZ;

-- Copy full_name to company_name for existing users
UPDATE users SET company_name = full_name WHERE company_name IS NULL;

-- Drop full_name if it exists (optional, keeping it for backward compatibility)
-- ALTER TABLE users DROP COLUMN IF EXISTS full_name;

-- Drop is_superuser if you don't need it (optional)
-- ALTER TABLE users DROP COLUMN IF EXISTS is_superuser;

-- Verify the changes
SELECT column_name, data_type FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;


