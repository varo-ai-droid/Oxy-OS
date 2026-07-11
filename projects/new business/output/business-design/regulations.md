## REGULATIONS RESEARCH

### Key Findings
1. **Visa Chargeback Rules (VCR)** - April 2024 update. Reason codes consolidated. Evidence requirements per code. Pre-arbitration mandatory for fraud disputes.
2. **Mastercard Chargeback Rules** - Similar structure. Reason codes different. Collaboration portal (MC Connect) for pre-dispute.
3. **Visa Reason Codes (2024)**:
   - **10.1** EMV Liability Shift Counterfeit Fraud
   - **10.2** EMV Liability Shift Non-Counterfeit Fraud
   - **10.3** Other Fraud - Card-Present
   - **10.4** Other Fraud - Card-Absent (MOST COMMON for e-commerce)
   - **11.1** Card Recovery Bulletin
   - **11.2** Declined Authorization
   - **11.3** No Authorization
   - **12.1** Late Presentment
   - **12.2** Incorrect Transaction Code
   - **12.3** Incorrect Currency
   - **12.4** Incorrect Account Number
   - **12.5** Incorrect Amount
   - **13.1** Merchandise/Services Not Received
   - **13.2** Cancelled Recurring Transaction
   - **13.3** Not as Described/Defective
   - **13.4** Counterfeit Merchandise
   - **13.5** Misrepresentation
   - **13.6** Credit Not Processed
   - **13.7** Cancelled Merchandise/Services
   - **13.8** Original Credit Transaction Not Accepted

### Evidence Requirements by Reason Code (Visa)
| Code | Name | Required Evidence | Win Rate (Industry) |
|------|------|-------------------|---------------------|
| 10.4 | Fraud - Card Absent | AVS match, CVV match, IP/device fingerprint, 3DS proof, customer comms, delivery proof | 25-35% |
| 13.1 | Not Received | Tracking + delivery confirmation, signature (if >$750), carrier proof, customer comms | 40-55% |
| 13.2 | Cancelled Recurring | Cancellation confirmation, policy acknowledgement, usage logs after cancel | 30-45% |
| 13.3 | Not as Described | Product description, photos, specs, return policy, customer comms, return tracking | 35-50% |
| 13.6 | Credit Not Processed | Refund proof, credit memo, processing timeline, policy | 50-65% |

### Timeline Requirements (Visa)
- **First Presentment**: 20 days from dispute date (was 30)
- **Pre-Arbitration**: 30 days from representment
- **Arbitration**: 10 days from pre-arb (fees: $500 filing, $250/hr)
- **Total Cycle**: 60-90 days typical

### Mastercard Reason Codes (Key)
- **4837** No Cardholder Authorization (Fraud)
- **4853** Cardholder Dispute - Not as Described
- **4854** Cardholder Dispute - Not Received
- **4855** Cancelled Recurring
- **4859** Addendum/No Show (Travel)
- **4860** Credit Not Processed

### Stripe Radar / Shopify Protect
- **Stripe Radar**: ML fraud scoring. Rules engine. Chargeback protection (Stripe covers fraud disputes, 0.4% fee). Limited to Stripe payments.
- **Shopify Protect**: Free for Shopify Payments. Covers fraud + "item not received" for eligible orders. Auto-submits evidence. Win rate ~40%.

### PCI DSS
- If handling full card data: SAQ D (300+ controls)
- **We don't handle card data** - only dispute evidence (tracking, emails, order data). PCI SAQ A applies (self-assessment, minimal).

### GDPR / CCPA
- **Data we process**: Customer email, name, shipping address, IP, order history
- **Lawful basis**: Legitimate interest (dispute defense) + Contract (merchant agreement)
- **Requirements**: 
  - Data Processing Addendum with merchants
  - 30-day retention for evidence (dispute cycle), then delete
  - Right to access/portability/delete
  - EU/US data transfer SCCs if hosting in US
- **Subprocessors**: Shopify, Google (Gmail), shipping carriers - need DPAs

### Shopify App Store Requirements
- **GDPR Webhooks** mandatory:
  - `customers/data_request` - return all customer data
  - `customers/redact` - delete customer data
  - `shop/redact` - delete shop data on uninstall
- **Privacy Policy** must cover: data collected, purpose, retention, subprocessors, rights
- **Terms of Service** must include: liability cap, indemnification, dispute resolution

### Financial Regulations
- **Money Transmission**: Not applicable (we don't hold funds)
- **Payment Facilitator**: Not applicable (Shopify Payments/Stripe are PF)
- **Sales Tax**: SaaS - varies by state. Economic nexus thresholds ($100k/200 transactions). Use TaxJar/Avalara.

### Industry Standards
- **Ethoca Alerts** (Mastercard): Pre-dispute alerts. 24-72hr notice. Cost: ~$0.50/alert.
- **Verifi CDRN** (Visa): Similar. ~$0.50/alert.
- **RDR (Rapid Dispute Resolution)**: Auto-resolve fraud disputes. Visa + Mastercard.
- **Order Insight** (Visa): Merchant provides order details to issuer pre-dispute.

### Compliance Checklist for MVP
- [ ] GDPR webhooks implemented
- [ ] Privacy Policy + Terms of Service
- [ ] Data Processing Addendum template
- [ ] 30-day auto-delete for evidence
- [ ] PCI SAQ A self-assessment
- [ ] Shopify App Store submission prep
- [ ] Subprocessor list (Shopify, email provider, hosting)
- [ ] Incident response plan (data breach)
- [ ] Vendor security reviews (annual)

### References
- Visa Core Rules (April 2024): visa.com/support/small-business/regulations-fees.html
- Mastercard Chargeback Guide: mastercard.com/content/dam/mccom/global/documents/chargeback-guide.pdf
- Stripe Radar Docs: stripe.com/docs/radar
- Shopify Protect: shopify.com/protect
- Ethoca Alerts: ethoca.com/alerts
- Verifi: verifi.com/solutions/cdrn