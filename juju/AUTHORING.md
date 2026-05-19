# Juju Pre-Algebra Study Guide — Authoring Rules

**Live URL:** https://a799608.github.io/mvp-guest-guides/juju/v3.html
**Repo file:** `juju/v3.html`
**Working clone:** `C:/temp/mvp-guest-guides/`
**Audit script:** `juju/audit_no_leaks.py`

## The Rule (set by Will, 2026-05-18)

> "as with previous versions you cannot give her the answers. it's ok to give her a summary at the beginning, but when she starts answering questions she has to do the work on her own."

Translation: **nothing visible BEFORE Juju attempts a question may contain the answer.** The point of the guide is for her to think, not to read the answer off the screen.

### What's OK

- **Section intro** (the `con` div at the top of each section): general methodology, formulas, rules of thumb. Summaries are encouraged.
- **Explanation** (3rd arg to `ck`/`cn`/`ce`/`cs`): full step-by-step solution. This only shows AFTER she answers correctly OR after her 2nd wrong attempt (question is then locked). She's already done the work.

### What's NOT OK

1. **Input `placeholder`** must NOT contain the literal answer or a clone of it.
   - ❌ `placeholder="e.g. x=-2"` when the answer is `x=-2`
   - ❌ `placeholder="like 2/15"` when the answer is `2/15`
   - ❌ `placeholder="like: closed right"` when the answer is `closed right`
   - ❌ `placeholder="e.g. 45h > 15+40h"` when the answer is `45h>15+40h` (the `ce` check strips spaces, so the placeholder with spaces still matches the answer)
   - ✅ `placeholder="your answer"`, `"simplified fraction"`, `"inequality with x"`, `"dot type + direction"`, `"number"`, `"yes or no"`, `"mean/median/mode"`

2. **Question prompt** must not include scaffolding parentheticals that telegraph structure.
   - ❌ `Write the inequality (Carpet Creations < Magic Carpet).`
   - ❌ `Write the inequality (perimeter <= 100 ft).`
   - ❌ `Find P(Daisy then Poppy) (no replacement — real flowers).` (gives away the "dependent" answer to the next question)
   - ✅ `Write the inequality.` — match the worksheet's original wording.

3. **Section intro** must not contain a worked example using the exact numbers of a specific question, nor state the answer to a specific question as a "rule".
   - ❌ Intro says `Example: "39 is what percent of 163?" means p = 39/163 * 100` while q169 IS that exact question.
   - ❌ Intro says `Real-world picking from a garden = dependent.` while q180 asks "are these events independent or dependent?".
   - ✅ Generic methodology: `Use a key: identify the percent, the part, and the whole, then plug into part = (percent/100) * whole.`

4. **First-attempt hint** (`ht` div) must give STRATEGY only, not numbers plugged in.
   - ❌ `0.35 × 56,000` (literally the calculation)
   - ❌ `Strict (<, >) = open. Less-than = arrow left.` (the exact answer for a graph question)
   - ❌ `(8/52) × (12/51), then simplify` (the full setup)
   - ❌ `-4+7=3` (gives the answer in the equation)
   - ✅ `percent (as decimal) × total`
   - ✅ `Dot type from strict vs inclusive; direction from less vs greater.`
   - ✅ `First daisy out of full total. After removing it, poppy out of what's left.`

## Authoring workflow

1. **Pull first.** `git -C C:/temp/mvp-guest-guides pull`
2. **Edit** `C:/temp/mvp-guest-guides/juju/v3.html`. Each new question:
   - Use a unique `q###` id (continue from the highest existing).
   - Pick the right check function:
     - `ck(n, "ans1|ans2", "explanation")` — string answer
     - `cn(n, target_number, "explanation")` — numeric (±0.05 tolerance)
     - `ce(n, "expr1|expr2", "explanation")` — algebraic; strips whitespace + lowercases before comparing
     - `cs(n, [array, of, numbers], "explanation")` — set of numbers (order-insensitive)
   - Apply the four rules above to placeholder, prompt, intro, hint.
3. **Run the audit:** `python C:/temp/mvp-guest-guides/juju/audit_no_leaks.py`
   - Must report `PLACEHOLDER LEAKS: 0` and (optionally) a hint-leak scan with 0 high-confidence flags.
   - Anything flagged: fix it BEFORE pushing.
4. **Extend the topic map** at the end of the file with one Object.assign(T,{...}) script per added section. Example:
   ```html
   <script>Object.assign(T,{167:"Percents",168:"Percents",...});</script>
   ```
5. **Commit + push** to `origin/main`. GitHub Pages serves the new version within ~30 sec.

## Reference: existing question count

As of 2026-05-19: **197 questions across 25 sections.** See live URL.

## History

- 2026-05-18: Will called out that q148-q197 (new) and Section 15 (existing q102-q108) were leaking answers in the input placeholder. Full sweep audited and fixed 36 placeholder leaks across the whole file. Audit script added.
- 2026-05-18: Memory file `feedback_juju_no_answer_leaks.md` written.
