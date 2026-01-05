"""Reset demo user password for E2E tests"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.security import hash_password
from app.core.database import get_db, engine
from sqlalchemy import text


async def reset_demo_user():
    """Reset demo user with correct password for E2E tests"""
    
    # Password for E2E tests
    demo_password = "Demo2026!"
    hashed_password = hash_password(demo_password)
    
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
        else:
            # Create user if not exists
            await conn.execute(
                text("""
                    INSERT INTO users (
                        email, 
                        hashed_password, 
                        company_name, 
                        is_verified, 
                        is_active,
                        subscription_plan,
                        subscription_status,
                        language,
                        country,
                        currency,
                        timezone,
                        locale
                    ) VALUES (
                        'demo@financeai.com',
                        :password,
                        'Demo Company',
                        TRUE,
                        TRUE,
                        'trial',
                        'active',
                        'fr',
                        'FR',
                        'EUR',
                        'Europe/Paris',
                        'fr_FR'
                    )
                """),
                {"password": hashed_password}
            )
            print(f"\n✅ Demo user created successfully!")
    
    print("\n✅ Demo user is ready for E2E tests!")
    print(f"   Login at: http://localhost:3000/auth/login")
    print(f"   Email: demo@financeai.com")
    print(f"   Password: {demo_password}")


if __name__ == "__main__":
    asyncio.run(reset_demo_user())


