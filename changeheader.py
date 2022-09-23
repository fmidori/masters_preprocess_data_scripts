import sys

fastafile = str(sys.argv[1])
maturefile = str(sys.argv[2])
outfile = open(maturefile + str(".modsp"), 'w')  
with open(fastafile, 'r') as f:
    header_list = []
    cont = 0
    for line in f:
        if line.startswith(">"):
            cont +=1
            if line.startswith(">as"):
                header = line.split('|')[0] + '|' + str(cont)
                header_list.append(header)
            elif "[" in line:
                #header = line.split(' ')[0] + '|' + line.split('[')[1]
                species = line.split('[')[1]
                species2 = species.split(']')[0]
                header = '>' + species.split(' ')[0] + '_' + species2.split(' ')[1] + '|' + str(cont)
                header_list.append(header)
            elif bool(line[1].isdigit())==True:
                #header = line.split(',')[0] + '|' + "TickSialoFam"
                header = ">TickSialoFam" + '|' + str(cont)
                header_list.append(header)
            elif "OS=" in line:
                species = line.split('OS=')[1]
                #header = line.split(' ')[0] + '|' + species.split(' ')[0] + ' ' + species.split(' ')[1]
                header = '>' + species.split(' ')[0] + '_' + species.split(' ')[1] + '|' + str(cont)
                header_list.append(header)
#print(header_list)
f.close()

with open(maturefile, 'r') as m:
    for line in m:
        if line.startswith('>'):
            number = int(line.split('_')[2]) #for Gly_Hya [2]
            #print(number)
            #header = header_list[number-1]
            #print(header)
            outfile.write(str(header_list[number-1]) + '\n')
        else:
            outfile.write(str(line) + '\n')
m.close()
outfile.close()




