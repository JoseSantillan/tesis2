import os
import util_bd, util_fasta
from Bio.SeqUtils import GC
import csv
from sklearn.externals.joblib import dump, load
import random
import string

def generar_modelo_CPAT(identificador, codigos_lncRNA, codigos_PCT):
    archivos = _rutas_archivos(identificador)
    if os.path.isdir(archivos["cpat"]["directorio_base"]):
        return
    _generar_directorios_cpat(archivos)
    _generar_data_cpat(archivos, codigos_lncRNA, codigos_PCT)
    _generar_modelo_cpat(archivos)

def generar_caracteristicas(identificador, transcritos):
    archivos = _rutas_archivos(identificador)
    if not os.path.isdir(archivos["cpat"]["directorio_base"]):
        raise Exception("No se encontró la carpeta del modelo CPAT {}, probablemente aún no ha generado este modelo. Ruta buscada: {}".format(identificador, archivos["cpat"]["directorio_base"]))
    _generar_transcritos_fasta(archivos, transcritos)
    _generar_caracteristicas_cpat(archivos, archivos["transcritos_fasta"])
    _generar_caracteristicas_diamond(archivos, archivos["transcritos_fasta"])
    _generar_caracteristicas(archivos, transcritos)

def generar_caracteristicas_cpat(identificador, transcritos):
    archivos = _rutas_archivos(identificador)
    if not os.path.isdir(archivos["cpat"]["directorio_base"]):
        raise Exception("No se encontró la carpeta del modelo CPAT {}, probablemente aún no ha generado este modelo. Ruta buscada: {}".format(identificador, archivos["cpat"]["directorio_base"]))
    _generar_transcritos_fasta(archivos, transcritos)
    _generar_caracteristicas_cpat(archivos, archivos["transcritos_fasta"])
    
def existe_modelo_cpat(identificador):
    archivos = _rutas_archivos(identificador)
    return os.path.isdir(archivos["cpat"]["directorio_base"])
    
def _rutas_archivos(identificador):
    if not os.path.isdir("./CPAT"):
        os.mkdir("./CPAT")
    if not os.path.isdir("./Diamond"):
        os.mkdir("./Diamond")
    if not os.path.isdir("./features"):
        os.mkdir("./features")
    
    archivos = {}
    archivos["cpat"] = { "directorio_base" : "./CPAT/{}".format(identificador) }
    archivos["cpat"]["data"] = { "directorio" : "{}/data".format(archivos["cpat"]["directorio_base"]) }
    archivos["cpat"]["data"]["lncRNA"] = "{}/lncRNA.fasta".format(archivos["cpat"]["data"]["directorio"])
    archivos["cpat"]["data"]["PCT"] = "{}/PCT.fasta".format(archivos["cpat"]["data"]["directorio"])
    archivos["cpat"]["data"]["CDS"] = "{}/CDS.fasta".format(archivos["cpat"]["data"]["directorio"])
    archivos["cpat"]["modelo"] = { "directorio" : "{}/modelo".format(archivos["cpat"]["directorio_base"]) }
    archivos["cpat"]["modelo"]["hexamer"] = "{}/hexamer.tsv".format(archivos["cpat"]["modelo"]["directorio"])
    archivos["cpat"]["modelo"]["prefijo_logit"] = "{}/{}".format(archivos["cpat"]["modelo"]["directorio"], identificador)
    archivos["cpat"]["modelo"]["logit"] = "{}.logit.RData".format(archivos["cpat"]["modelo"]["prefijo_logit"])
    archivos["cpat"]["modelo"]["prefijo_cpat"] = "{}/{}".format(archivos["cpat"]["modelo"]["directorio"], identificador)
    archivos["cpat"]["salida"] = "{}.dat".format(archivos["cpat"]["modelo"]["prefijo_cpat"])
    archivos["cpat"]["scripts"] = {
        "script_hexamer" : "~/anaconda3/bin/make_hexamer_tab.py",
        "script_logit" : "~/anaconda3/bin/make_logitModel.py",
        "script_cpat" : "~/anaconda3/bin/cpat.py"
    }
    archivos["diamond"] = { "directorio_base" : "./Diamond" }
    archivos["diamond"]["bd"] = "{}_BD/uniprot-viridiplantae-reviewed.dmnd".format(archivos["diamond"]["directorio_base"])
    archivos["diamond"]["script"] = "~/anaconda3/bin/diamond"
    archivos["diamond"]["salida"] = "{}/{}.tsv".format(archivos["diamond"]["directorio_base"], identificador)
    archivos["transcritos_fasta"] = "./data/{}.fasta".format(identificador)
    archivos["features"] = { "directorio_base" : "./features"}
    archivos["features"]["salida"] = "{}/{}.feat".format(archivos["features"]["directorio_base"], identificador)
    return archivos
    
def _generar_directorios_cpat(archivos):
    os.mkdir(archivos["cpat"]["directorio_base"])
    os.mkdir(archivos["cpat"]["data"]["directorio"])
    os.mkdir(archivos["cpat"]["modelo"]["directorio"])

