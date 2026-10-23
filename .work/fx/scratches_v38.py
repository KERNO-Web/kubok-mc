# v38: царапины для HUNT — короткие, тонкие, бледные, редкие. Три слоя: дерево (низ), бумага/фото (середина), верх (только ПК)
import random, math
def tile(name, size, n_scr, n_dust, colors, alpha, seed, length=(30, 140)):
    r = random.Random(seed); els = []
    for _ in range(n_scr):
        x, y = r.uniform(0, size), r.uniform(0, size)
        L = r.uniform(*length); ang = r.uniform(0, math.pi)  # любое направление, не только вертикаль
        dx, dy = math.cos(ang) * L, math.sin(ang) * L
        bend = r.uniform(-.18, .18) * L
        c = r.choice(colors); a = r.uniform(*alpha); w = r.uniform(.45, .95)
        els.append(f'<path d="M{x:.1f} {y:.1f} q{dx/2 - dy*bend/L:.1f} {dy/2 + dx*bend/L:.1f} {dx:.1f} {dy:.1f}" stroke="{c}" stroke-opacity="{a:.2f}" stroke-width="{w:.2f}" stroke-linecap="round" fill="none"/>')
        if r.random() < .35:  # короткий «отщеп» рядом — царапина выглядит живой
            els.append(f'<path d="M{x + dx*.6:.1f} {y + dy*.6:.1f} l{dx*.15 + r.uniform(-4,4):.1f} {dy*.15 + r.uniform(-4,4):.1f}" stroke="{c}" stroke-opacity="{a*.8:.2f}" stroke-width="{w*.8:.2f}" fill="none"/>')
    for _ in range(n_dust):
        els.append(f'<circle cx="{r.uniform(0,size):.1f}" cy="{r.uniform(0,size):.1f}" r="{r.uniform(.4,1.4):.2f}" fill="{r.choice(colors)}" fill-opacity="{r.uniform(*alpha):.2f}"/>')
    open(f'assets/fx/{name}.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">' + ''.join(els) + '</svg>')
tile('scratch-wood', 1100, 14, 30, ['#f3e2c4', '#f3e2c4', '#1a0f08'], (.12, .28), 11)
tile('scratch-paper', 620, 5, 14, ['#2b1d14', '#2b1d14', '#ffffff'], (.14, .3), 23, (24, 110))
tile('scratch-top', 1500, 6, 10, ['#ffffff', '#1a0f08'], (.1, .2), 37, (40, 150))
print('ok')
