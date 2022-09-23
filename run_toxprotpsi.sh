#!/bin/bash

dirname=${2}

cd "$dirname"
echo "dirname is $dirname"

pepfile=${1}
echo "pepfile is $pepfile" 

psiblast -query "$pepfile"  -db ../toxprot_db/toxprot -out "$dirname.psiblast.out" -evalue 1e-6 \
  -num_threads 8 -num_iterations 0 -inclusion_ethresh 1e-6 -max_target_seqs 50 -outfmt \
  '6 qseqid sseqid pident mismatch positive gapopen qcovs ppos evalue bitscore qlen  \
  slen qstart qend length'  2>psiblast.toxprot.err

echo "psiblast performed with toxprot database"

cut -f 2 "$dirname.psiblast.out" | cut -f 2 -d '|' | sort | uniq > "$dirname.header"

blastdbcmd -db ../toxprot_db/toxprot -dbtype prot -entry_batch "$dirname.header" \
  -out "$dirname.toxprot"

cd-hit -i "$dirname.toxprot" -o "$dirname.toxprot.cdhit.pep" -c 0.98 -aS 0.98 -T 8 \
  &>toxprot.cdhit 

echo "cdhit performed on toxprot proteins"
echo "number of proteins is `grep -c '>' $dirname.toxprot.cdhit.pep`"

cat "$pepfile" "$dirname.toxprot.cdhit.pep" > "$pepfile.complete"

cd-hit -i "$pepfile.complete" -o "$pepfile.complete.cdhit" -c 1.0 -aS 1.0 -aL 1.0 -T 8 \
  &>cdhit.compl.out  

echo "with duplicates `grep -c '>' $pepfile.complete`"
echo "number of total  proteins is `grep -c '>' $pepfile.complete.cdhit`"

