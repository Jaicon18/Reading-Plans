import pymupdf,numpy as np,sys
d=pymupdf.open('/tmp/claude-0/crset/CR_arch.pdf')
K=3.0
def ras(i,zoom,clip=None):
    p=d[i]; pix=p.get_pixmap(matrix=pymupdf.Matrix(zoom,zoom),clip=clip,colorspace=pymupdf.csGRAY)
    return (np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width)<128).astype(np.float32)
B=ras(16,K/9.0)
def corr(a,b):
    H=a.shape[0]+b.shape[0]; W=a.shape[1]+b.shape[1]
    c=np.fft.irfft2(np.fft.rfft2(b-b.mean(),(H,W))*np.conj(np.fft.rfft2(a-a.mean(),(H,W))),(H,W))
    iy,ix=np.unravel_index(np.argmax(c),c.shape); v=c.max()/np.sqrt(((a-a.mean())**2).sum()*((b-b.mean())**2).sum())
    if iy>H-a.shape[0]: iy-=H
    if ix>W-a.shape[1]: ix-=W
    return v,iy,ix
idx=int(sys.argv[1]); clip=pymupdf.Rect(*map(float,sys.argv[2:6])) if len(sys.argv)>5 else pymupdf.Rect(0,0,2300,1500)
for e in (12,13.5,18,24,27,36):
    A=ras(idx,K/e,clip); v,iy,ix=corr(A,B); print(e,round(v,4),iy,ix)
