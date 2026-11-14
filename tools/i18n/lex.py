# Lekser JS/HTML: wyciąga fragmenty tekstu (literały i statyczne części szablonów) oraz literały regex
import re,sys,json
PL=re.compile(r'[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]|\b(nie|na|do|się|jest|gracz\w*|kart\w*|robotnik\w*|złot\w*|kamie\w*|akcj\w*|pol[ea]|ruch\w*|faza|rund\w*|wybierz|zamknij|tak|brak|albo|oraz|dla|lub|koszt|wpływ\w*|energi\w*|kultur\w*|siła|chwał\w*|cud\w*|teren\w*|terytori\w*|technologi\w*|gra|stół|stoły|graj\w*|zapłać|weź|bierze|płaci|wysyła|kupuje|odkrywa|buduje|kończy|cofnij|Gotowe|Anuluj|Zagraj|Wyślij|Kup|Odkryj|Zbuduj|Zwiększ|Dowolna)\b',re.I)
def lex(src):
    out=[]  # (kind,start,end,text)
    i=0;n=len(src);stack=[]  # template nesting: stack of brace depth
    mode='code'
    def string(i,q):
        j=i+1
        while j<n and src[j]!=q:
            if src[j]=='\\': j+=2; continue
            if src[j]=='\n': break
            j+=1
        return j
    prev_sig=''  # last significant char for regex detection
    res=[]
    def tmpl(i):
        # i at backtick; returns end index after closing backtick, recording static chunks
        j=i+1; start=j
        while j<n:
            c=src[j]
            if c=='\\': j+=2; continue
            if c=='`':
                res.append(('t',start,j)); return j+1
            if c=='$' and j+1<n and src[j+1]=='{':
                res.append(('t',start,j)); j=code(j+2,'}'); start=j; continue
            j+=1
        return j
    def code(j,endch):
        depth=0; ps=''
        while j<n:
            c=src[j]
            if c in '"\'':
                k=string(j,c); res.append(('s',j+1,k)); j=k+1; ps='a'; continue
            if c=='`': j=tmpl(j); ps='a'; continue
            if c=='/' and j+1<n and src[j+1]=='/':
                k=src.find('\n',j); j=n if k<0 else k; continue
            if c=='/' and j+1<n and src[j+1]=='*':
                k=src.find('*/',j+2); j=n if k<0 else k+2; continue
            if c=='/' and (ps=='' or ps in '(,=:[!&|?{};+-*%<>~^\n' or ps=='kw'):
                # regex literal
                k=j+1; cls=False
                while k<n:
                    if src[k]=='\\': k+=2; continue
                    if src[k]=='[': cls=True
                    elif src[k]==']': cls=False
                    elif src[k]=='/' and not cls: break
                    elif src[k]=='\n': break
                    k+=1
                res.append(('r',j+1,k)); k+=1
                while k<n and src[k].isalpha(): k+=1
                j=k; ps='a'; continue
            if c=='{': depth+=1
            elif c=='}':
                if depth==0 and endch=='}': return j+1
                depth-=1
            if not c.isspace():
                if c.isalnum() or c in '_$)]': 
                    # keyword check
                    m=re.match(r'[A-Za-z_$][\w$]*',src[j:])
                    if m:
                        w=m.group(0); ps='kw' if w in ('return','typeof','case','in','of','do','else','new','delete','void','throw') else 'a'; j+=len(w); continue
                    ps='a'
                else: ps=c
            j+=1
        return j
    code(0,None)
    return res
if __name__=='__main__':
    html=open(sys.argv[1],encoding='utf-8').read()
    frags=[]
    for m in re.finditer(r'<script>([\s\S]*?)</script>',html):
        off=m.start(1); r=lex(m.group(1))
        for k,a,b in r: frags.append((k,off+a,off+b))
    json.dump(frags,open(sys.argv[2],'w'))
    pl=[(k,html[a:b]) for k,a,b in frags if PL.search(html[a:b])]
    print(len(frags),len(pl), len(set(x for k,x in pl if k!='r')), len([1 for k,x in pl if k=='r']))
