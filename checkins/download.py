import json
import re
import zulip
from typing import Any, Dict

# Match name mentions in the format `@User Name (pronouns) (batch)`
anything_in_parens = r"\([^\)]+\)"
name_rx = re.compile(
    r"@[\w\s-]+" + anything_in_parens + " " + anything_in_parens, re.IGNORECASE
)

# Images look like this:
# https://recurse.zulipchat.com/user_uploads/13/hlwpjv1y90ZsyRWFDdxEaXDp/ezgif-4-212dcc9592.gif
# user_uploads/13/hlwpjv1y90ZsyRWFDdxEaXDp/ezgif-4-212dcc9592.gif
image_rx = re.compile(
    r'(https://recurse.zulipchat.com)?/user_uploads/\w+/([\w-]+)/([^<"]+)'
)


def main():
    client = zulip.Client()

    request: Dict[str, Any] = {
        "include_anchor": True,
        "anchor": 0,
        "num_before": 1000,
        "num_after": 1000,
        "narrow": [
            {"operator": "topic", "operand": "Lee Trout"},
            {"operator": "stream", "operand": "checkins"},
        ],
    }
    result = client.get_messages(request)

    # Remove potentially sensitive info
    def remove_sensitive_keys(obj):
        if type(obj) != dict:
            return
        for k in list(obj.keys()):
            if type(obj[k]) is dict:
                remove_sensitive_keys(obj[k])
                continue
            if type(obj[k]) is list:
                for item in obj[k]:
                    remove_sensitive_keys(item)
                continue
            for sk in {"email", "full_name", "avatar_url"}:
                if sk in k.lower():
                    obj.pop(k)

    remove_sensitive_keys(result)

    # Clean content
    for msg in result["messages"]:
        # Remove user mentions
        msg["content"] = name_rx.sub("@Anonymous User", msg["content"])

        # Rewrite image locations
        for url, subdir, filename in image_rx.findall(msg["content"]):
            msg["content"] = re.sub(
                f'"/?user_uploads/\w+/{subdir}/{filename}"',
                f'"images/{subdir}-{filename}"',
                msg["content"],
            )

            if url:
                msg["content"] = re.sub(
                    f"{url}/user_uploads/\w+/{subdir}/{filename}",
                    f"images/{subdir}-{filename}",
                    msg["content"],
                )

    with open("messages.json", "w") as fh:
        fh.write(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
