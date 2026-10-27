Post three carousels by hand first (lane D). Then pick a lane.

## Path A: own Meta app, dry run only

```text
Write out, as numbered requests, exactly what you would send to publish
carousels/<folder>/final/*.jpg to my Instagram account.
Do not send any request, do not write a script yet, and do not ask me for a token.
Use media.example.com addresses in file order, the caption from caption.txt,
and show the token only as the name IG_ACCESS_TOKEN. Then list what I need in
place before a real run, and end with: "Nothing was sent."
```

Permissions: instagram_business_basic + instagram_business_content_publish only. JPEG only, max 10 items,
containers expire in 24 h. Token: 1 h → exchange for 60-day → refresh around day 50.

## Path B: Zernio, plan before schedule

```text
Prepare a schedule plan for carousels/<folder>/final/*.jpg on my connected
Instagram account at [DATE TIME + TIME ZONE].
Do not call any service. Do not use any key.
Show a table: the first line of the caption, the six files in order,
the account, the time with its offset.
Also write publish/plan.json: caption, six media entries (type and address),
platform, account, time, zone.
End with: "Nothing has been sent. Approve to schedule?"
```

Read four things: caption, order, account, time. Addresses must be real public JPEG URLs (test in a private window), never example.com and never Drive/Dropbox share links.
