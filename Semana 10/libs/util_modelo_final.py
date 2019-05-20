import os
import shutil
import util_fasta, util_caracteristicas
from sklearn.externals.joblib import Parallel, delayed, dump, load
import hashlib
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import LeaveOneGroupOut, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support, precision_recall_curve, average_precision_score
import hashlib
import util_fasta
import os
import numpy as np
import matplotlib.pyplot as plt

class Tesis2():
    def __init__(self, carpeta_base=".", n_jobs=-1, verbose=0, tuned_parameters=[{'svc__kernel': ['rbf'], 'svc__gamma': [1e-3], 'svc__C': [0.1,0.5,0.9,2]}], score = ['accuracy','precision','recall']):
        self.carpeta_base = carpeta_base
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.tuned_parameters = tuned_parameters
        self.score = score
        self.carpeta_data_base = self.carpeta_base + "/data"
        self.carpeta_fold_base = self.carpeta_base + "/folds"
        self.carpeta_modelo_base = self.carpeta_base + "/modelo_final"
        if not os.path.isdir(self.carpeta_base):
            os.mkdir(self.carpeta_base)
        self.diamond_db = "./feature_engine/Diamond_BD/uniprot-viridiplantae-reviewed.dmnd"
        self.modelo_final_generado = False
        self.modelo_referencial_generado = False
            
    def generar_modelo_final(self):
        if (self.verbose > 1): print("*************************************************")
        if (self.verbose > 1): print("*************** Generando llaves ****************")
        if (self.verbose > 1): print("*************************************************")
        self.generar_llaves_clases()
        if (self.verbose > 1): print("*************************************************")
        if (self.verbose > 1): print("***************** Armando folds *****************")
        if (self.verbose > 1): print("*************************************************")
        self.armar_folds()
        if (self.verbose > 1): print("*************************************************")
        if (self.verbose > 1): print("***** Generando modelo cpat para cada fold ******")
        if (self.verbose > 1): print("*************************************************")
        self.generar_cpats_de_folds()
        if (self.verbose > 1): print("*************************************************")
        if (self.verbose > 1): print("*** Ejecutando cpat y diamond sobre los folds ***")
        if (self.verbose > 1): print("*************************************************")
        self.ejecutar_cpat_diamond_folds()
        if (self.verbose > 1): print("*************************************************")
        if (self.verbose > 1): print("************* Serializando features *************")
        if (self.verbose > 1): print("*************************************************")
        self.generar_features_folds()
        if (self.verbose > 1): print("*************************************************")
        if (self.verbose > 1): print("************ Generando modelo final *************")
        if (self.verbose > 1): print("*************************************************")
        self.entrenar_modelo_final()
        self.modelo_final_generado = True
        if (self.verbose > 1): print("*************************************************")
        if (self.verbose > 1): print("******** Limpiando archivos intermedios *********")
        if (self.verbose > 1): print("*************************************************")
        self.limpiar_archivos_intermedios()
        if (self.verbose > 1):
            print("*************************************************")
            print("************* Mostrando resultados **************")
            print("*************************************************")
            self.mostrar_resultados()
            
    def generar_modelos_referenciales(self):
        if (self.verbose > 1): print("*************************************************")
        if (self.verbose > 1): print("******* Generando modelos referenciales *********")
        if (self.verbose > 1): print("*************************************************")
        self.entrenar_modelos_referenciales()
        self.modelo_referencial_generado = True
        if (self.modelo_final_generado and self.verbose > 1):
            print("*************************************************")
            print("************* Mostrando resultados **************")
            print("*************************************************")
            self.mostrar_resultados_referencial_vs_final()
        
    def carpeta_data(self):
        return self.carpeta_data_base

    def carpeta_fold(self):
        return self.carpeta_fold_base

    def carpeta_modelo(self):
        return self.carpeta_modelo_base
    
    def folder_clase(self, num_clase):
        return self.carpeta_data() + "/clase_" + str(num_clase)

    def archivo_clase(self, num_clase, tipo):
        return self.folder_clase(num_clase) + "/" + tipo + ".fa"

    def obtener_num_clases(self):
        num_clases = 0
        if not os.path.isfile(self.carpeta_base + "/num_clases.bin"):
            while os.path.isdir(self.folder_clase(num_clases + 1)):
                num_clases = num_clases + 1
            dump(num_clases, self.carpeta_base + "/num_clases.bin")
        num_clases = load(self.carpeta_base + "/num_clases.bin")
        return num_clases

    def iterador_clases(self):
        return range(1, self.obtener_num_clases() + 1)

    def obtener_primera_secuencia(self, num_clase):
        secuencias = util_fasta.leer_fasta(self.archivo_clase(num_clase, "lncRNA"), 1)
        return list(secuencias.keys())[0]

    def obtener_todas_las_secuencias(self):
        return {num_clase : self.obtener_primera_secuencia(num_clase) for num_clase in self.iterador_clases()}

    def generar_llaves_clases(self):
        secuencias = self.obtener_todas_las_secuencias()
        llaves = {num_clase : "" for num_clase in secuencias.keys()}
        llaves[0] = "" #llave cero corresponde a todo el universo
        for i_clase in self.iterador_clases():
            llaves[0] += secuencias[i_clase]
            for j_clase in self.iterador_clases():
                if (i_clase != j_clase):
                    llaves[j_clase] += secuencias[i_clase]
        llaves[0] = hashlib.sha224(llaves[0].encode()).hexdigest()
        for i_clase in self.iterador_clases():
            llaves[i_clase] = hashlib.sha224(llaves[i_clase].encode()).hexdigest()
        dump(llaves, self.carpeta_base + "/llaves_clases.bin")

    def obtener_llaves_clases(self):
        return load(self.carpeta_base + "/llaves_clases.bin")

    def carpeta_fold_clase(self, llave):
        return self.carpeta_fold() + "/fold_clase_" + str(llave)

    def archivo_fold_clase(self, llave, tipoTrainTest, tipoRNA):
        return self.carpeta_fold_clase(llave) + "/" + tipoTrainTest + "/" + tipoRNA + ".fa"

    def armar_fold_final(self, tipo):
        llave = self.obtener_llaves_clases()[0]
        with open(self.archivo_fold_clase(llave, "train", tipo), "w+") as outfile:
            for num_clase in self.iterador_clases():
                with open(self.archivo_clase(num_clase, tipo), "r") as infile:
                    for inline in infile:
                        outfile.write(inline)

    def armar_fold_clase(self, num_clase):
        llave = self.obtener_llaves_clases()[num_clase]
        os.mkdir(self.carpeta_fold_clase(llave))
        os.mkdir(self.carpeta_fold_clase(llave) + "/train")
        for tipo in ["lncRNA", "PCT", "CDS"]:
            with open(self.archivo_fold_clase(llave, "train", tipo), "w+") as outfile:
                for j_num_clase in self.iterador_clases():
                    if num_clase != j_num_clase:
                        with open(self.archivo_clase(j_num_clase, tipo)) as infile:
                            for inline in infile:
                                outfile.write(inline)
        os.mkdir(self.carpeta_fold_clase(llave) + "/test")
        for tipo in ["lncRNA", "PCT"]:
            with open(self.archivo_fold_clase(llave, "test", tipo), "w+") as outfile:
                with open(self.archivo_clase(num_clase, tipo)) as infile:
                    for inline in infile:
                        outfile.write(inline)
                    
    def armar_folds(self):
        if os.path.isdir(self.carpeta_fold()):
            shutil.rmtree(self.carpeta_fold())
        os.mkdir(self.carpeta_fold())
        llave = self.obtener_llaves_clases()[0]
        if not os.path.isdir(self.carpeta_fold_clase(llave)):
            os.mkdir(self.carpeta_fold_clase(llave))
        if not os.path.isdir(self.carpeta_fold_clase(llave) + "/train"):
            os.mkdir(self.carpeta_fold_clase(llave) + "/train")

        Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(delayed(wrapper_armar_fold_final)(self, tipo) for tipo in ["lncRNA", "PCT", "CDS"])
        Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(delayed(wrapper_armar_fold_clase)(self, num_clase) for num_clase in self.iterador_clases())
        
    def carpeta_fold_cpat(self, llave):
        return self.carpeta_fold_clase(llave) + "/cpat"

    def generar_cpat_fold(self, num_clase):
        llave = self.obtener_llaves_clases()[num_clase]
        archivo_lncRNA = self.archivo_fold_clase(llave, "train", "lncRNA")
        archivo_PCT = self.archivo_fold_clase(llave, "train", "PCT")
        archivo_CDS = self.archivo_fold_clase(llave, "train", "CDS")
        carpeta_cpat = self.carpeta_fold_cpat(llave)
        if not os.path.isdir(carpeta_cpat):
            os.mkdir(carpeta_cpat)
        util_caracteristicas.generar_modelo_CPAT(archivo_lncRNA, archivo_PCT, archivo_CDS, carpeta_cpat)

    def generar_cpat_final(self):
        llave = self.obtener_llaves_clases()[0]
        archivo_lncRNA = self.archivo_fold_clase(llave, "train", "lncRNA")
        archivo_PCT = self.archivo_fold_clase(llave, "train", "PCT")
        archivo_CDS = self.archivo_fold_clase(llave, "train", "CDS")
        carpeta_cpat = self.carpeta_fold_cpat(llave)
        if not os.path.isdir(carpeta_cpat):
            os.mkdir(carpeta_cpat)
        util_caracteristicas.generar_modelo_CPAT(archivo_lncRNA, archivo_PCT, archivo_CDS, carpeta_cpat)

    def limpieza_archivos_CDS(self, num_clase):
        llave = self.obtener_llaves_clases()[num_clase]
        os.remove(self.archivo_fold_clase(llave, "train", "CDS"))
        
    def generar_cpats_de_folds(self):
        self.generar_cpat_final()
        Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(delayed(wrapper_generar_cpat_fold)(self, num_clase) for num_clase in self.iterador_clases())
        self.limpieza_archivos_CDS(0)
        Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(delayed(wrapper_limpieza_archivos_CDS)(self, num_clase) for num_clase in self.iterador_clases())
    
    def ejecutar_cpat_fold(self, num_clase):
        llave = self.obtener_llaves_clases()[num_clase]
        archivo_lncRNA = self.archivo_fold_clase(llave, "train", "lncRNA")
        archivo_PCT = self.archivo_fold_clase(llave, "train", "PCT")
        carpeta_cpat = self.carpeta_fold_cpat(llave)
        util_caracteristicas.ejecutar_cpat(archivo_lncRNA, carpeta_cpat, archivo_lncRNA.replace(".fa", ".cpat"))
        os.remove(archivo_lncRNA.replace(".fa", ".cpat") + ".dat")
        os.remove(archivo_lncRNA.replace(".fa", ".cpat") + ".r")
        util_caracteristicas.ejecutar_cpat(archivo_PCT, carpeta_cpat, archivo_PCT.replace(".fa", ".cpat"))
        os.remove(archivo_PCT.replace(".fa", ".cpat") + ".dat")
        os.remove(archivo_PCT.replace(".fa", ".cpat") + ".r")

    def ejecutar_cpat_diamond_final(self):
        llave = self.obtener_llaves_clases()[0]
        archivo_lncRNA = self.archivo_fold_clase(llave, "train", "lncRNA")
        archivo_PCT = self.archivo_fold_clase(llave, "train", "PCT")
        diamond_db = self.diamond_db
        carpeta_cpat = self.carpeta_fold_cpat(llave)
        util_caracteristicas.ejecutar_diamond(archivo_lncRNA, diamond_db, archivo_lncRNA.replace(".fa", ".dmnd"))
        util_caracteristicas.ejecutar_diamond(archivo_PCT, diamond_db, archivo_PCT.replace(".fa", ".dmnd"))
        util_caracteristicas.ejecutar_cpat(archivo_lncRNA, carpeta_cpat, archivo_lncRNA.replace(".fa", ".cpat"))
        os.remove(archivo_lncRNA.replace(".fa", ".cpat") + ".dat")
        os.remove(archivo_lncRNA.replace(".fa", ".cpat") + ".r")
        util_caracteristicas.ejecutar_cpat(archivo_PCT, carpeta_cpat, archivo_PCT.replace(".fa", ".cpat"))
        os.remove(archivo_PCT.replace(".fa", ".cpat") + ".dat")
        os.remove(archivo_PCT.replace(".fa", ".cpat") + ".r")
        
    def ejecutar_cpat_diamond_folds(self):
        self.ejecutar_cpat_diamond_final()
        Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(delayed(wrapper_ejecutar_cpat_fold)(self, num_clase) for num_clase in self.iterador_clases())
        
    def archivo_features_clase(self, llave, tipoTrainTest, tipoRNA):
        return self.archivo_fold_clase(llave, tipoTrainTest, tipoRNA).replace(".fa", ".ft")

    def generar_features_fold(self, num_clase):
        llave = self.obtener_llaves_clases()[num_clase]
        features_base_lncRNA = self.archivo_features_clase(self.obtener_llaves_clases()[0], "train", "lncRNA")
        features_base_PCT = self.archivo_features_clase(self.obtener_llaves_clases()[0], "train", "PCT")
        for tipo in ["train", "test"]:
            archivo_lncRNA = self.archivo_fold_clase(llave, tipo, "lncRNA")
            archivo_PCT = self.archivo_fold_clase(llave, tipo, "PCT")
            archivo_cpat_lncRNA = self.archivo_fold_clase(llave, "train", "lncRNA").replace(".fa", ".cpat")
            archivo_cpat_PCT = self.archivo_fold_clase(llave, "train", "PCT").replace(".fa", ".cpat")
            salida_lncRNA = self.archivo_features_clase(llave, tipo, "lncRNA")
            salida_PCT = self.archivo_features_clase(llave, tipo, "PCT")
            util_caracteristicas.generar_features(archivo_lncRNA, features_base_lncRNA, archivo_cpat_lncRNA, salida_lncRNA)
            util_caracteristicas.generar_features(archivo_PCT, features_base_PCT, archivo_cpat_PCT, salida_PCT)

    def generar_features_final(self):
        llave = self.obtener_llaves_clases()[0]
        archivo_lncRNA = self.archivo_fold_clase(llave, "train", "lncRNA")
        archivo_PCT = self.archivo_fold_clase(llave, "train", "PCT")
        salida_lncRNA = self.archivo_features_clase(llave, "train", "lncRNA")
        salida_PCT = self.archivo_features_clase(llave, "train", "PCT")
        util_caracteristicas.generar_features_base(archivo_lncRNA, archivo_lncRNA.replace(".fa", ".cpat"), archivo_lncRNA.replace(".fa", ".dmnd"), salida_lncRNA)
        util_caracteristicas.generar_features_base(archivo_PCT, archivo_PCT.replace(".fa", ".cpat"), archivo_PCT.replace(".fa", ".dmnd"), salida_PCT)
        
    def generar_features_folds(self):
        self.generar_features_final()
        Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(delayed(wrapper_generar_features_fold)(self, num_clase) for num_clase in self.iterador_clases())
        
    def obtener_data_entrenamiento(self):
        llave = self.obtener_llaves_clases()[0]
        codigos_lncRNA = util_fasta.leer_fasta_list(self.archivo_fold_clase(llave, "train", "lncRNA"))
        codigos_PCT = util_fasta.leer_fasta_list(self.archivo_fold_clase(llave, "train", "PCT"))

        codigos_lncRNA = [(x[0],"") for x in codigos_lncRNA]
        codigos_PCT = [(x[0],"") for x in codigos_PCT]
        cantidad_transcritos = len(codigos_lncRNA)//self.obtener_num_clases()

        y = ([1] * len(codigos_lncRNA)) + ([0] * len(codigos_PCT))
        groups = list()
        for _ in range(2):
            for num_clase in self.iterador_clases():
                groups += ([num_clase] * (cantidad_transcritos))
        return codigos_lncRNA + codigos_PCT, y, groups, cantidad_transcritos

    def entrenar_modelo_final(self):
        if os.path.isdir(self.carpeta_modelo()):
            shutil.rmtree(self.carpeta_modelo())
        os.mkdir(self.carpeta_modelo())
        X_train, y_train, groups, cantidad_transcritos = self.obtener_data_entrenamiento()
        svm_pipeline = Pipeline(steps=[('features', GeneradorFeatures(self, cantidad_transcritos, self.obtener_num_clases())), ('scaler', RobustScaler()), ('svc', SVC())])
        logo = LeaveOneGroupOut()
        clf = GridSearchCV(svm_pipeline, self.tuned_parameters, cv=logo, scoring=self.score, n_jobs=self.n_jobs, refit="accuracy", return_train_score = True, verbose=self.verbose)
        clf.fit(X_train, y_train, groups) #requerido por LeaveOneGroupOut
        resultado = {
            "accuracy" : clf.cv_results_['mean_test_accuracy'][clf.best_index_],
            "precision" : clf.cv_results_['mean_test_precision'][clf.best_index_],
            "recall" : clf.cv_results_['mean_test_recall'][clf.best_index_]
        }
        dump(resultado, self.carpeta_modelo() + "/resultado.bin")
        dump(clf.best_params_, self.carpeta_modelo() + "/params.bin")
        dump(clf.cv_results_, self.carpeta_modelo() + "/cv_results.bin")
        dump(clf.best_estimator_, self.carpeta_modelo() + "/modelo.plk")
        
    def limpieza_archivos_finales_fasta_ruta(self, llave):
        shutil.rmtree(self.carpeta_fold_clase(llave))

    def limpieza_archivos_finales_fasta(self, num_clase):
        llave = self.obtener_llaves_clases()[num_clase]
        if num_clase == 0:
            shutil.rmtree(self.carpeta_fold_clase(llave) + "/train")
        else:
            self.limpieza_archivos_finales_fasta_ruta(llave)
    
    def limpiar_archivos_intermedios(self):
        self.limpieza_archivos_finales_fasta(0)
        Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(delayed(wrapper_limpieza_archivos_finales_fasta)(self, num_clase) for num_clase in self.iterador_clases())
        self.features_pre_generados = False
        
    def mostrar_resultados(self):
        if (not self.modelo_final_generado):
            print("Debe generar el modelo final")
            return
        display(load(self.carpeta_modelo() + "/cv_results.bin"))
        display(load(self.carpeta_modelo() + "/params.bin"))
        display(load(self.carpeta_modelo() + "/resultado.bin"))
        if (self.modelo_referencial_generado):
            self.mostrar_resultados_referencial_vs_final()
        
    def devolver_resultado(self):
        return load(self.carpeta_modelo() + "/resultado.bin")
        
    def devolver_mejor_parametro(self):
        return load(self.carpeta_modelo() + "/params.bin")
        
    def devolver_cv_results(self):
        return load(self.carpeta_modelo() + "/cv_results.bin")
        
    def devolver_mejor_modelo(self):
        return load(self.carpeta_modelo() + "/modelo.plk")
        
    def preparar_data_modelo_referencial(self, num_clase):
        carpeta_base_referencial = self.carpeta_base + "/modelos_referenciales/clase_" + str(num_clase)
        if not os.path.isdir(carpeta_base_referencial):
            os.mkdir(carpeta_base_referencial)
        if not os.path.isdir(carpeta_base_referencial + "/data"):
            os.mkdir(carpeta_base_referencial + "/data")
        clase_positiva = util_fasta.leer_fasta_list(self.archivo_clase(num_clase, "lncRNA"))
        PCT = util_fasta.leer_fasta(self.archivo_clase(num_clase, "PCT"))
        CDS = util_fasta.leer_fasta(self.archivo_clase(num_clase, "CDS"))
        clase_negativa = list()
        for k in PCT.keys():
            clase_negativa.append((k, PCT[k], CDS[k]))
        X = clase_positiva + clase_negativa
        y = ([1] * len(clase_positiva)) + ([0] * len(clase_negativa))
        skf = StratifiedKFold(n_splits=10)
        isplit = 1
        for _, test in skf.split(X, y):
            split_lncRNA = list()
            split_PCT = list()
            split_CDS = list()
            for itest in test:
                if y[itest] == 1:
                    split_lncRNA.append(X[itest])
                else:
                    split_PCT.append((X[itest][0], X[itest][1]))
                    split_CDS.append((X[itest][0], X[itest][2]))
            if not os.path.isdir(carpeta_base_referencial + "/data/clase_" + str(isplit)):
                os.mkdir(carpeta_base_referencial + "/data/clase_" + str(isplit))
            util_fasta.generar_fasta(split_lncRNA, carpeta_base_referencial + "/data/clase_" + str(isplit) + "/lncRNA.fa")
            util_fasta.generar_fasta(split_PCT, carpeta_base_referencial + "/data/clase_" + str(isplit) + "/PCT.fa")
            util_fasta.generar_fasta(split_CDS, carpeta_base_referencial + "/data/clase_" + str(isplit) + "/CDS.fa")
            isplit += 1
            
    def instanciar_modelo_referencial(self, num_clase):
        carpeta_base_referencial = self.carpeta_base + "/modelos_referenciales/clase_" + str(num_clase)
        return Tesis2(carpeta_base=carpeta_base_referencial, n_jobs=self.n_jobs, verbose=0, tuned_parameters=self.tuned_parameters, score=self.score)
        
    def crear_modelo_referencial(self, num_clase):
        carpeta_base_referencial = self.carpeta_base + "/modelos_referenciales/clase_" + str(num_clase)
        self.preparar_data_modelo_referencial(num_clase)
        tesis2 = self.instanciar_modelo_referencial(num_clase)
        tesis2.generar_modelo_final()
        shutil.rmtree(carpeta_base_referencial + "/data")
    
    def entrenar_modelos_referenciales(self):
        if not os.path.isdir(self.carpeta_base + "/modelos_referenciales"):
            os.mkdir(self.carpeta_base + "/modelos_referenciales")
        Parallel(n_jobs=self.n_jobs, verbose=self.verbose)(delayed(wrapper_crear_modelo_referencial)(self, num_clase) for num_clase in self.iterador_clases())
        
    def obtener_resultados_referencial_vs_final(self):
        resultado_referencial = list()
        resultado_final = list()
        if (not self.modelo_final_generado) or (not self.modelo_referencial_generado):
            print("Debe generar ambos modelos para obtener resultados comparativos")
            return resultado_referencial, resultado_final 
        parametros = self.devolver_mejor_parametro()
        resultados = self.devolver_cv_results()
        i_seleccionado = 0
        i_iter = 0
        for param in resultados["params"]:
            if parametros == param:
                i_seleccionado = i_iter
            i_iter += 1

        for i in range(self.obtener_num_clases()):
            resultado_referencial.append(self.instanciar_modelo_referencial(i+1).devolver_resultado()["accuracy"])
            resultado_final.append(resultados["split" + str(i) + "_test_accuracy"][i_seleccionado])
        return resultado_referencial, resultado_final
        
    def mostrar_resultados_referencial_vs_final(self):
        if (not self.modelo_final_generado) or (not self.modelo_referencial_generado):
            print("Debe generar ambos modelos para obtener resultados comparativos")
            return
        resultado_referencial, resultado_final = self.obtener_resultados_referencial_vs_final()
        for i in range(self.obtener_num_clases()):
            print("***************")
            print("*** CLASE " + str(i+1) + " ***")
            print("***************")

            acc_mr = resultado_referencial[i]
            acc_mf = resultado_final[i]

            print("Accuracy modelo referencial: " + '{:.1%}'.format(acc_mr))
            print("Accuracy modelo final: " + '{:.1%}'.format(acc_mf))
            print("")

        print("********************")
        print("*** MODELO FINAL ***")
        print("********************")  
        print("Accuracy modelo final: " + '{:.1%}'.format(self.devolver_resultado()["accuracy"]))
        print("")
        
    def generar_predictor_final(self):
        predictor = self.devolver_mejor_modelo()
        llave_fold_final = self.obtener_llaves_clases()[0]
        nuevo_generador_features = GeneradorFeaturesParaPredicciones(carpeta_base=self.carpeta_base, diamond_db=self.diamond_db, carpeta_cpat=self.carpeta_fold_cpat(llave_fold_final))
        predictor.steps.pop(0)
        predictor.steps.insert(0,['features', nuevo_generador_features])
        dump(predictor, self.carpeta_modelo() + "/modelo_final.plk")
        
    def reportar_predicciones(self, archivo_lncRNA, archivo_PCT):
        y_pred_lncRNA = self.realizar_predicciones(archivo_lncRNA)
        probs_lncRNA = self.realizar_predicciones_proba(archivo_lncRNA, features_calculados=True)
        y_pred_PCT = self.realizar_predicciones(archivo_PCT)
        probs_PCT = self.realizar_predicciones_proba(archivo_PCT, features_calculados=True)
        
        y_true = ([1] * len(y_pred_lncRNA)) + ([0] * len(y_pred_PCT))
        y_pred = np.concatenate((y_pred_lncRNA, y_pred_PCT))
        
        probs = np.concatenate((probs_lncRNA, probs_PCT))
        precision, recall, _ = precision_recall_curve(y_true, probs)
        average_precision = average_precision_score(y_true, probs)
        plt.step(recall, precision, color='b', alpha=0.2, where='post')
        plt.fill_between(recall, precision, step='post', alpha=0.2, color='b')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.ylim([0.0, 1.05])
        plt.xlim([0.0, 1.0])
        plt.title('2-class Precision-Recall curve: AP={0:0.2f}'.format(average_precision))
        
        return classification_report(y_true, y_pred, target_names=["lncRNA", "PCT"]), confusion_matrix(y_true, y_pred), precision_recall_fscore_support(y_true, y_pred, average='binary')
        
    def realizar_predicciones(self, archivo_fasta, features_calculados=False):
        predictor = load(self.carpeta_modelo() + "/modelo_final.plk")
        X_test = util_fasta.leer_fasta_list(archivo_fasta)
        predictor.set_params(features__features_calculados=features_calculados)
        return predictor.predict(X_test)
        
    def realizar_predicciones_proba(self, archivo_fasta, features_calculados=False):
        predictor = load(self.carpeta_modelo() + "/modelo_final.plk")
        X_test = util_fasta.leer_fasta_list(archivo_fasta)
        predictor.set_params(features__features_calculados=features_calculados)
        return predictor.decision_function(X_test)
        
