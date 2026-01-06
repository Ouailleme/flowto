"""PDF Generation service for invoices"""
from typing import Optional
from io import BytesIO
from datetime import datetime
import logging

from weasyprint import HTML, CSS
from jinja2 import Template

from app.models.invoice import Invoice
from app.models.user import User

logger = logging.getLogger(__name__)


class PDFService:
    """Service for generating PDF documents"""
    
    # HTML template for invoice
    INVOICE_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Facture {{ invoice.invoice_number }}</title>
        <style>
            @page {
                size: A4;
                margin: 2cm;
            }
            body {
                font-family: 'Helvetica', 'Arial', sans-serif;
                font-size: 11pt;
                color: #333;
                line-height: 1.6;
            }
            .header {
                display: flex;
                justify-content: space-between;
                margin-bottom: 40px;
                padding-bottom: 20px;
                border-bottom: 2px solid #4F46E5;
            }
            .company-info {
                flex: 1;
            }
            .company-name {
                font-size: 24pt;
                font-weight: bold;
                color: #4F46E5;
                margin-bottom: 10px;
            }
            .invoice-info {
                text-align: right;
            }
            .invoice-title {
                font-size: 28pt;
                font-weight: bold;
                color: #4F46E5;
                margin-bottom: 10px;
            }
            .invoice-number {
                font-size: 14pt;
                color: #666;
            }
            .parties {
                display: flex;
                justify-content: space-between;
                margin-bottom: 40px;
            }
            .party {
                flex: 1;
                padding: 20px;
                background: #F9FAFB;
                border-radius: 8px;
            }
            .party + .party {
                margin-left: 20px;
            }
            .party-title {
                font-weight: bold;
                font-size: 12pt;
                color: #4F46E5;
                margin-bottom: 10px;
            }
            .party-details {
                font-size: 10pt;
                color: #666;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 30px;
            }
            thead {
                background: #4F46E5;
                color: white;
            }
            th {
                padding: 12px;
                text-align: left;
                font-weight: bold;
            }
            td {
                padding: 12px;
                border-bottom: 1px solid #E5E7EB;
            }
            .text-right {
                text-align: right;
            }
            .totals {
                margin-left: auto;
                width: 300px;
            }
            .total-row {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
            }
            .total-row.grand-total {
                border-top: 2px solid #4F46E5;
                font-size: 14pt;
                font-weight: bold;
                color: #4F46E5;
                margin-top: 10px;
                padding-top: 15px;
            }
            .payment-info {
                margin-top: 40px;
                padding: 20px;
                background: #FEF3C7;
                border-left: 4px solid #F59E0B;
                border-radius: 4px;
            }
            .payment-title {
                font-weight: bold;
                color: #92400E;
                margin-bottom: 10px;
            }
            .footer {
                margin-top: 60px;
                padding-top: 20px;
                border-top: 1px solid #E5E7EB;
                text-align: center;
                font-size: 9pt;
                color: #9CA3AF;
            }
            .status-badge {
                display: inline-block;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 10pt;
                font-weight: bold;
                text-transform: uppercase;
            }
            .status-pending { background: #FEF3C7; color: #92400E; }
            .status-paid { background: #D1FAE5; color: #065F46; }
            .status-overdue { background: #FEE2E2; color: #991B1B; }
            .status-cancelled { background: #F3F4F6; color: #374151; }
        </style>
    </head>
    <body>
        <!-- Header -->
        <div class="header">
            <div class="company-info">
                <div class="company-name">{{ user.company_name }}</div>
                <div class="party-details">
                    {{ user.email }}<br>
                    {% if user.phone %}{{ user.phone }}<br>{% endif %}
                    {% if user.address %}{{ user.address }}<br>{% endif %}
                </div>
            </div>
            <div class="invoice-info">
                <div class="invoice-title">FACTURE</div>
                <div class="invoice-number">{{ invoice.invoice_number }}</div>
                <div class="status-badge status-{{ invoice.status }}">
                    {{ invoice.status | upper }}
                </div>
            </div>
        </div>

        <!-- Parties -->
        <div class="parties">
            <div class="party">
                <div class="party-title">Facturé à</div>
                <div class="party-details">
                    <strong>{{ invoice.client_name }}</strong><br>
                    {% if invoice.client_email %}{{ invoice.client_email }}<br>{% endif %}
                    {% if invoice.client_address %}{{ invoice.client_address }}<br>{% endif %}
                </div>
            </div>
            <div class="party">
                <div class="party-title">Détails de la facture</div>
                <div class="party-details">
                    <strong>Date d'émission:</strong> {{ invoice.issue_date.strftime('%d/%m/%Y') }}<br>
                    <strong>Date d'échéance:</strong> {{ invoice.due_date.strftime('%d/%m/%Y') }}<br>
                    {% if invoice.payment_terms %}
                    <strong>Conditions:</strong> {{ invoice.payment_terms }}<br>
                    {% endif %}
                </div>
            </div>
        </div>

        <!-- Items Table -->
        <table>
            <thead>
                <tr>
                    <th>Description</th>
                    <th class="text-right">Quantité</th>
                    <th class="text-right">Prix unitaire</th>
                    <th class="text-right">Montant</th>
                </tr>
            </thead>
            <tbody>
                {% for item in invoice.items %}
                <tr>
                    <td>
                        <strong>{{ item.description }}</strong>
                        {% if item.details %}<br><small>{{ item.details }}</small>{% endif %}
                    </td>
                    <td class="text-right">{{ item.quantity }}</td>
                    <td class="text-right">{{ "%.2f"|format(item.unit_price) }} {{ invoice.currency }}</td>
                    <td class="text-right">{{ "%.2f"|format(item.quantity * item.unit_price) }} {{ invoice.currency }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <!-- Totals -->
        <div class="totals">
            <div class="total-row">
                <span>Sous-total:</span>
                <span>{{ "%.2f"|format(invoice.subtotal) }} {{ invoice.currency }}</span>
            </div>
            {% if invoice.tax_amount > 0 %}
            <div class="total-row">
                <span>TVA ({{ invoice.tax_rate }}%):</span>
                <span>{{ "%.2f"|format(invoice.tax_amount) }} {{ invoice.currency }}</span>
            </div>
            {% endif %}
            {% if invoice.discount_amount > 0 %}
            <div class="total-row">
                <span>Remise:</span>
                <span>-{{ "%.2f"|format(invoice.discount_amount) }} {{ invoice.currency }}</span>
            </div>
            {% endif %}
            <div class="total-row grand-total">
                <span>TOTAL:</span>
                <span>{{ "%.2f"|format(invoice.total_amount) }} {{ invoice.currency }}</span>
            </div>
        </div>

        <!-- Payment Info -->
        {% if invoice.status != 'paid' and invoice.status != 'cancelled' %}
        <div class="payment-info">
            <div class="payment-title">Informations de paiement</div>
            <div>
                Merci de régler cette facture avant le <strong>{{ invoice.due_date.strftime('%d/%m/%Y') }}</strong>.<br>
                {% if invoice.payment_instructions %}
                {{ invoice.payment_instructions }}
                {% endif %}
            </div>
        </div>
        {% endif %}

        <!-- Notes -->
        {% if invoice.notes %}
        <div style="margin-top: 30px; padding: 15px; background: #F9FAFB; border-radius: 4px;">
            <strong>Notes:</strong><br>
            {{ invoice.notes }}
        </div>
        {% endif %}

        <!-- Footer -->
        <div class="footer">
            Document généré le {{ now.strftime('%d/%m/%Y à %H:%M') }}<br>
            {{ user.company_name }} - {{ user.email }}
        </div>
    </body>
    </html>
    """
    
    @staticmethod
    def generate_invoice_pdf(
        invoice: Invoice,
        user: User
    ) -> bytes:
        """
        Generate PDF for an invoice.
        
        Args:
            invoice: Invoice object
            user: User object (company info)
            
        Returns:
            PDF file as bytes
        """
        try:
            # Prepare template data
            template_data = {
                "invoice": invoice,
                "user": user,
                "now": datetime.utcnow(),
            }
            
            # Render HTML from template
            template = Template(PDFService.INVOICE_TEMPLATE)
            html_content = template.render(**template_data)
            
            # Generate PDF
            pdf_file = BytesIO()
            HTML(string=html_content).write_pdf(pdf_file)
            pdf_bytes = pdf_file.getvalue()
            
            logger.info(f"Generated PDF for invoice {invoice.id} ({len(pdf_bytes)} bytes)")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"Failed to generate PDF for invoice {invoice.id}: {e}")
            raise ValueError(f"PDF generation failed: {e}")
    
    @staticmethod
    def get_invoice_filename(invoice: Invoice) -> str:
        """
        Get standardized filename for invoice PDF.
        
        Args:
            invoice: Invoice object
            
        Returns:
            Filename string
        """
        # Format: Facture_INV-2024-001_ClientName.pdf
        safe_client_name = "".join(
            c for c in invoice.client_name if c.isalnum() or c in (' ', '-', '_')
        ).replace(' ', '_')
        
        return f"Facture_{invoice.invoice_number}_{safe_client_name}.pdf"

