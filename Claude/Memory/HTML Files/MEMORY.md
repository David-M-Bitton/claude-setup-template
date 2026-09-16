# HTML Files — build standards

🔴 **Read this before creating OR editing any HTML file or report.**

This folder ships two things you should use, not rebuild:

| File | What it is |
|---|---|
| `template.html` | the starter report — every rule below marked "template" is already wired up |
<!--os:mac-->
| `eval-check.py` | the pre-delivery check. `python3 eval-check.py <file.html>` |
<!--/os:mac-->
<!--os:win-->
| `eval-check.py` | the pre-delivery check. `python eval-check.py <file.html>` |
<!--/os:win-->

---

## Quick start (do this first)

1. **Start from the template — never rebuild from scratch.** Copy `template.html`. Dark/light mode, sticky hero, hamburger jump-menu, no-index meta, "Last Updated", notes, accordions + expand/collapse-all, sortable sticky tables, tooltips, print toggle, and delta arrows are already there.
2. **Swap the palette.** The template ships a neutral slate/blue palette as CSS variables at the top of `<style>`. Replace those hex values with whatever brand or personal colours fit, or leave them for something quick and clean.
3. Fill in content, set the page title + SEO `<title>` + Last Updated, then open the file. **Before sharing or publishing, run the eval-check** (`python3 eval-check.py <file.html>` on Mac, `python eval-check.py <file.html>` on Windows). Treat a fail as a blocker.

---

## Build standards — every HTML report MUST follow these

1. **Charts and visuals** — use them as much as possible (Chart.js via CDN). Show, don't just tell.
2. **Scannability** — tables, bullets, numbered lists. Easy to skim.
3. **Urgent flags up top** — anything major or urgent goes in a banner at the very top.
4. **No-index** *(template)* — every file carries `<meta name="robots" content="noindex,nofollow">` AND `<meta name="googlebot" content="noindex,nofollow">`, so it's never indexed if it ends up somewhere public.
5. **Accordions** *(template)* — every section is a toggle, **open by default**.
6. **Expand/collapse all** *(template)* — one control at the very top for every section at once.
7. **Tables** *(template)* — column headers **sticky** and **sortable** ascending/descending on click.
8. **Theme button** *(template)* — dark/light toggle at the top, labelled "Theme", persisted to localStorage.
9. **Last Updated** *(template)* — top-right, formatted like `Last Updated: Thursday, June 18, 2026 at 8:45 AM EDT`. Exact date and time of the update.
10. **Bold for emphasis** — bold the most important text to direct attention.
11. **Action items = checkboxes** *(template)* — to-do lists are checkboxes, not bullets, and the checked state saves to localStorage.
12. **Notes section** *(template)* — a notes box at the very top under the header, **collapsed by default**, saved to localStorage. Ignore cross-device sync.
13. **Comparisons** *(template)* — against a prior date, show **both number and percentage** with up/down arrows, green up / red down.
14. **Sticky hero header** *(template)* — the title hero is a small section that stays fixed as you scroll.
15. **SEO title** — the `<title>` matches the top-of-page title and is descriptive.
16. **Hamburger menu** *(template)* — top-right icon opens a dropdown of all sections to jump to.
17. **Tooltips** *(template)* — 13px font, 19px line-height, weight 400, black text.
18. **Less is more** — simple, clean, readable. Too much information is distracting. Push secondary detail into an **Appendix** at the very bottom, **collapsed by default**.
19. **Always run the eval-check before delivering.** It verifies the no-index meta and that the `<title>` was actually set. A fail is a blocker.
20. **Print-friendly is a TOGGLE, not a question** *(template)*. A printer icon in the hero button row switches the report to print layout — drops `max-height`/`overflow` on every data table and opens all sections — saved to localStorage, with a hover tooltip explaining it. **Off by default.** There is also an `@media print` block so an actual printout is correct even if the toggle was never switched on: **a scroll-boxed table (`max-height` + `overflow:auto`) prints only the visible rows and silently cuts the rest off.** ✅ Already built into `template.html` — do not re-implement it.
21. **On a COST or expense report, invert the delta colours.** Rule 13's green-up/red-down is for metrics where up is good. Spending more is bad — render increases red and decreases green, keeping the arrow pointing the true direction. Use a `.delta.cost` modifier so both behaviours coexist in one template.

### Already in the template
Rules 4, 5, 6, 7, 8, 9, 12, 14, 16, 17, 20 plus the checkbox / delta / appendix patterns (10, 11, 13, 18). **Add content; don't re-implement the chrome.**

---

## Font

`system-ui` stack (`system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif`) — fast, no web-font request, consistent with the OS. Keep it unless there's a specific reason to change.

---

## Sharing and publishing

Whatever the destination — a hosting service, a file share, or just sending the file — **keep the no-index meta tags (rule 4)** so it's never indexed if it becomes reachable on the open web.

🔴 **Always verify a published link anonymously — with `curl` or a logged-out browser, never only in your own signed-in browser.** A page can render perfectly to the world and come up blank in a signed-in session (third-party cookie and storage partitioning are the usual cause). **Do not debug the HTML file when that happens — it is not the file.** Confirm with an anonymous request first, and only then look at the content.

🔴 **To update a published report, overwrite the SAME hosted file** so the URL stays stable. Uploading a new copy gives a new link and breaks every link already sent.
