#!/bin/bash

pepfile=${1}
dirname=${2}
list_add=${3}
MSA=${4}

cd "$dirname"
echo "dirname is $dirname"
echo "pepfile with original sequences is $pepfile"
echo "original number of seq is `grep -c '>' $pepfile`"
echo "list of sequences to add is $list_add"

#take only ids from sequences names
#for ticks cut -f 1 -d ' ' 
cut -f 1 -d ' ' $list_add > "$list_add".uniprotID

#retrieve sequences from database 
blastdbcmd -db ../ArachnidaToxProt_add/ArachnidaToxProt_add -dbtype prot \
  -entry_batch $list_add.uniprotID -out $list_add.toxprot.pep 

#concatenate both files (original and added sequences)
cat $pepfile $list_add.toxprot.pep > $pepfile.added_without_cdhit.pep
echo "number of seqs after concat: `grep -c '>' $pepfile.added_without_cdhit.pep`"

#remove redundancy
cd-hit -i $pepfile.added_without_cdhit.pep -c 1.0  -aS 1.0 -aL 1.0  -o $pepfile.with_added.pep \
  1>cdhit.out 2>cdhit.err 
echo "number of seq without redundancy: `grep -c '>' $pepfile.with_added.pep`" 

#modify seq names, to just the name of family plus number
awk '/^>/{print ">'$dirname'_" ++i; next}{print}' $pepfile.with_added.pep \
  > $pepfile.with_added.mod.pep 
echo "final seq number with added seqs: `grep -c '>' $pepfile.with_added.mod.pep`"

#select only mature seqs 
if [ ! -f "$dirname.complete_added_mature.fasta" ]; then
   signalp -fasta "$pepfile.with_added.mod.pep" -mature -stdout -prefix "$dirname.complete_added" 1> signalp.out 2>signalp.err 
else
    echo "signalp already done"
fi 
echo "seqs with signalp: `grep -c '>' $dirname.complete_added_mature.fasta`"

#concat in one file only mature seqs
if [ ! -f $dirname.mature_added.pep ]; then
  grep '>' $pepfile.with_added.mod.pep > temp
  grep '>' $dirname.complete_added_mature.fasta >> temp
  sort temp | uniq -u | sed 's/>//' > temp1
  seqtk subseq $pepfile.with_added.mod.pep temp1 > temp2
  cat $dirname.complete_added_mature.fasta temp2 > $dirname.mature_added.pep
  rm temp temp1 temp2 
fi
echo "mature sequences final: `grep -c '>' $dirname.mature_added.pep`"

#get the id of longest seq
longseq=$( python3 ../seqlen.py "$dirname.mature_added.pep" | sort -nrk2 | head -1 | cut -f 1 )
echo "longest sequence is $longseq"

pepfile2="$dirname.mature_added.pep"
echo "pepfile2: $pepfile2"

#generate MSA according to chosen software
if [ $MSA == "clustalo" ]; then
    clustalo -i "$pepfile2" -o "$pepfile2.msa"  --threads=8 # --outfmt=clu  --threads=8 --infmt=fa  
    echo "clustalo performed"
fi

if [ $MSA == "mafft" ]; then
   linsi --thread 8 --maxiterate 1000 $pepfile2 > "$pepfile2.msa" 2> "mafft.out"
fi

if [ $MSA == "probcons" ]; then
    probcons -ir 1000 "$pepfile2" > "$pepfile2.msa" 2>"probcons.out" 
    echo "probcons performed"
fi

#retrive longest seq
echo "$longseq" > subject.header
seqtk subseq "$dirname.mature_added.pep" subject.header > subject.pep
rm subject.header

#get index of longest seq in MSA
index=$( grep '>' "$pepfile2.msa" | grep -w -n "$longseq" | cut -f 1 -d ':' )
#index=$( sed '1,3d' "$pepfile.msa" | grep -n "$longseq" | head -1 | cut -f 1 -d ':' )
echo "index in msa: $index"

#generate PSSM with added seqs
if [ ! -f $pepfile2.pssm ]; then
   psiblast -subject subject.pep -in_msa "$pepfile2.msa" -out_ascii_pssm \
  "$pepfile2.ascii.pssm" -out_pssm "$pepfile2.pssm" -msa_master_idx "$index" \
  1>psiblast.out
fi

echo "$pepfile2.pssm" > list

makeprofiledb -in list -title "$pepfile2.db.rps" -out "$pepfile2.db.rps"  -blastdb_version 5 -dbtype rps 
rpsblast -db $pepfile2.db.rps  -query "$pepfile2" -out rpsblast_teste_added.output \
  -evalue 1e-5 -outfmt 6
echo "found: `cut -f 1 rpsblast_teste_added.output | sort | uniq | wc -l`"
rm $pepfile2.db.rps.*

cp $pepfile2.pssm ../added_pssms/

