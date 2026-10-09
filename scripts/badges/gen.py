#!/usr/bin/env python3
"""Generate rounded badge SVGs into assets/badges/. Needs Pillow for text measuring."""
import json, os, html
from PIL import ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', 'assets', 'badges')
ICONS = json.load(open(os.path.join(HERE, 'icons.json'), encoding='utf-8'))
FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
H, RX, SP = 28, 8, 0.8
WINDOWS = 'M0 3.4 9.8 2v9.4H0zM11 1.8 24 0v11.4H11zM0 12.6h9.8V22L0 20.6zM11 12.6h13V24L11 22.2z'

# (file, label, brand colour, icon key or None)
TECH = [
 ('cpp', 'C++', '00599C', 'cplusplus'), ('csharp', 'C#', '239120', None), ('c', 'C', 'A8B9CC', 'c'),
 ('assembly', 'Assembly', '1F1F1F', 'gnubash'), ('python', 'Python', '3776AB', 'python'),
 ('ruby', 'Ruby', 'CC342D', 'ruby'), ('javascript', 'JavaScript', 'F7DF1E', 'javascript'),
 ('java', 'Java', 'ED8B00', 'openjdk'), ('html5', 'HTML5', 'E34F26', 'html5'), ('php', 'PHP', '777BB4', 'php'),
 ('rust', 'Rust', '1F1F1F', 'rust'), ('wpf', 'WPF', '512BD4', 'dotnet'),
 ('avalonia', 'Avalonia', '8B44AC', 'avaloniaui'), ('qt', 'Qt', '41CD52', 'qt'), ('lua', 'Lua', '2C2D72', 'lua'),
 ('gdscript', 'GDScript', '478CBF', 'godotengine'), ('ghidra', 'Ghidra', 'E0115F', None),
 ('ida-pro', 'IDA Pro', '1E5AA8', None), ('cachyos', 'CachyOS', '1793D1', 'cachyos'),
 ('windows', 'Windows', '0078D4', 'WINDOWS'),
]
LINKS = [
 ('glitxh-tech', 'GLITXH.TECH', 'googlechrome'), ('discord', 'DISCORD', 'discord'), ('x', 'X', 'x'),
 ('youtube', 'YOUTUBE', 'youtube'), ('twitch', 'TWITCH', 'twitch'), ('nexusmods', 'NEXUSMODS', None),
 ('gamebanana', 'GAMEBANANA', 'gamebanana'), ('linkin-bio', 'LINKIN.BIO', 'linktree'),
]

def lum(h):
    r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return .2126 * r + .7152 * g + .0722 * b

def tw(t):
    return FONT.getlength(t) + SP * len(t)

def icon(key, x, fg):
    if not key:
        return ''
    d = WINDOWS if key == 'WINDOWS' else ICONS[key]
    return f'<path transform="translate({x} 7) scale({14/24})" fill="#{fg}" d="{d}"/>'

def badge(label, fill, fg, key, split=None):
    t = label.upper()
    pad, ic = 12, (14 + 8 if key else 0)
    w = round(pad + ic + tw(t) + pad)
    tx = pad + ic
    if split:  # grey icon segment + coloured label segment
        sw = pad + 14 + 10 if key else 0
        w = round(sw + 12 + tw(t) + 12)
        tx = sw + 12
        body = (f'<clipPath id="c"><rect width="{w}" height="{H}" rx="{RX}"/></clipPath><g clip-path="url(#c)">'
                f'<rect width="{w}" height="{H}" fill="#{fill}"/>'
                + (f'<rect width="{sw}" height="{H}" fill="#{split}"/>' if key else '') + '</g>')
        ico = icon(key, pad, fg)
    else:
        body = f'<rect width="{w}" height="{H}" rx="{RX}" fill="#{fill}"/>'
        ico = icon(key, pad, fg)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{H}" viewBox="0 0 {w} {H}" role="img" aria-label="{html.escape(label)}">'
            f'<title>{html.escape(label)}</title>{body}{ico}'
            f'<text x="{tx}" y="18.4" fill="#{fg}" font-family="Verdana,\'DejaVu Sans\',sans-serif" font-size="12" font-weight="700" '
            f'letter-spacing="{SP}" textLength="{tw(t) - SP:.1f}" lengthAdjust="spacingAndGlyphs">{html.escape(t)}</text></svg>')

os.makedirs(OUT, exist_ok=True)
for f, label, c, k in TECH:
    open(os.path.join(OUT, f + '.svg'), 'w', encoding='utf-8').write(badge(label, c, '111111' if lum(c) > .45 else 'FFFFFF', k))
for f, label, k in LINKS:
    open(os.path.join(OUT, f + '.svg'), 'w', encoding='utf-8').write(badge(label, 'E0115F', 'FFFFFF', k, split='6a6f79'))
print('wrote', len(TECH) + len(LINKS), 'badges')
