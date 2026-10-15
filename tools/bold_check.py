#!/usr/bin/env python3
"""List * and ** emphasis delimiters that GitHub (cmark-gfm) will not pair, per CommonMark's
flanking rules: an opener must be left-flanking (not followed by whitespace, and not followed by
punctuation unless preceded by whitespace/punctuation); a closer is the mirror image.
"Punctuation" is ASCII punctuation plus Unicode P* categories, as in cmark-gfm — symbols such as
¥ or → are not. This bites CJK copy, which has no spaces: **…）**です, *（注）*です and
これは**`code`**です all show literal asterisks.

Scope: this models GitHub's renderer, i.e. the wiki and the READMEs. The site's docs/ pages go
through kramdown, which is more lenient, so a failure here may still render there — fix it anyway,
since the wiki copy is the source. It is a lint, not a parser: openers and closers are told apart
by counting within each paragraph (blank-line-separated run), so a stray literal * or ** in a
paragraph shifts every later report in it. Fenced code, code spans, thematic breaks and list
bullets are skipped. Not handled (none occur in these docs): fences indented 4+ spaces or left
unclosed, escaped backticks, an escaped backslash before *, and runs of 4+ asterisks.
usage: tools/bold_check.py file..."""
import re, string, sys, unicodedata

def kind(c):
    if c == "" or c.isspace(): return "s"
    if c in string.punctuation or unicodedata.category(c).startswith("P"): return "p"
    return "l"

def blank(m):  # spaces, same length: offsets still match the source, and the lines read as blank
    return re.sub(r"[^\n]", " ", m.group(0))

bad = 0
for f in sys.argv[1:]:
    src = open(f, encoding="utf-8").read()
    text = re.sub(r"(?ms)^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[^\n]*$", blank, src)        # fenced blocks
    text = re.sub(r"(?m)^ {0,3}(?:\*[ \t]*){3,}$", blank, text)                    # thematic breaks
    # code spans (may wrap, but not across a blank line): keep the backticks, which are
    # punctuation to the flanking rules
    text = re.sub(r"(`+)((?:(?!\n[ \t]*\n)[^`])+?)\1",
                  lambda m: m.group(1) + re.sub(r"[^\n]", "x", m.group(2)) + m.group(1), text)
    for blk in re.finditer(r"(?:[^\n]*\S[^\n]*\n?)+", text):
        b0, body = blk.start(), blk.group(0)
        count = {1: 0, 2: 0}
        for m in re.finditer(r"(?<![\\*])\*+(?!\*)", body):
            i, run = m.start(), len(m.group(0))
            line_start = i == 0 or body[i-1] == "\n" or body[body.rfind("\n", 0, i)+1:i].strip(" \t>") == ""
            pre = body[i-1] if i else ""; post = body[m.end()] if m.end() < len(body) else ""
            if line_start and run == 1 and kind(post) == "s":
                continue                                    # a "* " list bullet
            b, a = kind(pre), kind(post)
            left = a != "s" and (a != "p" or b in "sp")
            right = b != "s" and (b != "p" or a in "sp")
            for size in ((1, 2) if run == 3 else (run,) if run in (1, 2) else ()):
                k = count[size]; count[size] += 1
                if (k % 2 == 0 and not left) or (k % 2 == 1 and not right):
                    bad += 1
                    at = b0 + i; n = text.count("\n", 0, at) + 1
                    ls = src.rfind("\n", 0, at) + 1; le = src.find("\n", at); le = len(src) if le < 0 else le
                    what = ("opener" if k % 2 == 0 else "closer") + (" (*)" if size == 1 else "")
                    print(f"{f}:{n}: {what} …{src[max(ls, at-14):min(le, at+14)].strip()}…")
sys.exit(1 if bad else 0)
