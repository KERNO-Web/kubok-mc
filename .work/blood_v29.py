# v29: брызги крови (SVG) для «Пропали без вести»: основное пятно + капли + потёк, края рваные через feTurbulence
import random, math
def splat(seed):
    r=random.Random(seed)
    cx,cy=r.uniform(32,68), r.uniform(28,60)
    shapes=[]
    # ядро
    for _ in range(9):
        a=r.uniform(0,6.28); d=r.uniform(0,6)
        shapes.append(f'<circle cx="{cx+math.cos(a)*d:.1f}" cy="{cy+math.sin(a)*d:.1f}" r="{r.uniform(3,7.5):.1f}"/>')
    # лучи-брызги
    for _ in range(r.randint(10,15)):
        a=r.uniform(0,6.28); L=r.uniform(14,34)
        for k in range(3):
            t=L*(0.45+0.25*k)
            shapes.append(f'<circle cx="{cx+math.cos(a)*t:.1f}" cy="{cy+math.sin(a)*t:.1f}" r="{max(.8,4.2-k*1.3)*r.uniform(.6,1.2):.1f}"/>')
    # мелкие капли
    for _ in range(40):
        a=r.uniform(0,6.28); t=r.uniform(18,46)
        shapes.append(f'<circle cx="{cx+math.cos(a)*t:.1f}" cy="{cy+math.sin(a)*t:.1f}" r="{r.uniform(.5,2.2):.1f}"/>')
    # потёки вниз
    for _ in range(r.randint(1,3)):
        x=cx+r.uniform(-9,9); y=cy+r.uniform(4,9); h=r.uniform(14,34); w=r.uniform(1.6,3.2)
        shapes.append(f'<rect x="{x-w/2:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{w/2:.1f}"/><circle cx="{x:.1f}" cy="{y+h:.1f}" r="{w*0.85:.1f}"/>')
    g=''.join(shapes)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><filter id="f" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency=".09" numOctaves="2" seed="{seed}"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter><radialGradient id="g" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#5e0306"/><stop offset=".55" stop-color="#8f080d"/><stop offset="1" stop-color="#b3121a"/></radialGradient></defs><g filter="url(#f)" fill="url(#g)" opacity=".92">{g}</g></svg>'''
for i,seed in enumerate((11,23,37),1):
    open(f'assets/blood-{i}.svg','w').write(splat(seed))
print('ok')
