import json,re,glob,sys
sys.path.insert(0,'.')
from lex import lex
import os
D=os.path.dirname(os.path.abspath(__file__)); os.chdir(D)
SRC=os.path.join(D,'../../index.html'); OUT=os.path.join(D,'../../en.html')
h=open(SRC,encoding='utf-8').read()
c=json.load(open('cand.json')); M={}
for f in sorted(glob.glob('tr/b*.json')):
  for k,v in json.load(open(f)).items(): M[c[int(k.strip())]]=v
M.update(json.load(open('tr2.json')))
M.update({'brak wpływu – bez chwały':'no influence – no glory','<p class="an">Brak kart imperialnych na ręce – zamiast karty tracisz 3 punkty kultury.</p><div class="row"><button class="btn primary" id="lsNone">−3 kultury</button></div>':'<p class="an">No Imperial cards in hand – instead of a card you lose 3 culture points.</p><div class="row"><button class="btn primary" id="lsNone">−3 culture</button></div>','nie ma karty imperialnej do oddania: −3 kultury (wydarzenie)':'has no Imperial card to give up: −3 culture (event)',' kam.':' stone',' kam.)':' stone)','kam.':'stone',' o ':' ',' z ':' of ',' z 3':' of 3',' z: <b>':' from: <b>',' i ':' and ',' w ':' in '})
US=[('Favour','Favor'),('favour','favor'),('colour','color'),('Colour','Color'),('defence','defense'),('Defence','Defense'),('honour','honor'),('centre','center'),('grey','gray'),('Grey','Gray'),('cancelled','canceled'),('labour','labor')]
def us(s):
  for a,b in US: s=s.replace(a,b)
  return s
REG={
r'^osiąga cel publiczny':r'^(osiąga cel publiczny|achieves a public goal)',
r'Odkryj|odkryci':r'Odkryj|odkryci|Discover|discover',
r'populacj':r'populacj|population',
r'terytori':r'terytori|territor',
r'cywiln':r'cywiln|civil',
r'militarn|wojownik':r'militarn|wojownik|military|warrior',
r'technologi':r'technologi|technolog',
r'cud':r'cud|wonder',
r'Karawan|karawan':r'Karawan|karawan|Caravan|caravan',
r'kart[ęa] imperialn':r'kart[ęa] imperialn|Imperial card',
r'chwał':r'chwał|glory|Glory',
r'buduje fort':r'buduje fort|builds a fort',
r'\(−(\d+) (złot|kamie|energi|wpływ)':r'\(−(\d+) (złot|kamie|energi|wpływ|gold|stone|energy|influence)',
r'^(Dodatkowo|Wybierz)':r'^(Dodatkowo|Wybierz|Additionally|Choose)',
r'^Nowy robotnik$':r'^(Nowy robotnik|New worker)$',
r'^Kup 3\. ambasadora$':r'^(Kup 3\. ambasadora|Buy a 3rd ambassador)$',
r'^Weź 1 złoto, 1 wpływ, 1 energię i 1 kamień$':r'^(Weź 1 złoto, 1 wpływ, 1 energię i 1 kamień|Take 1 gold, 1 influence, 1 energy and 1 stone)$',
r'^Wykonaj 2 dowolne akcje główne$':r'^(Wykonaj 2 dowolne akcje główne|Take 2 main actions of your choice)$',
r'^Wykonaj 1 dowolną akcję główną$':r'^(Wykonaj 1 dowolną akcję główną|Take 1 main action of your choice)$',
r'(pozostało \d+ z \d+|wybierz jeszcze: \d+|użycia Warsztatów: \d+ z 3)':r'(pozostało \d+ z \d+|wybierz jeszcze: \d+|użycia Warsztatów: \d+ z 3|remaining:? \d+ of \d+|choose another: \d+|Workshops uses: \d+ of 3)',
r'^(Robotnik na|Wojownik na|Odkryj terytorium): ':r'^(Robotnik na|Wojownik na|Odkryj terytorium|Worker on|Warrior on|Discover a territory): ',
r'^(Osobna akcja z karty|Tańsza akcja pola \(z kartą\))( · )?':r'^(Osobna akcja z karty|Tańsza akcja pola \(z kartą\)|Separate action from the card|Cheaper space action \(with the card\))( · )?',
r'^Wariant: ':r'^(Wariant|Variant): ',
r' · Wariant:.*$':r' · (Wariant|Variant):.*$',
r'^Wariant:.*$':r'^(Wariant|Variant):.*$',
r'taniej o (\d+) (zł|kam|ener|wpł)':r'(?:taniej o|cheaper by) (\d+) (zł|kam|ener|wpł|gold|stone|energy|influence)',
r'zagrywa kartę imperialną w fazie akcji':r'zagrywa kartę imperialną w fazie akcji|plays an Imperial card in the action phase',
r'przesuwa (ambasadora|plemię|piramidę)':r'(przesuwa|moves) (ambasadora|plemię|piramidę|ambassador|tribe|pyramid)',
r'cywilną':r'cywilną|civil',r'terytorium':r'terytorium|territor',r'etap cudu':r'etap cudu|wonder stage',r'militarną':r'militarną|military',r'kolonizacji':r'kolonizacji|colonization',
r'wpływ↔kamień':r'wpływ↔kamień|influence↔stone',r'wpływ↔energia':r'wpływ↔energia|influence↔energy',
r'Beringa':r'Beringa|Bering',r'Kolumb':r'Kolumb|Columbus',r'Piotra':r'Piotra|Peter',r'Machu':r'Machu',r'Wawel':r'Wawel',
r'^pasuje':r'^(pasuje|passes)',r'^tor dyplomacji ':r'^(tor dyplomacji|diplomacy track) ',
}
def esc_for(q,s):
  if q in '"\'':
    s=re.sub(r'(?<!\\)'+re.escape(q),'\\'+q,s)
    assert '\n' not in s
  else:
    s=re.sub(r'(?<!\\)`','\\`',s)
  return s
