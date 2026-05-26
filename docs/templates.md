# Customizing Templates

Templates use Jinja2 and extend `base.html`.

## Creating a custom page type

1. Create `templates/my-page.html`:
```html
{% extends "base.html" %}
{% block title %}My Page{% endblock %}
{% block content %}
<h1>{{ item.name }}</h1>
{% endblock %}
```

2. Register it in your generator config.

## Available template variables
Each template receives the data object it renders plus `site_config` (the full config.yaml contents).
