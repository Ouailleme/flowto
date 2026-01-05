-- Fix demo user password hash
-- Password: Demo2026!
-- Hash generated with bcrypt (cost factor 12)

UPDATE users 
SET hashed_password = '$2b$12$LQv3c1yqBWVHxkd0LHAkCODpm6Z4jKQJX9KQjP8.HvO8F8X9YCxOy',
    updated_at = NOW()
WHERE email = 'demo@financeai.com';

-- Verify update
SELECT email, created_at, updated_at, is_verified 
FROM users 
WHERE email = 'demo@financeai.com';


