"""Simple script to reset demo user password"""
import asyncio
import sys
from pathlib import Path
import bcrypt

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import engine
from sqlalchemy import text


async def reset_demo_user():
    """Reset demo user with correct password for E2E tests"""
    
    # Password for E2E tests
    demo_password = "Demo2026!"
    
    # Hash password with bcrypt directly
    password_bytes = demo_password.encode('utf-8')[:72]  # Truncate to 72 bytes for bcrypt
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    print("🔐 Resetting demo user password...")
    print(f"   Email: demo@financeai.com")
    print(f"   Password: {demo_password}")
    print(f"   Hashed: {hashed_password[:50]}...")
    
    # Update password in database
    async with engine.begin() as conn:
        result = await conn.execute(
            text("""
                UPDATE users 
                SET hashed_password = :password,
                    is_verified = TRUE,
                    is_active = TRUE,
                    company_name = 'Demo Company',
                    subscription_plan = 'trial',
                    subscription_status = 'active'
                WHERE email = 'demo@financeai.com'
                RETURNING email, company_name
            """),
            {"password": hashed_password}
        )
        
        user = result.fetchone()
        
        if user:
            print(f"\n✅ Demo user updated successfully!")
            print(f"   Email: {user[0]}")
            print(f"   Company: {user[1]}")
            
            # Verify the password works
            verify_result = bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))
            print(f"\n🔐 Password verification: {'✅ OK' if verify_result else '❌ FAILED'}")
        else:
            print(f"\n❌ Demo user not found!")
    
    print("\n✅ Demo user is ready for E2E tests!")
    print(f"   Login at: http://localhost:3000/auth/login")
    print(f"   Email: demo@financeai.com")
    print(f"   Password: {demo_password}")


if __name__ == "__main__":
    asyncio.run(reset_demo_user())


