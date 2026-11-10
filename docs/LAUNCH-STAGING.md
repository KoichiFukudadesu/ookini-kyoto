# ookini Kyoto Pass — Launch staging (2026-11-11)

This branch is a **safe preparation branch**. It does not change the public Netlify site or enable payments.

## Verified facts
- Existing Netlify production site: https://ookini-kyoto.netlify.app
- Netlify production currently comes from a manual Drop deployment; Git-based continuous deployment has not been configured.
- The default GitHub branch does not currently contain the production site `index.html`.
- The latest preserved preview candidate is in ChatGPT Library: `/試作/ookini-preview-cta-route-fix-20261111-0317.zip` (21 files). It is not yet proven to work on an actual iPhone Safari device.
- The existing home-page visual concept (version 15) must remain unchanged unless the owner requests otherwise.

## Release gates (do not skip)
1. Back up the live production HTML and verify the backup.
2. Review the candidate files for credentials, private data, payment activation and unwanted external calls **before** putting them in this public GitHub repository.
3. Validate relative asset paths, HTML navigation, and missing-file / 404 handling.
4. Deploy to a **non-production** preview and check actual HTTPS and iPhone Safari navigation; do not infer success from Netlify `ready` alone.
5. Review Stripe checkout and Supabase webhook security. Existing notes identify missing expected Price ID, currency and amount validation; do not activate real payments before resolving and testing this.
6. Only after approval, connect the existing Netlify project to the correct GitHub repository and verify a small reversible change end-to-end.
7. Preserve an easy rollback path to the previous Netlify deploy.

## Immediate next step
Connect Git continuous deployment for the **existing** Netlify project only after the candidate is reviewed and staged; do not create a second public site accidentally. Netlify UI: Project configuration > Build & deploy > Continuous deployment > Link repository (labels may differ).

This branch contains planning and checks only, not site assets.
