## PLATFORM_APIS RESEARCH

### Key Findings
1. **Shopify Admin API (GraphQL)** is the primary integration. Rate limit: 1000 points/100ms (50 req/sec equivalent). Dispute webhook: `disputes/create`, `disputes/update`. Evidence submission via `disputeEvidenceCreate` mutation.
2. **Gmail API** (Google Workspace) for customer email evidence. Rate limit: 250 quota units/user/sec. Requires OAuth + sensitive scope verification ($15-75k/year for verification).
3. **Shipping Carrier APIs**: UPS (Rate limit: 1000/hr), FedEx (500/hr), USPS (no published limit), DHL (1000/hr). All require account credentials.
4. **3PL APIs**: ShipBob (REST, 100/min), ShipStation (REST, 40/min), Deliverr (GraphQL, 60/min). Webhooks for fulfillment events.
5. **ERP APIs**: NetSuite (SuiteTalk, 1000/min), Cin7 (REST, 60/min), DEAR (REST, 60/min). Complex auth (OAuth 1.0a for NetSuite).
6. **Shopify App Store**: 2-4 week review. Requirements: GDPR webhook, mandatory webhooks, embedded app via App Bridge, billing via Shopify Billing API.

### Shopify Admin API Details
```
Dispute Webhook Payload:
{
  "id": "gid://shopify/Dispute/123",
  "amount": {"amount": "150.00", "currency": "USD"},
  "reason": "FRAUDULENT",
  "status": "UNDER_REVIEW",
  "evidence_due_by": "2024-07-18T23:59:59Z",
  "order": { "id": "gid://shopify/Order/456", "email": "customer@example.com" }
}

Evidence Submission:
mutation disputeEvidenceCreate($disputeId: ID!, $evidence: DisputeEvidenceInput!) {
  disputeEvidenceCreate(disputeId: $disputeId, evidence: $evidence) {
    dispute { id status }
    userErrors { field message }
  }
}

DisputeEvidenceInput fields:
- customerEmailAddress
- customerName
- customerPurchaseIp
- duplicateChargeDocumentation
- productDescription
- receipt
- shippingAddress
- shippingCarrier
- shippingDate
- shippingDocumentation
- shippingTrackingNumber
- uncategorizedFile (base64, max 10MB)
- uncategorizedText
```

### Rate Limits & Costs
| API | Rate Limit | Cost | Notes |
|-----|------------|------|-------|
| Shopify Admin | 1000 pts/100ms | Free | Points vary by query complexity |
| Shopify Billing | N/A | Free | Shopify takes 15-20% of app revenue |
| Gmail API | 250 units/sec | Free* | *Scope verification $15-75k/yr |
| Outlook/Graph | 10k/10min | Free | Easier verification than Gmail |
| UPS | 1000/hr | Free | Need UPS account |
| FedEx | 500/hr | Free | Need FedEx account |
| USPS | Unlimited* | Free | *With USPS Web Tools account |
| ShipStation | 40/min | $9.99/mo+ | Popular with merchants |
| ShipBob | 100/min | Custom | 3PL, need partnership |
| NetSuite | 1000/min | License | Complex OAuth 1.0a |

### App Store Approval Checklist
- [ ] GDPR webhook: `customers/data_request`, `customers/redact`, `shop/redact`
- [ ] Mandatory webhooks registered
- [ ] Embedded via App Bridge 3.0
- [ ] Billing via Shopify Billing API (no external payments)
- [ ] Privacy policy URL
- [ ] Terms of service URL
- [ ] Support email
- [ ] App listing: screenshots, video, description
- [ ] Test on development store
- [ ] Submit for review (2-4 weeks)

### Reference Implementations
- **Chargeflow**: Uses Shopify webhooks + Admin API for evidence. Embedded app. Managed service layer on top.
- **Order Printer Pro**: PDF generation via Admin API + liquid templates.
- **Klaviyo**: Deep Shopify integration, webhook-heavy, App Bridge embedded.
- **Recharge**: Subscription billing, complex webhook orchestration.

### Technical Architecture Recommendations
```
Evidence Collection Pipeline:
1. Dispute webhook received → Queue job (Redis/Bull)
2. Parallel fetch:
   - Shopify: Order, fulfillments, customer, timeline
   - Gmail/Outlook: Threads matching order email
   - Shipping: Tracking events via carrier API
   - 3PL: Fulfillment records, photos, scans
   - ERP: Inventory movements, refund records
3. Reason Code Mapper: Select evidence fields per code
4. Packet Builder: Generate PDF + structured data
5. Merchant Review UI: Embedded App Bridge modal
6. Submit: disputeEvidenceCreate mutation
6. Webhook: disputes/update → Track outcome
```

### Risks
- Gmail API verification cost ($15-75k) and timeline (4-8 weeks)
- Shopify rate limits during dispute spikes (Black Friday)
- 3PL API access requires partnerships (not self-serve)
- NetSuite OAuth 1.0a complexity

### Recommendations
- **Phase 1**: Shopify only (orders, fulfillments, customer emails via Shopify timeline)
- **Phase 2**: Add Gmail/Outlook via email forwarding (avoid API verification)
- **Phase 3**: Shipping carrier APIs (UPS/FedEx/USPS) - self-serve
- **Phase 4**: 3PL/ERP via partnerships
- Use email forwarding (`chargebacks@merchant.com`) as MVP for customer comms
- Build reason-code mapper as configurable JSON, not hardcoded