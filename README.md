<img src="assets/banner.jpg" alt="Jonathan Andrei, Senior Full Stack Developer. github.com/JonathanSolvesProblems and jonathansolvesproblems.com. Python, TypeScript, React, Next.js, LLM Agents, RAG, AWS." width="100%">

I build software that actually ships. Most of what is below started as a deadline and
ended as something that runs: agentic flaky-test triage that took **1st place at UiPath
AgentHack 2026**, WCAG audio description for entire video archives, and clinical decision
support written back into FHIR behind a human approval gate.

I work mostly in TypeScript and Python, lately on AI agents and developer tooling, and I
care more about whether a thing survives contact with real input than about how clean it
looks in a diagram.

I take on project work: AI agents, RAG pipelines, developer tooling, and integrations.
Details and selected work at [**jonathansolvesproblems.com**](https://jonathansolvesproblems.com).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/board-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="assets/board-light.svg">
  <img alt="Shipping board: my six most recently pushed projects, with stack and date." src="assets/board-dark.svg">
</picture>

<!-- SHIPPING-LOG:START -->
| Project | What it is | Stack |
| --- | --- | --- |
| **[culprit](https://github.com/JonathanSolvesProblems/culprit)** | A stack trace for model decay. Walks DataHub's end-to-end ML lineage from a degraded production… | Python |
| **[changelog-studio](https://github.com/JonathanSolvesProblems/changelog-studio)** | A Replit template. Connect GitHub or Linear, and it drafts your release note, publishes the pag… | TypeScript |
| **[flakewarden](https://github.com/JonathanSolvesProblems/flakewarden)** | Agentic flaky-test triage and self-healing reviewer for UiPath Test Cloud. 90.7% triage accurac… | Python |
| **[overtone](https://github.com/JonathanSolvesProblems/overtone)** | WCAG 2.1 audio description for an entire video archive, generated in place on Backblaze B2 so r… | Python |
| **[maternal-guard-prompt-opinion-hackathon](https://github.com/JonathanSolvesProblems/maternal-guard-prompt-opinion-hackathon)** | MCP server and clinician dashboard for severe preeclampsia. Five tool returns become a one-clic… | TypeScript |
| **[Viva-OpenAI-Build-Week](https://github.com/JonathanSolvesProblems/Viva-OpenAI-Build-Week)** | An automated oral exam for code: grade the understanding, not the artifact. Found a hidden defe… | TypeScript |
<!-- SHIPPING-LOG:END -->

<details>
<summary>How this page keeps itself current</summary>

<br>

The board is not a third-party widget. It is an SVG this repo generates from my own
push history, so it reflects what I actually touched last rather than a static image
I updated once and forgot.

```
scripts/build_profile.py     queries the GitHub API, renders both themes, rewrites the table
scripts/build_banner.py      renders the banner from assets/portrait.png
assets/board-*.svg           dark and light boards, swapped by prefers-color-scheme
.github/workflows/           re-runs the generator every Monday and commits any change
```

Run `python scripts/build_profile.py` to refresh it by hand.

</details>
