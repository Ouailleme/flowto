"""Initialize database with sample data"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import date, datetime, timedelta
from decimal import Decimal

from app.config import settings
from app.core.database import Base
from app.models.user import User
from app.models.bank_account import BankAccount
from app.models.transaction import Transaction
from app.models.invoice import Invoice
from app.core.security import hash_password


async def init_db():
    """Initialize database with tables and sample data"""
    
    # Create engine
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Tables created")
    
    # Create session
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with SessionLocal() as session:
        # Create demo user
        demo_user = User(
            email="demo@financeai.com",
            hashed_password=hash_password("demo123"),
            full_name="Demo User",
            is_active=True,
            language="fr",
            country="FR",
            currency="EUR",
            timezone="Europe/Paris",
            locale="fr_FR",
        )
        session.add(demo_user)
        await session.flush()
        
        print(f"✅ User created: {demo_user.email}")
        
        # Create bank account
        bank_account = BankAccount(
            user_id=demo_user.id,
            bank_name="BNP Paribas",
            account_type="checking",
            iban="FR7630006000011234567890189",
            balance=Decimal("15000.00"),
            currency="EUR",
            is_active=True,
        )
        session.add(bank_account)
        await session.flush()
        
        print(f"✅ Bank account created: {bank_account.bank_name}")
        
        # Create sample transactions
        transactions_data = [
            ("VIREMENT LOYER BUREAU JANVIER", Decimal("-1500.00"), "loyer_bureau"),
            ("VIR CLIENT ACME CORP", Decimal("2500.00"), "vente_client"),
            ("PRELEVEMENT EDF JANVIER", Decimal("-120.00"), "electricite_eau"),
            ("FOURNITURES BUREAU AMAZON", Decimal("-89.99"), "fournitures_bureau"),
            ("VIR CLIENT BETA SAS", Decimal("1800.00"), "vente_client"),
            ("SALAIRE EMPLOYE JEAN", Decimal("-2200.00"), "salaire_employe"),
            ("FRAIS BANCAIRES", Decimal("-15.00"), "frais_bancaires"),
        ]
        
        for i, (desc, amount, category) in enumerate(transactions_data):
            tx = Transaction(
                bank_account_id=bank_account.id,
                date=datetime.utcnow() - timedelta(days=30-i),
                description=desc,
                amount=amount,
                currency="EUR",
                transaction_type="credit" if amount > 0 else "debit",
                category=category,
                category_confidence=Decimal("0.95"),
                is_reconciled=False,
            )
            session.add(tx)
        
        print(f"✅ {len(transactions_data)} transactions created")
        
        # Create sample invoices
        invoices_data = [
            ("INV-2026-001", "ACME Corp", Decimal("2500.00"), "pending", 30),
            ("INV-2026-002", "Beta SAS", Decimal("1800.00"), "paid", 15),
            ("INV-2026-003", "Gamma Ltd", Decimal("3200.00"), "pending", 45),
            ("INV-2026-004", "Delta Inc", Decimal("1200.00"), "overdue", -5),
        ]
        
        for inv_num, client, amount, status, days_offset in invoices_data:
            invoice = Invoice(
                user_id=demo_user.id,
                invoice_number=inv_num,
                client_name=client,
                client_email=f"{client.lower().replace(' ', '.')}@example.com",
                amount=amount,
                tax_amount=amount * Decimal("0.20"),
                total_amount=amount * Decimal("1.20"),
                currency="EUR",
                issue_date=date.today() - timedelta(days=abs(days_offset)),
                due_date=date.today() + timedelta(days=days_offset),
                status=status,
                is_reconciled=(status == "paid"),
            )
            session.add(invoice)
        
        print(f"✅ {len(invoices_data)} invoices created")
        
        await session.commit()
    
    await engine.dispose()
    
    print("\n🎉 Database initialized successfully!")
    print("\n📝 Demo credentials:")
    print("   Email: demo@financeai.com")
    print("   Password: demo123")


if __name__ == "__main__":
    asyncio.run(init_db())


