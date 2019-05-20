import os

def generar_fasta(secuencias, archivo, tamanio_por_linea=80):
    t_tamanio = tamanio_por_linea
    f = open(archivo ,"w+")
    for transcrito in secuencias:
        f.write(">%s\n" % (transcrito[0].strip().upper()))
        seq = transcrito[1]
        t_partes = [seq[i:i+t_tamanio] for i in range(0, len(seq), t_tamanio)]
        for t_parte in t_partes:
            f.write("%s\n" % (t_parte))
    f.close()

def leer_fasta(archivo, limite = 0):
    transcritos = {}
    cod_secuencia = ""
    secuencia = ""
    f = open(archivo, "r")
    for linea in f:
        if linea.startswith(">"):
            if secuencia != "":
                transcritos[cod_secuencia] = secuencia
                secuencia = ""
                limite -= 1
                if limite == 0:
                    break
            cod_secuencia = linea.rstrip("\n").lstrip(">").strip().upper()
        else:
            secuencia += linea.rstrip("\n")
    if secuencia != "":
        transcritos[cod_secuencia] = secuencia
        secuencia = ""
    f.close()
    return transcritos

def leer_fasta_list(archivo, limite = 0):
    transcritos = list()
    cod_secuencia = ""
    secuencia = ""
    f = open(archivo, "r")
    for linea in f:
        if linea.startswith(">"):
            if secuencia != "":
                transcritos.append((cod_secuencia, secuencia))
                secuencia = ""
                limite -= 1
                if limite == 0:
                    break
            cod_secuencia = linea.rstrip("\n").lstrip(">").strip().upper()
        else:
            secuencia += linea.rstrip("\n")
    if secuencia != "":
        transcritos.append((cod_secuencia, secuencia))
        secuencia = ""
    f.close()
    return transcritos
