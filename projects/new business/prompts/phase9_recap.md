# Phase 9: Recap - HTML Package

## All Artifacts
{{artifacts_json}}

## Company Name: {{company_name}}
## Generated: {{timestamp}}

## Your Task
Generate a SINGLE `index.html` file - the complete company recap.

### Required Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{company_name}} - Company Builder Recap</title>
  <style>/* Embedded CSS: clean, technical, printable, dark-mode */</style>
</head>
<body>
  <header class="hero">
    <h1>{{company_name}}</h1>
    <p class="tagline">[from brand guide]</p>
    <p class="meta">Built in ~4 hours by multi-agent orchestration</p>
  </header>

  <nav class="toc">
    <ul>
      <li><a href="#business-plan">Business Plan</a></li>
      <li><a href="#brand">Brand</a></li>
      <li><a href="#research">Research</a></li>
      <li><a href="#product">Product</a></li>
      <li><a href="#videos">Videos</a></li>
      <li><a href="#red-team">Red Team</a></li>
      <li><a href="#done">Definition of Done</a></li>
    </ul>
  </nav>

  <main>
    <section id="business-plan">
      <h2>Business Plan</h2>
      [Rendered markdown from business-design/business-plan.md]
    </section>

    <section id="brand">
      <h2>Brand</h2>
      [brand-guide.md + logo preview]
    </section>

    <section id="research">
      <h2>Research</h2>
      <h3>Pain Hunt</h3>
      [pain-hunt/candidates.md]
      <h3>Tournament</h3>
      [tournament/scores.md + winner.md]
    </section>

    <section id="product">
      <h2>Product</h2>
      <h3>Landing Page</h3>
      [Screenshot/embed + link to product/index.html]
    </section>

    <section id="videos">
      <h2>Video Scripts</h2>
      <h3>Launch Video</h3>
      [videos/launch-script.md]
      <h3>Founder Video</h3>
      [videos/founder-script.md]
    </section>

    <section id="red-team">
      <h2>Red Team Verdict</h2>
      [red-team/verdict.md + fixes.md]
    </section>

    <section id="done">
      <h2>✅ Definition of Done</h2>
      <ul class="checklist">
        <li><input type="checkbox" checked disabled> Stranger understands business in 5 min</li>
        <li><input type="checkbox" checked disabled> Video scripts complete</li>
        <li><input type="checkbox" checked disabled> Landing page runs locally</li>
        <li><input type="checkbox" checked disabled> Red team: VIABLE WITH FIXES</li>
        <li><input type="checkbox" checked disabled> All fixes applied</li>
        <li><input type="checkbox" checked disabled> Domain available</li>
        <li><input type="checkbox" checked disabled> Brand guide complete</li>
      </ul>
    </section>
  </main>

  <footer>
    Generated {{timestamp}} | <a href="#">View on GitHub</a>
  </footer>
</body>
</html>
```

### CSS Requirements
- Clean, technical aesthetic (Stripe/Linear docs style)
- CSS variables for light/dark mode
- Print-friendly (@media print)
- Syntax highlighting for code blocks
- Collapsible sections with <details>
- Sticky TOC on desktop

## Output
Return ONLY the complete HTML file. Use artifact paths to link/read files.