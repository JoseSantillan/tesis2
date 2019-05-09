from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import util_caracteristicas, util_fasta
from sklearn.preprocessing import StandardScaler
from sklearn.externals.joblib import dump, load
from sklearn.utils import shuffle
import random

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import string
import os
import hashlib

from sklearn.externals.joblib import Parallel, delayed
from sklearn.model_selection import PredefinedSplit

def generar_features_generales(X_train, y_train):
    #generar todos los features
    identificador = "final"
    codigos_lncRNA = {}
    codigos_PCT = {}
    for i in range(len(X_train)):
        if y_train[i] == 0:
            codigos_PCT[X_train[i][0]] = X_train[i][1]
        else:
            codigos_lncRNA[X_train[i][0]] = X_train[i][1]
    util_caracteristicas.generar_modelo_CPAT(identificador, codigos_lncRNA, codigos_PCT)
    util_caracteristicas.generar_caracteristicas(identificador, {**codigos_lncRNA, **codigos_PCT})

def generar_fit(X, y):
    #ejecutar cpat para el conjunto de datos
    identificador = "final"
    id_cpat = identificador + "_fold_" + hashlib.sha224(''.join([x[0] for x in X]).encode()).hexdigest()
    codigos_lncRNA = {}
    codigos_PCT = {}
    for i in range(len(y)):
        if y[i] == 0:
            codigos_PCT[X[i][0]] = X[i][1]
        else:
            codigos_lncRNA[X[i][0]] = X[i][1]
    util_caracteristicas.generar_modelo_CPAT(id_cpat, codigos_lncRNA, codigos_PCT)
    util_caracteristicas.generar_caracteristicas_cpat(identificador, {**codigos_lncRNA, **codigos_PCT})
    
def obtener_folds(ps, X_train, y_train):
    for train_index, test_index in ps.split():
        yield [X_train[x] for x in train_index], [y_train[y] for y in train_index]

class GeneradorFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, identificador=None, folds_completos=None):
        if identificador is None:
            return
        self.identificador = identificador
        self.folds_completos = folds_completos
        
    def fit(self, X, y=None):
        #ejecutar cpat para el conjunto de datos
        identificador = self.identificador
        self._id_cpat = identificador + "_fold_" + hashlib.sha224(''.join([x[0] for x in X]).encode()).hexdigest()
        if self._id_cpat == identificador + "_fold_" + self.folds_completos:
            self._id_cpat = identificador
        return self
        
    def transform(self, X):
        #obtener caracteristicas
        identificador = self.identificador
        id_cpat = self._id_cpat
        codigos = {codigo[0]:codigo[1] for codigo in X}
        util_caracteristicas.generar_caracteristicas_cpat(id_cpat, codigos)
        dict_features = util_caracteristicas.obtener_caracteristicas(identificador, id_cpat, codigos)
        return [list(x.values()) for x in dict_features.values()]

def generar_sub_modelos(especie, folds, modelo):
    X_train = folds[especie]["X_train"]
    y_train = folds[especie]["y_train"]
    modelo.fit(X_train, y_train)
    dump(modelo, './modelo_final/modelo_{}.plk'.format(especie))
    
def crear_modelo_final(especies, tuned_parameters, scores, n_jobs):
    print("Iniciando creación del modelo final")
    if not os.path.isdir("./modelo_final"):
        os.mkdir("./modelo_final")
    
    X = list()
    y = list()
    test_fold = list()
    indice_fold = 0
    folds = {}
    
    for especie in especies:
        folds[especie] = { "llaves" : list(), "X_train" : list(), "y_train" : list() }
        
    for especie in especies:
        identificador = especie
        codigos_lncRNA = util_fasta.leer_fasta("./data/" + identificador + ".lncRNA.fasta")
        codigos_PCT = util_fasta.leer_fasta("./data/" + identificador + ".PCT.fasta")
        
        _x = list(codigos_lncRNA.items()) + list(codigos_PCT.items())
        _y = ([1] * len(codigos_lncRNA)) + ([0] * len(codigos_PCT))
        X = X + _x
        y = y + _y
        test_fold = test_fold + ([indice_fold] * (len(codigos_lncRNA) + len(codigos_PCT)))
        
        folds[especie]["indice"] = indice_fold
        for especie_2 in especies:
            if especie != especie_2:
                folds[especie_2]["llaves"] = folds[especie_2]["llaves"] + [item[0] for item in _x]
                folds[especie_2]["X_train"] = folds[especie_2]["X_train"] + _x
                folds[especie_2]["y_train"] = folds[especie_2]["y_train"] + _y
        
        indice_fold = indice_fold + 1
        
    folds_especies = {}
    for especie in especies:
        folds[especie]["llave_hash"] = "final_fold_" + hashlib.sha224(''.join(folds[especie]["llaves"]).encode()).hexdigest()
        folds_especies[folds[especie]["llave_hash"]] = {
            "especie" : especie,
            "fold" : folds[especie]["indice"],
            "num_transcritos" : len(folds[especie]["llaves"]),
            "X_train" : folds[especie]["X_train"], 
            "y_train" : folds[especie]["y_train"]
        }
    dump(folds_especies, './modelo_final/folds_especies.bin')
        
    X_train, y_train = X, y #shuffle(X, y, random_state=0)
    identificador = "final"
    folds_completos = hashlib.sha224(''.join([x[0] for x in X_train]).encode()).hexdigest()
    svm_pipeline = Pipeline(steps=[('features', GeneradorFeatures(identificador, folds_completos)), ('svc', SVC())])
    ps = PredefinedSplit(test_fold)
    
    generar_features_generales(X_train, y_train)
    print("Prepocesamiento de transcritos previos al entrenamiento del modelo final")
    Parallel(n_jobs=n_jobs, verbose=0)(delayed(generar_fit)(X, y) for X, y in obtener_folds(ps, X_train, y_train))
    
    for score in scores:
        print("Entrenamiento del modelo con grid search")
        clf = GridSearchCV(svm_pipeline, tuned_parameters, cv=ps, scoring=score, n_jobs=n_jobs, refit="accuracy")
        clf.fit(X_train, y_train)
        resultado = {
            "accuracy" : clf.cv_results_['mean_test_accuracy'][clf.best_index_],
            "precision" : clf.cv_results_['mean_test_precision'][clf.best_index_],
            "recall" : clf.cv_results_['mean_test_recall'][clf.best_index_]
        }
        dump(resultado, './modelo_final/resultado_{}.bin'.format(identificador))
        dump(clf.best_params_, './modelo_final/params_{}.bin'.format(identificador))
        dump(clf.cv_results_, './modelo_final/cv_results_{}.bin'.format(identificador))
        dump(clf.best_estimator_, './modelo_final/modelo_{}.plk'.format(identificador))
        
        print("Generación de modelos finales dejando afuera una especie")
        Parallel(n_jobs=n_jobs, verbose=0)(delayed(generar_sub_modelos)(especie, folds, clf.best_estimator_) for especie in especies)
        
        #means = clf.cv_results_['mean_test_accuracy']
        #stds = clf.cv_results_['std_test_accuracy']
        #for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        #    print("%0.3f (+/-%0.03f) for %r"
        #          % (mean, std * 2, params))
        #print()

        #print("Detailed classification report:")
        #print()
        #print("The model is trained on the full development set.")
        #print("The scores are computed on the full evaluation set.")
        #print()
        #y_true, y_pred = y_test, clf.predict(X_test)
        #print(classification_report(y_true, y_pred))
        #print()
