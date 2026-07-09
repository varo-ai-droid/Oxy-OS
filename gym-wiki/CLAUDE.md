# Gym Wiki - Exercise Science Research Knowledge Base

This is the schema and operational guide for the Gym Wiki, a fitness research knowledge base built on the LLM Wiki pattern.

## Purpose

Build a comprehensive, interlinked collection of exercise science knowledge. Track research papers, training methodologies, physiological mechanisms, and synthesize insights over time.

## Directory Structure

```
gym-wiki/
├── raw/                    # Immutable source documents
│   ├── research-papers/    # PDF studies, academic papers
│   ├── articles/           # Web articles, blog posts
│   └── notes/              # Manual annotations, thoughts
├── wiki/                   # LLM-maintained markdown files
│   ├── entities/           # Specific entities: exercises, researchers, studies
│   ├── concepts/           # Abstract concepts: physiological mechanisms, training principles
│   ├── research/           # Study summaries and meta-analyses
│   ├── comparisons/        # Method vs method, study vs study
│   └── index.md           # Content catalog (read first when answering queries)
└── log.md                 # Chronological activity log
```

## Page Templates

### Exercise Entity (`wiki/entities/exercise-name.md`)

```markdown
---
tags: [entity/exercise]
aliases: [alternate names]
category: [[muscle-group]]
equipment: [[equipment-type]]
difficulty: easy|medium|hard
primary-muscles: [muscle1, muscle2]
secondary-muscles: [muscle3]
---

# Exercise Name

## Description
Brief description of the exercise.

## Form Cues
Key points for proper execution.

## Variations
Links to related exercises.

## Evidence
List of studies supporting effectiveness or proper form.

## Related Pages
- [[Related concepts]]
```

### Study Entity (`wiki/entities/study-title.md`)

```markdown
---
tags: [entity/study]
year: 2024
journal: [[Journal Name]]
authors: [[Researcher 1]], [[Researcher 2]]
doi: 10.xxxx
key-findings: [finding1, finding2]
related-studies: [[other-study]]
---

# Study Title

## Citation
Full citation in standard format.

## Abstract
Summary of the study.

## Key Findings
Bullet points of main results.

## Methodology Notes
Sample size, population, measurement methods.

## Implications
Why this matters for training practice.

## Contradictions/Questions
Note any conflicting evidence or limitations.
```

### Concept Page (`wiki/concepts/concept-name.md`)

```markdown
---
tags: [concept]
aliases: [alternate terms]
related-concepts: [[related-concept]]
evidence-level: high|medium|low
---

# Concept Name

## Definition
Clear definition of the concept.

## Scientific Basis
Physiological or biomechanical explanation.

## Evidence
References to supporting research.

## Practical Applications
How this applies to training.

## See Also
Links to related concepts and exercises.
```

## Workflows

### Ingest Workflow
When processing a new source:
1. Read the source and discuss key takeaways with user
2. Determine what entity/concept pages need to be created or updated
3. Create summary pages in appropriate directories
4. Update wiki/index.md with new entries
5. Cross-link to existing pages where relevant
6. Note any contradictions with existing content
7. Append entry to log.md with date and action type

### Query Workflow
When answering questions:
1. Read wiki/index.md to identify relevant pages
2. Read the most relevant wiki pages
3. Synthesize answer with citations to wiki pages
4. Optionally create a new wiki page for valuable insights

### Lint Workflow
Periodic health check:
1. Look for contradiction markers without resolution
2. Find orphan pages (no inbound links)
3. Identify concepts mentioned but lacking their own pages
4. Check for stale claims that newer evidence contradicts
5. Suggest follow-up questions or sources to investigate

## Dataview Queries (Examples)

```dataview
TABLE year, journal FROM #entity/study SORT year DESC
TABLE key-findings AS "Findings" FROM #entity/study
LIST FROM #concept WHERE contains(related-concepts, [[hypertrophy]])
```

## Citation Convention

Internal links to wiki pages: `[[Page Name]]`
External links: `[text](url)`
Studies: `[[Study Title#Key Findings]]` or `[[Study Title|citation]]`

## Contradiction Markers

Use `> [!warning]` blocks to flag potential contradictions:
- Claims that newer evidence challenges
- Conflicting interpretations in different sources
- Areas needing further investigation
