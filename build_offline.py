#!/usr/bin/env python3
"""Build self-contained, offline, SAS-branded HTML from the APC docs markdown.

- No CDN / network calls: fonts fall back to system stacks, all CSS inlined.
- Admonitions, tables, fenced code + syntax highlighting rendered.
- All local .md links flattened to sibling .html (works as a flat folder or as
  individually downloaded files placed side-by-side).
- Vanilla-JS copy buttons on code blocks (offline).
"""
import re, os, sys, html
from pathlib import Path
import markdown
from pygments.formatters import HtmlFormatter

DOCS = Path(sys.argv[1])
OUT  = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

# --- source files in course order (from mkdocs.yml nav) -------------------
PAGES = [
    ("index.md",                         "Home"),
    ("lessons/lesson-01-foundations.md", "1. Foundations"),
    ("lessons/lesson-02-arduino-digital.md", "2. Board & Digital I/O"),
    ("lessons/lesson-03-arduino-analog.md",  "3. Analog, PWM & Serial"),
    ("lessons/lesson-04-arduino-sensors.md", "4. Sensors & Actuators"),
    ("lessons/lesson-05-arduino-project.md", "5. Arduino Mini-project"),
    ("lessons/lesson-06-pi-intro.md",   "6. Linux & Remote Access"),
    ("lessons/lesson-07-pi-gpio.md",    "7. Python, Thonny & GPIO"),
    ("lessons/lesson-08-pi-buses.md",   "8. ADC, I2C & SPI"),
    ("lessons/lesson-09-pi-project.md", "9. Pi Mini-project"),
    ("lessons/lesson-10-whisplay-intro.md", "10. Meet the HAT & LCD"),
    ("lessons/lesson-11-whisplay-io.md",    "11. Buttons, LED & Audio"),
    ("lessons/lesson-12-whisplay-game.md",  "12. Whisplay Game"),
    ("lessons/lesson-13-capstone-build.md", "13. Capstone Build"),
    ("lessons/lesson-14-capstone-demo.md",  "14. Capstone Demo"),
    ("appendix/raspberry-pi.md", "Appendix: Raspberry Pi"),
    ("appendix/arduino.md",      "Appendix: Arduino"),
    ("appendix/whisplay.md",     "Appendix: Whisplay"),
]

def out_name(src): return Path(src).name.replace(".md", ".html")

# --- link flattening: any local .md -> basename.html (+ anchor) -----------
def flatten_links(md_text):
    def repl(m):
        label, target = m.group(1), m.group(2)
        if re.match(r'^[a-z]+://', target) or target.startswith('#') or target.startswith('mailto:'):
            return m.group(0)
        anchor = ''
        if '#' in target:
            target, anchor = target.split('#', 1)
            anchor = '#' + anchor
        if target.endswith('.md'):
            target = Path(target).name[:-3] + '.html'
            return f'[{label}]({target}{anchor})'
        return m.group(0)
    return re.sub(r'\[([^\]]*)\]\(([^)]+)\)', repl, md_text)

# --- pygments CSS (dark, SAS code style) ----------------------------------
PYG_CSS = HtmlFormatter(style="monokai").get_style_defs('.codehilite')

FONT_DISPLAY = "'Barlow Condensed','Oswald','Arial Narrow',sans-serif"
FONT_BODY    = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"
FONT_MONO    = "'SF Mono',Menlo,Consolas,'Roboto Mono','Liberation Mono',monospace"

