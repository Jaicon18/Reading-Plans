import sys, pickle, pdfplumber
P = '/tmp/chuze/plano/bidset_SIN_MARKUPS.pdf'; i = int(sys.argv[1])
with pdfplumber.open(P) as pdf:
    pg = pdf.pages[i]
    ws = [{k: w[k] for k in ('text', 'x0', 'x1', 'top', 'bottom', 'size')} for w in pg.extract_words(extra_attrs=['size'])]
    pickle.dump(dict(i=i, w=pg.width, h=pg.height, ws=ws), open('/tmp/chuze/words/%03d.pkl' % i, 'wb'))
