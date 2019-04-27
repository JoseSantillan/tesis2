from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import util_caracteristicas, util_fasta
from sklearn.preprocessing import StandardScaler
from sklearn.externals.joblib import dump, load
from sklearn.utils import shuffle

def crear_modelo_referencial(identificador, tuned_parameters, scores, n_jobs):
    #print("lectura de archivos fasta...")
    
    codigos_lncRNA = util_fasta.leer_fasta("./data/" + identificador + ".lncRNA.fasta")
    codigos_PCT = util_fasta.leer_fasta("./data/" + identificador + ".PCT.fasta")
    
    #print("levantamiento de features...")
    
    util_caracteristicas.generar_modelo_CPAT(identificador, codigos_lncRNA.keys(), codigos_PCT.keys())
    
    dict_features_lncRNA = util_caracteristicas.generar_caracteristicas(identificador, codigos_lncRNA)
    dict_features_PCT = util_caracteristicas.generar_caracteristicas(identificador, codigos_PCT)
    
    features_lncRNA = [list(x.values()) for x in dict_features_lncRNA.values()]
    features_PCT = [list(x.values()) for x in dict_features_PCT.values()]
    
    #print("inicio generación del modelo...")
    
    X = features_lncRNA + features_PCT
    y = ([1] * len(features_lncRNA)) + ([0] * len(features_PCT))
    #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)
    X_train, y_train = shuffle(X, y, random_state=0)
    
    #feature_scaler = StandardScaler()
    #feature_scaler=load('./modelos_referenciales/feature_scaler_{}.bin'.format(identificador))
    #X_train = feature_scaler.fit_transform(X_train)  
    #X_test = feature_scaler.transform(X_test)
    #dump(feature_scaler, './modelos_referenciales/feature_scaler_{}.bin'.format(identificador), compress=True)
    
    for score in scores:
        #print("# Tuning hyper-parameters for %s" % score)
        #print()

        clf = GridSearchCV(SVC(), tuned_parameters, cv=10,
                           scoring=score, n_jobs=n_jobs, refit="accuracy")
        clf.fit(X_train, y_train)
        dump(clf.best_estimator_, './modelos_referenciales/modelo_{}.pkl'.format(identificador), compress = 1)
        #clf=load('./modelos_referenciales/{}.pkl'.format(identificador))

        #print("Best parameters set found on development set:")
        #print()
        #print(clf.best_params_)
        #print()
        #print("Grid scores on development set:")
        #print()
        
        resultado = {
            "accuracy" : clf.cv_results_['mean_test_accuracy'][clf.best_index_],
            "precision" : clf.cv_results_['mean_test_precision'][clf.best_index_],
            "recall" : clf.cv_results_['mean_test_recall'][clf.best_index_]
        }
        dump(resultado, './modelos_referenciales/resultado_{}.bin'.format(identificador))
        
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
