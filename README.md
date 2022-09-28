## Scripts in python and Bash used in my Master's Thesis to perform preprocessing of data 

- GenerateProfile.sh: Generate PSSM profile from fasta file (convert to MSA) and run RPSBLAST to test. 

- MakeNewPSSM.sh: generate PSSM profile from fasta with added sequences from ToxProt database. The MSA created can be Probcons, Clustalo or MAFFT. 

- run_toxprot.sh: Run tool PSIBLAST vs ToxProt database and remove redundancy with CDHIT. 

- changeheader.py: Change header names of fasta file to standardize file as "protein|species_of_origin|number"

- changeheaderIP.py: Change header names of fasta file to standardize file for InterproScan (IP) analysis as "protein|species_of_origin|database_of_origin|family_name|number"

- createtable.py: Generate tsv file with information of protein id, species and domains found in InterproScan. 

- generate_table.py: Generate tsv with information from prediction of proteins (TransDecoder longorfs), classification of toxins (ArachnoFamTox), prediction of signal peptide (SignalP), Transcritps per million kilo bases (TPM - RSEM) and identification of toxins performed by BLASTp vs ToxProt database. 

- parsehmmscan.py: Parse HMMSCAN 3 DomTab output.
