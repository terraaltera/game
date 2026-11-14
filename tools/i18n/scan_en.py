import json,re,sys
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from lex import lex
from wordfreq import zipf_frequency as z
h=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'../../en.html'),encoding='utf-8').read()
OK={'Czapla','Młody','Filippo','Adam','Wawel','Samarkanda','Mauretania','Polonia','Dorada','Guiana','czapla','mlody','filip','adam','Bolesław','Kraków','Wieliczka'}
def ispl(w):
  if w in OK: return False
  if re.search('[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]',w): return True
  lw=w.lower(); p=z(lw,'pl'); e=z(lw,'en')
  return p>=1.5 and p>e+0.3 and len(w)>=3
res={}
for m in re.finditer(r'<script>([\s\S]*?)</script>',h):
  off=m.start(1)
  for k,a,b in lex(m.group(1)):
    if k=='r': continue
    t=h[off+a:off+b]
    s=re.sub(r'\b(class|id|style|data-[\w-]+|src|href|for|type|min|max|value)="[^"]*"','',t)
    s=re.sub(r'<\/?[a-zA-Z][\w-]*','',s)
    pw=[w for w in re.findall(r"[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]+",s) if ispl(w)]
    if pw: res.setdefault(t,(h.count('\n',0,off+a)+1,pw))
for t,(ln,pw) in sorted(res.items(),key=lambda x:x[1][0]): print(ln,repr(t[:110]),pw[:3])
print(len(res))
