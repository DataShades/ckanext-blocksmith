There are two ways to install `ckanext-blocksmith`:

1. From source (recommended for development):
```bash
pip install -e .
```

2. From PyPI (recommended for production):
```bash
pip install ckanext-blocksmith
```

After installing the extension, **initialize the database** tables by running:

```bash
ckan -c PATH_TO_CONFIG db upgrade -p blocksmith
```
