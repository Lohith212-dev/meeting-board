"""Turn a Teams transcript (.docx or .vtt) into plain lines: `Speaker Name   m:ss  text`.

Usage: python extract_transcript.py "<transcript.docx|.vtt>" <out.txt>
Prints the number of speaker lines and the meeting length it found.
"""
import html
import re
import sys
import zipfile
from pathlib import Path


def from_docx(path):
    x = zipfile.ZipFile(path).read("word/document.xml").decode("utf8")
    paras = re.findall(r"<w:p[ >].*?</w:p>", x, flags=re.S)
    out = [html.unescape("".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", p))) for p in paras]
    return [o for o in out if o.strip()]


def from_vtt(path):
    lines, cur = [], None
    for raw in Path(path).read_text(encoding="utf8", errors="replace").splitlines():
        m = re.match(r"(\d+):(\d\d):(\d\d)\.\d+\s+-->", raw)
        if m:
            h, mi, s = map(int, m.groups())
            cur = f"{h}:{mi:02d}:{s:02d}" if h else f"{mi}:{s:02d}"
            continue
        v = re.match(r"<v ([^>]+)>(.*?)(</v>)?$", raw.strip())
        if v and cur:
            lines.append(f"{v.group(1)}   {cur}{html.unescape(v.group(2))}")
    return lines


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    lines = from_vtt(src) if src.suffix.lower() == ".vtt" else from_docx(src)
    out.write_text("\n".join(lines), encoding="utf8")
    speech = [l for l in lines if re.match(r"^(.+?)\s{2,}(\d+(?::\d+){1,2})", l)]
    last = re.match(r"^(.+?)\s{2,}(\d+(?::\d+){1,2})", speech[-1]).group(2) if speech else "?"
    print(f"{len(speech)} speaker lines, last timestamp {last}, saved to {out}")


if __name__ == "__main__":
    main()
