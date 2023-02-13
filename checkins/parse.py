import json
from textwrap import dedent

import emoji
from html5print import HTMLBeautifier


def main():
    raw_messages = None
    with open("messages.json") as fh:
        raw_messages = json.load(fh)

    parsed_messages = []

    for msg in raw_messages["messages"]:
        parsed_messages.append(emoji.emojize(msg["content"], language="alias"))

    with open("output.html", "w") as fh:
        html_output = """<!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
            <style>img.emoji {height: 1em;}</style>
        </head>
        <body>
        """

        for msg in parsed_messages:
            html_output += f'<div class="message">{msg}</div>\n'

        html_output += """</body>
        </html>
        """

        html_output = HTMLBeautifier.beautify(html_output, 2)
        with open("output.html", "w") as fh:
            fh.write(html_output)


if __name__ == "__main__":
    main()
