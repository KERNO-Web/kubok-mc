# v23 «Кто держит круг»: новые фото организаторов (вырезки без фона), огромный ник за спиной, на наведении второй кадр в цвете
p='index.html'; s=open(p).read()
def stage(key, name, lines, alt_a, alt_b):
    return (f'<div class="org__stage">\n          <h3 class="org__name" aria-label="{name}">' + '<br>'.join(lines) + '</h3>\n'
            f'          <img class="org__ph org__ph--a" src="assets/orgs/{key}-a.webp" alt="{alt_a}" loading="lazy">\n'
            f'          <img class="org__ph org__ph--b" src="assets/orgs/{key}-b.webp" alt="{alt_b}" loading="lazy">\n        </div>')
old_h='''        <img src="assets/bw/org-halloween.jpg" alt="Halloween" width="450" height="530" loading="lazy">
        <h3 class="org__name">Halloween</h3>'''
old_p='''        <img src="assets/bw/org-pohoronil.jpg" alt="МЦ Похоронил" width="500" height="625" loading="lazy">
        <h3 class="org__name">МЦ Похоронил</h3>'''
assert old_h in s and old_p in s
s=s.replace(old_h,'        '+stage('halloween','Halloween',['Halloween'],'Halloween','Halloween смеётся с микрофоном'))
s=s.replace(old_p,'        '+stage('pohoronil','МЦ Похоронил',['МЦ','Похоронил'],'МЦ Похоронил','МЦ Похоронил в кожаной куртке'))
s=s.replace('style.css?v=40','style.css?v=41')
open(p,'w').write(s)
p='style.css'; s=open(p).read()
s+='''
/* v23 Кто держит круг: вырезка человека поверх огромного ника (как лого за людьми на обложке), наведение = второй кадр в цвете */
.org__stage { position: relative; aspect-ratio: 6 / 5; overflow: hidden; isolation: isolate; background: radial-gradient(60% 70% at 50% 75%, #2b2420, #0c0a09 72%); }
.org__stage::after { content: ""; position: absolute; inset: 0; z-index: 3; pointer-events: none; background: var(--speck); opacity: .18; mix-blend-mode: screen; }
.org__stage .org__name { position: absolute; z-index: 0; inset: 5% 0 auto; margin: 0; text-align: center; font: 700 clamp(70px, 10.5vw, 200px)/.8 var(--disp); color: var(--accent); white-space: normal; transform: skewX(-8deg); transform-origin: 50% 50%; letter-spacing: -.01em; }
.org__ph { position: absolute; z-index: 1; bottom: 0; left: 50%; height: 90%; width: auto; max-width: none; aspect-ratio: auto; translate: -50% 0; object-fit: contain; filter: grayscale(1) contrast(1.12) brightness(.95) drop-shadow(0 0 40px rgba(0, 0, 0, .6)); transition: opacity .45s var(--ease), scale .6s var(--ease); transform-origin: 50% 100%; }
.org__ph--b { opacity: 0; scale: .97; filter: contrast(1.05) drop-shadow(0 0 40px rgba(0, 0, 0, .6)); }
.org:hover .org__ph--a { opacity: 0; scale: 1.02; }
.org:hover .org__ph--b { opacity: 1; scale: 1; }
.org__stage + .org__copy { margin-top: 0; }
'''
open(p,'w').write(s)
