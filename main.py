import os,json
from urllib.request import*
V=0,100,300,310,500,900,2e4
A=abs;E=enumerate
R=1,-1,16,-16;B=15,17,-15,-17
D={2:(33,31,18,14,-33,-31,-18,-14),3:B,4:R,5:R+B,6:R+B}
L=2e4
def fen(f):
 p=f.split();b=[0]*128
 for r,x in zip(range(7,-1,-1),p[0].split('/')):
  q=0
  for z in x:
   if z.isdigit():q+=int(z)
   else:b[r*16+q]=(1-2*z.islower())*' PNBRQK'.index(z.upper());q+=1
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
     if z*s>0 and A(z)in(k,5):return 1
     break
    x+=d
 for d in D[6]:
  x=q+d
  if not x&136 and b[x]==s*6:return 1
 return 0
def gen(P):
 b,s,c,e=P
 for i,p in E(b):
  if p*s<1:continue
  k=A(p)
  if k==1:
   d=16*s;j=i+d
   if not b[j]:
     yield i,j,5 if j//16 in(0,7)else 0
     if i//16==1+5*(s<0)and not b[j+d]:yield i,j+d,0
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
     a=112*(s<0)
     if c&1+3*(s<0)and b[a+5]==b[a+6]==0 and b[a+7]==s*4 and not atk(b,a+5,-s)and not atk(b,a+6,-s):yield i,a+6,0
     if c&2+6*(s<0)and b[a+1]==b[a+2]==b[a+3]==0 and b[a]==s*4 and not atk(b,a+3,-s)and not atk(b,a+2,-s):yield i,a+2,0
def play(P,m):
 b,s,c,e=P;i,j,u=m;a=list(b);p=a[i];z=a[j];a[i]=0;a[j]=s*u if u else p
 if A(p)==1 and j==e and not z:a[j-16*s]=0
 if A(p)==6 and A(j-i)==2:r=(7 if j>i else 0)+112*(s<0);a[(i+j)//2]=a[r];a[r]=0
 ne=i+16*s if A(p)==1 and A(j-i)==32 else-1
 for q,x in((4,3),(0,2),(7,1),(116,12),(112,8),(119,4)):
  if i==q or j==q:c&=~x
 return tuple(a),-s,c,ne
def mv(P,q=0):
 for m in gen(P):
  c=C(P,m)
  if q>1 and not c:continue
  b,s,_,_=play(P,m)
  if q==1 and not c and not atk(b,b.index(s*6),-s):continue
  if s*6 in b and not atk(b,b.index(-s*6),s):yield m
def val(P):
 b=P[0];t=0;h=min(32,sum(A(z)-1 for z in b if 1<A(z)<6))
 for i,p in E(b):
  if not p:continue
  s=1-2*(p<0);k=A(p);r=A(7*(s<0)-i//16);f=i&7;x=V[k]
  if k==1:
   x+=r*(5-h//8)-h*r*(A(2*f-7)>4)
   if all(j&136 or b[j]!=-s for j in(i+15*s,i+16*s,i+17*s)):x+=r*r*(32-h)//16
  elif k in(2,3):x+=30-5*(A(2*f-7)+A(2*r-7))
  elif k==6:x+=20*sum(not(i+s*d)&136 and b[i+s*d]==s for d in(15,16,17))-h*(r*2+min(f,7-f)+3*(s not in b[f::16]))+(32-h)*(20-5*(A(f-3.5)+A(r-3.5)))*(-s*5 not in b)
  t+=s*x
 return int(t*P[1])
T={};K={};n=0
def C(P,m):return P[0][m[1]]or(A(P[0][m[0]])==1 and m[1]==P[3])or m[2]
def O(P,a,d=0):
 b=P[0];return sorted(a,key=lambda m:(m==K.get(d))*4e3+V[A(b[m[1]])]*16-V[A(b[m[0]])]+m[2]*9e2,reverse=1)
def search(P,d,a,z,h=0):
 global n;n+=1
 if n>L:raise EOFError
 b,s,c,e=P;check=atk(b,b.index(s*6),-s);M=list(mv(P,(d<1 and not check)*(1+(d<0))))
 if d<1 and not check:
  x=val(P)
  if x>=z:return z
  if x>a:a=x
 q=P,d;w=T.get(q)
 if w and w>=z:return w
 if not M:return -3e4+h if check else 0
 for i,m in E(O(P,M,h)):
  Q=play(P,m)
  r=i>3 and d>2 and not C(P,m)and not atk(Q[0],Q[0].index(Q[1]*6),-Q[1])
  if i:x=-search(Q,d-1-r,-a-1,-a,h+1);x=-search(Q,d-1,-z,-a,h+1)if x>a else x
  else:x=-search(Q,d-1,-z,-a,h+1)
  if x>a:a=x;T[q]=x
  if a>=z:
   if not C(P,m):K[h]=m
   break
 return a
def choose(f,A):
 global n,T,K;P=fen(f);best=A[0];T={};K={}
 for d in range(1,9):
  n=0
  try:
   a=-3e4
   for m in O(P,list(mv(P))):
    x=-search(play(P,m),d-1,-3e4,-a,1)
    if x>a:a,bm=x,m
   i,j,u=bm;best='abcdefgh'[i&7]+str(i//16+1)+'abcdefgh'[j&7]+str(j//16+1)+('q'if u else'')
  except EOFError:break
 return best
U=os.environ['MAKEFUN_ENV_URL']
def post(p,x):
 return json.load(urlopen(Request(U+p,json.dumps(x).encode())))
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
