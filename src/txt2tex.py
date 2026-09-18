"""
plaintext asli (.txt) -> LaTeX, plus the source link
Usage: python src/txt2tex.py <plaintext.txt> <source-url> -o <output.tex>
"""

import argparse

SPECIALS = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
            "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}",
            "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
            '"': r"\textquotedbl{}", "'": r"\textquotesingle{}",
            "-": "-{}", "—": "---"}


def escape(line):
    line = line.replace("\\[", "[").replace("\\]", "]")
    return "".join(SPECIALS.get(c, c) for c in line)


def convert(text, url):
    out = [r"\begin{tcolorbox}[breakable, colback=white, colframe=black!80,",
           r"  boxrule=0.6pt, arc=0mm, left=3mm, right=3mm, top=2mm, bottom=2mm]",
           r"\ttfamily\small\raggedright"]
    for line in text.strip().split("\n"):
        line = line.strip()
        out.append(escape(line) + r"\par" if line else r"\medskip")
    out += [r"\bigskip",
            r"Sumber:\par",
            r"\hspace*{1.5em}- \url{%s}" % url.replace("%", r"\%"),
            r"\end{tcolorbox}"]
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("plaintext")
    ap.add_argument("url")
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()

    text = open(args.plaintext, encoding="utf-8").read()
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(convert(text, args.url))


if __name__ == "__main__":
    main()
