# CounterBrief — Full Business Explanation

---

## What It Is
**Chargeback evidence automation for Shopify merchants.** Instead of generic templates that banks reject, CounterBrief auto-assembles reason-code-specific evidence packets from the merchant's actual data (Shopify orders, customer emails, shipping tracking, 3PL records). The merchant reviews in 2 minutes, clicks submit, and wins.

---

## The Core Insight
**Visa/Mastercard have 18+ reason codes, each requiring different evidence.**
- **10.4 (Fraud Card-Absent):** Needs AVS + CVV + IP match + 3DS + tracking + delivery proof
- **13.1 (Not Received):** Needs tracking + delivery confirmation + signature (if >$750)
- **13.2 (Cancelled Recurring):** Needs cancellation confirmation + policy acknowledgement + usage logs
- **13.3 (Not as Described):** Needs product photos + specs + return policy + comms

**Current tools (Chargeflow, Chargebacks911, Midigator) use ONE template for ALL codes.** That's why win rates are 20–30%.

---

## How It Works (Technical Flow)

```
1. DISPUTE RECEIVED
   └─ Shopify/Stripe webhook: disputes/create → triggers evidence job

2. EVIDENCE HUNT (parallel, async)
   ├─ Shopify Admin API: Order, fulfillments, customer timeline, metafields
   ├─ Email (Gmail/Outlook OAuth or forwarding): Thread matching order email
   ├─ Carrier APIs (UPS/FedEx/USPS/DHL): Tracking events, delivery scans, signatures
   ├─ 3PL APIs (ShipBob/ShipStation/Deliverr): Fulfillment records, photos, scans
   └─ ERP APIs (NetSuite/Cin7/DEAR): Inventory movements, refund records

3. REASON CODE MAPPER
   └─ Configurable JSON: 18 codes × 20 evidence fields → selects exact requirements

4. PACKET BUILDER
   └─ Generates PDF + structured JSON, mapped to bank evidence fields

5. MERCHANT REVIEW (embedded App Bridge modal)
   └─ Shows: "We found tracking (delivered), customer email ('love it!'), IP match, AVS/CVV match. Missing: signature for 13.1. Include anyway? [Yes] [No]"

6. SUBMIT
   └─ disputeEvidenceCreate mutation → bank

7. OUTCOME TRACKING
   └─ Webhook updates → win/loss analytics by reason code → confidence model improves
```

---

## Business Model (Hybrid Tiers)

| Plan | Monthly Base | Per Response | Included Responses | Best For |
|------|--------------|--------------|-------------------|----------|
| **Starter** | $0 | $29 | 0 | <20 disputes/mo, variable volume |
| **Growth** | $49 | $19 | 10/mo | 20–100 disputes/mo (most merchants) |
| **Scale** | $199 | $9 | 50/mo | 100+ disputes/mo, predictable billing |
| **Enterprise** | Custom | Custom | Unlimited | Multi-store, ERP, SLA, dedicated CSM |

**Key:** Pay when you win. No monthly minimum on Starter. First dispute builds free.

---

## Unit Economics (Month 24, Post-Fixes)

| Metric | Value |
|--------|-------|
| Stores | 1,500 |
| Blended MRR/store | $180 |
| **ARR** | **$7.2M** |
| Monthly logo churn | 3% |
| Expansion revenue | 25% |
| Net revenue retention | 122% |
| Gross margin | 78% |
| CAC payback | 0.9 months |
| LTV:CAC | 22:1 |

---

## Market

| Layer | Calculation | Value |
|-------|-------------|-------|
| **TAM** | 2M Shopify + 2M Stripe + PayPal/Braintree × 2 disputes/mo × $19 | $912M/yr |
| **SAM** | Shopify Payments/Stripe stores with 50+ orders/mo × 3 disputes × $19 | $342M/yr |
| **SOM (Yr 1)** | 500 stores × 3 disputes × $19 | $342k/yr |
| **SOM (Yr 3)** | 1,500 stores × 4 disputes × $25 (blended) | $7.2M/yr |

**ICP:** Shopify store, $100k–$10M GMV, 50–500 orders/mo, Shopify Payments or Stripe, 3+ chargebacks/mo.

---

## Go-to-Market (3 Prongs)

### 1. Chargeflow Churn Intercept (Week 1–2)
- `counterbrief.com/vs/chargeflow` comparison page
- SEO: "Chargeflow alternative", "Chargeflow pricing", "Chargeflow reviews"
- Lead magnet: "Free chargeback audit — we analyze your last 5 disputes"
- Target: 200+ Chargeflow churners/month

### 2. Reason-Code SEO Engine (Week 2–4)
| Keyword | Volume | Page |
|---------|--------|------|
| "visa reason code 10.4 evidence" | 1,200/mo | Guide + auto-build demo |
| "how to win shopify chargeback" | 800/mo | Comparison + case study |
| "chargeback representment template" | 500/mo | Free tool (email capture) |

