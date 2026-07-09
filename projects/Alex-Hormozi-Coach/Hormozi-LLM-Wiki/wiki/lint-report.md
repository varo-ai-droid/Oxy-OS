# Lint Report - July 5, 2026

## Executive Summary
Lint pass identified **31 broken wikilinks** across wiki pages. Several concepts are referenced but lack dedicated documentation. Cross-reference network is generally healthy but has gaps. No new orphan pages identified since last report.

---

## 1. Broken Wikilinks

### Critical Missing Pages (Referenced Multiple Times)

| Missing Page | Referenced In | Priority |
|--------------|---------------|----------|
| `[[Cold Outreach]]` | Rule of 100.md, Core Four.md | High |
| `[[Content Marketing]]` | Rule of 100.md, Core Four.md | High |
| `[[Paid Advertising]]` | Rule of 100.md, Core Four.md | High |
| `[[Warm Outreach]]` | Core Four.md | High |
| `[[Decoy Offer]]` | Advanced Offer Stacking.md | Medium |
| `[[Offer Enhancers]]` | MAGIC Naming.md | Medium |
| `[[Social Proof]]` | Perceived Likelihood of Achievement.md, Guarantees.md | Medium |

### Low Priority (Inline Concepts - Glossary Only)

| Missing Page | Referenced In | Notes |
|--------------|---------------|-------|
| `[[Status]]` | Dream Outcome.md | Could be inline concept |
| `[[Premium Pricing]]` | Photography Business Transformation.md | Related to Grand Slam Offer |
| `[[Time Delay]]` | Done-For-You.md | Exists in Value Equation context |
| `[[Effort & Sacrifice]]` | Done-For-You.md | Exists in Value Equation context |
| `[[Consistency]]` | Rule of 100.md | Inline with Rule of 100 |
| `[[1x Rule]]` | Delivery Cube.md | Typographical - should be `[[10x Rule]]` |
| `[[Supply and Demand]]` | Scarcity.md | Economics background concept |
| `[[FOMO]]` | Scarcity.md | Psychology concept |
| `[[Deadlines]]` | Urgency.md | Inline with Urgency |
| `[[Time-Based Offers]]` | Urgency.md | Inline with Urgency |
| `[[Market Selection]]` | Starving Crowd.md | Related to Starving Crowd |
| `[[Pain Point]]` | Starving Crowd.md | Related to Starving Crowd |
| `[[Risk]]` | Guarantees.md | Inline with Guarantees |
| `[[Conversion Rate]]` | Guarantees.md | Metric, could be inline |
| `[[Systems]]` | Scale vs Skill.md | Scaling concept |
| `[[100M Leads]]` | Core Four.md, index.md | Audio playlist reference |
| `[[$100M Money Models Audiobook]]` | index.md | Audio playlist |
| `[[$100M Offers Audiobook]]` | index.md | Audio playlist |
| `[[$100M Leads Audiobook]]` | index.md | Audio playlist |
| `[[$100M Lost Chapters Audiobook]]` | index.md | Audio playlist |

---

## 2. Orphan Pages

Pages with minimal or no incoming links:

| Page | Incoming Links | Recommendation |
|------|----------------|----------------|
| `[[Rendezvous Point]]` | From Coaching Workflow, Done-For-You, Customer Avatar, Guarantees | Adequate - good cross-link network |
| `[[Scale vs Skill]]` | From MOSY 6, Core Four, AI Leverage | Adequate - good cross-link network |

*Note: No significant orphan pages identified - cross-link network appears healthy.*

---

## 3. Missing Cross-References

Pages that should link to each other but currently don't:

- `[[Coaching Workflow]]` → `[[Rule of 100]]` ✓ (Already has link in Related Topics)
- `[[Core Four]]` → `[[Rule of 100]]` ✓ (Already has link in Related Topics)
- `[[MOSY 6]]` → `[[Value Equation]]` ✓ (Already has link in Related Topics)
- `[[Delivery Cube]]` → `[[Done-For-You]]` ✓ (Already has link in Related Topics)

*Note: Cross-reference recommendations from previous lint have been addressed.*

---

## 4. Potential Contradictions / Inconsistencies

### Issues Found:

1. **Delivery Cube Format**: Uses standard heading format (consistent with other frameworks).

2. **Redundancy**: Both `raw/alex-hormozi-coaching-methodology.md` and `raw/researches/2026-07-05-alex-hormozi-coaching-philosophy.md` cover similar ground. The research file has more recent timestamp and should be primary.

3. **glossary.md**: `[[What-Why-How Framework]]` is defined but has no incoming wikilinks. This should be either:
   - Linked from relevant pages (coaching-related)
   - Removed if not a core concept

---

## 5. Undocumented Concepts in Raw Sources

From `raw/researches/2026-07-05-alex-hormozi-coaching-philosophy.md`:

- **ROI Calculator** - Mentioned as mental model but no dedicated page
- **"Alex and Moses"** - Referenced query that could use a note page

---

## 6. Suggestions for New Investigations

Based on broken links:

- [ ] Create `[[Cold Outreach]]` page - 10-step process mentioned in Core Four
- [ ] Create `[[Content Marketing]]` page - Content posting strategy
- [ ] Create `[[Paid Advertising]]` page - Paid ads optimization
- [ ] Create `[[Warm Outreach]]` page - Relationship-based outreach
- [ ] Create `[[Decoy Offer]]` page - Strategy mentioned in Advanced Offer Stacking
- [ ] Create `[[Social Proof]]` page - Key for Perceived Likelihood & Guarantees
- [ ] Create `[[Offer Enhancers]]` page - Related to MAGIC Naming

---

## 7. Cross-Reference Health Score

- **Total Wikilinks Found**: 274
- **Broken Wikilinks**: 31 (11.3%)
- **Orphan Pages**: 0-2 pages (adequately linked)
- **Missing Cross-References**: 0 identified pairs

---

## 8. Duplicate/Redundant Links

The following pages link to each other bidirectionally (healthy cross-references):
- `[[Grand Slam Offer]]` ↔ `[[Value Equation]]`
- `[[Grand Slam Offer]]` ↔ `[[Money Models]]`
- `[[Grand Slam Offer]]` ↔ `[[Scarcity]]`
- `[[Grand Slam Offer]]` ↔ `[[Urgency]]`
- `[[Grand Slam Offer]]` ↔ `[[Guarantees]]`
- `[[Grand Slam Offer]]` ↔ `[[Attraction Offers]]`
- `[[Grand Slam Offer]]` ↔ `[[Upsell Offers]]`
- `[[Grand Slam Offer]]` ↔ `[[Downsell Offers]]`
- `[[Grand Slam Offer]]` ↔ `[[Continuity Offers]]`
- `[[Grand Slam Offer]]` ↔ `[[Customer Financed Acquisition]]`
- `[[Grand Slam Offer]]` ↔ `[[Customer Avatar]]`

---

*Lint performed: July 5, 2026*
*Next recommended lint: After creating missing pages*