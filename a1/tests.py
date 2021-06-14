from html5lib import HTMLParser

parser = HTMLParser(strict=True)
with open("docs/index.html", "r") as f:
    document = parser.parse(f)
