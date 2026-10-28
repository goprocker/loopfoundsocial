# LoopFound Social

The content workspace for **@teamloopfound**: a six-slide Instagram carousel workflow, prepared with Claude and approved by a human before anything goes out.

LoopFound helps local shops and service businesses turn outdated or missing websites into ones that get found on Google and AI search. Every post answers one question: *"Why are my competitors getting customers from Google while people can't even find my business online?"*

> Tagline: **get found online** · Call to action: *Comment FOUND and get a free 5-point website audit.*

## How it works

Each carousel goes through two halves: **Make** and **Run**.

| Step | Prompt | What happens | Output |
|---|---|---|---|
| 1 | `01-read-references.md` | Study reference slides for structure only | `refs/notes.md`, `style/style-dna.md` |
| 2 | `02-plan-6-slides.md` | Hooks plus a six-slide plan | `copy.md` |
| 3 | `03-write-prompts.md` | One image prompt per slide, style block pasted unchanged | `prompts.md` |
| 4 | `04-daily-run.md` | Evening run: research, topic, copy, prompts, caption | a new dated carousel folder |
| 5 | `05-generate-and-check.md` | Generate images by hand, then a six-point quality check | `final/` |
| 6 | `06-caption.md` | Caption, with each claim checked against a source | `caption.txt` |
| 7 | `07-publish.md` | Publishing lanes (manual first) | `publish/` |
| 8 | `08-replies-and-review.md` | FOUND keyword replies and the weekly review | `automations/`, `review/` |

## Folder map

```
CLAUDE.md              Brand brief. Claude reads it every session.
style/style-dna.md     Locked style block, pasted above every image prompt
prompts/               Reusable prompts, numbered in the order you use them
refs/                  Reference screenshots ref_01 to ref_06 + notes.md
carousels/<date>-<topic>/
  brief.md             Topic and approval status
  research.md          Candidates with links and dates
  copy.md              Six slides: headline, body, source for each fact
  prompts.md           Six image prompts
  caption.txt          Instagram caption
  final/               Approved slides (.png, .jpg, .prompt.txt)
automations/           FOUND keyword reply rules
publish/               Publishing setup
review/funnel.csv      Results tracking
```

## Ground rules

1. **No invented facts.** Every link, fact or number needs a source. Without one, the copy says *Needs a fact*.
2. **Approval before spending.** Show the plan and the credit count, then wait for a yes.
3. **Prepare only.** Nothing is posted, messaged or scheduled without approval.
4. **Keys stay in `.env`.** Copy `.env.example` to `.env`. It is git-ignored and never pasted into a chat.
5. **References are studied, never copied.** No names, handles, logos or wording from them, and no real brand logos on slides.

## Visual style

3:4 portrait (1080×1440). Muted, film-grain photography with off-white type `#F4F1EA` and a single accent: signal orange `#FF5A1F`. The signature motif is one subject found among many, circled by hand in orange. The full spec is in [`style/style-dna.md`](style/style-dna.md).

## Setup

```bash
git clone https://github.com/goprocker/loopfoundsocial.git
cd loopfoundsocial
cp .env.example .env   # then fill in IMAGE_API_KEY, IG_USER_ID, IG_ACCESS_TOKEN
```

Open the folder in Claude Code. `CLAUDE.md` loads automatically, and you start with the prompts in `prompts/`.
