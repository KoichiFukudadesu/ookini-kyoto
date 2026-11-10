# ookini Kyoto Pass — release blockers (2026-11-11)

## Source verified
ChatGPT Library: /試作/ookini-staging-verified-20261111.zip (21 files, ZIP CRC passed).

## Important product reality
The current pass screen is a **simulation only**. It visibly states no real purchase, authentication, entitlement, or AI API calls; US$9.98 is explicitly illustrative and awaiting approval. No Stripe checkout integration was found in the static HTML. Do not represent this as a purchasable product.

## Release gates
- [x] 21-file archive integrity confirmed.
- [x] Four seasonal image files and both MP4s are present.
- [x] Home CTA links to the Discover page.
- [ ] Deploy a separate non-production HTTPS preview without touching the existing live site.
- [ ] Test the actual URL on iPhone Safari, including 320px width, navigation, video playback, free emergency help, and demo pass.
- [ ] Preserve a backup of the currently deployed single-file homepage.
- [ ] Confirm and approve final price and currency.
- [ ] Implement and test Stripe checkout, webhooks, and server-side entitlement verification. Existing security audit noted missing expected Price ID, amount, and currency verification.
- [ ] Run real payment test-mode end-to-end and refund/replay/duplicate event cases.
- [ ] Obtain owner approval before switching production traffic or enabling live charges.

## Current limitation
The connected Netlify management tools can inspect the project but do not expose a ZIP upload/deploy or Git-linking operation. No production deploy or payment change was made in this preparation step.

## Recommended next action
Use a temporary, separately named Netlify preview site or connect GitHub staging to a non-production environment; verify that preview access controls permit the owner's iPhone to open it. Do not overwrite the existing production site or publish unpublished source code in a public repository without review.
