"""Test authentication directly without FastAPI"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.services.auth_service import AuthService
from app.config import settings

async def test_auth():
    """Test authentication"""
    print("Testing authentication...")
    print(f"DATABASE_URL: {settings.DATABASE_URL[:50]}...")
    
    # Create engine
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        print("\n[OK] Database session created")
        
        # Test authentication
        print("\n[TEST] Attempting to authenticate...")
        print("   Email: demo@financeai.com")
        print("   Password: Demo2026!")
        
        try:
            user = await AuthService.authenticate_user(
                session,
                "demo@financeai.com",
                "Demo2026!"
            )
            
            if user:
                print(f"\n[SUCCESS] Authentication successful!")
                print(f"   User ID: {user.id}")
                print(f"   Email: {user.email}")
                print(f"   Full Name: {user.full_name}")
                print(f"   Is Active: {user.is_active}")
                print(f"   Is Verified: {user.is_verified}")
                
                # Test token creation
                print("\n[TEST] Creating tokens...")
                tokens = AuthService.create_tokens(user.id)
                print(f"[SUCCESS] Access Token: {tokens['access_token'][:50]}...")
                print(f"[SUCCESS] Refresh Token: {tokens['refresh_token'][:50]}...")
            else:
                print(f"\n[FAILED] Authentication failed!")
                
        except Exception as e:
            print(f"\n[ERROR] Error during authentication:")
            print(f"   {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_auth())

