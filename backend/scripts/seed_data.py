"""
Seed database with realistic demo data.
Creates 3 users with invoices, transactions, and other data.
"""
import asyncio
import sys
from pathlib import Path
from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.security import hash_password
from app.models.user import User
from app.models.invoice import Invoice
from app.models.transaction import Transaction
from app.models.bank_account import BankAccount
from app.models import Base

# Demo users
DEMO_USERS = [
    {
        "email": "demo@flowto.fr",
        "password": "Demo123!",
        "full_name": "Demo User",
        "company_name": "Demo Corp",
        "company_size": "10-50",
        "is_verified": True,
    },
    {
        "email": "alice@startup.com",
        "password": "Alice123!",
        "full_name": "Alice Johnson",
        "company_name": "TechStartup SAS",
        "company_size": "1-10",
        "is_verified": True,
    },
    {
        "email": "bob@enterprise.com",
        "password": "Bob123!",
        "full_name": "Bob Martin",
        "company_name": "Enterprise Inc",
        "company_size": "200+",
        "is_verified": True,
    },
]

# Demo invoices per user
DEMO_INVOICES = [
    {
        "invoice_number": "INV-2026-001",
        "client_name": "Acme Corporation",
        "client_email": "accounting@acme.com",
        "amount": Decimal("2500.00"),
        "tax_amount": Decimal("500.00"),
        "currency": "EUR",
        "issue_date": date.today() - timedelta(days=30),
        "due_date": date.today() + timedelta(days=30),
        "status": "pending",
        "description": "Consulting services - December 2025",
    },
    {
        "invoice_number": "INV-2026-002",
        "client_name": "Startup SAS",
        "client_email": "finance@startup.com",
        "amount": Decimal("1200.00"),
        "tax_amount": Decimal("240.00"),
        "currency": "EUR",
        "issue_date": date.today() - timedelta(days=45),
        "due_date": date.today() - timedelta(days=15),
        "status": "overdue",
        "description": "Software development - November 2025",
    },
    {
        "invoice_number": "INV-2026-003",
        "client_name": "MegaCorp Ltd",
        "client_email": "billing@megacorp.com",
        "amount": Decimal("5000.00"),
        "tax_amount": Decimal("1000.00"),
        "currency": "EUR",
        "issue_date": date.today() - timedelta(days=60),
        "due_date": date.today() - timedelta(days=30),
        "payment_date": date.today() - timedelta(days=25),
        "status": "paid",
        "description": "Annual maintenance contract",
    },
]


async def create_demo_users(session: AsyncSession):
    """Create demo users."""
    print("Creating demo users...")
    users = []
    
    for user_data in DEMO_USERS:
        user = User(
            id=uuid4(),
            email=user_data["email"],
            hashed_password=hash_password(user_data["password"]),
            full_name=user_data["full_name"],
            company_name=user_data["company_name"],
            company_size=user_data["company_size"],
            is_verified=user_data["is_verified"],
            is_active=True,
        )
        session.add(user)
        users.append(user)
        print(f"  ✓ Created user: {user.email}")
    
    await session.flush()
    return users


async def create_demo_invoices(session: AsyncSession, user: User):
    """Create demo invoices for a user."""
    print(f"Creating invoices for {user.email}...")
    
    for invoice_data in DEMO_INVOICES:
        # Calculate total amount
        total_amount = invoice_data["amount"] + invoice_data["tax_amount"]
        
        invoice = Invoice(
            id=uuid4(),
            user_id=user.id,
            invoice_number=f"{user.email.split('@')[0].upper()}-{invoice_data['invoice_number']}",
            client_name=invoice_data["client_name"],
            client_email=invoice_data["client_email"],
            amount=invoice_data["amount"],
            tax_amount=invoice_data["tax_amount"],
            total_amount=total_amount,
            currency=invoice_data["currency"],
            issue_date=invoice_data["issue_date"],
            due_date=invoice_data["due_date"],
            payment_date=invoice_data.get("payment_date"),
            status=invoice_data["status"],
            description=invoice_data["description"],
        )
        session.add(invoice)
        print(f"  ✓ Created invoice: {invoice.invoice_number} ({invoice.status})")


async def create_demo_bank_accounts(session: AsyncSession, user: User):
    """Create demo bank accounts for a user."""
    print(f"Creating bank accounts for {user.email}...")
    
    accounts = [
        {
            "bank_name": "BNP Paribas",
            "account_name": "Compte Courant Pro",
            "account_type": "checking",
            "balance": Decimal("15000.00"),
            "currency": "EUR",
            "is_active": True,
        },
        {
            "bank_name": "Crédit Agricole",
            "account_name": "Compte Épargne",
            "account_type": "savings",
            "balance": Decimal("25000.00"),
            "currency": "EUR",
            "is_active": True,
        },
    ]
    
    for account_data in accounts:
        account = BankAccount(
            id=uuid4(),
            user_id=user.id,
            bank_name=account_data["bank_name"],
            account_name=account_data["account_name"],
            account_type=account_data["account_type"],
            balance=account_data["balance"],
            currency=account_data["currency"],
            is_active=account_data["is_active"],
        )
        session.add(account)
        print(f"  ✓ Created bank account: {account.account_name} ({account.bank_name})")


async def main():
    """Main seed function."""
    print("\n" + "=" * 60)
    print("SEEDING DATABASE WITH DEMO DATA")
    print("=" * 60 + "\n")
    
    # Create async engine
    engine = create_async_engine(settings.database_url, echo=False)
    
    # Create tables
    async with engine.begin() as conn:
        print("Ensuring database tables exist...")
        await conn.run_sync(Base.metadata.create_all)
        print("✓ Database schema ready\n")
    
    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        try:
            # Create users
            users = await create_demo_users(session)
            print()
            
            # Create data for each user
            for user in users:
                await create_demo_invoices(session, user)
                await create_demo_bank_accounts(session, user)
                print()
            
            # Commit transaction
            await session.commit()
            
            print("=" * 60)
            print("✓ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("\nDemo credentials:")
            for user_data in DEMO_USERS:
                print(f"  Email: {user_data['email']}")
                print(f"  Password: {user_data['password']}")
                print()
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ ERROR: {e}")
            raise
    
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())

