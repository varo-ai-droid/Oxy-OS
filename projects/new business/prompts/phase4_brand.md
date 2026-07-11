# Phase 4: Brand - Iteration {{iteration}}/6

## Business Plan
{{business_plan}}

{{#if previous_feedback}}
## Previous Feedback
{{previous_feedback}}
{{/if}}

## Task by Iteration
{{#if iteration == 1}}
### 1. BRAND STRATEGY
- **Name**: Available .com, memorable, spells phonetically
- **Tagline**: ≤5 words, says what it does
- **Positioning**: "For [who], [name] is the [category] that [benefit] unlike [alternative]"
- **Voice**: 3 adjectives + 3 anti-adjectives
- **Core Message**: One thing everyone must remember
{{/if}}

{{#if iteration >= 2 and iteration <= 4}}
### {{iteration}}. LOGO CONCEPT
Generate an SVG logo concept description:
- **Metaphor**: [Visual metaphor for the brand]
- **Typography**: [Font pairing + rationale]
- **Colors**: [Hex codes + psychology]
- **Mark**: [Icon description]
- **Variations**: horizontal, stacked, icon-only, favicon

Output as detailed prompt for image generator.
{{/if}}

{{#if iteration == 5}}
### 5. BRAND GUIDELINES
Assemble complete guide:
- Logo usage (clear space, min size, don'ts)
- Color palette (primary, secondary, neutral, semantic)
- Typography (headings, body, code, scale)
- Imagery style
- Voice examples (do/don't)
- Templates (social, email, deck)
{{/if}}

{{#if iteration == 6}}
### 6. FINAL POLISH
Refine based on all feedback. Output:
1. brand-guide.md (complete)
2. logo.svg prompt (final)
{{/if}}

## Output
Save as structured markdown. For logo: detailed SVG prompt.