"""Reconciliation service - AI-powered invoice matching"""
from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from uuid import UUID
from decimal import Decimal
from datetime import datetime
import logging

from app.models.reconciliation import Reconciliation
from app.models.transaction import Transaction
from app.models.invoice import Invoice
from app.schemas.reconciliation import ReconciliationCreate, ReconciliationSuggestion
from app.integrations.claude_client import ClaudeClient
from app.services.invoice_service import InvoiceService

logger = logging.getLogger(__name__)


class ReconciliationService:
    """Service for bank reconciliation (transaction ↔ invoice matching)"""
    
    @staticmethod
    async def create_reconciliation(
        db: AsyncSession,
        user_id: UUID,
        reconciliation_data: ReconciliationCreate
    ) -> Reconciliation:
        """
        Create a reconciliation (link transaction to invoice).
        
        Args:
            db: Database session
            user_id: User ID
            reconciliation_data: Reconciliation data
            
        Returns:
            Created reconciliation
        """
        # Verify transaction and invoice belong to user
        transaction = await db.get(Transaction, reconciliation_data.transaction_id)
        invoice = await db.get(Invoice, reconciliation_data.invoice_id)
        
        if not transaction or not invoice:
            raise ValueError("Transaction or invoice not found")
        
        # Verify ownership (through bank account for transaction)
        from app.models.bank_account import BankAccount
        bank_account = await db.get(BankAccount, transaction.bank_account_id)
        
        if not bank_account or bank_account.user_id != user_id:
            raise ValueError("Transaction does not belong to user")
        
        if invoice.user_id != user_id:
            raise ValueError("Invoice does not belong to user")
        
        # Check if already reconciled
        if transaction.is_reconciled:
            raise ValueError("Transaction already reconciled")
        
        if invoice.is_reconciled:
            raise ValueError("Invoice already reconciled")
        
        # Create reconciliation
        reconciliation = Reconciliation(
            user_id=user_id,
            transaction_id=reconciliation_data.transaction_id,
            invoice_id=reconciliation_data.invoice_id,
            match_score=reconciliation_data.match_score,
            match_method=reconciliation_data.match_method,
            ai_reasoning=reconciliation_data.ai_reasoning,
            validated_by=reconciliation_data.validated_by,
            validated_at=datetime.utcnow(),
            notes=reconciliation_data.notes
        )
        
        db.add(reconciliation)
        
        # Update transaction and invoice
        transaction.is_reconciled = True
        transaction.reconciliation_id = reconciliation.id
        
        invoice.is_reconciled = True
        invoice.reconciliation_id = reconciliation.id
        invoice.status = "paid"
        invoice.payment_date = transaction.date.date()
        
        await db.flush()
        
        logger.info(
            f"Reconciliation created: Transaction {transaction.id} ↔ "
            f"Invoice {invoice.invoice_number} (method: {reconciliation.match_method})"
        )
        
        return reconciliation
    
    @staticmethod
    async def suggest_reconciliations(
        db: AsyncSession,
        user_id: UUID,
        transaction_id: UUID,
        ai_client: ClaudeClient = None
    ) -> List[ReconciliationSuggestion]:
        """
        Get AI-powered reconciliation suggestions for a transaction.
        
        Args:
            db: Database session
            user_id: User ID
            transaction_id: Transaction ID to match
            ai_client: Claude AI client (optional, created if not provided)
            
        Returns:
            List of reconciliation suggestions
        """
        # Get transaction
        transaction = await db.get(Transaction, transaction_id)
        if not transaction:
            raise ValueError("Transaction not found")
        
        # Verify ownership
        from app.models.bank_account import BankAccount
        bank_account = await db.get(BankAccount, transaction.bank_account_id)
        if not bank_account or bank_account.user_id != user_id:
            raise ValueError("Transaction does not belong to user")
        
        # Get pending invoices
        from app.schemas.invoice import InvoiceFilter
        invoices, _ = await InvoiceService.get_invoices(
            db,
            user_id,
            InvoiceFilter(status="pending", is_reconciled=False),
            page=1,
            page_size=100
        )
        
        if not invoices:
            return []
        
        # Try exact matches first (amount + reference)
        suggestions = []
        
        # 1. Exact amount match
        for invoice in invoices:
            if abs(transaction.amount - invoice.total_amount) < Decimal("0.01"):
                # Check if invoice number in description
                if invoice.invoice_number.lower() in transaction.description.lower():
                    suggestions.append(ReconciliationSuggestion(
                        transaction_id=transaction.id,
                        invoice_id=invoice.id,
                        match_score=Decimal("1.0"),
                        match_method="exact",
                        reasoning=f"Montant exact ({invoice.total_amount}) et référence trouvée",
                        transaction_description=transaction.description,
                        transaction_amount=transaction.amount,
                        invoice_number=invoice.invoice_number,
                        invoice_amount=invoice.total_amount
                    ))
                else:
                    suggestions.append(ReconciliationSuggestion(
                        transaction_id=transaction.id,
                        invoice_id=invoice.id,
                        match_score=Decimal("0.85"),
                        match_method="reference",
                        reasoning=f"Montant exact ({invoice.total_amount})",
                        transaction_description=transaction.description,
                        transaction_amount=transaction.amount,
                        invoice_number=invoice.invoice_number,
                        invoice_amount=invoice.total_amount
                    ))
        
        # 2. If no exact match, use AI
        if not suggestions and ai_client:
            try:
                # Format data for AI
                transaction_data = {
                    "description": transaction.description,
                    "amount": float(transaction.amount),
                    "currency": transaction.currency,
                    "date": transaction.date.isoformat()
                }
                
                invoices_data = [
                    {
                        "invoice_number": inv.invoice_number,
                        "client_name": inv.client_name,
                        "total_amount": float(inv.total_amount),
                        "currency": inv.currency,
                        "due_date": inv.due_date.isoformat()
                    }
                    for inv in invoices
                ]
                
                ai_match = await ai_client.find_matching_invoice(
                    transaction_data,
                    invoices_data
                )
                
                if ai_match:
                    matched_invoice = ai_match["invoice"]
                    invoice = next(
                        inv for inv in invoices
                        if inv.invoice_number == matched_invoice["invoice_number"]
                    )
                    
                    suggestions.append(ReconciliationSuggestion(
                        transaction_id=transaction.id,
                        invoice_id=invoice.id,
                        match_score=ai_match["match_score"],
                        match_method=ai_match["match_method"],
                        reasoning=ai_match["reasoning"],
                        transaction_description=transaction.description,
                        transaction_amount=transaction.amount,
                        invoice_number=invoice.invoice_number,
                        invoice_amount=invoice.total_amount
                    ))
                    
            except Exception as e:
                logger.error(f"AI reconciliation error: {e}")
        
        # Sort by score
        suggestions.sort(key=lambda x: x.match_score, reverse=True)
        
        return suggestions[:5]  # Top 5 suggestions
    
    @staticmethod
    async def auto_reconcile_transaction(
        db: AsyncSession,
        user_id: UUID,
        transaction_id: UUID,
        ai_client: ClaudeClient = None
    ) -> Optional[Reconciliation]:
        """
        Automatically reconcile a transaction if high-confidence match found.
        
        Auto-reconciles if:
        - Match score >= 0.95
        - Method is "exact"
        
        Args:
            db: Database session
            user_id: User ID
            transaction_id: Transaction ID
            ai_client: Claude AI client
            
        Returns:
            Reconciliation if auto-matched, None otherwise
        """
        suggestions = await ReconciliationService.suggest_reconciliations(
            db,
            user_id,
            transaction_id,
            ai_client
        )
        
        if not suggestions:
            return None
        
        best_match = suggestions[0]
        
        # Auto-reconcile if high confidence
        if best_match.match_score >= Decimal("0.95") and best_match.match_method == "exact":
            reconciliation_data = ReconciliationCreate(
                transaction_id=transaction_id,
                invoice_id=best_match.invoice_id,
                match_score=best_match.match_score,
                match_method=best_match.match_method,
                ai_reasoning=best_match.reasoning,
                validated_by="ai"
            )
            
            reconciliation = await ReconciliationService.create_reconciliation(
                db,
                user_id,
                reconciliation_data
            )
            
            logger.info(f"Auto-reconciled transaction {transaction_id}")
            return reconciliation
        
        return None
    
    @staticmethod
    async def get_reconciliation_stats(
        db: AsyncSession,
        user_id: UUID
    ) -> dict:
        """
        Get reconciliation statistics for user.
        
        Returns:
            Stats dict with counts
        """
        from sqlalchemy import func
        
        # Total reconciliations
        total_result = await db.execute(
            select(func.count(Reconciliation.id))
            .where(Reconciliation.user_id == user_id)
        )
        total = total_result.scalar() or 0
        
        # By method
        method_result = await db.execute(
            select(
                Reconciliation.match_method,
                func.count(Reconciliation.id)
            )
            .where(Reconciliation.user_id == user_id)
            .group_by(Reconciliation.match_method)
        )
        by_method = dict(method_result.all())
        
        # By validator
        validator_result = await db.execute(
            select(
                Reconciliation.validated_by,
                func.count(Reconciliation.id)
            )
            .where(Reconciliation.user_id == user_id)
            .group_by(Reconciliation.validated_by)
        )
        by_validator = dict(validator_result.all())
        
        return {
            "total": total,
            "by_method": by_method,
            "by_validator": by_validator,
            "auto_reconciliation_rate": (
                by_validator.get("ai", 0) / total * 100 if total > 0 else 0
            )
        }


