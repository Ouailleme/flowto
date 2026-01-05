"""Test database connection with asyncpg"""
import asyncio
import asyncpg

async def test_connection():
    """Test PostgreSQL connection"""
    print("Testing PostgreSQL connection...")
    
    # Try different connection methods
    configs = [
        {
            "name": "localhost with password",
            "host": "localhost",
            "port": 5433,
            "user": "financeai",
            "password": "financeai2026",
            "database": "financeai"
        },
        {
            "name": "127.0.0.1 with password",
            "host": "127.0.0.1",
            "port": 5433,
            "user": "financeai",
            "password": "financeai2026",
            "database": "financeai"
        },
        {
            "name": "localhost without password (trust)",
            "host": "localhost",
            "port": 5433,
            "user": "financeai",
            "password": None,
            "database": "financeai"
        },
    ]
    
    for config in configs:
        print(f"\n[TEST] {config['name']}")
        print(f"  Host: {config['host']}:{config['port']}")
        print(f"  User: {config['user']}")
        print(f"  Password: {'***' if config['password'] else 'None'}")
        
        try:
            if config['password']:
                conn = await asyncpg.connect(
                    host=config['host'],
                    port=config['port'],
                    user=config['user'],
                    password=config['password'],
                    database=config['database']
                )
            else:
                conn = await asyncpg.connect(
                    host=config['host'],
                    port=config['port'],
                    user=config['user'],
                    database=config['database']
                )
            
            # Test query
            result = await conn.fetchval("SELECT 'Connection OK'")
            print(f"  [SUCCESS] {result}")
            
            # Close connection
            await conn.close()
            
        except Exception as e:
            print(f"  [FAILED] {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())


