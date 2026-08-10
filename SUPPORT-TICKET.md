# GitHub Support ticket draft

Submit at https://support.github.com/ (category: Profile / Account).
Everything below was verified on 2026-08-10. Paste from the divider down.

---

**Subject:** Profile README is not rendering on my profile page despite a correctly configured repository

My profile README does not appear on https://github.com/JonathanSolvesProblems, even
though the repository meets every documented requirement. The repository's own page
renders the README correctly, so this appears to be specific to the profile-page mirror.

**Account:** JonathanSolvesProblems
**Repository:** https://github.com/JonathanSolvesProblems/JonathanSolvesProblems

Current configuration, verified through the REST API:

| Property | Value |
| --- | --- |
| Repository name vs. account login | byte-identical (compared programmatically) |
| Visibility | public |
| Fork | false |
| Archived / disabled | false |
| Default branch | main |
| README | `README.md` at repository root, 3234 bytes |
| Anonymous access | repo page, raw README, and raw assets all return HTTP 200 |
| Repo's own page | renders the README correctly, including images |
| Profile page | no README block rendered |

**How I am measuring this.** A profile that renders a README serves a
`<div class="Box tmp-mt-4 profile-readme">` server-side inside
`<turbo-frame id="user-profile-frame">`. Counting that string in the served HTML:

    curl -sL https://github.com/JonathanSolvesProblems | grep -oic "profile-readme"   ->  0
    curl -sL https://github.com/chrisipanaque        | grep -oic "profile-readme"   ->  1

The second is an unrelated public profile used as a control, to show the check itself
is valid.

**Causes I have already eliminated by direct test:**

1. Name mismatch. Login and repository name compared programmatically, byte-identical.
2. README content. I temporarily replaced the README with a single plain line
   (`# Hello` plus one sentence) and pushed. The profile still rendered nothing, so
   this is not a Markdown or asset problem.
3. Private-to-public history. The repository was originally created private and later
   made public. I then deleted that approach and created a brand-new repository that
   was public from the moment of creation. The behaviour is identical.
4. Stale internal association. I renamed the repository away and back, and pushed
   fresh commits afterward to generate new push events. No effect.
5. Caching on my side. Checked with cache-busting query strings, with a cold
   incognito browser profile, and while signed in as the account owner. All agree.
6. A GitHub incident. githubstatus.com reported all systems operational with zero
   active incidents throughout.
7. Profile privacy settings. "Make profile private and hide activity" is unchecked;
   pinned repositories and the contribution graph render publicly as normal.

The condition has persisted for over 12 hours across two separate repositories.

Could you check whether something server-side is preventing this account's profile
README from being associated or rendered?