CSS = f"""
:root{{
  --sas-navy:#1B2A5E; --sas-crimson:#C8102E; --sas-gold:#F0B432;
  --sas-charcoal:#2C2C2C; --sas-gray:#F4F4F4; --sas-teal:#005F73; --sas-white:#fff;
}}
*{{box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{margin:0;font-family:{FONT_BODY};color:var(--sas-charcoal);
  background:var(--sas-gray);line-height:1.7;font-size:17px;}}
.wrap{{max-width:860px;margin:0 auto;background:var(--sas-white);
  min-height:100vh;box-shadow:0 0 40px rgba(0,0,0,.06);}}
/* Banner */
.banner{{background:var(--sas-navy);border-bottom:3px solid var(--sas-gold);
  padding:18px 40px;display:flex;align-items:center;justify-content:space-between;gap:16px;}}
.sas-logo-box{{display:inline-flex;flex-direction:column;border:2px solid #fff;
  padding:6px 12px;font-family:{FONT_DISPLAY};font-weight:700;font-size:13px;
  letter-spacing:.22em;text-transform:uppercase;line-height:1.25;color:#fff;position:relative;}}
.sas-logo-sub{{position:absolute;bottom:-2px;right:-2px;border:2px solid #fff;
  padding:1px 6px;font-size:8px;letter-spacing:.18em;background:var(--sas-navy);line-height:1.5;}}
.banner .course{{color:#fff;font-family:{FONT_DISPLAY};text-transform:uppercase;
  letter-spacing:.12em;font-size:15px;text-align:right;opacity:.92;}}
.banner .course b{{color:var(--sas-gold);font-weight:700;}}
/* Content */
.content{{padding:34px 40px 60px;}}
.content h1{{font-family:{FONT_DISPLAY};text-transform:uppercase;color:var(--sas-navy);
  font-weight:700;font-size:34px;letter-spacing:.02em;line-height:1.12;
  border-top:3px solid var(--sas-gold);padding-top:18px;margin:.2em 0 .6em;}}
.content h2{{font-family:{FONT_DISPLAY};text-transform:uppercase;color:var(--sas-navy);
  font-weight:700;font-size:24px;letter-spacing:.03em;margin:1.7em 0 .5em;
  padding-bottom:6px;border-bottom:2px solid #e3e6ef;}}
.content h3{{font-family:{FONT_BODY};color:var(--sas-teal);font-weight:700;
  text-transform:uppercase;letter-spacing:.06em;font-size:15px;margin:1.5em 0 .4em;}}
.content h4{{color:var(--sas-navy);font-size:16px;margin:1.3em 0 .3em;}}
.content a{{color:var(--sas-crimson);text-decoration:none;border-bottom:1px solid rgba(200,16,46,.35);}}
.content a:hover{{border-bottom-color:var(--sas-crimson);}}
blockquote{{margin:1.2em 0;padding:.6em 1.1em;background:var(--sas-gray);
  border-left:4px solid var(--sas-gold);color:#444;font-style:italic;}}
blockquote p{{margin:.3em 0;}}
hr{{border:0;border-top:2px solid #e3e6ef;margin:2em 0;}}
/* Tables */
table{{border-collapse:collapse;width:100%;margin:1.3em 0;font-size:15.5px;}}
th{{background:var(--sas-navy);color:var(--sas-gold);font-family:{FONT_BODY};
  text-transform:uppercase;letter-spacing:.05em;font-size:12.5px;text-align:left;
  padding:9px 12px;}}
td{{padding:8px 12px;border-bottom:1px solid #e7e9f0;vertical-align:top;}}
tr:nth-child(even) td{{background:var(--sas-gray);}}
/* Inline + block code */
code{{font-family:{FONT_MONO};font-size:.9em;background:#eef0f6;color:#22245e;
  padding:.12em .4em;border-radius:0;}}
pre{{position:relative;margin:1.3em 0;}}
.codehilite,pre>code{{display:block;background:#1a1a2e;color:#f2f2f2;
  border-top:3px solid var(--sas-gold);padding:16px 18px;overflow:auto;
  font-family:{FONT_MONO};font-size:14px;line-height:1.55;}}
.codehilite code{{background:none;color:inherit;padding:0;}}
.codehilite pre{{margin:0;}}
.copy-btn{{position:absolute;top:8px;right:8px;background:rgba(255,255,255,.1);
  color:#fff;border:1px solid rgba(255,255,255,.25);font-family:{FONT_BODY};
  font-size:11px;letter-spacing:.08em;text-transform:uppercase;padding:3px 9px;
  cursor:pointer;z-index:2;}}
.copy-btn:hover{{background:var(--sas-crimson);border-color:var(--sas-crimson);}}
{PYG_CSS}
/* Admonitions */
.admonition{{margin:1.4em 0;border:1px solid #e0e3ec;border-left-width:5px;
  background:#fafbfe;padding:0 16px 12px;}}
.admonition-title{{font-family:{FONT_BODY};font-weight:700;text-transform:uppercase;
  letter-spacing:.05em;font-size:13px;margin:0 -16px 8px;padding:9px 16px;
  background:#eef1f8;color:var(--sas-navy);}}
.admonition.note{{border-left-color:var(--sas-teal);}}
.admonition.note .admonition-title{{background:#e4f0f2;color:var(--sas-teal);}}
.admonition.tip,.admonition.hint{{border-left-color:#1f9d55;}}
.admonition.tip .admonition-title,.admonition.hint .admonition-title{{background:#e4f4ea;color:#1f7a45;}}
.admonition.warning,.admonition.caution{{border-left-color:var(--sas-gold);}}
.admonition.warning .admonition-title,.admonition.caution .admonition-title{{background:#fdf3dc;color:#8a6400;}}
.admonition.danger,.admonition.error{{border-left-color:var(--sas-crimson);}}
.admonition.danger .admonition-title,.admonition.error .admonition-title{{background:#fbe4e7;color:var(--sas-crimson);}}
.admonition>p:last-child{{margin-bottom:0;}}
details.admonition{{padding-bottom:0;}}
details.admonition>.admonition-title{{cursor:pointer;margin-bottom:0;}}
details[open].admonition>.admonition-title{{margin-bottom:8px;}}
img{{max-width:100%;height:auto;}}
/* Offline notice + nav */
.offline-note{{background:#fdf3dc;border:1px solid var(--sas-gold);border-left:5px solid var(--sas-gold);
  padding:10px 16px;font-size:14px;margin:0 0 12px;color:#6b5108;}}
.dl-bar{{display:flex;gap:10px;flex-wrap:wrap;margin:0 0 22px;}}
.dl-btn{{font-family:{FONT_BODY};font-size:13px;font-weight:700;text-transform:uppercase;
  letter-spacing:.06em;padding:9px 16px;border:1px solid var(--sas-navy);background:#fff;
  color:var(--sas-navy);cursor:pointer;text-decoration:none;display:inline-block;line-height:1;}}
.dl-btn:hover{{background:var(--sas-navy);color:#fff;border-bottom-color:var(--sas-navy);}}
.dl-btn.primary{{background:var(--sas-crimson);border-color:var(--sas-crimson);color:#fff;}}
.dl-btn.primary:hover{{background:#a30d26;border-color:#a30d26;}}
.pagenav{{display:flex;justify-content:space-between;gap:12px;margin:36px 0 0;
  border-top:2px solid #e3e6ef;padding-top:18px;flex-wrap:wrap;}}
.pagenav a{{flex:1;min-width:160px;border:1px solid #d7dae6;padding:10px 14px;
  text-decoration:none;border-bottom:1px solid #d7dae6;color:var(--sas-navy);
  font-size:14px;background:#fff;}}
.pagenav a:hover{{border-color:var(--sas-navy);}}
.pagenav .lbl{{display:block;font-size:11px;text-transform:uppercase;letter-spacing:.08em;
  color:#999;margin-bottom:2px;}}
.pagenav .next{{text-align:right;}}
footer.sas{{background:var(--sas-navy);color:#c7cde4;padding:16px 40px;
  font-size:12px;letter-spacing:.04em;text-align:center;border-top:3px solid var(--sas-gold);}}
footer.sas b{{color:var(--sas-gold);}}
@media(max-width:640px){{.banner,.content,footer.sas{{padding-left:20px;padding-right:20px;}}}}
@media print{{body{{background:#fff;}}.wrap{{box-shadow:none;max-width:100%;}}.copy-btn{{display:none;}}}}
"""

