'''print info for Sentinel2 zip files downloaded to current directory
'''
import os
import sys

x= [y.strip() for y in os.popen("ls -1 | grep S2").readlines()]

total = 0
out = 0
for f in x:
    #print(f)
    lines = [L.strip() for L in open(f).readlines()]
    for line in lines:
        w = line.strip().split()
        w[0] = w[0].replace('-', '')
        ds = w[3].split('_')[2].split('T')[0]
        #print(w, ds)


        total += 1
        if len(w) != 4:
            print("Err:" + w); sys.exit(1)

        if ds != w[0]:
            print(f, ":", ds, w); #sys.exit(1)
            out+= 1

print("out", out)
print("total", total)
print(100. * out/total )
