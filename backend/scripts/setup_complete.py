"""Complete setup script - Creates DB, tables, and demo data"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from datetime import datetime, timedelta, date
from decimal import Decimal
import uuid

from app.config import settings
from app.core.database import Base
from app.core.security import hash_password
from app.models.user import User
from app.models.bank_account import BankAccount
from app.models.transaction import Transaction
from app.models.invoice import Invoice


async def setup_complete():
    """Complete setup: create tables + demo data"""
    
    print("🚀 FinanceAI - Complete Setup")
    print("=" * 50)
    
    # Create engine
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
    )
    
    try:
        # Step 1: Create all tables
        print("\n📊 Step 1: Creating database tables...")
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        print("✅ All tables created!")
        
        # Step 2: Create demo user
        print("\n👤 Step 2: Creating demo user...")
        SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        
        async with SessionLocal() as session:
            # Create user
            demo_user = User(
                id=uuid.uuid4(),
                email="demo@financeai.com",
                hashed_password=hash_password("demo123"),
                full_name="Demo User",
                company_name="Demo Company SAS",
                is_active=True,
                is_verified=True,
                language="fr",
                country="FR",
                currency="EUR",
                timezone="Europe/Paris",
                locale="fr_FR",
            )
            session.add(demo_user)
            await session.flush()
            
            print(f"✅ User created: {demo_user.email}")
            
            # Step 3: Create bank account
            print("\n🏦 Step 3: Creating bank account...")
            bank_account = BankAccount(
                id=uuid.uuid4(),
                user_id=demo_user.id,
                bank_name="BNP Paribas",
                account_type="checking",
                iban="FR7630006000011234567890189",
                balance=Decimal("15420.50"),
                currency="EUR",
                is_active=True,
            )
            session.add(bank_account)
            await session.flush()
            
            print(f"✅ Bank account created: {bank_account.bank_name}")
            
            # Step 4: Create transactions
            print("\n💸 Step 4: Creating transactions...")
            transactions_data = [
                ("VIREMENT LOYER BUREAU JANVIER 2026", Decimal("-1500.00"), "loyer_bureau", datetime(2026, 1, 5)),
                ("VIR CLIENT ACME CORP - FACTURE 2026-001", Decimal("2500.00"), "vente_client", datetime(2026, 1, 4)),
                ("PRELEVEMENT EDF ELECTRICITE", Decimal("-120.50"), "electricite_eau", datetime(2026, 1, 3)),
                ("FOURNITURES BUREAU AMAZON BUSINESS", Decimal("-89.99"), "fournitures_bureau", datetime(2026, 1, 3)),
                ("VIR CLIENT BETA SAS - FACTURE 2026-002", Decimal("1800.00"), "vente_client", datetime(2026, 1, 2)),
                ("SALAIRE EMPLOYE JEAN DUPONT", Decimal("-2200.00"), "salaire_employe", datetime(2026, 1, 1)),
                ("FRAIS BANCAIRES DECEMBRE", Decimal("-15.00"), "frais_bancaires", datetime(2025, 12, 31)),
                ("VIR CLIENT GAMMA LTD - CONSULTING", Decimal("3200.00"), "vente_client", datetime(2025, 12, 30)),
                ("ABONNEMENT SAAS GITHUB PRO", Decimal("-45.00"), "abonnement_saas", datetime(2025, 12, 29)),
                ("RESTAURANT CLIENT BUSINESS", Decimal("-85.50"), "repas_affaires", datetime(2025, 12, 28)),
            ]
            
            for desc, amount, category, tx_date in transactions_data:
                tx = Transaction(
                    id=uuid.uuid4(),
                    bank_account_id=bank_account.id,
                    date=tx_date,
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
            
            # Step 5: Create invoices
            print("\n📄 Step 5: Creating invoices...")
            invoices_data = [
                ("INV-2026-001", "ACME Corp", "contact@acme.com", Decimal("2500.00"), "paid", date(2026, 1, 1), date(2026, 1, 31), True),
                ("INV-2026-002", "Beta SAS", "finance@beta.fr", Decimal("1800.00"), "paid", date(2026, 1, 2), date(2026, 2, 1), True),
                ("INV-2026-003", "Gamma Ltd", "billing@gamma.com", Decimal("3200.00"), "pending", date(2026, 1, 3), date(2026, 2, 2), False),
                ("INV-2025-012", "Delta Inc", "ap@delta.com", Decimal("1200.00"), "overdue", date(2025, 12, 15), date(2025, 12, 30), False),
                ("INV-2026-004", "Epsilon GmbH", "rechnung@epsilon.de", Decimal("4500.00"), "pending", date(2026, 1, 4), date(2026, 2, 3), False),
            ]
            
            for inv_num, client, email, amount, status, issue, due, reconciled in invoices_data:
                tax = amount * Decimal("0.20")  # 20% TVA
                invoice = Invoice(
                    id=uuid.uuid4(),
                    user_id=demo_user.id,
                    invoice_number=inv_num,
                    client_name=client,
                    client_email=email,
                    amount=amount,
                    tax_amount=tax,
                    total_amount=amount + tax,
                    currency="EUR",
                    issue_date=issue,
                    due_date=due,
                    status=status,
                    is_reconciled=reconciled,
                    description=f"Services de conseil et développement pour {client}",
                )
                session.add(invoice)
            
            print(f"✅ {len(invoices_data)} invoices created")
            
            # Commit all
            await session.commit()
            
        print("\n" + "=" * 50)
        print("🎉 Setup complete!")
        print("\n📝 Demo credentials:")
        print("   Email: demo@financeai.com")
        print("   Password: demo123")
        print("\n🌐 Access:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        print("\n✅ Ready to use!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        await engine.dispose()
    
    return True


if __name__ == "__main__":
    success = asyncio.run(setup_complete())
    sys.exit(0 if success else 1)