ZIP_NAME = "APC-Semester1-Offline.zip"

PAGE_JS = """
// Copy buttons (idempotent — safe if markup already contains one)
document.querySelectorAll('pre').forEach(function(pre){
  if(pre.querySelector('.copy-btn'))return;
  var b=document.createElement('button');b.className='copy-btn';b.textContent='Copy';
  b.addEventListener('click',function(){
    var code=pre.querySelector('code')||pre;
    navigator.clipboard.writeText(code.innerText).then(function(){b.textContent='Copied';
      setTimeout(function(){b.textContent='Copy';},1500);});
  });
  pre.appendChild(b);
});
// Save this single self-contained page to the student's laptop
function downloadThisLesson(){
  var html='<!DOCTYPE html>\\n'+document.documentElement.outerHTML;
  var blob=new Blob([html],{type:'text/html;charset=utf-8'});
  var a=document.createElement('a');
  a.href=URL.createObjectURL(blob);
  a.download=(location.pathname.split('/').pop()||'lesson.html');
  document.body.appendChild(a);a.click();
  setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},1000);
}
"""

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — Advanced Physical Computing</title>
<style>{css}</style>
</head>
<body>
<div class="wrap">
  <header class="banner">
    <span class="sas-logo-box">SHANGHAI<br>AMERICAN<br>SCHOOL<span class="sas-logo-sub">PX</span></span>
    <span class="course">Advanced Physical<br><b>Computing</b> · 2026&ndash;27</span>
  </header>
  <main class="content">
    <div class="offline-note">Offline copy for download. The live version with search lives on the course GitHub site.</div>
    <div class="dl-bar">
      <button class="dl-btn primary" onclick="downloadThisLesson()">&#8681; Download this lesson</button>
      <a class="dl-btn" href="{zip}" download>&#8681; Download whole course (.zip)</a>
    </div>
    {body}
    {pagenav}
  </main>
  <footer class="sas">Shanghai American School &middot; Puxi High School &middot; <b>Advanced Physical Computing</b> &middot; Semester 1, 2026&ndash;27</footer>
