import sys

fastafile = str(sys.argv[1]) 
maturefile = str(sys.argv[2])
fam_name = str(sys.argv[3])
outfile = open(maturefile + str(".modip"), 'w')  

with open(fastafile, 'r') as f:
    header_list = []
    cont = 0
    for line in f:
        if line.startswith(">"):
            cont +=1
            #name|species|origin|id_arachnida(fam_num)
            if line.startswith(">as"):
                header = line.split('|')[0] + '|Spider|' +'AS|' + str(fam_name) + '_' + str(cont) 
                #header = str(id_uniprot) + '|Spider|' + 'Uniprot|' + str(fam_name) + '_' + str(cont) 
                header_list.append(header)
            elif "[" in line:
                #header = line.split(' ')[0] + '|' + line.split('[')[1]
                species = line.split('[')[1]
                species2 = species.split(']')[0]
                header = line.split(' ')[0] + '|' + species.split(' ')[0] + '_' + species2.split(' ')[1] +'|TSA|' + fam_name+ '_' + str(cont)
                header_list.append(header)
            elif bool(line[1].isdigit())==True:
                #header = line.split(',')[0] + '|' + "TickSialoFam"
                header = str(line.split(',')[0]) + '|Tick|TickSialoFam|' + str(fam_name)+ '_' + str(cont)
                header_list.append(header)
            elif "OS=" in line:
                species = line.split('OS=')[1]
                if line.startswith(">sp|"):
                    #header = line.split(' ')[0] + '|' + species.split(' ')[0] + ' ' + species.split(' ')[1]
                    header =  ">" + str(line.split('|')[1]) + '|' +  species.split(' ')[0] + '_' + species.split(' ')[1] +'|Uniprot|' + str(fam_name)+ '_' + str(cont)
                    header_list.append(header)
                elif line.startswith(">tr|"):
                    #header = line.split(' ')[0] + '|' + species.split(' ')[0] + ' ' + species.split(' ')[1]
                    header =  ">" + str(line.split('|')[1]) + '|' +  species.split(' ')[0] + '_' + species.split(' ')[1] +'|Uniprot|' + str(fam_name)+ '_' + str(cont)
                    header_list.append(header)
                else:
                    header =  str(line.split(' ')[0]) + '|' +  species.split(' ')[0] + '_' + species.split(' ')[1] +'|Uniprot|' + str(fam_name)+ '_' + str(cont)
                    header_list.append(header)
            elif line.startswith('>JA'):
                header = str(line.split(' ')[0]) + '|Tick|TickSialoFam|' + str(fam_name)+ '_' + str(cont)
                header_list.append(header)
            elif line.startswith('>AE'):
                header = str(line.split(' ')[0]) + '|Tick|TickSialoFam|' + str(fam_name)+ '_' + str(cont)
                header_list.append(header)
           # else: print(line)
#print(len(header_list))
f.close()

with open(maturefile, 'r') as m:
    for line in m:
        if line.startswith('>'):
            number = int(line.split('_')[1])
            #number = int(line.split('_')[2]) #gly_hya
            #print(number)
            #header = header_list[number-1]
            #print(header)
            outfile.write(str(header_list[number-1]) + '\n')
        else:
            outfile.write(str(line))
m.close()
outfile.close()




