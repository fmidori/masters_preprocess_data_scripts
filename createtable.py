import sys 

def domains(tsv):
    with open(tsv, 'r') as t:
        domains = {}
        c = 2 
        for line in t:
            dom = line.split('\t')[4]
            if dom not in domains:
                domains[dom] = c
                c += 1 
    return domains 

def create_table(tsv, dom):
    table = open( tsv + '.domains', 'w')
    ls = list(dom.keys())
    ls.insert(0, 'prot_id' )
    ls.insert(1, 'species' )
    lendom = len(dom) + 2
    with open(tsv, 'r') as t:
        for last_line in t:
            pass

    with open(tsv, 'r') as t:
        ant = 'prot_id'  
        for line in t:
            if line.startswith('sp|'):
                header = line.split('\t')[0].split('|')[1]
                specie = line.split('\t')[0].split('|')[3]
            elif line.startswith('as:'):
                header = line.split('\t')[0]
                if '|' in header:
                    header = line.split('|')[0]
                specie = 'Spider'  
            else:
                header = line.split('\t')[0].split('|')[0]
                specie = line.split('\t')[0].split('|')[1]
            coord = '[' + line.split('\t')[6] + ',' + line.split('\t')[7] + ']'
            domain = line.split('\t')[4]
            evalue = line.split('\t')[8]
            if header == ant:
                ls[dom[domain]] = str(coord + '|' + evalue)
            else: 
                new_line = '\t'.join(ls)
                table.write(str(new_line) + '\n')
                ls = ['-'] * lendom 
                ls[0] = header
                ls[1] = specie
                ls[dom[domain]] = str(coord + '|' + evalue)
            if line == last_line:
                new_line = '\t'.join(ls)
                table.write(str(new_line) + '\n')
            ant = header
    return None  





if __name__ == "__main__":
    tsv = str(sys.argv[1])
    dom = domains(tsv)
    create_table(tsv,dom)




