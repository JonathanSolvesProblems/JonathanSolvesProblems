<img src="assets/banner.jpg" alt="Jonathan Andrei, Senior Full Stack Developer. github.com/JonathanSolvesProblems and jonathansolvesproblems.com. Python, TypeScript, React, Next.js, LLM Agents, RAG, AWS." width="100%">

<!-- SHIPATON-CTA:START -->
> **I'm looking for a few Android beta testers right now** (through September 2026, for the [RevenueCat Shipaton](https://shipaton.com)).
>
> I'm shipping **Elbow Room Mobile**: point your phone at a room and it measures the place, works out what you'd need to buy to renovate it, and tells you whether the sofa you're about to order can actually get up your stairs. Every furniture app shows you the sofa in the room; none of them tell you it can't get up the stairs.
>
> If you have an Android phone and two minutes: sign up (your email stays private) with **[this quick form](https://docs.google.com/forms/d/e/1FAIpQLScqcwbK-zQkTl8ZuONInbX4OWp4Yq305slCRiBjJbwt7T3mSg/viewform)**, I'll add you, then opt in to the **[closed test](https://play.google.com/apps/testing/com.jonathanandrei.elbowroom)**. Two-minute **[demo](https://www.youtube.com/watch?v=wrayVbYHAH0)**. Happy to test yours back.
<!-- SHIPATON-CTA:END -->

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
| **[will-it-focus](https://github.com/JonathanSolvesProblems/will-it-focus)** | An autofocus compatibility agent for cameras, lenses and adapters, built on Sanity Context. Eve… | TypeScript |
| **[unsay](https://github.com/JonathanSolvesProblems/unsay)** | Unsay: an AI medication-safety agent that goes back and un-says what it told you. Bitemporal ag… | Python |
| **[sticker](https://github.com/JonathanSolvesProblems/sticker)** | Calls licensed pharmacies to find what a prescription actually costs in cash, and prices every… | Python |
| **[daythirty](https://github.com/JonathanSolvesProblems/daythirty)** | An agent that works a California health insurance denial end to end. Statutory deadline, publis… | Python |
| **[northbound](https://github.com/JonathanSolvesProblems/northbound)** | Load board that knows which US freight a Canadian truck can legally haul. RoadStar Hackathon 20… | TypeScript |
| **[dailies](https://github.com/JonathanSolvesProblems/dailies)** | Smart-glasses POV footage of a film shoot becomes queryable continuity records. Gemini reads ev… | Python |
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
