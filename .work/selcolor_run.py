# прогон выборочного цвета: фото организаторов + 12 кадров фона -> assets/sc/<имя>.webp
import subprocess, os, re
os.makedirs('assets/sc', exist_ok=True); os.makedirs('.work/sctmp', exist_ok=True)
items=[f'assets/orgs/{n}.webp' for n in ('halloween-a','pohoronil-a','h-01','h-02','h-03','h-07','p-01','p-02','p-04','p-06')]
html=open('index.html').read()
items+=sorted(set(re.findall(r'assets/krug/(?:svoboda|btb)/\d\d\.jpg', html.split('class="lower__bg"')[1].split('</div></div>')[0])))
for src in items:
    name=src.split('/')[-2]+'-'+os.path.splitext(os.path.basename(src))[0] if 'krug' in src else os.path.splitext(os.path.basename(src))[0]
    tmp=f'.work/sctmp/{name}.png'
    r=subprocess.run(['.work/selcolor',src,tmp],capture_output=True,text=True,check=True)
    subprocess.run(['cwebp','-quiet','-q','80','-alpha_q','90',tmp,'-o',f'assets/sc/{name}.webp'],check=True)
    print(name, r.stderr.strip())
