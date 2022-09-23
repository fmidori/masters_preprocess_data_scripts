#!/bin/bash

dirname=${2}

cd "$dirname"
echo "dirname is $dirname"

touch subject.header
pepfile=${1}
echo "pepfile is $pepfile" 

longseq=$( python3 ../seqlen.py "$pepfile" | sort -nrk2 | head -1 | cut -f 1 )
echo "longest sequence is $longseq"

if [ ! -f "$pepfile.msa" ]; then
    clustalo -i "$pepfile" -o "$pepfile.msa"  --threads=8 # --outfmt=clu  --threads=8 --infmt=fa  
    echo "clustalo performed"
else
    echo "clustalo already done"
fi

echo "$longseq" > subject.header
seqtk subseq "$pepfile" subject.header > subject.pep
rm subject.header

index=$( grep '>' "$pepfile.msa" | grep -n "$longseq" | cut -f 1 -d ':' )
#index=$( sed '1,3d' "$pepfile.msa" | grep -n "$longseq" | head -1 | cut -f 1 -d ':' )
echo "index in msa: $index" 

awk '/^>/{print ">'$dirname'_" ++i; next}{print}' "$pepfile.msa" > "$pepfile.msa.mod"

psiblast -subject subject.pep -in_msa "$pepfile.msa.mod" -out_ascii_pssm "$pepfile.ascii.pssm" \
  -out_pssm "$pepfile.pssm" -msa_master_idx "$index" 1>psiblast.out 

echo "PSSM generated" 

touch list 
echo "$pepfile.pssm" > list 

makeprofiledb -in list -title "$pepfile.db.rps" -out "$pepfile.db.rps" \
  -blastdb_version 5 -dbtype rps 

rpsblast -db "$pepfile.db.rps"  -query "$pepfile" -out rpsblast_teste.output \
  -evalue 1e-3 -outfmt 6

echo "RPS done" 


