from Bio import SearchIO 
import sys 

hmmFile = sys.argv[1]
#threshold = float(sys.argv[2])

with open(hmmFile, 'r') as f:
    for record in SearchIO.parse(f, 'hmmscan3-domtab'):
        #print(str(record.id) + '\t')
        hits = record.hits
        hsps = record.hsps
        num_hits = len(hits)
        num_hsps = len(hsps)

        if num_hits > 0:
            for i in range(0,num_hits):
                if (hsps[i].evalue <= 0.1) or (hsps[i].evalue == 0):
                    print(str(record.id) + '\t' + str(hits[i].id) + '\t' + str(hsps[i].evalue) + '\t' +
                            str(hsps[i].bitscore) + '\t' + str(hsps[i].acc_avg) +  
                            '\t' +  str(record.seq_len) + '\t' + str(hits[i].description) + '\t' + 
                            str(hsps[i].env_start) + '\t' + str(hsps[i].env_end) )
        else:
            if (hsps.evalue <= 0.1) or (hsps.evalue == 0):
                print(str(record.id) + '\t' + str(hits.id) + '\t' + str(hsps.evalue) + 
                        '\t' + str(hsps.bitscore) + '\t' + str(hsps.acc_avg) + 
                        '\t' +  str(record.seq_len) + '\t' + str(hits.description) + '\t' + 
                        str(hsps.env_start) + '\t' + str(hsps.env_end) )

f.close()
