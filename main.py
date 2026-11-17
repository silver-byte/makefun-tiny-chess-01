import os,json,urllib.request
V=0,100,300,310,500,900,20000
D={2:(33,31,18,14,-33,-31,-18,-14),3:(15,17,-15,-17),4:(1,-1,16,-16),5:(1,-1,16,-16,15,17,-15,-17),6:(1,-1,16,-16,15,17,-15,-17)}
L=7000
def fen(f):
 p=f.split();b=[0]*128
 for r,x in zip(range(7,-1,-1),p[0].split('/')):
  q=0
  for z in x:
   if z.isdigit():q+=int(z)
   else:b[r*16+q]=(1 if z.isupper()else-1)*' PNBRQK'.index(z.upper());q+=1
 c=sum(1<<'KQkq'.index(z)for z in p[2]if z in'KQkq');e=-1 if p[3]=='-'else ord(p[3][0])-97+16*(int(p[3][1])-1)
 return tuple(b),1 if p[1]=='w'else-1,c,e
def atk(b,q,s):
 for d in 15,17:
  x=q-s*d
  if not x&136 and b[x]==s:return 1
 for d in D[2]:
  x=q+d
  if not x&136 and b[x]==s*2:return 1
 for k in 3,4:
  for d in D[k]:
   x=q+d
   while not x&136:
    z=b[x]
    if z:
     if z*s>0 and abs(z)in(k,5):return 1
     break
    x+=d
 for d in D[6]:
  x=q+d
  if not x&136 and b[x]==s*6:return 1
 return 0
def gen(P):
 b,s,c,e=P
 for i,p in enumerate(b):
  if p*s<1:continue
  k=abs(p)
  if k==1:
   d=16*s;j=i+d
   if not b[j]:
    yield i,j,5 if j//16 in(0,7)else 0
    if i//16==(1 if s>0 else 6)and not b[j+d]:yield i,j+d,0
   for j in i+d-1,i+d+1:
    if not j&136 and(b[j]*s<0 or j==e):yield i,j,5 if j//16 in(0,7)else 0
  else:
   for d in D[k]:
    j=i+d
    while not j&136 and b[j]*s<=0:
     yield i,j,0
     if b[j]or k in(2,6):break
     j+=d
   if k==6 and not atk(b,i,-s):
    a=0 if s>0 else 112
    if c&(1 if s>0 else 4)and b[a+5]==b[a+6]==0 and b[a+7]==s*4 and not atk(b,a+5,-s)and not atk(b,a+6,-s):yield i,a+6,0
    if c&(2 if s>0 else 8)and b[a+1]==b[a+2]==b[a+3]==0 and b[a]==s*4 and not atk(b,a+3,-s)and not atk(b,a+2,-s):yield i,a+2,0
def play(P,m):
 b,s,c,e=P;i,j,u=m;a=list(b);p=a[i];z=a[j];a[i]=0;a[j]=s*u if u else p
 if abs(p)==1 and j==e and not z:a[j-16*s]=0
 if abs(p)==6 and abs(j-i)==2:r=(7 if j>i else 0)+(0 if s>0 else 112);a[(i+j)//2]=a[r];a[r]=0
 ne=i+16*s if abs(p)==1 and abs(j-i)==32 else-1
 for q,x in((4,3),(0,2),(7,1),(116,12),(112,8),(119,4)):
  if i==q or j==q:c&=~x
 return tuple(a),-s,c,ne
def moves(P):
 for m in gen(P):
  Q=play(P,m);b,s,_,_=Q
  if s*6 in b and not atk(b,b.index(-s*6),s):yield m
def val(P):
 t=0
 for i,p in enumerate(P[0]):
  if not p:continue
  k=abs(p);r=i//16 if p>0 else 7-i//16;f=i&7;x=V[k]
  if k==1:x+=r*3-3*abs(f-3.5)
  elif k in(2,3):x+=30-6*(abs(f-3.5)+abs(r-3.5))
  elif k==6:x+=(-6*(r+abs(f-3.5))if sum(abs(z)in(4,5)for z in P[0])>2 else 6*(r-abs(f-3.5)))
  t+=(1 if p>0 else-1)*x
 return int(t*P[1])
T={};K={};n=0
class S(Exception):pass
def capture(P,m):return P[0][m[1]]or(abs(P[0][m[0]])==1 and m[1]==P[3])or m[2]
def order(P,a,t=0,d=0):
 b=P[0];return sorted(a,key=lambda m:(m==t)*99999+(m==K.get(d))*4000+V[abs(b[m[1]])]*16-V[abs(b[m[0]])]+m[2]*900,reverse=True)
def search(P,d,a,z,h=0):
 global n;n+=1
 if n>L:raise S
 b,s,c,e=P;check=atk(b,b.index(s*6),-s);M=list(moves(P))
 if d<1 and not check:
  x=val(P)
  if x>=z:return z
  if x>a:a=x
  M=[m for m in M if capture(P,m)]
 q=P,d;w=T.get(q);tm=w[1]if w else 0
 if w and w[0]>=z:return w[0]
 if not M:return -30000+h if check else 0
 best=-30000
 for i,m in enumerate(order(P,M,tm,h)):
  Q=play(P,m)
  if i:x=-search(Q,d-1,-a-1,-a,h+1);x=-search(Q,d-1,-z,-a,h+1)if x>a and x<z else x
  else:x=-search(Q,d-1,-z,-a,h+1)
  if x>best:best=x;T[q]=x,m
  if x>a:a=x
  if a>=z:
   if not capture(P,m):K[h]=m
   break
 return a
def choose(f,A):
 global n,T,K;P=fen(f);best=A[0];pv=0;T={};K={}
 for d in range(1,9):
  n=0
  try:
   a=-30000;bm=0
   for m in order(P,list(moves(P)),pv):
    x=-search(play(P,m),d-1,-30000,-a,1)
    if x>a:a,bm=x,m
   if bm:
    pv=bm;i,j,u=bm;w='abcdefgh'[i&7]+str(i//16+1)+'abcdefgh'[j&7]+str(j//16+1)+('q'if u else'')
    if w in A:best=w
  except S:break
 return best
U=os.environ['MAKEFUN_ENV_URL']
def post(p,x):
 r=urllib.request.Request(U+p,json.dumps(x).encode(),{'Content-Type':'application/json'});return json.load(urllib.request.urlopen(r))
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
