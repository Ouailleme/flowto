"""Test PostgreSQL connection WITHOUT password (trust mode)"""
import asyncio
import asyncpg

async def test_connection():
    print("Testing PostgreSQL connection (trust mode)...")
    print("URL: postgresql://financeai@127.0.0.1:5433/financeai")
    
    try:
        conn = await asyncpg.connect(
            user='financeai',
            # NO PASSWORD for trust mode
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