#wrappers para ejecución en paralelo
def wrapper_armar_fold_final(tesis2, tipo):
    tesis2.armar_fold_final(tipo)
        
def wrapper_armar_fold_clase(tesis2, num_clase):
    tesis2.armar_fold_clase(num_clase)
    
def wrapper_generar_cpat_fold(tesis2, num_clase):
    tesis2.generar_cpat_fold(num_clase)
    
def wrapper_limpieza_archivos_CDS(tesis2, num_clase):
    tesis2.limpieza_archivos_CDS(num_clase)
    
def wrapper_ejecutar_cpat_fold(tesis2, num_clase):
    tesis2.ejecutar_cpat_fold(num_clase)
    
def wrapper_generar_features_fold(tesis2, num_clase):
    tesis2.generar_features_fold(num_clase)
    
def wrapper_limpieza_archivos_finales_fasta(tesis2, num_clase):
    tesis2.limpieza_archivos_finales_fasta(num_clase)

def wrapper_crear_modelo_referencial(tesis2, num_clase):
    tesis2.crear_modelo_referencial(num_clase)

class GeneradorFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, tesis2=None, cantidad_transcritos=None, num_clases=None):
        if cantidad_transcritos is None:
            return
        self.cantidad_transcritos = cantidad_transcritos
        self.num_clases = num_clases
        self.tesis2 = tesis2

    def fit(self, X, y=None):
        self._llave_fold = self.obtener_llave_fold(X)
        return self

    def transform(self, X):
        return self.obtener_features_pre_calculados(X)

    def obtener_llave_fold(self, X):
        cod_secuencias = ""
        num_transcritos = len(X)
        num_transcritos_por_grupo = self.cantidad_transcritos
        for i in range(num_transcritos//(num_transcritos_por_grupo*2)):
            cod_secuencias += X[i * num_transcritos_por_grupo][0]
        llave = hashlib.sha224(cod_secuencias.encode()).hexdigest()
        return llave

    def obtener_features_pre_calculados(self, X):
        llave = self._llave_fold
        tipo = "train"
        if os.path.isfile(self.tesis2.archivo_fold_clase(llave, "test", "lncRNA")):
            secuencias = util_fasta.leer_fasta(self.tesis2.archivo_fold_clase(llave, "test", "lncRNA"), 1)
            if list(secuencias.keys())[0] == X[0][0]:
                tipo = "test"
        features = list(load(self.tesis2.archivo_features_clase(llave, tipo, "lncRNA")).values())
        features += list(load(self.tesis2.archivo_features_clase(llave, tipo, "PCT")).values())
        return [list(x.values()) for x in features]

class GeneradorFeaturesParaPredicciones(BaseEstimator, TransformerMixin):
    def __init__(self, carpeta_base=None, diamond_db=None, carpeta_cpat=None, features_calculados=False):
        if carpeta_base is None:
            return
        self.carpeta_base = carpeta_base
        self.diamond_db = diamond_db
        self.carpeta_cpat = carpeta_cpat
        self.features_calculados = features_calculados

    def fit(self, X, y=None):
        raise Exception('Este modelo no admite fit')
        return self

    def transform(self, X):
        carpeta_transform = self.carpeta_base + "/transform"
        if not os.path.isdir(carpeta_transform):
            os.mkdir(carpeta_transform)
        archivo_fasta = carpeta_transform + "/secuencias.fa"
        if (not self.features_calculados):
            self.generar_archivos_fasta(archivo_fasta, X)
            self.ejecutar_diamond_cpat(archivo_fasta)
            self.generar_features(archivo_fasta)
        return self.obtener_features_pre_calculados(archivo_fasta)
                          
    def generar_archivos_fasta(self, archivo_fasta, X):
        util_fasta.generar_fasta(X, archivo_fasta)
    
    def ejecutar_diamond_cpat(self, archivo_fasta):
        diamond_db = self.diamond_db
        carpeta_cpat = self.carpeta_cpat
        util_caracteristicas.ejecutar_diamond(archivo_fasta, diamond_db, archivo_fasta.replace(".fa", ".dmnd"))
        util_caracteristicas.ejecutar_cpat(archivo_fasta, carpeta_cpat, archivo_fasta.replace(".fa", ".cpat"))
        os.remove(archivo_fasta.replace(".fa", ".cpat") + ".dat")
        os.remove(archivo_fasta.replace(".fa", ".cpat") + ".r")
        
    def generar_features(self, archivo_fasta):
        util_caracteristicas.generar_features_base(archivo_fasta, archivo_fasta.replace(".fa", ".cpat"), archivo_fasta.replace(".fa", ".dmnd"), archivo_fasta.replace(".fa", ".ft"))

    def obtener_features_pre_calculados(self, archivo_fasta):
        features = list(load(archivo_fasta.replace(".fa", ".ft")).values())
        return [list(x.values()) for x in features]
