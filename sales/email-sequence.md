# Post-Purchase Email Sequence

## Email 1 — Welcome (send immediately)

**Subject:** Your InfraDocs Generator is ready 🎉

Hi,

Thanks for purchasing InfraDocs Generator!

**Get started in 3 steps:**
1. `pip install infradocs` (or `pip install -e .` from source)
2. Edit the sample YAML files in `sample-data/`
3. Run `infradocs build --input sample-data --output output/site`

Open `output/site/index.html` and you'll see your documentation portal.

Full docs are in the `docs/` folder. Reply to this email if you get stuck.

— NexuFrame

---

## Email 2 — Tips (send day 3)

**Subject:** 3 things most people miss in InfraDocs

Hi,

A few power-user tips:

1. **Run `infradocs validate` before building** — catches missing fields before they cause errors
2. **Store your YAML in Git** — then your docs auto-update whenever you push
3. **The print stylesheet is built in** — open any page in Chrome and print to PDF for a clean client report

If you're on the MSP tier, you can replace `templates/base.html` to add your own logo and branding.

— NexuFrame

---

## Email 3 — Review request (send day 7)

**Subject:** Quick question about InfraDocs

Hi,

Hope InfraDocs has been useful! If it's saved you time, we'd really appreciate a short review on Gumroad — it helps other IT admins find it.

[Leave a review →]

Got a feature request? Reply here — we read every one.

— NexuFrame
