"""Claude AI client for transaction categorization and reconciliation"""
import anthropic
from typing import List, Dict, Optional, Tuple
from decimal import Decimal
import json
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class ClaudeAIError(Exception):
    """Claude AI error"""
    pass


class ClaudeClient:
    """
    Client for Claude AI (Anthropic)
    
    Used for:
    - Transaction categorization
    - Fuzzy invoice reconciliation
    - Email generation for reminders
    """
    
    def __init__(self, api_key: str = None):
        """Initialize Claude client"""
        self.api_key = api_key or settings.CLAUDE_API_KEY
        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def categorize_transaction(
        self,
        description: str,
        amount: Decimal,
        transaction_type: str
    ) -> Tuple[str, Decimal]:
        """
        Categorize a transaction using Claude AI.
        
        Args:
            description: Transaction description
            amount: Transaction amount
            transaction_type: credit or debit
            
        Returns:
            Tuple of (category, confidence_score)
        """
        prompt = f"""You are a financial transaction categorization expert for French SMEs.

Categorize this transaction into ONE of these categories:
- salaire_employe
- loyer_bureau
- fournitures_bureau
- services_professionnels
- publicite_marketing
- frais_bancaires
- assurance
- impots_taxes
- achat_materiel
- frais_deplacement
- telecommunications
- electricite_eau
- vente_client
- remboursement
- autre

Transaction:
- Description: {description}
- Amount: {amount} EUR
- Type: {transaction_type}

Respond ONLY with valid JSON (no markdown, no explanation):
{{
  "category": "category_name",
  "confidence": 0.95,
  "reasoning": "Brief explanation in French"
}}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.3,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            
            # Parse JSON response
            result = json.loads(content)
            
            category = result.get("category", "autre")
            confidence = Decimal(str(result.get("confidence", 0.5)))
            
            logger.info(
                f"Transaction categorized: '{description[:50]}' → {category} "
                f"(confidence: {confidence})"
            )
            
            return category, confidence
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {content}")
            return "autre", Decimal("0.0")
        except Exception as e:
            logger.error(f"Claude categorization error: {e}")
            raise ClaudeAIError(f"Categorization failed: {e}")
    
    async def find_matching_invoice(
        self,
        transaction: Dict,
        invoices: List[Dict]
    ) -> Optional[Dict]:
        """
        Find matching invoice for a transaction using fuzzy AI matching.
        
        Args:
            transaction: Transaction data
            invoices: List of pending invoices
            
        Returns:
            Best matching invoice with score and reasoning, or None
        """
        if not invoices:
            return None
        
        # Format invoices for prompt
        invoices_text = "\n".join([
            f"- Invoice {inv['invoice_number']}: "
            f"{inv['client_name']}, "
            f"{inv['total_amount']} {inv['currency']}, "
            f"due {inv['due_date']}"
            for inv in invoices
        ])
        
        prompt = f"""You are an expert in bank reconciliation for French SMEs.

Given this bank transaction, find the best matching invoice.

Transaction:
- Description: {transaction['description']}
- Amount: {transaction['amount']} {transaction['currency']}
- Date: {transaction['date']}

Pending Invoices:
{invoices_text}

Rules:
- Amounts should match (±5% tolerance acceptable)
- Date should be close (within 30 days)
- Look for client name or invoice number in description
- Consider partial payments

Respond ONLY with valid JSON (no markdown):
{{
  "match_found": true/false,
  "invoice_number": "INV-XXX" or null,
  "match_score": 0.95,
  "match_method": "exact"/"reference"/"fuzzy_ai",
  "reasoning": "Brief explanation in French"
}}"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=700,
                temperature=0.2,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            result = json.loads(content)
            
            if not result.get("match_found"):
                return None
            
            # Find the invoice
            invoice_number = result.get("invoice_number")
            matched_invoice = next(
                (inv for inv in invoices if inv["invoice_number"] == invoice_number),
                None
            )
            
            if matched_invoice:
                logger.info(
                    f"Invoice match found: Transaction '{transaction['description'][:50]}' "
                    f"→ Invoice {invoice_number} (score: {result['match_score']})"
                )
                
                return {
                    "invoice": matched_invoice,
                    "match_score": Decimal(str(result["match_score"])),
                    "match_method": result.get("match_method", "fuzzy_ai"),
                    "reasoning": result.get("reasoning", "")
                }
            
            return None
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {content}")
            return None
        except Exception as e:
            logger.error(f"Claude reconciliation error: {e}")
            return None
    
    async def generate_reminder_email(
        self,
        invoice: Dict,
        reminder_type: str,
        language: str = "fr"
    ) -> Dict[str, str]:
        """
        Generate personalized reminder email using Claude.
        
        Args:
            invoice: Invoice data
            reminder_type: first, second, final
            language: Email language (fr, en, es, de, it, nl)
            
        Returns:
            Dict with subject and body (HTML)
        """
        tone_map = {
            "first": "professional and courteous",
            "second": "firmer but still polite",
            "final": "formal and urgent"
        }
        
        tone = tone_map.get(reminder_type, "professional")
        
        prompt = f"""You are an expert in writing professional payment reminder emails for French SMEs.

Write a {tone} payment reminder email in {language.upper()}.

Invoice details:
- Invoice number: {invoice['invoice_number']}
- Client: {invoice['client_name']}
- Amount: {invoice['total_amount']} {invoice['currency']}
- Due date: {invoice['due_date']}
- Days overdue: {invoice.get('days_overdue', 'N/A')}

This is the {reminder_type} reminder.

Respond with valid JSON (no markdown):
{{
  "subject": "Email subject",
  "body_html": "<html>Email body with proper HTML formatting</html>"
}}

Requirements:
- Professional tone
- Clear call to action
- Payment instructions
- Contact information placeholder
- Proper HTML structure
"""
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.content[0].text.strip()
            result = json.loads(content)
            
            logger.info(
                f"Reminder email generated for invoice {invoice['invoice_number']} "
                f"({reminder_type})"
            )
            
            return {
                "subject": result.get("subject", f"Reminder: Invoice {invoice['invoice_number']}"),
                "body": result.get("body_html", "")
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Claude response: {content}")
            # Fallback
            return {
                "subject": f"Reminder: Invoice {invoice['invoice_number']}",
                "body": f"<p>Dear {invoice['client_name']},</p><p>This is a reminder about invoice {invoice['invoice_number']}.</p>"
            }
        except Exception as e:
            logger.error(f"Claude email generation error: {e}")
            raise ClaudeAIError(f"Email generation failed: {e}")
    
    async def categorize_transactions_batch(
        self,
        transactions: List[Dict]
    ) -> List[Tuple[str, Decimal]]:
        """
        Categorize multiple transactions in one call (more efficient).
        
        Args:
            transactions: List of transactions
            
        Returns:
            List of (category, confidence) tuples
        """
        # For simplicity, call individual categorization
        # In production, could batch in single prompt
        results = []
        for tx in transactions:
            category, confidence = await self.categorize_transaction(
                tx["description"],
                Decimal(str(tx["amount"])),
                tx.get("transaction_type", "debit")
            )
            results.append((category, confidence))
        
        return results


