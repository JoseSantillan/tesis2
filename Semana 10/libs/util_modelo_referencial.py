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

class GeneradorFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, identificador=None, X_train=None,y_train=None):
        #generar todos los features
        self.identificador = identificador
        if X_train is None or y_train is None:
            return
        codigos_lncRNA = {}
        codigos_PCT = {}
        for i in range(len(X_train)):
            if y_train[i] == 0:
                codigos_PCT[X_train[i][0]] = X_train[i][1]
            else:
                codigos_lncRNA[X_train[i][0]] = X_train[i][1]
        util_caracteristicas.generar_modelo_CPAT(identificador, codigos_lncRNA, codigos_PCT)
        util_caracteristicas.generar_caracteristicas(identificador, {**codigos_lncRNA, **codigos_PCT})
        
    def fit(self, X, y=None):
        #ejecutar cpat para el conjunto de datos
        identificador = self.identificador
        self._id_cpat = identificador + "_fold_" + hashlib.sha224(''.join([x[0] for x in X]).encode()).hexdigest()#str(hash(frozenset({x[0]:1 for x in X})))
        id_cpat = self._id_cpat
        if util_caracteristicas.existe_modelo_cpat(id_cpat):
            return self
        codigos_lncRNA = {}
        codigos_PCT = {}
        for i in range(len(y)):
            if y[i] == 0:
                codigos_PCT[X[i][0]] = X[i][1]
            else:
                codigos_lncRNA[X[i][0]] = X[i][1]
        util_caracteristicas.generar_modelo_CPAT(id_cpat, codigos_lncRNA, codigos_PCT)
        util_caracteristicas.generar_caracteristicas_cpat(identificador, {**codigos_lncRNA, **codigos_PCT})
        return self
        
    def transform(self, X):
        #obtener caracteristicas
        identificador = self.identificador
        id_cpat = self._id_cpat
        codigos = {codigo[0]:codigo[1] for codigo in X}
        util_caracteristicas.generar_caracteristicas_cpat(id_cpat, codigos)
        dict_features = util_caracteristicas.obtener_caracteristicas(identificador, id_cpat, codigos)

        return [list(x.values()) for x in dict_features.values()]

def crear_modelo_referencial(identificador, tuned_parameters, scores, n_jobs, cv):
    if not os.path.isdir("./modelos_referenciales"):
        os.mkdir("./modelos_referenciales")
    
    codigos_lncRNA = util_fasta.leer_fasta("./data/" + identificador + ".lncRNA.fasta")
    codigos_PCT = util_fasta.leer_fasta("./data/" + identificador + ".PCT.fasta")
    
    X = list(codigos_lncRNA.items()) + list(codigos_PCT.items())
    y = ([1] * len(codigos_lncRNA)) + ([0] * len(codigos_PCT))
    X_train, y_train = X, y #shuffle(X, y, random_state=0)
    svm_pipeline = Pipeline(steps=[('features', GeneradorFeatures(identificador, X_train, y_train)), ('svc', SVC())])
    
    for score in scores:
        clf = GridSearchCV(svm_pipeline, tuned_parameters, cv=cv, scoring=score, n_jobs=n_jobs, refit="accuracy")
        clf.fit(X_train, y_train)
        resultado = {
            "accuracy" : clf.cv_results_['mean_test_accuracy'][clf.best_index_],
            "precision" : clf.cv_results_['mean_test_precision'][clf.best_index_],
            "recall" : clf.cv_results_['mean_test_recall'][clf.best_index_]
        }
        dump(resultado, './modelos_referenciales/resultado_{}.bin'.format(identificador))
        dump(clf.best_estimator_, './modelos_referenciales/modelo_{}.plk'.format(identificador), compress = 1)
        
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
