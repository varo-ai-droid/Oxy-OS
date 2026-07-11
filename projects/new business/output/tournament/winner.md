# Tournament Winner: Chargeback Evidence Automation for Shopify

## Selected Candidate
**Chargeback Evidence Automation for Shopify** (Score: 54.6/60 - Unanimous #1)

---

## Problem Statement
Shopify merchants lose $3-5k/mo to winnable chargebacks because:
1. Evidence compilation is manual (2+ hours per dispute)
2. Current tools send generic templates that don't match reason code requirements
3. Evidence scattered across Shopify (orders), Gmail (customer comms), ShipStation (tracking), ERP (inventory)
4. No automation for reason-code-specific evidence packets

## Target Customer
- **Primary**: Shopify merchants with 3+ chargebacks/month ($100k-50M GMV)
- **Sweet spot**: $1M-10M GMV, selling physical goods, using 3PL/fulfillment
- **Pain acuity**: Losing money NOW, explicitly paying for tools that don't work
- **Reachability**: Shopify App Store, r/Shopify, agencies, Twitter

## Market Size
- 2.4M Shopify stores globally
- ~30% (720k) experience chargebacks
- ~15% (108k) have 3+/month = high-value segment
- TAM: 108k × $19-500/mo = $25-600M ARR potential
- SAM (reachable via app store): 30k × $49/mo = ~$18M ARR Year 1

## Competitive Landscape
| Competitor | Price | Approach | Gap |
|------------|-------|----------|-----|
| Chargeflow | $200-2000/mo | Managed service + templates | Generic templates, no reason-code logic |
| Chargebacks911 | $500-5000/mo | Full managed | Expensive, black box, 23% win rate |
| Midigator | $300-3000/mo | Software + services | Complex UI, not Shopify-native |
| Signifyd | Revenue share | Fraud prevention | Not chargeback representment |
| Shopify Native | Free | Basic notification | No evidence help |

**Our Wedge**: "Evidence Automation, Not Templates"
- Pull real data (tracking, emails, order history, IP, usage)
- Map to EXACT reason code requirements (Visa 10.4 ≠ 13.1)
- Merchant reviews, clicks approve - done in 2 minutes not 2 hours

## Business Model
- **Core**: $19/approved response (usage-based, aligned incentives)
- **Pro**: $99/mo + $9/response (higher volume, A/B testing, analytics)
- **Enterprise**: $499/mo + custom (multi-store, ERP sync, dedicated support)
- **No success fee** - merchant keeps 100% of recovered revenue

## Unit Economics (Projected)
| Metric | Core | Pro | Enterprise |
|--------|------|-----|------------|
| Monthly responses | 10 | 50 | 200 |
| Revenue/mo | $190 | $549 | $2,299 |
| CAC (app store + content) | $150 | $300 | $2,000 |
| Payback period | <1 mo | <1 mo | 1 mo |
| Gross margin | 85% | 88% | 90% |
| LTV (24 mo churn) | $4,500 | $13,000 | $55,000 |

## Go-to-Market
1. **Shopify App Store** - SEO for "chargeback evidence", "dispute automation"
2. **Content** - "Why Chargeflow lost my $4k chargeback" case studies
3. **Agency Partnerships** - 50+ Shopify Plus agencies resell
4. **Twitter/X** - Founder-led, "building in public" chargeback wins
5. **SEO** - "Visa reason code 10.4 evidence template" etc.

## Technical Architecture
```
┌─────────────────────────────────────────────────────┐
│                  Shopify App (Embedded)              │
├─────────────────────────────────────────────────────┤
│  Webhook: disputes/create → Trigger Evidence Job    │
├─────────────────────────────────────────────────────┤
│  Evidence Graph Builder                             │
│  ├─ Shopify Orders/Fullfillments/Customer API       │
│  ├─ Gmail/Outlook API (customer communications)     │
│  ├─ Shipping APIs (UPS, FedEx, USPS, DHL)           │
│  ├─ 3PL APIs (ShipBob, ShipStation, Deliverr)       │
│  └─ ERP APIs (NetSuite, Cin7, DEAR)                 │
├─────────────────────────────────────────────────────┤
│  Reason Code Mapper (Visa/MC/Amex/Discover)         │
│  ├─ 10.4: Fraud → Tracking + IP + AVS + 3DS         │
│  ├─ 13.1: Not Received → Tracking + Delivery Proof  │
│  ├─ 13.2: Cancelled Recurring → Cancellation Proof  │
│  └─ 13.3: Product Not as Described → Photos + Specs │
├─────────────────────────────────────────────────────┤
│  Packet Builder → PDF/HTML Evidence Package         │
├─────────────────────────────────────────────────────┤
│  Merchant Review UI → One-Click Submit to Shopify   │
└─────────────────────────────────────────────────────┘
```

## Reason Code Coverage (MVP)
| Priority | Reason Code | Name | Evidence Required |
|----------|-------------|------|-------------------|
| P0 | 10.4 | Fraud - Card Present | Tracking, IP match, AVS, 3DS, device fingerprint |
| P0 | 10.5 | Fraud - Card Not Present | Tracking, IP, email, billing/shipping match, 3DS |
| P0 | 13.1 | Not Received | Tracking, delivery confirmation, signature, customer comms |
| P0 | 13.2 | Cancelled Recurring | Cancellation email, policy, usage logs |
| P1 | 13.3 | Not as Described | Product photos, specs, customer comms, return policy |
| P1 | 13.6 | Credit Not Processed | Refund proof, return tracking, policy |
| P2 | 12.5 | Incorrect Amount | Order details, pricing, tax calc |
| P2 | 13.7 | Defective | Photos, return, warranty, manufacturer defect |

## Key Differentiators
1. **Reason-code-native** - Not "one template fits all"
2. **Evidence graph** - Connects disparate data sources automatically
3. **Merchant-in-the-loop** - 2-minute review vs 2-hour compilation
4. **Usage-based pricing** - Only pay when you use it, aligned incentives
5. **Shopify-native** - Embedded app, webhooks, zero setup friction

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Shopify builds native | Medium | High | Move fast, build ecosystem (agencies, integrations), become default |
| Low win rates persist | Low | High | Publish win rate benchmarks, A/B test evidence packets, iterate |
| API rate limits | Medium | Medium | Queue-based processing, caching, batch APIs |
| Gmail API restrictions | Low | Medium | Also support Outlook, IMAP, forward-to-email fallback |
| Chargeflow copies | High | Medium | Patent reason-code mapper, build switching costs (integrations) |

## Next Steps (Phase 3: Business Design)
1. Deep competitor pricing analysis
2. Shopify App Store requirements & approval timeline
3. Visa/MC chargeback rulebook mapping (VCR 10.4, 13.1, etc.)
4. Unit economics model with real CAC data
5. Technical spike: Evidence graph builder prototype
6. Design partner recruitment (5-10 Shopify merchants)

---

*Winner selected by 5-judge tournament from 18 candidates across 10 sources. Unanimous decision.*