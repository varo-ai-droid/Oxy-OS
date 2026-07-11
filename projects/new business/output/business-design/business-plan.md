# Business Plan: CounterBrief

**The Evidence Engine for Shopify Chargebacks**

---

## Executive Summary

**Problem**: Shopify merchants lose $30B+ annually to chargebacks. 60-80% are "friendly fraud" (customer received item, claims they didn't). Current tools (Chargeflow, Chargebacks911, Midigator) send generic templates that banks reject. Win rates: 20-30%.

**Solution**: CounterBrief auto-assembles reason-code-specific evidence packets from Shopify, email, shipping, 3PL, and ERP data. Merchant reviews → clicks submit. Win rate target: 55%+.

**Business Model**: $19 per approved response (usage-based). $99/mo Pro for predictability. $499/mo Enterprise for multi-store/ERP.

**Market**: 2M+ Shopify stores. 500k+ have chargeback problems. TAM: $2.4B (at $19 × 5 disputes/store/mo). SAM: $600M (Shopify Payments + Stripe, 50+ orders/mo).

**Traction Plan**: Launch on Shopify App Store. Target Chargeflow churners. 50 stores Month 3 → 500 Month 12 → 1,500 Month 24. $480k MRR at Month 24.

---

## 1. Problem

### The Chargeback Crisis
- **$30B+** annual chargeback losses for e-commerce (2023)
- **60-80%** are "friendly fraud" — customer got product, disputes anyway
- **$15-100** fee per dispute + lost revenue + operational cost
- Average merchant: **2-5% revenue lost** to chargebacks

### Why Current Tools Fail
| Tool | Model | Win Rate | Fatal Flaw |
|------|-------|----------|------------|
| Chargeflow | Managed service, $200-2000/mo | 23% | Generic templates, no reason-code logic |
| Chargebacks911 | Managed, $500-5000/mo | 30% | Black box, no transparency |
| Midigator | SaaS $300-1000/mo | 28% | Complex UI, manual evidence mapping |
| Shopify Protect | Free (Shopify Payments) | ~40% | Only fraud + not-received, auto-only |

**Root Cause**: Visa/Mastercard have **18+ reason codes**, each requiring **different evidence**. Current tools use **one template for all**.

### Merchant Pain (Verbatim)
> "I'm losing $3-5k/month to chargebacks. Chargeflow just sends templates banks reject. I need something that pulls my tracking, emails, order history and builds a REAL case." — r/Shopify

> "Our support team spends 15+ hrs/week compiling evidence. Data is in Shopify, Gmail, ShipStation. No tool connects these." — r/SaaS

> "Chargeback reason codes are a nightmare. Visa 10.4 vs 13.1 need totally different evidence. My app doesn't even tell me which code I'm fighting." — r/ecommerce

---

## 2. Solution: CounterBrief

### Core Value Prop
**"Win the disputes templates lose. Evidence assembled in seconds, not hours. $19 per win. You keep 100%."**

### How It Works
```
1. DISPUTE RECEIVED → Webhook from Shopify/Stripe
2. EVIDENCE HUNT → Parallel fetch: Order, Fulfillments, Customer Timeline, Emails, Tracking, 3PL, ERP
3. REASON CODE MAP → Select exact evidence fields for Visa 10.4 / 13.1 / 13.2 / etc.
4. PACKET BUILD → PDF + structured data, mapped to bank requirements
5. MERCHANT REVIEW → Embedded App Bridge modal: "This looks right? [Submit]"
6. SUBMIT → disputeEvidenceCreate mutation → Bank
7. OUTCOME TRACK → Webhook updates → Win/Loss analytics
```

### Key Differentiators
| Feature | CounterBrief | Chargeflow | Midigator |
|---------|-------------|------------|-----------|
| Reason-code-native evidence | ✅ | ❌ | Partial |
| Multi-source evidence (Shopify + Email + Shipping + 3PL) | ✅ | ❌ | ❌ |
| Transparent packet before submit | ✅ | ❌ | ✅ |
| Win rate analytics by reason code | ✅ | ❌ | Partial |
| Usage pricing ($19/win) | ✅ | ❌ ($200+/mo) | ❌ ($300+/mo) |
| 2-week implementation | ✅ | 4-6 weeks | 4-8 weeks |

### Product Roadmap
- **MVP (Month 1-2)**: Shopify only, 4 reason codes (10.4, 13.1, 13.2, 13.3), email via forwarding
- **V1 (Month 3-4)**: Gmail/Outlook OAuth, UPS/FedEx/USPS APIs, all 18 reason codes
- **V2 (Month 6)**: 3PL integrations (ShipBob, ShipStation), ERP (NetSuite), A/B testing responses
- **V3 (Month 12)**: Pre-dispute (Ethoca/Verifi), RDR, multi-platform (Stripe, Braintree, PayPal)

---

## 3. Market

### TAM / SAM / SOM
| Metric | Calculation | Value |
|--------|-------------|-------|
| **TAM** | 2M Shopify stores × 5 disputes/mo × $19 | **$2.4B/yr** |
| **SAM** | 500k stores (50+ orders/mo, Shopify Payments/Stripe) × 3 disputes × $19 | **$342M/yr** |
| **SOM (Yr 1)** | 500 stores × 3 disputes × $19 | **$342k/yr** |
| **SOM (Yr 3)** | 5,000 stores × 4 disputes × $25 (blended) | **$6M/yr** |

### Target Customer (ICP)
- **Primary**: Shopify store, $100k-$10M GMV, 50-500 orders/mo, Shopify Payments or Stripe
- **Pain**: 3+ chargebacks/mo, using Chargeflow or nothing, losing money
- **Buyer**: Founder / Operations Lead / Finance Controller
- **Trigger**: "Just lost a $2k chargeback I should've won"

### Competitive Landscape
```
                    High Win Rate
                          ↑
        CounterBrief      ●
                          |
                          |
        Midigator         ●
                          |
        Shopify Protect   ●
                          |
        Chargeflow        ●
                          |
                          └──────────────────→ Low Price
                         Free          $500/mo
```

**Moats** (building over time):
1. **Reason-code evidence map** — proprietary mapping of 18 codes × 20 evidence types
2. **Win rate data** — network effect: more disputes = better models
3. **Shopify ecosystem lock-in** — App Store, App Bridge, Billing API
4. **Agency channel** — top 50 agencies become distribution

---

## 4. Business Model

### Pricing
| Plan | Price | Includes | Target |
|------|-------|----------|--------|
| **Core** | $19 / approved response | All reason codes, Shopify evidence, email forwarding, win analytics | <20 disputes/mo |
| **Pro** | $99/mo + $9/response | + Gmail/Outlook OAuth, Shipping APIs, A/B testing, priority support | 20-100 disputes/mo |
| **Enterprise** | $499/mo + $5/response | + 3PL/ERP sync, multi-store, dedicated CSM, SLA, custom mappings | 100+ disputes/mo |

### Unit Economics (Month 12, Pro Plan)
| Metric | Value |
|--------|-------|
| Avg MRR/store | $280 |
| CAC (blended) | $250 |
| LTV (24 mo) | $5,000 |
| LTV:CAC | 20:1 |
| Payback | 0.9 months |
| Gross Margin | 72% |
| Monthly Churn | 3% |

### Revenue Projections
| Month | Stores | MRR | ARR |
|-------|--------|-----|-----|
| 3 | 50 | $11,000 | $132k |
| 6 | 150 | $37,500 | $450k |
| 12 | 500 | $140,000 | $1.68M |
| 18 | 1,000 | $280,000 | $3.36M |
| 24 | 1,500 | $480,000 | $5.76M |

---

## 5. Go-to-Market

### Channel Strategy (Priority Order)
1. **Shopify App Store SEO** (40% of acquisitions)
   - Keywords: "chargeback", "dispute", "chargeback protection", "Chargeflow alternative"
   - Launch with 5 video case studies, 20+ 5-star reviews (beta users)
   
2. **Chargeflow Churn Intercept** (25%)
   - SEO: "Chargeflow alternative", "Chargeflow pricing", "Chargeflow reviews"
   - Comparison page: "Why merchants switch from Chargeflow to CounterBrief"
   - Target: 200+ Chargeflow churners/month (estimated)

3. **Agency Partnerships** (20%)
   - Top 50 Shopify Plus agencies
   - 20% rev share for first year
   - Co-marketing: "Chargeback audit" lead magnet

4. **Content/SEO** (15%)
   - "Visa reason code 10.4 evidence guide" (1,200 searches/mo)
   - "How to win Shopify chargebacks" (800 searches/mo)
   - Weekly case studies: "How [Brand] recovered $12k in 30 days"

### Launch Sequence
- **Week 1-2**: Beta with 10 design partners (free, feedback)
- **Week 3-4**: Public App Store launch, 20 reviews seeded
- **Month 2**: Chargeflow comparison page live, agency outreach
- **Month 3**: Content engine (2 posts/week), first paid search test
- **Month 4**: Pro plan launch, first enterprise pilot

---

## 6. Product & Engineering

### Tech Stack
- **Frontend**: React + TypeScript, Shopify App Bridge 3.0, Polaris UI
- **Backend**: Node.js/TypeScript (Fastify), PostgreSQL, Redis (Bull queues)
- **Hosting**: Vercel (frontend), Railway/Render (backend), RDS Postgres
- **PDF**: @react-pdf/renderer (client-side) or Puppeteer (server)
- **Auth**: Shopify OAuth (primary), Google/Microsoft OAuth (email)

### Architecture
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Shopify    │────▶│  Webhook    │────▶│  Evidence   │
│  Webhooks   │     │  Handler    │     │  Collector  │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    ▼                          ▼                          ▼
            ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
            │  Shopify    │            │  Email      │            │  Shipping   │
            │  Admin API  │            │  (Forward)  │            │  APIs       │
            └─────────────┘            └─────────────┘            └─────────────┘
                    │                          │                          │
                    └──────────────────────────┼──────────────────────────┘
                                               ▼
                                    ┌─────────────────────┐
                                    │  Reason Code Mapper │
                                    │  (JSON Config)      │
                                    └──────────┬──────────┘
                                               ▼
                                    ┌─────────────────────┐
                                    │  Packet Builder     │
                                    │  (PDF + JSON)       │
                                    └──────────┬──────────┘
                                               ▼
                                    ┌─────────────────────┐
                                    │  Merchant Review    │
                                    │  (App Bridge Modal) │
                                    └──────────┬──────────┘
                                               ▼
                                    ┌─────────────────────┐
                                    │  Submit to Bank     │
                                    │  (disputeEvidenceCreate)    │
                                    └─────────────────────┘
```

### Team Plan
| Role | Month 1-3 | Month 4-6 | Month 7-12 |
|------|-----------|-----------|------------|
| Founder/CEO | Product, Sales, Fundraising | Sales, Fundraising | Strategy, Hiring |
| Founding Engineer | Backend, Shopify API, PDF | Email, Shipping APIs | 3PL/ERP, Scale |
| Founding Engineer | Frontend, App Bridge, UX | A/B Testing, Analytics | Enterprise, Multi-platform |
| Support/Success | - | 1 (part-time) | 2 (full-time) |
| Growth/Marketing | - | - | 1 (content, SEO, partnerships) |

---

## 7. Financial Plan

### Startup Costs (Pre-Revenue)
| Item | Cost |
|------|------|
| Legal (incorporation, terms, privacy) | $5,000 |
| Shopify App Store review prep | $2,000 |
| Gmail API verification | $15,000 |
| Infrastructure (3 months) | $1,500 |
| Design/UX contractor | $8,000 |
| **Total** | **$31,500** |

### Funding
- **Bootstrap to $10k MRR** (Month 4-6)
- **Optional**: $200-500k SAFE at $5-8M cap for faster growth
- **No institutional VC needed** — capital efficient, high margins

### Key Metrics Dashboard
| Metric | Target | Frequency |
|--------|--------|-----------|
| MRR | $480k (Mo 24) | Weekly |
| Stores | 1,500 (Mo 24) | Weekly |
| Win Rate | >55% | Daily |
| Monthly Churn | <3% | Weekly |
| NPS | >50 | Monthly |
| CAC Payback | <2 months | Monthly |
| LTV:CAC | >10:1 | Monthly |

---

## 8. Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Shopify increases take rate (15%→25%) | Medium | High | Build direct billing option, multi-platform |
| Chargeflow copies reason-code logic | High | Medium | Speed: launch first, win rate data moat |
| Gmail API verification denied/delayed | Medium | Medium | Email forwarding MVP, Outlook easier |
| Merchant stores close (churn) | High | Medium | Target established stores ($100k+ GMV) |
| Visa/MC change reason codes | Low | High | Configurable JSON mapper, not hardcoded |
| Key engineer leaves | Medium | High | Document everything, equity vesting |

---

## 9. 90-Day Execution Plan

### Month 1: Build MVP
- [ ] Shopify App scaffolding + OAuth + Billing API
- [ ] Dispute webhook handler + evidence collector (Shopify only)
- [ ] Reason code mapper (4 codes: 10.4, 13.1, 13.2, 13.3)
- [ ] PDF packet builder + App Bridge review modal
- [ ] Submit via disputeEvidenceCreate
- [ ] 10 design partners onboarded (free beta)

### Month 2: Launch
- [ ] App Store submission + approval
- [ ] 5 video case studies from beta
- [ ] Chargeflow comparison page live
- [ ] First 20 paying customers ($19/response)
- [ ] Email forwarding for customer comms

### Month 3: Scale
- [ ] Gmail/Outlook OAuth integration
- [ ] UPS/FedEx/USPS API integration
- [ ] All 18 reason codes mapped
- [ ] Pro plan ($99/mo) launch
- [ ] Agency outreach (top 50)
- [ ] Content engine: 2 posts/week

### Success Criteria (Month 3)
- 50 paying stores
- $11k MRR
- 55%+ win rate
- <3% monthly churn
- 20+ 5-star App Store reviews

---

## Appendix: Reason Code Evidence Map (Sample)

### Visa 10.4 - Fraud Card-Absent
**Required**: AVS match, CVV match, IP/device fingerprint, 3DS proof, delivery proof, customer comms
**Our Sources**: Shopify (AVS/CVV/IP), Signifyd/Riskified (3DS), Shipping API (delivery), Email (comms)

### Visa 13.1 - Merchandise Not Received
**Required**: Tracking + delivery confirmation, signature (if >$750), carrier proof, delivery address match
**Our Sources**: Shipping API (tracking events), Shopify (shipping address), Carrier (delivery scan)

### Visa 13.2 - Cancelled Recurring
**Required**: Cancellation confirmation, policy acknowledgement, usage logs after cancel
**Our Sources**: Shopify (subscription events), Email (cancellation confirmation), App analytics (usage)

### Visa 13.3 - Not as Described
**Required**: Product description, photos, specs, return policy, customer comms, return tracking
**Our Sources**: Shopify (product data), Email (comms), Shipping (return tracking), 3PL (inspection photos)

---

**CounterBrief** — Win the disputes templates lose.
*Built for Shopify. Priced for merchants. Designed to win.*