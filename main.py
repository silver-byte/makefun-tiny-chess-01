import os,json
from urllib.request import*
V=0,100,300,310,500,900,2e4
A=abs;E=enumerate;G=range
R=1,-1,16,-16;B=15,17,-15,-17
D={2:(33,31,18,14,-33,-31,-18,-14),3:B,4:R,5:R+B,6:R+B}
L=3e4
J=[[[V[k]+(k==1)*(r*(5-h//8)-h*r*((x:=A(2*f-7))>4))+(k in(2,3))*(30-5*x-5*(y:=A(2*r-7)))+(k==2)*min(r,7-r)*2+(k==3)*(7-A(f-r))*2+(k==4)*(5*(r==5)+15*(r==6))+(k==5)*(7-(x+y)//2)+(k==6)*(-h*(r*2+min(f,7-f))+(32-h)*(20-2.5*x-2.5*y))for r in G(8)for f in G(8)]for k in G(7)]for h in G(33)]
def fen(f):
 p=f.split();b=[0]*128
 for r,x in zip(G(7,-1,-1),p[0].split('/')):
  q=0
  for z in x:
   if z.isdigit():q+=int(z)
   else:b[r*16+q]=(1-2*z.islower())*' PNBRQK'.index(z.upper());q+=1
 c=sum(1<<'KQkq'.index(z)for z in p[2]if z in'KQkq');e=-1 if p[3]=='-'else ord(p[3][0])-97+16*(int(p[3][1])-1)
 return tuple(b),1 if p[1]=='w'else-1,c,e
def X(b,q,s):
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
    if k==6 and not X(b,i,-s):
     a=112*(s<0)
     for j,r,x in((a+6,a+7,1+3*(s<0)),(a+2,a,2+6*(s<0))):
      if c&x and b[r]==s*4 and all(not b[q]for q in G(min(i,r)+1,max(i,r)))and not X(b,(i+j)//2,-s)and not X(b,j,-s):yield i,j,0
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
  if q==1 and not c and not X(b,b.index(s*6),-s):continue
  if s*6 in b and not X(b,b.index(-s*6),s):yield m
def val(P):
 b=P[0];t=0;h=min(32,sum(A(z)-1 for z in b if 1<A(z)<6));j=J[h]
 for i,p in E(b):
  if not p:continue
  s=1-2*(p<0);k=A(p);r=A(7*(s<0)-i//16);f=i&7;x=j[k][r*8+f]
  if k==6:x+=20*sum(not(i+s*d)&136 and b[i+s*d]==s for d in(15,16,17))-h*3*(s not in b[f::16])-(32-h)*(20-5*(A(f-3.5)+A(r-3.5)))*(-s*5 in b)
  t+=s*x
 return int(t*P[1])
T={};n=0
def C(P,m):return P[0][m[1]]or(A(P[0][m[0]])==1 and m[1]==P[3])or m[2]
def O(P,a):
 b=P[0];return sorted(a,key=lambda m:V[A(b[m[1]])]*16-V[A(b[m[0]])]+m[2]*9e2,reverse=1)
def S(P,d,a,z,h=0):
 global n;n+=1
 if n>L:raise EOFError
 b,s=P[:2];c=X(b,b.index(s*6),-s);M=list(mv(P,(d<1 and not c)*(1+(d<0))))
 if d<1 and not c:
  x=val(P)
  if x>=z:return z
  if x>a:a=x
  M=[m for m in M if not b[m[1]]or m[2]or x+V[A(b[m[1]])]+150>a]
 q=P,d;w=T.get(q)
 if w and w>=z:return w
 if not M:return -3e4+h if c else 0
 for i,m in E(O(P,M)):
  Q=play(P,m)
  r=i>3 and d>2 and not C(P,m)and not X(Q[0],Q[0].index(Q[1]*6),-Q[1])
  if i:x=-S(Q,d-1-r,-a-1,-a,h+1);x=-S(Q,d-1,-z,-a,h+1)if x>a else x
  else:x=-S(Q,d-1,-z,-a,h+1)
  if x>a:a=x;T[q]=x
  if a>=z:break
 return a
def choose(f,A):
 global n,T;P=fen(f);b=A[0];T={}
 for d in G(1,9):
  n=0
  try:
   a=-3e4
   for m in O(P,list(mv(P))):
    x=-S(play(P,m),d-1,-3e4,-a,1)
    if x>a:a,bm=x,m
   i,j,u=bm;b='abcdefgh'[i&7]+str(i//16+1)+'abcdefgh'[j&7]+str(j//16+1)+('q'if u else'')
  except EOFError:break
 return b
U=os.environ['MAKEFUN_ENV_URL']
def post(p,x):
 return json.load(urlopen(Request(U+p,json.dumps(x).encode())))
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
