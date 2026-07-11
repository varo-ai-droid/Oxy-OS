# Brand Guide: CounterBrief

## Name
**CounterBrief** — "Counter" (oppose, fight back) + "Brief" (legal evidence packet). Two syllables, spells phonetically, .com available.

## Tagline
**Win the disputes templates lose.**

## Positioning
> For Shopify merchants losing money to chargebacks, CounterBrief is the evidence automation platform that builds reason-code-specific packets from your real data — so you approve in 2 minutes, not 2 hours. Unlike Chargeflow or Midigator that send generic templates, CounterBrief maps 18 reason codes to exact evidence requirements, pulling from Shopify, email, shipping, and 3PL automatically.

## Voice & Tone

### Adjectives (Do)
- **Sharp** — precise, technical, no fluff
- **Empowering** — merchant is the hero, we're the tool
- **Relentless** — we fight for every dollar

### Anti-Adjectives (Don't)
- **Corporate** — no "solutions," "leverage," "synergy"
- **Passive** — no "we help you," "enables"
- **Fear-mongering** — no "don't get crushed," "protect yourself"

### Voice Examples

| Context | Do | Don't |
|---------|-----|-------|
| Hero headline | "Win the disputes templates lose." | "Protect your revenue from chargebacks." |
| Feature | "Reason-code-native evidence. Auto-built." | "Our solution provides automated evidence generation." |
| Error | "Dispute not found. Check the ID." | "We're sorry, an error occurred." |
| CTA | "Connect Shopify. Win your first dispute." | "Get started with our platform today." |
| Case study | "[Brand] recovered $47k in 30 days." | "[Brand] leveraged our solution for success." |

## Core Message
**One sentence**: CounterBrief builds the exact evidence packet your reason code demands — from your data — so you win winnable chargebacks.

**Three pillars**:
1. **Reason-code-native** — Visa 10.4 ≠ 13.1. We know the difference.
2. **Your data, assembled** — Shopify + Email + Shipping + 3PL → one packet.
3. **You approve, we submit** — 2-minute review, one click, $19 per win.

## Visual Identity

### Logo
- **Mark**: Stylized "CB" — left serif (argument), right mono (evidence)
- **Variations**: Horizontal, stacked, icon-only (favicon), mono
- **Clear space**: 1x icon height on all sides
- **Min size**: 24px width (icon), 120px width (horizontal)

### Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| **Primary** | `#F59E0B` (Amber 500) | CTAs, highlights, logo accent |
| **Primary Dark** | `#D97706` (Amber 600) | Hover states |
| **Background** | `#0F172A` (Slate 950) | Dark mode base |
| **Surface** | `#1E293B` (Slate 800) | Cards, modals |
| **Border** | `#334155` (Slate 700) | Dividers, inputs |
| **Text Primary** | `#F8FAFC` (Slate 50) | Headings, body |
| **Text Secondary** | `#94A3B8` (Slate 400) | Captions, muted |
| **Success** | `#22C55E` (Green 500) | Win badges, positive |
| **Warning** | `#F59E0B` (Amber 500) | Pending, review needed |
| **Error** | `#EF4444` (Red 500) | Losses, critical |
| **Light Mode BG** | `#FFFFFF` | Light mode base |
| **Light Mode Surface** | `#F1F5F9` (Slate 100) | Light mode cards |

### Typography

| Role | Font | Scale |
|------|------|-------|
| **Heading** | **Space Grotesk** (Variable) | Display: 48/56, H1: 36/44, H2: 30/38, H3: 24/32 |
| **Body** | **IBM Plex Sans** (Variable) | LG: 18/28, Base: 16/24, SM: 14/20, XS: 12/16 |
| **Code/Evidence** | **IBM Plex Mono** | 13/20 |
| **UI/Label** | **IBM Plex Sans Medium** | 13/20 |

**Scale Ratio**: 1.25 (Major Third) — harmonious, technical feel

### Imagery Style
- **Screenshots**: Real product UI, dark mode, annotated with evidence fields
- **Illustrations**: Technical diagrams (evidence graph, reason code map) — mono line weight, amber accents
- **Photography**: None (avoids stock feel). If needed: merchant at desk, laptop screen visible, natural light.

### Iconography
- **Style**: 2px stroke, rounded caps, 24×24 grid
- **Set**: Custom — dispute, evidence, reason-code, win, loss, tracking, email, packet
- **Amber accent** on active/primary actions

---

## Templates

### Social Card (1200×630)
```
┌────────────────────────────────────────────────────────┐
│  [Logo]  CounterBrief                    [Win Badge]   │
│                                                         │
│  "Win the disputes templates lose."                    │
│                                                         │
│  [Screenshot: Evidence packet with reason code 10.4]   │
│                                                         │
│  $19 per win · Shopify App Store                       │
└────────────────────────────────────────────────────────┘
```

### Email Template
```
Subject: [Brand] recovered $47k in chargebacks

Body:
Sharp. No fluff.

[Brand] was losing $3k/mo to friendly fraud.
Chargeflow sent templates. Banks rejected them.

CounterBrief connected Shopify + Gmail + ShipStation.
First dispute: Visa 10.4. Evidence auto-built.
Merchant reviewed 2 min. Clicked submit.
Won. $2,847 recovered.

Now they win 55%+ (was 23%).

$19 per win. You keep 100%.

[CTA: Connect Shopify → Win your first dispute]

— Nate, Founder
```

### Deck Template
- **Slide 1**: Logo + Tagline
- **Slide 2**: Problem (3 stats + 1 quote)
- **Slide 3**: Solution (3 pillars)
- **Slide 4**: Product (annotated screenshot)
- **Slide 5**: Win rate comparison chart
- **Slide 6**: Pricing
- **Slide 7**: Roadmap
- **Slide 8**: Team + Contact

---

## Do's and Don'ts

| Do | Don't |
|----|-------|
| Use "evidence packet" not "response" | Say "chargeback response" |
| Say "win rate" not "success rate" | Use "success rate" |
| Lead with merchant win | Lead with "our platform" |
| Show real UI screenshots | Use abstract illustrations |
| Quote specific reason codes | Say "all chargebacks" |
| Price per win ($19) | Hide pricing |

---

## Brand Checklist (Launch)
- [ ] Logo files (SVG, PNG @ 1x/2x/3x, favicon)
- [ ] Color tokens in code (CSS variables, Tailwind config)
- [ ] Fonts self-hosted (Space Grotesk, IBM Plex Sans/Mono)
- [ ] Component library: Button, Card, Modal, Badge, Table
- [ ] Dark mode default, light mode toggle
- [ ] Social cards generated (og:image)
- [ ] Email templates in codebase
- [ ] App Store screenshots (5) + video
- [ ] Comparison page: CounterBrief vs Chargeflow
- [ ] Case study template ready