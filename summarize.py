import csv 
import pandas as pd

def col_num(tsv):
    reader = csv.reader(open(tsv),delimiter='\t')
    num =  int(len(next(reader)))
    return num 

def sum_of_col(tsv,col_num):
    df = pd.read_csv(tsv, sep='\t', header=None)
    sum_col = df.iloc[:,col_num].sum()
    return sum_col 


def dic_fam(tsv):
    #tpm_col = col_num(tsv) - 1 
    with open(tsv,"r") as t:
        famdic = {}
        tpmdic = {}
        #high_sum_tpm = 0 
        #for i in range(8,tpm_col):
         #   sum_tpm = sum_of_col(tsv,i)
          #  if (float(sum_tpm) > float(high_sum_tpm)):
           #     high_sum_tpm = sum_tpm 
            #    col = int(i) #column with highest TPM
       # print(str(tsv) + " " + str(col) + " " + str(high_sum_tpm))
        for line in t:
            has_tpm = False 
            tpm = float(line.split('\t')[9].strip())
            if tpm >= 1:
                has_tpm = True

            #score = int(line.split('\t')[4].strip())
            signalp = str(line.split('\t')[8].strip())

            if (has_tpm == True) and (signalp == "SP(Sec/SPI)"):
                fam = line.split('\t')[1].strip()
                if fam in famdic:
                    famdic[fam] += 1
                    tpmdic[fam] += tpm
                else:
                    famdic[fam] = 1 
                    tpmdic[fam] = tpm
    
    avgdic = {}
    for key in tpmdic.keys():
        avgdic[key] = tpmdic[key]/famdic[key]

    return famdic,avgdic

def dic_to_df(dic,tsv):
    #name = tsv #.split(".")[2].split(".")[0]
    #df = pd.DataFrame.from_dict(dic, orient="index",columns=[tsv])
    df = pd.DataFrame(list(dic.items()),columns=['Component', tsv])
    return df 

if __name__ == "__main__":
    tsvs = ["I_holocyclus","I_ricinus_SG","I_ricinus_WB","O_turicata",
             "R_appendiculatus","R_bursa","R_microplus","R_pulchellus"]
             #,"O_brasiliensis"]

    list_fam = []
    list_tpm = []
    for tsv in tsvs:
        table = "classification_results." + tsv + ".tsv.signalpAndTPM"
        famdic,avgdic = dic_fam(table)
        list_tpm.append(avgdic)
        list_fam.append(famdic)
        
         
    for i in range(len(list_fam)):
        if i == 0:
            df_fam = dic_to_df((list_fam[0]),tsvs[0])
            df_tpm = dic_to_df((list_tpm[0]),tsvs[0])
        else:
            df_fam = pd.merge(df_fam,dic_to_df(list_fam[i],tsvs[i]),on=["Component"],how="outer")
            df_tpm = pd.merge(df_tpm,dic_to_df(list_tpm[i],tsvs[i]),on=["Component"], how="outer")
        #print(df_fam)

        #df = pd.merge(df_fam,df_tpm, on=["Component"])
    df_fam.fillna(0, inplace=True)
    df_tpm.fillna(0, inplace=True)
    #print(df_fam)
    #print(df_tpm)
    df_fam.to_csv("./tick_toxins_total.tsv", sep='\t')
    df_tpm.to_csv("./tick_toxins_tpm.tsv", sep='\t')
        #pd.concat(famdic,avgdic)
       
        
