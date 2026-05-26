# FAQ

**Q: Can I use this offline?**
Yes. InfraDocs generates plain HTML with no external dependencies.

**Q: Can I add custom sections?**
Yes. Add a new YAML file and a matching Jinja2 template. See docs/templates.md.

**Q: Does it support Windows?**
Yes. Python 3.8+ on Windows, Mac, and Linux.

**Q: Can I white-label the output?**
Yes with the MSP license. Replace `templates/base.html` with your own branding.

**Q: How do I add a logo?**
Set `logo: path/to/logo.png` in `config.yaml`. The path is relative to `config.yaml`.

**Q: Is the data stored anywhere?**
No. InfraDocs reads your files and writes HTML. No data leaves your machine.

**Q: Can multiple people edit the same data?**
Yes. Store your YAML files in Git and run `infradocs build` in your CI pipeline.

**Q: How do I export to PDF?**
Open the generated site in Chrome, then File → Print → Save as PDF. The print CSS is optimised for this.

**Q: What happens if a required field is missing?**
`infradocs validate` reports all errors before building. The build will skip malformed records.

**Q: Can I run it as part of a CI/CD pipeline?**
Yes. `infradocs build` exits 0 on success, non-zero on error.
