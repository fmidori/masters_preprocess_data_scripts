import sys 
#from Bio import SeqIO

table = str(sys.argv[1])
#fasta = str(sys.argv[2])

families = {}
with open(table) as t:
    for line in t:
        family = line.split('\t')[1]
        header = line.split('\t')[0]
        if family not in families:
            families[family] = 1 
            fam_file = open(str(family), 'w')
            if bool(header[0].isdigit()) == False:
#                fam_file.write(str(header.split(' ')[0]) +  '\n')
                fam_file.write(str(header) + '\n')
        else: 
            families[family] += 1
            fam_file = open(str(family), 'a')
            if bool(header[0].isdigit()) == False:
#                fam_file.write(str(header.split(' ')[0]) +  '\n')
                fam_file.write(str(header) + '\n')
t.close()
#print(sum(families.values()))
print(families)

#for key in families.keys():
#   fam_file = open(str(key), 'r')
#   fam_pep = open(str(key) + '.pep', 'w')
#   for line in fam_file:


