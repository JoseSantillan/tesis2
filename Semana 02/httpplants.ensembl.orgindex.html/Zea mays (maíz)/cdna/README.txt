#### README ####

IMPORTANT: Please note you can download correlation data tables,
supported by Ensembl, via the highly customisable BioMart and
EnsMart data mining tools. See http://www.ensembl.org/biomart/martview or
http://www.ebi.ac.uk/biomart/ for more information.

##################
Fasta cDNA dumps
#################

These files hold the cDNA sequences corresponding to Ensembl gene 
predictions. cDNA consists of transcript sequences for actual and possible
genes, including pseudogenes, NMD and the like. See the file names 
explanation below for different subsets of both known and predicted 
transcripts.

------------
FILE NAMES
------------
The files are consistently named following this pattern:
<species>.<assembly>.<sequence type>.<status>.fa.gz

<species>: The systematic name of the species.
<assembly>: The assembly build name.
<sequence type>: cdna for cDNA sequences
<status>
  * 'cdna.all' - the super-set of all transcripts resulting from
     Ensembl gene predictions (see more below).
  * 'cdna.abinitio' - transcripts resulting from 'ab initio' gene prediction
     algorithms such as SNAP and GENSCAN. In general all 'ab initio'
     predictions are solely based on the genomic sequence and do not
     use other experimental evidence. Therefore, not all GENSCAN or SNAP
     cDNA predictions represent biologically real cDNAs.
     Consequently, these predictions should be used with care.

EXAMPLES  (Note: Most species do not sequences for each different <status>)
  for Human:
    Homo_sapiens.NCBI36.cdna.all.fa.gz
      cDNA sequences for all transcripts
    Homo_sapiens.NCBI36.cdna.abinitio.fa.gz
      cDNA sequences for 'ab-initio' prediction transcripts.

FASTA Sequence Header Lines
------------------------------
The FASTA sequence header lines are designed to be consistent across
all types of Ensembl FASTA sequences.  This gives enough information
for the sequence to be identified outside the context of the FASTA file.

General format:

>ID SEQTYPE:STATUS LOCATION GENE

Example of an Ensembl cDNA header:

>ENST00000289823 cdna chromosome:NCBI35:8:21922367:21927699:1 gene:ENSG00000158815 gene_biotype:protein_coding transcript_biotype:protein_coding
 ^               ^    ^     ^                                       ^                    ^                           ^       
 ID              |    |  LOCATION                         GENE: gene stable ID        GENE: gene biotype        TRANSCRIPT: transcript biotype
                 |  STATUS
              SEQTYPE


