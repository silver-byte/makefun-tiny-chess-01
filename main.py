import re
W=[100,320,330,500,1000,100,30,150]
L=3e4
A=abs;E=enumerate;G=range;Q=' PNBRQK'
R=1,-1,16,-16;B=15,17,-15,-17
D={2:(33,31,18,14,-33,-31,-18,-14),3:B,4:R,5:R+B,6:R+B}
J=[[r*8 if k==1 else 24-3*A(2*f-7)-3*A(2*r-7)if k in(2,3)else 0 for r in G(8)for f in G(8)]for k in G(7)]
def F(f):
 p=f.split();b=[0]*128
 for r,x in zip(G(7,-1,-1),p[0].split('/')):
  q=0
  for z in x:
   if z<'A':q+=int(z)
   else:b[r*16+q]=(1-2*z.islower())*Q.index(z.upper());q+=1
 c=sum(1<<'KQkq'.index(z)for z in p[2]if z>'-');e=-1 if p[3]=='-'else ord(p[3][0])-97+16*(int(p[3][1])-1)
 return tuple(b),2*(p[1]=='w')-1,c,e,*map(int,p[4:])
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
def g(P):
 b,s,c,e=P[:4]
 for i,p in E(b):
  if p*s<1:continue
  k=A(p)
  if k==1:
   d=16*s;j=i+d
   if not b[j]:
    for u in((2,3,4,5)if j//16 in(0,7)else(0,)):yield i,j,u
    if i//16==1+5*(s<0)and not b[j+d]:yield i,j+d,0
   for j in i+d-1,i+d+1:
    if not j&136 and(b[j]*s<0 or j==e):
     for u in((2,3,4,5)if j//16 in(0,7)else(0,)):yield i,j,u
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
def Y(P,m):
 b,s,c,e,h,f=P;i,j,u=m;a=list(b);p=a[i];z=a[j];a[i]=0;a[j]=s*u if u else p
 if A(p)==1 and j==e and not z:a[j-16*s]=0;z=-s
 if A(p)==6 and A(j-i)==2:r=(7 if j>i else 0)+112*(s<0);a[(i+j)//2]=a[r];a[r]=0
 ne=i+16*s if A(p)==1 and A(j-i)==32 else-1
 for q,x in((4,3),(0,2),(7,1),(116,12),(112,8),(119,4)):
  if i==q or j==q:c&=~x
 return tuple(a),-s,c,ne,0 if z or A(p)==1 else h+1,f+(s<0)
def N(P):
 for m in g(P):
  q=Y(P,m);b,s=q[:2]
  if s*6 in b and not X(b,b.index(-s*6),s):yield m
def U(m):
 i,j,p=m;return chr(97+(i&7))+str(i//16+1)+chr(97+(j&7))+str(j//16+1)+('  nbrq'[p]if p else'')
def O(P):
 b,s,c,e,h,f=P;v='/'.join(re.sub(r'\.+',lambda m:str(len(m[0])),''.join('.'if not p else(Q[A(p)]if p>0 else Q[A(p)].lower())for p in b[r*16:r*16+8]))for r in G(7,-1,-1))
 c=''.join(x for i,x in E('KQkq')if c>>i&1)or'-';e='-'if e<0 else chr(97+(e&7))+str(e//16+1)
 return v+' '+('w'if s>0 else'b')+' '+c+' '+e+f' {h} {f}'
legal=lambda f:[U(m)for m in N(F(f))]
def apply(f,u):
 P=F(f);return O(Y(P,next(m for m in N(P)if U(m)==u)))
def val(P):
 b,s=P[:2];t=0
 for i,p in E(b):
  if p:k=A(p);r=A(7*(p<0)-i//16);t+=(1-2*(p<0))*(W[k-1]+J[k][r*8+(i&7)]*W[5]//100)
 t+=W[6]*((b.count(3)>1)-(b.count(-3)>1));return t*s
Z=EOFError;T=K={};n=0
def H(P):
 b,s,c,e=P[:4];z=c*17^(e+1)*31^(s<0)
 for i,p in E(b):
  if p:z^=(i*13+p+7)*0x9e3779b1
 return z
def S(P,d,a,z,h=0):
 global n;n+=1
 if n>L:raise Z
 b,s=P[:2];k=H(P);t=T.get(k);q=t if t else 0;c=X(b,b.index(s*6),-s);M=list(N(P))
 if d<1 and not c:
  x=val(P)
  if x>=z:return z
  if x>a:a=x
  M=[m for m in M if b[m[1]]or m[2]]
 if not M:return -3e4+h if c else 0
 M.sort(key=lambda m:(m==q)*1e6+(m==K.get(h))*1e5+(b[m[1]]and W[A(b[m[1]])-1])*16-W[A(b[m[0]])-1],reverse=1)
 for m in M:
  x=-S(Y(P,m),d-1,-z,-a,h+1)
  if x>a:a=x;q=m
  if a>=z:
   if not b[m[1]]:K[h]=m
   break
 T[k]=q;return a
def best(f):
 global n,T,K;P=F(f);r=next(N(P));n=0;T={};K={}
 try:
  for d in G(1,20):
   a=-3e4
   for m in N(P):
    x=-S(Y(P,m),d-1,-3e4,-a,1)
    if x>a:a,b=x,m
   r=b
 except Z:pass
 return U(r)
choose=lambda f,A:best(f)
if __name__=='__main__':
 import os,json
 from urllib.request import*
 q=os.getenv('MAKEFUN_ENV_URL')
 p=lambda a,x:json.load(urlopen(Request(q+a,json.dumps(x).encode())))
 while(g:=p('/game',{}))['status']!='done':
  while g['status']=='your_move':g=p('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
