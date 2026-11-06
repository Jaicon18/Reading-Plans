"""Detect guest-bath showers: two diagonal lines sharing one endpoint (tip near drain end) whose other
endpoints are aligned on the same x (vertical end) or the same y (horizontal end) = the shower end wall face.
Returns (orientation, end_coord, span_lo, span_hi, tip_x, tip_y)."""
from vec import segs  # copiado de auditoria_U138_2/tools (detector del auditor U-138 #2)
def showers(pi):
    dg = [s for s in segs(pi) if abs(s[0]-s[2]) > 2 and abs(s[1]-s[3]) > 2 and s[4] < 0.5 and
          ((s[0]-s[2])**2 + (s[1]-s[3])**2) ** 0.5 < 90]
    out = set()
    for i in range(len(dg)):
        for j in range(i+1, len(dg)):
            A = [(dg[i][0], dg[i][1]), (dg[i][2], dg[i][3])]; B = [(dg[j][0], dg[j][1]), (dg[j][2], dg[j][3])]
            for p in A:
                for q in B:
                    if abs(p[0]-q[0]) < 0.3 and abs(p[1]-q[1]) < 0.3:
                        pa = A[1] if p == A[0] else A[0]; qb = B[1] if q == B[0] else B[0]
                        if abs(pa[0]-qb[0]) < 0.3 and abs(pa[1]-qb[1]) > 15:
                            out.add(('V', round(pa[0],2), round(min(pa[1],qb[1]),2), round(max(pa[1],qb[1]),2), round(p[0],2), round(p[1],2)))
                        elif abs(pa[1]-qb[1]) < 0.3 and abs(pa[0]-qb[0]) > 15:
                            out.add(('H', round(pa[1],2), round(min(pa[0],qb[0]),2), round(max(pa[0],qb[0]),2), round(p[0],2), round(p[1],2)))
    return sorted(out)
if __name__ == '__main__':
    for pi in (16, 17, 18, 19):
        sh = showers(pi); print(pi, len(sh))
        for s in sh: print('  ', s, 'end %.2f ft, length %.2f ft' % ((s[3]-s[2])/9, abs((s[1]-(s[4] if s[0]=='V' else s[5])))/9))
