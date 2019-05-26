import os
import util_fasta
from Bio.SeqUtils import GC
import csv
from sklearn.externals.joblib import dump, load
#import random
#import string
#import shutil

def generar_modelo_CPAT(archivo_lncRNA, archivo_PCT, archivo_CDS, carpeta_cpat):
    _generar_modelo_CPAT_hexamer(archivo_lncRNA, archivo_CDS, carpeta_cpat)
    _generar_modelo_CPAT_logit(archivo_lncRNA, archivo_PCT, carpeta_cpat)

def _generar_modelo_CPAT_hexamer(archivo_lncRNA, archivo_CDS, carpeta_cpat):
    script = "~/anaconda3/bin/make_hexamer_tab.py"
    fasta_cds = "'" + archivo_CDS + "'" 
    fasta_lncRNA = "'" + archivo_lncRNA + "'"
    salida = "'" + carpeta_cpat + "/hexamer.tsv" + "'"
    comando = "{} -c {} -n {} > {}".format(script, fasta_cds, fasta_lncRNA, salida)
    os.system(comando)
    
def _generar_modelo_CPAT_logit(archivo_lncRNA, archivo_PCT, carpeta_cpat):
    script = "~/anaconda3/bin/make_logitModel.py"
    hexamer = "'" + carpeta_cpat + "/hexamer.tsv" + "'"
    fasta_pct = "'" + archivo_PCT + "'" 
    fasta_lncRNA = "'" + archivo_lncRNA + "'"
    salida = "'" + carpeta_cpat + "/fold" + "'"
    comando = "{} -x {} -c {} -n {} -o {}".format(script, hexamer, fasta_pct, fasta_lncRNA, salida)
    os.system(comando)
    
def ejecutar_diamond(archivo_entrada, diamond_db, archivo_salida):
    script = "~/anaconda3/bin/diamond"
    diamond_bd = "'" + diamond_db + "'"
    salida = "'" + archivo_salida + "'"
    comando = "{} blastx -d {} -q {} -o {} -k 5 --gapopen 11 --gapextend 1 --more-sensitive -f 6 qseqid pident length qframe qstart qend sstart send evalue bitscore".format(script, diamond_bd, archivo_entrada, salida)
    os.system(comando)

def ejecutar_cpat(archivo_entrada, carpeta_cpat, archivo_salida):
    script = "~/anaconda3/bin/cpat.py"
    logit = "'" + carpeta_cpat + "/fold.logit.RData" + "'"
    hexamer = "'" + carpeta_cpat + "/hexamer.tsv" + "'"
    salida = "'" + archivo_salida + "'"
    comando = "{} -g {} -d {} -x {} -o {}".format(script, archivo_entrada, logit, hexamer, salida)
    os.system(comando)
    
def generar_features_base(archivo_entrada, archivo_cpat, archivo_diamond, archivo_salida):
    transcritos = util_fasta.leer_fasta(archivo_entrada)
    transcript_dict = {}
    for k in transcritos.keys():
        transcript_dict[k.strip().upper()] = {
            "length" : len(transcritos[k]),
            "gc" : GC(transcritos[k]),
            "orf_length" : 0,
            "orf_coverage" : float(0),
            "hexamer_score" : float(0),
            "fickett_score" : float(0),
            "identity" : float(0),
            "align_length" : float(0),
            "align_perc_len" : float(0),
            "align_perc_orf" : float(0)
        }
    
    #adaptado de https://github.com/gbgolding/crema/blob/master/bin/featuresetup_module.py
    with open(archivo_cpat, "r") as f:
        cpat_reader = csv.reader(f, delimiter=("\t"))
        next(cpat_reader, None) # skip header
        for row in cpat_reader:
            cod_secuencia = row[0]
            transcript_dict[cod_secuencia]["orf_length"] = float(row[2])
            transcript_dict[cod_secuencia]["orf_coverage"] = float(row[2])/float(transcript_dict[cod_secuencia]["length"])
            transcript_dict[cod_secuencia]["fickett_score"] = float(row[3])
            transcript_dict[cod_secuencia]["hexamer_score"] = float(row[4])
    
    with open(archivo_diamond, "r") as f:
        tab_reader = csv.reader(f, delimiter=("\t"))
        line_1 = next(tab_reader)
        first = line_1[0].upper()
        score = [float(line_1[9])]
        with_len = [[first, float(line_1[1]), float(line_1[2]), float(line_1[3]), float(line_1[9])]] # name identity length frame score
        for row in tab_reader:
            if row[0].upper() == first:
                score.append(float(row[9]))
                with_len.append([row[0].upper(), float(row[1]), float(row[2]), float(row[3]), float(row[9])])
            else:
                transcript_dict[first]["identity"] = float(0)
                transcript_dict[first]["align_length"] = float(0)
                max_value = max(score)
                max_index = score.index(max_value)
                max_len_ident = with_len[max_index]
                if max_len_ident[3] > 0:
                    transcript_dict[first]["identity"] = float(max_len_ident[1])
                    transcript_dict[first]["align_length"] = float(max_len_ident[2])
                    transcript_dict[first]["align_perc_len"] = float(transcript_dict[first]["align_length"]/transcript_dict[first]["length"])
                    transcript_dict[first]["align_perc_orf"] = (0 if transcript_dict[first]["orf_length"] == 0 else float(transcript_dict[first]["align_length"]/transcript_dict[first]["orf_length"]))
                score = [float(row[9])]
                first = row[0].upper()
                with_len = [[first, float(row[1]), float(row[2]), float(row[3]), float(row[9])]]
        transcript_dict[first]["identity"] = float(0)
        transcript_dict[first]["align_length"] = float(0)
        max_value = max(score)
        max_index = score.index(max_value)
        max_len_ident = with_len[max_index]
        if max_len_ident[3] > 0:
            transcript_dict[first]["identity"] = float(max_len_ident[1])
            transcript_dict[first]["align_length"] = float(max_len_ident[2])
    #fin de código adaptado de https://github.com/gbgolding/crema/blob/master/bin/featuresetup_module.py
    
    dump(transcript_dict, archivo_salida)

def generar_features(archivo_entrada, features_base, archivo_cpat, archivo_salida):
    transcritos = util_fasta.leer_fasta(archivo_entrada)
    features_globales = load(features_base)
    transcript_dict = {}
    for k in transcritos.keys():
        transcript_dict[k.strip().upper()] = {
            "length" : features_globales[k.strip().upper()]["length"],
            "gc" : features_globales[k.strip().upper()]["gc"],
            "orf_length" : features_globales[k.strip().upper()]["orf_length"],
            "orf_coverage" : features_globales[k.strip().upper()]["orf_coverage"],
            "hexamer_score" : float(0),
            "fickett_score" : float(0),
            "identity" : features_globales[k.strip().upper()]["identity"],
            "align_length" : features_globales[k.strip().upper()]["align_length"],
            "align_perc_len" : features_globales[k.strip().upper()]["align_perc_len"],
            "align_perc_orf" : features_globales[k.strip().upper()]["align_perc_orf"]
        }
    
    with open(archivo_cpat, "r") as f:
        cpat_reader = csv.reader(f, delimiter=("\t"))
        next(cpat_reader, None) # skip header
        for row in cpat_reader:
            cod_secuencia = row[0].strip().upper()
            if cod_secuencia in transcript_dict:
                transcript_dict[cod_secuencia]["fickett_score"] = float(row[3])
                transcript_dict[cod_secuencia]["hexamer_score"] = float(row[4])
                
    dump(transcript_dict, archivo_salida)
