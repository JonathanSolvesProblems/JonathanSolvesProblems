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
| **[possessed](https://github.com/JonathanSolvesProblems/possessed)** | Your link checker is green. Some of those links now open a casino. Gemma 4 reads the pages and… | Python |
| **[swatchless](https://github.com/JonathanSolvesProblems/swatchless)** | A colour-match desk for hair retailers: the customer wearing the shade before they buy, on YouC… | TypeScript |
| **[floodplain](https://github.com/JonathanSolvesProblems/floodplain)** | Runs the test suites of a package's dependents before and after a release, in forked Nebius San… | Python |
| **[setpiece](https://github.com/JonathanSolvesProblems/setpiece)** | Seated mixed reality previs for VFX shots: block the shot on your table with your hands and lea… | TypeScript |
| **[will-it-focus](https://github.com/JonathanSolvesProblems/will-it-focus)** | An autofocus compatibility agent for cameras, lenses and adapters, built on Sanity Context. Eve… | TypeScript |
| **[orvandel-wake-now](https://github.com/JonathanSolvesProblems/orvandel-wake-now)** | Wake Now for Orvandel, a free browser MMORPG: planning docs and source built with the Devpost L… | TypeScript |
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
