#!/usr/bin/env python3
"""Refresh SEO metadata, sitemap, and public Markdown mirrors from the site.

Run from any directory with Python 3. Dates describe this editorial update;
article publication dates are retained from their existing structured data.
"""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin
from html import escape, unescape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://imdennie.com/'
UPDATED = '2026-09-23'
FILES = ['index.html', 'story.html', 'approach.html', 'resume.html',
         'case/numi.html', 'case/tysha.html', 'case/karta.html',
         'blog/index.html'] + [str(p.relative_to(ROOT)) for p in sorted((ROOT / 'blog').glob('*.html')) if p.name != 'index.html']
DESCRIPTIONS = {
    'index.html': 'Dennie Ordynskyi is a product designer at DraftKings and the creator of Numi, Tysha, and Karta. Explore his work, approach, and writing.',
    'story.html': 'From Ukraine to products used by millions: the story of Dennie Ordynskyi, a product designer at DraftKings and the creator of three independent products.',
    'approach.html': 'How Dennie Ordynskyi designs products: understand the problem, prototype early, simplify complex experiences, and follow the idea through to launch.',
    'resume.html': 'Dennie Ordynskyi’s résumé: 14+ years in product design, experience at DraftKings, and the design and launch of Numi, Tysha, and Karta.',
    'case/numi.html': 'How Dennie Ordynskyi designed and launched Numi, an AI nutrition app for iPhone. Explore photo logging, product decisions, and the App Store release.',
    'case/tysha.html': 'Designing Tysha, a baby-sleep sound app for one-handed use at 3 a.m. A case study in calm interfaces, offline audio, and shipping an iPhone app solo.',
    'case/karta.html': 'Designing Karta, a QR ordering and payment platform for restaurants. Explore the guest experience, owner dashboard, and product decisions.',
    'blog/index.html': 'Notes by Dennie Ordynskyi on product design, AI interfaces, design careers, and building independent apps from idea to launch.',
    'blog/how-to-become-a-product-designer.html': 'How to become a product designer in 2026: practical advice on skills, portfolios, first jobs, and AI from a designer with 14+ years of experience.',
    'blog/shipping-apps-solo-with-ai.html': 'What changed when a product designer built and shipped Numi and Tysha solo with AI: prototyping, iteration, and the design work that still matters.',
    'blog/designing-ai-products.html': 'Six lessons from designing Numi, an AI nutrition app: uncertainty, latency, correction, trust, and interfaces for probabilistic products.',
    'blog/ai-product-design.html': 'Designing AI products for the cost of being wrong: correction paths, draft states, output length, and lessons from shipping real products.',
    'blog/ux-for-machine-learning-the-interface-is-a-measuring-device.html': 'How interface design shapes what machine learning systems learn: correction paths, checkability, and knowing when to show nothing.',
    'blog/ai-ux-patterns-that-survive-contact-with-a-real-model.html': 'Seven AI UX patterns from shipping Numi: correction-first results, useful waiting states, deterministic scores, and knowing when to stay silent.',
}

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta = {}; self.title = ''; self.in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta': self.meta[a.get('name', a.get('property', ''))] = a.get('content', '')
        if tag == 'title': self.in_title = True
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title += data

def canonical(path):
    return BASE + ('' if path == 'index.html' else 'blog/' if path == 'blog/index.html' else path)

person = {
    '@type': 'Person', '@id': BASE + '#person', 'name': 'Dennie Ordynskyi',
    'alternateName': 'Denys Ordynskyi', 'url': BASE,
    'image': BASE + 'dist/img/hero/dennie-hero.png', 'jobTitle': 'Product Designer',
    'description': 'Product designer at DraftKings and creator of Numi, Tysha, and Karta, based in Kyiv, Ukraine.',
    'worksFor': {'@type': 'Organization', 'name': 'DraftKings'},
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Kyiv', 'addressCountry': 'UA'},
    'knowsLanguage': ['Ukrainian', 'English', 'Russian'],
    'knowsAbout': ['Product design', 'User experience design', 'Design systems', 'AI product design', 'Mobile and web applications'],
    'sameAs': ['https://www.linkedin.com/in/dennieo/'],
}
website = {'@type': 'WebSite', '@id': BASE + '#website', 'name': 'Dennie Ordynskyi', 'url': BASE,
           'publisher': {'@id': BASE + '#person'}, 'inLanguage': 'en'}
