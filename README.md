<img src="assets/banner.jpg" alt="Jonathan Andrei, Senior Full Stack Developer. github.com/JonathanSolvesProblems and jonathansolvesproblems.com. Python, TypeScript, React, Next.js, LLM Agents, RAG, AWS." width="100%">

I build software that actually ships. Most of what is below started as a deadline and
ended as something that runs, against real data, in front of real users.

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
| **[coldpath](https://github.com/JonathanSolvesProblems/coldpath)** | Prove whether an Arm binary can actually use the chip's matrix hardware. Static ISA verifier +… | Python |
| **[culprit](https://github.com/JonathanSolvesProblems/culprit)** | A stack trace for model decay. Walks DataHub's end-to-end ML lineage from a degraded production… | Python |
| **[Motion-Capture-Hand](https://github.com/JonathanSolvesProblems/Motion-Capture-Hand)** | Hardware motion-capture hand that drives a rigged 3D hand in Blender in real time. An Arduino r… | C++ |
| **[maternal-guard-prompt-opinion-hackathon](https://github.com/JonathanSolvesProblems/maternal-guard-prompt-opinion-hackathon)** | Winner, Agents Assemble: The Healthcare AI Endgame (4,335 participants). MCP server and clinici… | TypeScript |
| **[flakewarden](https://github.com/JonathanSolvesProblems/flakewarden)** | 1st place, Test Cloud track, UiPath AgentHack 2026 (333+ submissions, 104 countries). Agentic f… | Python |
| **[overtone](https://github.com/JonathanSolvesProblems/overtone)** | WCAG 2.1 audio description for an entire video archive, generated in place on Backblaze B2 so r… | Python |
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