def _generar_data_cpat(archivos, codigos_lncRNA, codigos_PCT):
    query = "SELECT cod_secuencia, secuencia FROM secuencias WHERE cod_secuencia IN ('{}')".format("', '".join(codigos_lncRNA))
    secuencias = util_bd.resultados_query(query)
    util_fasta.generar_fasta(secuencias, archivos["cpat"]["data"]["lncRNA"])
    query = "SELECT cod_secuencia, secuencia FROM secuencias WHERE cod_secuencia IN ('{}')".format("', '".join(codigos_PCT))
    secuencias = util_bd.resultados_query(query)
    util_fasta.generar_fasta(secuencias, archivos["cpat"]["data"]["PCT"])
    query = "SELECT cod_secuencia, coding FROM secuencias_CDS WHERE cod_secuencia IN ('{}')".format("', '".join(codigos_PCT))
    secuencias = util_bd.resultados_query(query)
    util_fasta.generar_fasta(secuencias, archivos["cpat"]["data"]["CDS"])

def _generar_modelo_cpat(archivos):
    _generar_hexamer_cpat(archivos)
    _generar_logit_cpat(archivos)
    
def _generar_hexamer_cpat(archivos):
    script = archivos["cpat"]["scripts"]["script_hexamer"]
    fasta_cds = "'" + archivos["cpat"]["data"]["CDS"] + "'" 
    fasta_lncRNA = "'" + archivos["cpat"]["data"]["lncRNA"] + "'"
    salida = "'" + archivos["cpat"]["modelo"]["hexamer"] + "'"
    comando = "{} -c {} -n {} > {}".format(script, fasta_cds, fasta_lncRNA, salida)
    os.system(comando)
    
def _generar_logit_cpat(archivos):
    script = archivos["cpat"]["scripts"]["script_logit"]
    hexamer = "'" + archivos["cpat"]["modelo"]["hexamer"] + "'"
    fasta_pct = "'" + archivos["cpat"]["data"]["PCT"] + "'" 
    fasta_lncRNA = "'" + archivos["cpat"]["data"]["lncRNA"] + "'"
    salida = "'" + archivos["cpat"]["modelo"]["prefijo_logit"] + "'"
    comando = "{} -x {} -c {} -n {} -o {}".format(script, hexamer, fasta_pct, fasta_lncRNA, salida)
    os.system(comando)

def _generar_transcritos_fasta(archivos, transcritos):
    transcritos_array = transcritos.items()
    util_fasta.generar_fasta(transcritos_array, archivos["transcritos_fasta"])
    
def _generar_caracteristicas_cpat(archivos, transcritos_fasta):
    script = archivos["cpat"]["scripts"]["script_cpat"]
    logit = "'" + archivos["cpat"]["modelo"]["logit"] + "'"
    hexamer = "'" + archivos["cpat"]["modelo"]["hexamer"] + "'"
    salida = "'" + archivos["cpat"]["modelo"]["prefijo_cpat"] + "'"
    comando = "{} -g {} -d {} -x {} -o {}".format(script, transcritos_fasta, logit, hexamer, salida)
    os.system(comando)

def _generar_caracteristicas_diamond(archivos, transcritos_fasta):
    script = archivos["diamond"]["script"]
    diamond_bd = "'" + archivos["diamond"]["bd"] + "'"
    salida = "'" + archivos["diamond"]["salida"] + "'"
    comando = "{} blastx -d {} -q {} -o {} -k 5 --gapopen 11 --gapextend 1 --more-sensitive -f 6 qseqid pident length qframe qstart qend sstart send evalue bitscore".format(script, diamond_bd, transcritos_fasta, salida)
    os.system(comando)

def _generar_caracteristicas(archivos, transcritos):
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
    
    with open(archivos["cpat"]["salida"], "r") as f:
        cpat_reader = csv.reader(f, delimiter=("\t"))
        for row in cpat_reader:
            cod_secuencia = row[0]
            transcript_dict[cod_secuencia]["orf_length"] = float(row[2])
            transcript_dict[cod_secuencia]["orf_coverage"] = float(row[2])/float(transcript_dict[cod_secuencia]["length"])
            transcript_dict[cod_secuencia]["fickett_score"] = float(row[3])
            transcript_dict[cod_secuencia]["hexamer_score"] = float(row[4])
    
    #adaptado de https://github.com/gbgolding/crema/blob/master/bin/featuresetup_module.py
    with open(archivos["diamond"]["salida"], "r") as f:
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
    
    dump(transcript_dict, archivos["features"]["salida"])

def obtener_caracteristicas(identificador, id_cpat, transcritos):
    archivos = _rutas_archivos(identificador)
    archivos_cpat = _rutas_archivos(id_cpat)
    if not os.path.isfile(archivos["features"]["salida"]):
        raise Exception("Debe primero generar la base de datos de caracteristicas " + identificador)
    if not os.path.isfile(archivos_cpat["cpat"]["salida"]):
        raise Exception("Debe primero generar la base de datos de caracteristicas para CPAT " + id_cpat)
    
    features_globales = load(archivos["features"]["salida"])
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
    
    with open(archivos_cpat["cpat"]["salida"], "r") as f:
        cpat_reader = csv.reader(f, delimiter=("\t"))
        for row in cpat_reader:
            cod_secuencia = row[0].strip().upper()
            if cod_secuencia in transcript_dict:
                transcript_dict[cod_secuencia]["fickett_score"] = float(row[3])
                transcript_dict[cod_secuencia]["hexamer_score"] = float(row[4])
    
    return transcript_dict