records = []
favicon = re.search(r'<link\b[^>]*rel="icon"[^>]*>', (ROOT / 'index.html').read_text(), re.S)[0]
for path in FILES:
    file = ROOT / path; text = file.read_text(); head, body = text.split('</head>', 1)
    meta = Metadata(); meta.feed(head)
    title = meta.title.strip(); desc = DESCRIPTIONS.get(path, meta.meta.get('description', ''))
    url = canonical(path)
    old_schema = [json.loads(x) for x in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', head, re.S)]
    old_nodes = [n for s in old_schema for n in s.get('@graph', [s])]
    article = next((n for n in old_nodes if n.get('@type') in ['Article', 'BlogPosting']), None)
    is_article = article is not None
    image = BASE + 'dist/img/social/portfolio.jpg'; width, height = 1280, 720
    image_alt = 'Dennie Ordynskyi — product designer and builder, portfolio homepage'
    if path.startswith('case/'):
        name = Path(path).stem; image = BASE + f'dist/img/social/{name}.jpg'; width, height = 1340, 1174
        image_alt = f'{name.title()} product overview — case study by Dennie Ordynskyi'
    elif path == 'blog/how-to-become-a-product-designer.html':
        image = BASE + 'dist/img/blog/how-to-become-a-product-designer.jpg'; width, height = 1600, 900
        image_alt = 'How to become a product designer — article by Dennie Ordynskyi'
    elif (ROOT / 'blog/cards' / (Path(path).stem + '.png')).exists():
        image = BASE + 'blog/cards/' + Path(path).stem + '.png'; width, height = 1200, 630
        image_alt = title
    elif path in ['blog/shipping-apps-solo-with-ai.html', 'blog/designing-ai-products.html']:
        image = BASE + 'dist/img/social/numi.jpg'; width, height = 1340, 1174
        image_alt = 'Numi, the iPhone nutrition app designed and built by Dennie Ordynskyi'

    webpage_type = 'ProfilePage' if path in ['index.html', 'story.html', 'resume.html'] else 'CollectionPage' if path == 'blog/index.html' else 'WebPage'
    webpage = {'@type': webpage_type, '@id': url + '#webpage', 'url': url, 'name': title,
               'description': desc, 'inLanguage': 'en', 'dateModified': UPDATED,
               'isPartOf': {'@id': BASE + '#website'}, 'about': {'@id': BASE + '#person'},
               'primaryImageOfPage': {'@type': 'ImageObject', 'url': image, 'width': width, 'height': height}}
    nodes = [person, website, webpage]
    if webpage_type == 'ProfilePage': webpage['mainEntity'] = {'@id': BASE + '#person'}
    if article:
        article = dict(article); article.pop('@context', None)
        article.pop('creator', None)
        article.update({'@id': url + '#article', 'url': url, 'description': desc, 'image': image,
                        'author': {'@id': BASE + '#person'}, 'publisher': {'@id': BASE + '#person'},
                        'mainEntityOfPage': {'@id': url + '#webpage'}, 'inLanguage': 'en'})
        article['isPartOf'] = {'@id': BASE + ('blog/#blog' if path.startswith('blog/') else '#website')}
        if path in ['case/numi.html', 'case/tysha.html']: article['dateModified'] = UPDATED
        webpage['mainEntity'] = {'@id': url + '#article'}; nodes.append(article)
    if path == 'blog/index.html':
        nodes.append({'@type': 'Blog', '@id': BASE + 'blog/#blog', 'url': BASE + 'blog/', 'name': title,
                      'description': desc, 'author': {'@id': BASE + '#person'}, 'inLanguage': 'en',
                      'blogPost': [{'@id': canonical(p) + '#article'} for p in FILES if p.startswith('blog/') and p != path]})
        webpage['mainEntity'] = {'@id': BASE + 'blog/#blog'}
    if path != 'index.html':
        crumbs = [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': BASE}]
        if path.startswith('case/'):
            crumbs.append({'@type': 'ListItem', 'position': 2, 'name': 'Work', 'item': BASE + '#work'})
        elif path.startswith('blog/') and path != 'blog/index.html':
            crumbs.append({'@type': 'ListItem', 'position': 2, 'name': 'Writing', 'item': BASE + 'blog/'})
        crumbs.append({'@type': 'ListItem', 'position': len(crumbs) + 1, 'name': title.split(' — ')[0], 'item': url})
        nodes.append({'@type': 'BreadcrumbList', '@id': url + '#breadcrumbs', 'itemListElement': crumbs})
        webpage['breadcrumb'] = {'@id': url + '#breadcrumbs'}

    def strip_meta(match):
        parser = Metadata(); parser.feed(match[0]); key = next(iter(parser.meta), '')
        return '' if key in ['description', 'robots', 'theme-color'] or key.startswith(('og:', 'twitter:', 'article:')) else match[0]
    head = re.sub(r'<meta\b[^>]*>', strip_meta, head, flags=re.S)
    head = re.sub(r'<script[^>]*type="application/ld\+json"[^>]*>.*?</script>', '', head, flags=re.S)
    head = re.sub(r'<link\b[^>]*rel="(?:canonical|describedby|alternate)"[^>]*>', '', head, flags=re.S)
    head = re.sub(r'<noscript>\s*</noscript>', '', head)
    head = re.sub(r'<!-- (?:No-FOUC.*?|Open Graph / Twitter|Shared portfolio controls;.*?) -->', '', head)
    # Use one consistent favicon and analytics initialization on every page.
    head = re.sub(r'<link\b[^>]*rel="icon"[^>]*>', '', head, flags=re.S)
    seen_analytics = [False]
    def dedupe_analytics(match):
        if "gtag('config'" not in match[0]: return match[0]
        if seen_analytics[0]: return ''
        seen_analytics[0] = True
        return match[0]
    head = re.sub(r'<script\b[^>]*>.*?</script>', dedupe_analytics, head, flags=re.S)
    def tag(key, value, prop=False):
        return f'    <meta {"property" if prop else "name"}="{key}" content="{escape(str(value), quote=True)}" />'
    block = [favicon, tag('description', desc), tag('robots', 'index, follow, max-image-preview:large'), tag('theme-color', '#ffffff'),
             f'    <link rel="canonical" href="{url}" />',
             '    <link rel="describedby" href="/llms.txt" type="text/plain" />',
             f'    <link rel="alternate" type="text/markdown" href="/{path}.md" title="Markdown version" />']
    for key, val in {'type': 'article' if is_article else 'website', 'site_name': 'Dennie Ordynskyi', 'locale': 'en_US',
                     'title': title, 'description': desc, 'url': url, 'image': image, 'image:width': width,
                     'image:height': height, 'image:type': 'image/png' if image.endswith('.png') else 'image/jpeg', 'image:alt': image_alt}.items():
        block.append(tag('og:' + key, val, True))
    for key, val in {'card': 'summary_large_image', 'title': title, 'description': desc, 'image': image, 'image:alt': image_alt}.items():
        block.append(tag('twitter:' + key, val))
    if article:
        for key, field in [('published_time', 'datePublished'), ('modified_time', 'dateModified')]:
            if article.get(field): block.append(tag('article:' + key, article[field], True))
    block.append('    <script type="application/ld+json">\n' + json.dumps({'@context': 'https://schema.org', '@graph': nodes}, ensure_ascii=False, indent=2) + '\n    </script>')
    head = re.sub(r'\n\s*\n', '\n\n', head).rstrip()
    text = head + '\n' + '\n'.join(block) + '\n  </head>' + body
    text = re.sub(r'(/?dist/open-studio/style\.css)\?v=[^"\s]+', r'\1?v=20260923-pointer', text)
    text = re.sub(r'/dist/open-studio/pages.css\?v=[^"\s]+', '/dist/open-studio/pages.css?v=20260923-tysha-device', text)
    file.write_text('\n'.join(line.rstrip() for line in text.splitlines()) + '\n')
    records.append((path, url, title, desc))

class Markdown(HTMLParser):
    """Export visible main content only; preserve destinations and headings."""
    def __init__(self, url):
        super().__init__(); self.url = url; self.active = False; self.parts = []; self.links = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'main': self.active = True
        if not self.active: return
        if tag in ['script', 'style', 'svg']: self.skip += 1
        if self.skip: return
        if tag in ['h1', 'h2', 'h3', 'h4']: self.parts.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag in ['p', 'section', 'article', 'div', 'ul', 'ol', 'figure', 'dl']: self.parts.append('\n\n')
        elif tag == 'li': self.parts.append('\n- ')
        elif tag == 'br': self.parts.append(' ')
        elif tag == 'a': self.parts.append('['); self.links.append(urljoin(self.url, a.get('href', '')))
        elif tag == 'img' and a.get('alt'): self.parts.append('\n\n![' + a['alt'] + '](' + urljoin(self.url, a.get('src', '')) + ')\n\n')
        elif tag in ['strong', 'b']: self.parts.append('**')
    def handle_endtag(self, tag):
        if tag == 'main': self.active = False
        if not self.active: return
        if tag in ['script', 'style', 'svg']: self.skip = max(0, self.skip - 1); return
        if self.skip: return
        if tag == 'a' and self.links: self.parts.append('](' + self.links.pop() + ')')
        elif tag in ['strong', 'b']: self.parts.append('**')
        elif tag == 'dt': self.parts.append(': ')
        elif tag == 'span': self.parts.append(' ')
        elif tag in ['p', 'h1', 'h2', 'h3', 'h4', 'dd', 'section', 'article', 'div', 'ul', 'ol', 'figure']: self.parts.append('\n\n')
    def handle_data(self, data):
        if self.active and not self.skip: self.parts.append(re.sub(r'\s+', ' ', data))

full = ['# Dennie Ordynskyi — public website content', f'Updated: {UPDATED}. Generated from the public HTML pages; canonical URLs are listed for each page.']
for path, url, title, desc in records:
    parser = Markdown(url); parser.feed((ROOT / path).read_text())
    content = ''.join(parser.parts)
    content = re.sub(r' *\n *', '\n', content); content = re.sub(r'\n{3,}', '\n\n', content).strip()
    content = re.sub(r'\[\s+(!\[.*?\]\(.*?\))\s+\]\((.*?)\)', r'[\1](\2)', content)
    doc = f'Source: {url}\n\nUpdated: {UPDATED}\n\n{content}\n'
    (ROOT / (path + '.md')).write_text(doc)
    full.append(f'## {title}\n\n{doc}')
(ROOT / 'llms-full.txt').write_text('\n\n---\n\n'.join(full) + '\n')

intro = f'''# Dennie Ordynskyi

> Product designer at DraftKings and creator of Numi, Tysha, and Karta. Based in Kyiv, Ukraine, with 14+ years of experience designing mobile and web products.

Updated: {UPDATED}. Dennie (also known as Denys Ordynskyi) designs and builds independent products from idea to launch. Numi is released on the App Store. Tysha is also available on the App Store; Karta is a live restaurant ordering and payment web platform. He is open to senior product design roles and select collaborations, working with teams in the US and Europe.

This index links to Markdown versions of the public website. Each document identifies its canonical HTML source. The case studies explain project decisions; the résumé contains the career history. Original article publication dates remain in the HTML metadata.

## Profile and approach
'''
lines = [intro]
for path, url, title, desc in records:
    if not path.startswith(('case/', 'blog/')): lines.append(f'- [{title}]({BASE}{path}.md): {desc}')
lines.append('\n## Case studies\n')
for path, url, title, desc in records:
    if path.startswith('case/'): lines.append(f'- [{title}]({BASE}{path}.md): {desc}')
lines.append('\n## Writing\n')
for path, url, title, desc in records:
    if path.startswith('blog/'): lines.append(f'- [{title}]({BASE}{path}.md): {desc}')
lines.append('''
## Products and contact

- [Numi](https://getnumi.app): Released iPhone nutrition app with photo-based meal logging, macros, micronutrients, insights, and fasting.
- [Tysha](https://tyshaapp.com): Baby-sleep sound app with real-time noise mixing, saved Rooms, and a fading sleep timer; works offline without accounts or ads.
- [Karta](https://karta-nu.vercel.app/): QR ordering and payments for restaurants, with a guest menu and an owner dashboard.
- [Linc project](https://imdennie.com/#linc): Cloud studio platform for content creators; Dennie was the founding product designer.
- [Earlier work](https://imdennie.com/#track-record): MyGoTrainer, Shipshape, Chatbox, and e-commerce project galleries.
- [LinkedIn](https://www.linkedin.com/in/dennieo/): Professional profile.
- [Contact](https://imdennie.com/#contact): Senior product design roles and select collaborations.

## Optional

- [Complete public website text](https://imdennie.com/llms-full.txt): Combined Markdown content from all public pages.
- [Sitemap](https://imdennie.com/sitemap.xml): Canonical HTML pages for crawlers.
''')
(ROOT / 'llms.txt').write_text('\n'.join(lines).strip() + '\n')
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for path, url, title, desc in records:
    sitemap.append(f'  <url><loc>{escape(url)}</loc><lastmod>{UPDATED}</lastmod></url>')
sitemap.append('</urlset>')
(ROOT / 'sitemap.xml').write_text('\n'.join(sitemap) + '\n')
print(f'Updated metadata, structured data, sitemap, and Markdown mirrors for {len(records)} pages.')
