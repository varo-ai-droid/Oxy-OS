# Phase 3: Business Design - Researcher {{researcher_id}}/{{total_researchers}}

## Business Concept
{{business_concept}}

## Focus Area: {{focus_area}}

## Your Task
Produce a deep research brief for your focus area. This will feed directly into the business plan.

### If focus_area = "competitors":
- Top 10 direct/indirect competitors with pricing
- Feature gaps from G2/Capterra/Chrome Store reviews
- Their positioning & messaging
- Market share estimates

### If focus_area = "platform_apis":
- Required APIs (Shopify, Stripe, Vercel, AWS, etc.)
- Rate limits, costs, webhook reliability
- App store approval process & requirements
- Reference implementations

### If focus_area = "regulations":
- Visa/MC chargeback rules (VCR, reason codes, time limits)
- GDPR/CCPA for customer data
- Shopify App Store requirements
- PCI DSS if handling payments

### If focus_area = "unit_economics":
- CAC by channel (SEO, paid, partnerships, content)
- LTV at $19/mo, $49/mo, $99/mo
- Churn benchmarks for B2B SaaS
- Support cost per ticket
- Gross margin at scale

## Output Format
```
## {{focus_area | upper}} RESEARCH

### Key Findings
1. [Specific, cited finding]
2. [Specific, cited finding]

### Data Points
- [Metric]: [Value] (Source: [URL/Ref])

### Risks
- [Risk with evidence]

### Recommendations
- [Actionable recommendation]
```

Cite sources. Be specific. No fluff.