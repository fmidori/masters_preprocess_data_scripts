import sys 

def gen_dic(tsv):
    dic = {}
    with open(tsv, "r") as t:
        for line in t:
            header = line.split('\t')[0].strip()
            score = line.split('\t')[1].strip()
                #header = line.split('\t')[0].rsplit('.',1)[0]
            dic[header] = score
    return dic

def first_hit(tsv):
    output = open(tsv + ".first_hit" , "w")
    with open(tsv, "r") as t:
        prev_header = "header"
        for line in t:
            header = line.split('\t')[0].strip()
            if header != prev_header:
                output.write(line)
                prev_header = header
    return str(tsv + ".first_hit")

def all_headers(fasta):
    headers = []
    with open(fasta, "r") as f:
        for line in f:
            if line.startswith(">"):
                header = line.split(" ")[0].replace(">","")
                headers.append(header)
    return headers
                
def get_headers(tsv):
    headers = []
    with open(tsv, "r") as t:
        for line in t:
            header = line.split('\t')[0]
            headers.append(header)
    return headers

def gen_sets(tick): 
    fasta     = "longest_orfs.cdhit." + str(tick) + ".pep" 
    class_tsv = "classification_results." + str(tick) + ".tsv"
    signalp   = str(tick) + ".complete.signalp"
    tpm       = "TPM.RSEM." + str(tick)
    toxprot   = "toxprot_results." + str(tick) + ".tsv"

    toxprot_fh = first_hit(toxprot) #only first hit of toxprot
    all_toxins = get_headers(class_tsv) + get_headers(toxprot_fh) 
    all_prot  = all_headers(fasta) #list with all headers
    non_toxins = list(set(all_prot) - set(all_toxins))

    signalp_dic = gen_dic(signalp)
    tpm_dic = gen_dic(tpm)

    files = [ class_tsv , toxprot_fh ] 
    
    for f in files:
        out = open(f + ".signalpAndTPM" , "w" )
        print(f)
        with open(f, "r") as t:
            signalp_pos = 0 
            signalp_neg = 0 
            for line in t:
                header_signalp  = line.split('\t')[0].strip()
                header_tpm = line.split('\t')[0].rsplit('.',1)[0]

                if float(tpm_dic[header_tpm]) >= 1:
                    if signalp_dic[header_signalp] == "SP(Sec/SPI)":
                        signalp_pos += 1 
                        out.write(line.strip() + "\t" + signalp_dic[header_signalp] + "\t" + tpm_dic[header_tpm] + "\n")
                    elif signalp_dic[header_signalp] == "OTHER":
                        signalp_neg += 1
        print("with","without")
        print(signalp_pos, signalp_neg)

    signalp_pos_nt = 0
    signalp_neg_nt = 0
    for i in non_toxins:
        header_tpm = i.rsplit('.',1)[0]
        if float(tpm_dic[header_tpm]) >= 1:
            if signalp_dic[i] == "SP(Sec/SPI)":
                signalp_pos_nt += 1 
            elif signalp_dic[i] == "OTHER":
                signalp_neg_nt += 1
    

    print("with NonToxins","without NonToxins")
    print(signalp_pos_nt, signalp_neg_nt)
    return None


if __name__ == "__main__":
    ticks = ["I_holocyclus","I_ricinus_SG","I_ricinus_WB","O_turicata",
             "R_appendiculatus","R_bursa","R_microplus","R_pulchellus",
             "O_brasiliensis"]
    for i in ticks:
        gen_sets(i)

    #print(all_headers("longest_orfs.cdhit.O_turicata.pep"))

