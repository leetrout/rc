# Zulip Topic Export

This directory contains an archive of my checkins while at RC.

The compiled content is in [output.html](output.html).

## Using the tools

- Get your API Key https://zulip.com/api/api-keys
- `pip install -r requirements.txt`
- Download messages `python download.py`
- Manumatically replace borked images in `messages.json`
  - Open all 403 links and download the images from `.../<random>/file.name` to `images/file.name`
  - Replace all links with regex
    - `https://recurse.zulipchat.com/user_uploads/13/([\w-]+)/([^\\]+)`
    - `images/$1-$2`
- Parse `python parse.py`
- Serve `output.html`
