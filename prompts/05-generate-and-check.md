# Generate (Lesson 5 and 6)

## Riverflow
Read aloud before every click: "GPT 2, 2K, 3:4, one." (model GPT Image 2 High, 2K, 3:4, one image).
Loop per slide: copy prompt → empty box → paste → read row → generate → download PNG → name 0N-name-gpt → riverflow/.

## Google Flow
Agent Settings first: Confirm before generating = Always, default 3:4 ×1, Save. Then wrap every prompt:

```text
Generate exactly one image, 3:4 portrait.
Use the prompt below word for word.
Do not rewrite, shorten, or improve it.

PROMPT:
[paste slide, style block included]
```
Download 2K, rename 0N-name-flow, move to flow/. One message every 2–3 minutes.

Reference with a job (optional):
```text
Use the attached image only as a reference for paper texture and the softness
of the illustration. Do not copy its layout, its words, its colours,
or its subject.
```

Judge slide by slide: spelling → layout → family. All six keepers from one engine.

# Check (six points)

```text
I have attached six slides, copy.md and style-dna.md.

Make a table with one row per slide and these columns: copy exact, extra words,
footer on both sides, colours within the palette, interface or logo elements,
readable at phone size.

At the bottom, two sentences. Tell me which one slide most needs
regenerating and why, or say none.

Do not regenerate anything and do not edit any file.
```
Then your own pass at phone size.

# Fix one slide only
Append to that slide's prompt, same engine, same four settings:
```text
Correction: the previous version showed "[WHAT IT SHOWED]." The correct text is
"[EXACT TEXT FROM copy.md]" Change nothing else about the slide.
```
Re-check the whole slide. Same word fails twice → shorten the text in copy and prompt.

# Finish
final/01-cover … 06-cta as .png + .jpg + .prompt.txt (slide 3's prompt file includes the correction if used).
