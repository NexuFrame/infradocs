# Configuration

InfraDocs reads `config.yaml` from your project root.

| Key | Default | Description |
|-----|---------|-------------|
| `site_name` | `"My Infrastructure"` | Title shown in the portal header |
| `input_dir` | `"data"` | Directory containing YAML/CSV input files |
| `output_dir` | `"output/site"` | Where to write the generated HTML |
| `theme` | `"dark"` | Color theme (`dark` or `light`) |
| `logo` | `""` | Path to logo image (optional) |
| `footer` | `""` | Footer text on all pages |

Example `config.yaml`:
```yaml
site_name: "Acme Corp IT"
input_dir: data
output_dir: output/site
theme: dark
footer: "IT Department — Internal Use Only"
```
