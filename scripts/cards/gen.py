#!/usr/bin/env python3
"""Generate repo cards (assets/cards/) and account-wide stat badges (assets/badges/stat-*.svg).

Needs the GitHub CLI (`gh`) logged in. Run from anywhere: python scripts/cards/gen.py
"""
import datetime, html, json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, '..', '..', 'assets')
CARDS = os.path.join(ASSETS, 'cards')
ACTIVITY = os.path.join(ASSETS, 'activity')
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


def fmt_date(d):
    return f"{d.strftime('%b')} {d.day}, {d.year}"


def fetch_activity():
    """Return profile counts + contribution days from GraphQL, or None if a query fails."""
    head = json.loads(gh('api', 'graphql', '-f', 'query=query{user(login:"%s"){createdAt followers{totalCount} '
                         'pullRequests{totalCount} issues{totalCount} '
                         'repositoriesContributedTo(first:1,contributionTypes:[COMMIT,ISSUE,PULL_REQUEST,REPOSITORY]){totalCount} '
                         'repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){nodes{languages(first:12,orderBy:{field:SIZE,direction:DESC}){edges{size node{name color}}}}}}}' % OWNER) or '{}')
    user = (head.get('data') or {}).get('user')
    if not user:
        return None
    first_year = int(user['createdAt'][:4])
    this_year = datetime.date.today().year
    parts = ' '.join(f'y{y}:contributionsCollection(from:"{y}-01-01T00:00:00Z",to:"{y}-12-31T23:59:59Z")'
                     '{contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}'
                     for y in range(first_year, this_year + 1))
    cal = json.loads(gh('api', 'graphql', '-f', 'query=query{user(login:"%s"){%s}}' % (OWNER, parts)) or '{}')
    cal = (cal.get('data') or {}).get('user')
    if not cal:
        return None
    days = {}
    for year in cal.values():
        for week in year['contributionCalendar']['weeks']:
            for d in week['contributionDays']:
                days[datetime.date.fromisoformat(d['date'])] = d['contributionCount']
    return {'user': user, 'days': days}


def streaks(days):
    today = datetime.date.today()
    best, best_range, run, start = 0, None, 0, None
    for d in sorted(d for d in days if d <= today):
        if days[d] > 0:
            if run == 0:
                start = d
            run += 1
            if run > best:
                best, best_range = run, (start, d)
        else:
            run = 0
    end = today if days.get(today, 0) > 0 else today - datetime.timedelta(days=1)
    cur, d = 0, end
    while days.get(d, 0) > 0:
        cur += 1
        d -= datetime.timedelta(days=1)
    cur_range = (end - datetime.timedelta(days=cur - 1), end) if cur else None
    return cur, cur_range, best, best_range


def frame(w, h, title, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}" font-family="{FONT}">'
            f'<title>{esc(label)}</title><rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="10" fill="{BG}" stroke="{BORDER}"/>'
            + (f'<text x="25" y="36" fill="{PINK}" font-size="18" font-weight="700">{esc(title)}</text>' if title else '')
            + body + '</svg>')


def stats_card(act, total_stars):
    u, days = act['user'], act['days']
    rows = [('Total Stars Earned', total_stars), ('Total Contributions', sum(days.values())),
            ('Pull Requests', u['pullRequests']['totalCount']), ('Issues', u['issues']['totalCount']),
            ('Repos Contributed To', u['repositoriesContributedTo']['totalCount']), ('Followers', u['followers']['totalCount'])]
    body = ''.join(f'<text x="25" y="{68 + i * 24}" fill="{TEXT}" font-size="14">{esc(label)}</text>'
                   f'<text x="460" y="{68 + i * 24}" fill="#ffffff" font-size="14" font-weight="700" text-anchor="end">{value:,}</text>'
                   for i, (label, value) in enumerate(rows))
    return frame(495, 215, f"{OWNER}'s GitHub Stats", body, 'GitHub stats')


def streak_card(act):
    days = act['days']
    today = datetime.date.today()
    total = sum(days.values())
    first = min((d for d, c in days.items() if c), default=today)
    cur, cur_range, best, best_range = streaks(days)

    def col(cx, big, label, sub, ring=False):
        out = ''
        if ring:
            out += (f'<circle cx="{cx}" cy="82" r="38" fill="none" stroke="#21262d" stroke-width="6"/>'
                    f'<circle cx="{cx}" cy="82" r="38" fill="none" stroke="{PINK}" stroke-width="6" stroke-linecap="round" stroke-dasharray="190 239" transform="rotate(-90 {cx} 82)"/>')
        out += (f'<text x="{cx}" y="{92 if ring else 90}" fill="#ffffff" font-size="{30 if ring else 28}" font-weight="700" text-anchor="middle">{big}</text>'
                f'<text x="{cx}" y="148" fill="{PINK if ring else TEXT}" font-size="14" font-weight="{700 if ring else 400}" text-anchor="middle">{esc(label)}</text>'
                f'<text x="{cx}" y="168" fill="{MUTED}" font-size="11" text-anchor="middle">{esc(sub)}</text>')
        return out

    rng = lambda r: f'{fmt_date(r[0])} - {fmt_date(r[1])}' if r else 'No streak'
    body = (col(85, f'{total:,}', 'Total Contributions', f'{fmt_date(first)} - Present')
            + col(247, cur, 'Current Streak', rng(cur_range), ring=True)
            + col(410, best, 'Longest Streak', rng(best_range)))
    return frame(495, 195, None, body, 'GitHub streak')


def langs_card(act):
    sizes, colors = {}, {}
    for repo in act['user']['repositories']['nodes']:
        repo_total = sum(e['size'] for e in repo['languages']['edges']) or 1
        for e in repo['languages']['edges']:
            sizes[e['node']['name']] = sizes.get(e['node']['name'], 0) + e['size'] / repo_total
            colors[e['node']['name']] = e['node']['color'] or MUTED
    total = sum(sizes.values()) or 1
    top = sorted(sizes.items(), key=lambda kv: -kv[1])[:6]
    body = ''
    for i, (name, size) in enumerate(top):
        y, pct = 60 + i * 30, size / total * 100
        body += (f'<text x="25" y="{y + 10}" fill="{TEXT}" font-size="13">{esc(name)}</text>'
                 f'<rect x="140" y="{y}" width="260" height="10" rx="5" fill="#21262d"/>'
                 f'<rect x="140" y="{y}" width="{max(260 * pct / 100, 4):.1f}" height="10" rx="5" fill="{colors[name]}"/>'
                 f'<text x="470" y="{y + 10}" fill="{MUTED}" font-size="13" text-anchor="end">{pct:.1f}%</text>')
    return frame(495, 60 + len(top) * 30 + 6, 'Top Languages (by repo)', body, 'Top languages')


def activity(total_stars):
    act = fetch_activity()
    if not act:
        print('activity: GraphQL failed, keeping existing cards')
        return
    os.makedirs(ACTIVITY, exist_ok=True)
    for name, svg in (('stats', stats_card(act, total_stars)), ('streak', streak_card(act)), ('languages', langs_card(act))):
        with open(os.path.join(ACTIVITY, name + '.svg'), 'w', encoding='utf-8') as f:
            f.write(svg)
    print('activity cards written')


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
    activity(totals['stars'])


if __name__ == '__main__':
    main()
