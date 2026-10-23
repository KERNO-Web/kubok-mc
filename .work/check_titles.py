# сверка: настоящие заголовки роликов YouTube (oEmbed) для всех ID на сайте
import re, json, urllib.request
js=open('app.js').read()
ids=re.findall(r'\["([A-Za-z0-9_-]{11})", "([^"]*)"(?:, "([^"]*)")?\]', js)
out=[]
for vid, a, b in ids:
    site=(b or a)
    try:
        with urllib.request.urlopen(f'https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json', timeout=15) as r:
            t=json.load(r)['title']
    except Exception as e:
        t='ОШИБКА '+str(e)[:40]
    out.append(f'{vid} | сайт: {a}{" | "+b if b else ""}\n    YT: {t}')
print('\n'.join(out))
