# Troubleshooting

## `FileNotFoundError: config.yaml not found`
Run `infradocs build` from the directory containing `config.yaml`, or pass `--config path/to/config.yaml`.

## `KeyError: 'hostname'`
A device in `devices.yaml` is missing a required field. Run `infradocs validate` to see all errors.

## `UnicodeDecodeError` on CSV load
Save your CSV as UTF-8. In Excel: File → Save As → CSV UTF-8.

## Output directory is empty
Check that `input_dir` in `config.yaml` points to a directory with at least one `.yaml` file.

## Jinja2 `TemplateNotFound`
The `templates/` directory must be in the same directory as `config.yaml` or set `INFRADOCS_TEMPLATES` env var.
