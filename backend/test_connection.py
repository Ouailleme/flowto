"""Test PostgreSQL connection"""
import asyncio
import asyncpg

async def test_connection():
    print("Testing PostgreSQL connection...")
    print("URL: postgresql://financeai:financeai2026@127.0.0.1:5433/financeai")
    
    try:
        conn = await asyncpg.connect(
            user='financeai',
            password='financeai2026',
            database='financeai',
            host='127.0.0.1',
            port=5433
        )
        print("✅ Connection successful!")
        
        # Test query
        version = await conn.fetchval('SELECT version()')
        print(f"PostgreSQL version: {version}")
        
        await conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_connection())