20 reason-code guides (programmatic from config JSON). Each: checklist, video, CTA.

### 3. Agency Channel (Month 2+)
- Top 50 Shopify Plus agencies (manage 5,000+ stores)
- 30% rev share Year 1, 15% Year 2+
- Co-branded "Chargeback Audit" lead gen
- Agency gets: audit tool, client portal, recurring revenue

---

## Moats (Building Over Time)

1. **Reason-code evidence map** — 360 mappings (18 codes × 20 evidence types), versioned JSON, test suite (100 synthetic disputes/code)
2. **Win-rate data network effect** — More disputes = better confidence scoring = higher win rates = more merchants
3. **Shopify ecosystem lock-in** — App Store, App Bridge embedded, Billing API, webhook-first
4. **Agency distribution** — Top 50 agencies become default recommenders

---

## Red Team Summary (Viable With Fixes)

| Attack | Verdict | Fix |
|--------|---------|-----|
| TAM too small | WEAK | Phase 2: Stripe/PayPal/Braintree; Phase 3: Fraud prevention |
| Pricing volatile | WEAK | Hybrid tiers (base + usage), predictable floor |
| Evidence accuracy | WEAK | Confidence scoring (0–1), human-in-loop threshold, email forwarding MVP |
| Distribution | WEAK | Chargeflow churn intercept + programmatic SEO + agency rev-share |
| Legal (UPL) | WEAK | Payments counsel ($5k/mo), UPL-safe copy, "compiler not lawyer" |
| Retention | WEAK | Risk score + pre-dispute alerts (Ethoca/Verifi) + RDR enrollment |

---

## 90-Day Execution Plan

| Month | Milestone |
|-------|-----------|
| **1** | Incorporate, register counterbrief.com, retain payments counsel ($5k/mo). Build MVP: Shopify app scaffold + webhook handler + evidence collector (Shopify only) + email forwarding + async queue (BullMQ) + PDF builder + App Bridge review modal. |
| **2** | Deploy to 10 design partners (free). Collect win-rate data. Launch comparison page + 20 reason-code guides. Begin agency outreach (top 50). |
| **3** | Shopify App Store submission + approval. First 20 paying customers. Pro plan ($49/mo) launch. Stripe direct webhook integration (Phase 2). Risk score MVP (per-order scoring). |
| **4–6** | PayPal/Braintree dispute APIs. Ethoca/Verifi pre-dispute alerts. RDR auto-enrollment. Scale plan ($199/mo). 3 agency partners live. Content engine: 2 case studies/week. |

---

## Financial Projections (Conservative)

| Month | Stores | MRR | ARR |
|-------|--------|-----|-----|
| 3 | 50 | $11k | $132k |
| 6 | 150 | $37.5k | $450k |
| 12 | 500 | $140k | $1.68M |
| 18 | 1,000 | $280k | $3.36M |
| 24 | 1,500 | $480k | $5.76M |

*Post-fix model: $7.2M ARR at Month 24 (vs $4.8M pre-fix)*

---

## Team & Capital

**Current:** 1 founder (Nate — lived the pain, lost $4,200 Black Friday 2023)

**Hiring Plan:**
- Month 1–3: 2 founding engineers (backend + frontend)
- Month 4–6: 1 support/success, 1 growth (content/SEO/partnerships)
- Month 7–12: 2 more engineers, 1 CSM for Enterprise

**Funding:** $500k SAFE @ $8M cap — 18-month runway to $1M ARR. No institutional VC needed (capital efficient, high margins). Optional Series A at $3M ARR.

---

## Why Now

1. **Chargeback volume rising** — Friendly fraud up 20% YoY (post-COVID e-commerce surge)
2. **Shopify Payments dominance** — 60%+ of Shopify GMV, unified dispute webhook
3. **API maturity** — Carrier APIs, email OAuth, 3PL APIs all production-ready
4. **Incumbents stagnant** — Chargeflow UI unchanged in 3 years, Midigator legacy, Shopify Protect covers only 2 reason codes
5. **Regulatory tailwind** — Visa/MC pushing pre-dispute resolution (Ethoca/Verifi/RDR) — we integrate early

---

## The Ask

**$500k SAFE @ $8M cap**  
→ 18 months runway to $1M ARR  
→ 2 engineers + payments counsel + App Store launch + 3 agency partners

**Contact:** nate@counterbrief.com | counterbrief.com

---

**Bottom line:** Merchants lose winnable disputes because evidence is scattered and templates are generic. CounterBrief connects the data, maps to the reason code, builds the packet, and lets the merchant approve in 2 minutes. $19 per win. You keep 100%.