</div>
<script>{js}</script>
</body>
</html>
"""

EXTS = ['admonition','pymdownx.details','fenced_code','codehilite',
        'pymdownx.inlinehilite','attr_list','md_in_html','tables','toc']
EXT_CFG = {'codehilite': {'guess_lang': False, 'css_class': 'codehilite'}}

def build_pagenav(i):
    parts = []
    if i > 0:
        s,t = PAGES[i-1]
        parts.append(f'<a class="prev" href="{out_name(s)}"><span class="lbl">&larr; Previous</span>{html.escape(t)}</a>')
    else:
        parts.append('<span style="flex:1"></span>')
    if i < len(PAGES)-1:
        s,t = PAGES[i+1]
        parts.append(f'<a class="next" href="{out_name(s)}"><span class="lbl">Next &rarr;</span>{html.escape(t)}</a>')
    return '<nav class="pagenav">' + ''.join(parts) + '</nav>'

count = 0
for i,(src,title) in enumerate(PAGES):
    p = DOCS / src
    text = flatten_links(p.read_text(encoding='utf-8'))
    md = markdown.Markdown(extensions=EXTS, extension_configs=EXT_CFG)
    body = md.convert(text)
    out_file = OUT / out_name(src)
    out_file.write_text(TEMPLATE.format(title=html.escape(title), css=CSS, body=body,
                        pagenav=build_pagenav(i), js=PAGE_JS, zip=ZIP_NAME), encoding='utf-8')
    count += 1
    print(f"  {src:45s} -> {out_name(src)}")

# --- bundle every page into the whole-course zip --------------------------
# Build in a scratch path, then overwrite bytes in place: the Schoology mount
# blocks unlink/rename, so zip's default temp-file swap fails — direct write works.
import zipfile, tempfile
tmp_zip = os.path.join(tempfile.gettempdir(), ZIP_NAME)
with zipfile.ZipFile(tmp_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(OUT.glob("*.html")):
        z.write(f, f.name)
with open(OUT / ZIP_NAME, 'wb') as dst:
    dst.write(open(tmp_zip, 'rb').read())
print(f"  {'(bundle)':45s} -> {ZIP_NAME}")
print(f"Done: {count} HTML files + 1 zip -> {OUT}")
