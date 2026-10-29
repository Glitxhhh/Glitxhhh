#!/usr/bin/env python3
"""Generate repo cards (assets/cards/) and account-wide stat badges (assets/badges/stat-*.svg).

Needs the GitHub CLI (`gh`) logged in. Run from anywhere: python scripts/cards/gen.py
"""
import html, json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', '..', 'assets')
CARDS = os.path.join(ASSETS, 'cards')
BADGES = os.path.join(ASSETS, 'badges')
OWNER = 'Glitxhhh'

# (owner/repo, description override or None to use the repo's own)
PINNED = [
    ('oogiefied/HubcapUI', None),
    ('Glitxhhh/YipYip-Recomp', 'Avatar: The Last Airbender (PS2) recompiled to C++.'),
    ('Glitxhhh/FortniteAFKXPMonitor', 'Cross-platform AFK XP tool for Fortnite (.NET + Avalonia).'),
    ('Glitxhhh/XenobladeChroniclesRecompiled', 'Windows port of the Xenoblade games via static recompilation.'),
    ('Glitxhhh/CachyAutoClicker', 'Native C++/Qt6 auto-clicker for Wayland using uinput.'),
    ('Glitxhhh/SRCWUnlocker', 'DLL-based unlocker for Sonic Racing CrossWorlds.'),
]
LANG_COLORS = {'C#': '#178600', 'C++': '#f34b7d', 'C': '#555555', 'Python': '#3572A5', 'Rust': '#dea584',
               'JavaScript': '#f1e05a', 'Java': '#b07219', 'Lua': '#000080', 'Ruby': '#701516', 'HTML': '#e34c26'}
PINK, BG, BORDER, TEXT, MUTED = '#E0115F', '#0d1117', '#30363d', '#c9d1d9', '#8b949e'
FONT = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
REPO_ICON = ('M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z')
STAR_ICON = ('M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.75.75 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1 .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Z')
FORK_ICON = ('M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z')


def gh(*args):
    out = subprocess.run(['gh', *args], capture_output=True, text=True, encoding='utf-8')
    return out.stdout if out.returncode == 0 else ''


def esc(s):
    return html.escape(s, quote=True)


def trunc(s, n):
    return s if len(s) <= n else s[:n - 1].rstrip() + '…'


def card(slug, info, desc):
    name = info['name']
    desc = trunc(desc or info.get('description') or 'No description provided', 62)
    lang = (info.get('primaryLanguage') or {}).get('name')
    x, items = 24, []
    if lang:
        items.append(f'<circle cx="{x + 5}" cy="96" r="5" fill="{LANG_COLORS.get(lang, MUTED)}"/>'
                     f'<text x="{x + 16}" y="100" fill="{TEXT}" font-size="12">{esc(lang)}</text>')
        x += 16 + len(lang) * 7 + 18
    for icon, count in ((STAR_ICON, info['stargazerCount']), (FORK_ICON, info['forkCount'])):
        if count:
            items.append(f'<path transform="translate({x} 88) scale(1)" fill="{PINK}" d="{icon}"/>'
                         f'<text x="{x + 20}" y="100" fill="{TEXT}" font-size="12">{count}</text>')
            x += 20 + len(str(count)) * 7 + 14
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="420" height="120" viewBox="0 0 420 120" role="img" aria-label="{esc(slug)}" font-family="{FONT}">'
            f'<title>{esc(slug)}</title>'
            f'<rect x="0.5" y="0.5" width="419" height="119" rx="10" fill="{BG}" stroke="{BORDER}"/>'
            f'<path transform="translate(24 20)" fill="{PINK}" d="{REPO_ICON}"/>'
            f'<text x="48" y="33" fill="{PINK}" font-size="17" font-weight="700">{esc(name)}</text>'
            f'<text x="24" y="65" fill="{TEXT}" font-size="12.5">{esc(desc)}</text>'
            + ''.join(items) + '</svg>')


def stat(label, value):
    label, value = label.upper(), f'{value:,}'
    lw, vw = 22 + len(label) * 9.2, 24 + len(value) * 9.6
    w = round(lw + vw)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="28" viewBox="0 0 {w} 28" role="img" aria-label="{esc(label)} {esc(value)}">'
            f'<title>{esc(label)} {esc(value)}</title>'
            f'<clipPath id="c"><rect width="{w}" height="28" rx="8"/></clipPath><g clip-path="url(#c)">'
            f'<rect width="{w}" height="28" fill="{PINK}"/><rect width="{lw:.0f}" height="28" fill="#6a6f79"/></g>'
            f'<g font-family="Verdana,\'DejaVu Sans\',sans-serif" font-size="12" font-weight="700" letter-spacing="0.8" fill="#FFFFFF">'
            f'<text x="12" y="18.4" textLength="{len(label) * 9.2 - 0.8:.1f}" lengthAdjust="spacingAndGlyphs">{esc(label)}</text>'
            f'<text x="{lw + 12:.0f}" y="18.4" textLength="{len(value) * 9.6 - 0.8:.1f}" lengthAdjust="spacingAndGlyphs">{esc(value)}</text></g></svg>')


def main():
    os.makedirs(CARDS, exist_ok=True)
    for slug, desc in PINNED:
        info = json.loads(gh('repo', 'view', slug, '--json', 'name,description,primaryLanguage,stargazerCount,forkCount') or '{}')
        if not info:
            print('skip (not found):', slug)
            continue
        with open(os.path.join(CARDS, info['name'] + '.svg'), 'w', encoding='utf-8') as f:
            f.write(card(slug, info, desc))
        print('card', info['name'])

    repos = json.loads(gh('repo', 'list', OWNER, '--limit', '200', '--visibility', 'public',
                          '--json', 'name,stargazerCount,forkCount') or '[]')
    downloads = 0
    for r in repos:
        rel = gh('api', f"repos/{OWNER}/{r['name']}/releases", '--paginate', '--jq', '[.[].assets[].download_count]|add // 0')
        downloads += sum(int(n) for n in rel.split() if n.isdigit())
    totals = {'repos': len(repos), 'stars': sum(r['stargazerCount'] for r in repos),
              'forks': sum(r['forkCount'] for r in repos), 'downloads': downloads}
    for key, value in totals.items():
        with open(os.path.join(BADGES, f'stat-{key}.svg'), 'w', encoding='utf-8') as f:
            f.write(stat(key, value))
    print('totals', totals)


if __name__ == '__main__':
    main()