out=[]; pos=0; used=set(); miss=[]
for m in re.finditer(r'<script>([\s\S]*?)</script>',h):
  off=m.start(1)
  for k,a,b in lex(m.group(1)):
    a+=off; b+=off; t=h[a:b]
    if k=='r':
      if t in REG: new=REG[t]; used.add(t)
      else: continue
    else:
      if t not in M: continue
      q=h[a-1]; q=q if q in '"\'' else '`'
      new=esc_for(q,us(M[t]))
    out.append(h[pos:a]); out.append(new); pos=b
out.append(h[pos:]); e=''.join(out)
print('unused REG',[r for r in REG if r not in used])
POST=[
('plays an Imperial card in the phase ${dip?"diplomacy":"actions"}','plays an Imperial card in the ${dip?"diplomacy":"action"} phase'),
('const RG={złot:"g",kamie:"s",energi:"e",wpływ:"i"}','const RG={złot:"g",kamie:"s",energi:"e",wpływ:"i",gold:"g",stone:"s",energy:"e",influence:"i"}'),
('{zł:"g",kam:"s",ener:"e",wpł:"i"}[m[2]]','{zł:"g",kam:"s",ener:"e",wpł:"i",gold:"g",stone:"s",energy:"e",influence:"i"}[m[2]]'),
('Take ${gen?"genius":"worker"} of ${n.j+1}. space','Take ${gen?"genius":"worker"} from ${n.j+1}. space'),
('>Język stołu<','>Table language<'),
('Kingdoms · gra online</p>','Kingdoms · online game</p>'),('<h2>Logowanie</h2>','<h2>Log in</h2>'),('for="lgP">Hasło<','for="lgP">Password<'),('id="lgGo">Zaloguj<','id="lgGo">Log in<'),
('<a href="terra/" style="color:var(--brass-2,#e8c766)">O grze Terra Altera</a> · <a href="terra/indexang.html" style="color:var(--brass-2,#e8c766)">About the game</a>','<a href="terra/indexang.html" style="color:var(--brass-2,#e8c766)">About Terra Altera</a> · <a href="terra/" style="color:var(--brass-2,#e8c766)">Polish website</a>'),
('id="create">Załóż stół<','id="create">Create table<'),('aria-label="Język / Language"','aria-label="Language / Język"'),
]
for a,b in POST:
  n=e.count(a); assert n>=1,a; e=e.replace(a,b)
HELP=open('help_en.html',encoding='utf-8').read()
i=e.index('<div id="help"'); j=e.index('</div>\n</div>',i)+len('</div>\n</div>')
e=e[:i]+HELP.strip()+e[j:]
e=e.replace('<title>Terra Altera online</title>','<title>Terra Altera online</title>\n<script>window.TA_LANG="en";</script>',1)
open(OUT,'w',encoding='utf-8').write(e)
print('ok',len(e))
