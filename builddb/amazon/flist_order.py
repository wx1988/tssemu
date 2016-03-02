lines = open("bad_review_list.csv","r").readlines()

rdic = {str(d):chr( ord('A')+d) for d in range(10)}
print rdic
outf = open("bad_review_list_replace.csv", 'w')
for line in lines:
    line = line.strip()
    for d in rdic.keys():
        line = line.replace( d, rdic[d])
    print>>outf,line
outf.close()
