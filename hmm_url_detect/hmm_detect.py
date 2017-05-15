import numpy as np
from hmmlearn import hmm
import urlparse
import urllib
def etl(str):
    vers=[]
    for i, c in enumerate(str):
        c=c.lower()
        if   ord(c) >= ord('a') and  ord(c) <= ord('z'):
            vers.append([ord('A')])
        elif ord(c) >= ord('0') and  ord(c) <= ord('9'):
            vers.append([ord('N')])
        else:
            vers.append([ord('C')])
    return vers

def ischeck(data):
    return 1
samp = [
    "/0_1/include/dialog/select_media.php?userid=admin123",
    "/0_1/include/dialog/select_media.php?userid=root",
    "/0_1/include/dialog/select_media.php?userid=maidou0806",
    "/0_1/include/dialog/select_media.php?userid=52maidou",
    "/0_1/include/dialog/select_media.php?userid=wjq_2014",
    "/0_1/include/dialog/select_media.php?userid=mzc-cxy",
    ]

m_list = []
X_lens = []
for line in samp:
    result = urlparse.urlparse(line)
    query = urllib.unquote(result.query)
    params = urlparse.parse_qsl(query, True)
    print params
    for k, v in params:
        vers = etl(v)
        m_list.append(vers)
        X_lens.append(len(vers))
X= np.concatenate(m_list)
remodel = hmm.GaussianHMM(n_components=3, covariance_type="full", n_iter=100)
remodel.fit(X,X_lens)

filename = "url_sample.txt"
N = 3
T = 10
with open(filename) as f:
    for line in f:
        # 切割参数
        result = urlparse.urlparse(line)
        # url解码
        query = urllib.unquote(result.query)
        params = urlparse.parse_qsl(query, True)
        print params
        for k, v in params:
            if ischeck(v) and len(v) >=N :
                vers = etl(v)
                pro = remodel.score(vers)
                if pro <= T:
                    print  "PRO:%d V:%s LINE:%s " % (pro,v,line)
