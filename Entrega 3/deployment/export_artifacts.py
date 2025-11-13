import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
from sklearn.svm import SVC


ROOT = Path(__file__).resolve().parents[2]
DATASET_PATH = ROOT / 'Entrega 2' / 'landmarks_data.csv'
OUTPUT_DIR = Path(__file__).resolve().parent / 'models'
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_dataset():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f'No se encontró el dataset en {DATASET_PATH}')
    df = pd.read_csv(DATASET_PATH)
    X = df.drop(columns=['class'])
    y = df['class']
    return df, X, y


def build_pipelines():
    pca_svm = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler()),
        ('pca', PCA(n_components=60, random_state=42)),
        ('classifier', SVC(kernel='rbf', C=10, gamma=0.01, class_weight='balanced', probability=False, random_state=42))
    ])

    rf = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('classifier', RandomForestClassifier(
            n_estimators=400,
            max_depth=None,
            min_samples_leaf=1,
            class_weight='balanced',
            n_jobs=-1,
            random_state=42
        ))
    ])
    return pca_svm, rf


def main():
    df, X, y = load_dataset()

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    feature_names = list(X.columns)

    pca_svm_pipeline, rf_pipeline = build_pipelines()

    print('[INFO] Ajustando pipeline PCA+SVM (60 componentes)...')
    pca_svm_pipeline.fit(X, y_encoded)

    print('[INFO] Ajustando RandomForest (baseline)...')
    rf_pipeline.fit(X, y_encoded)

    artefacts = {
        'pca_svm_pipeline': OUTPUT_DIR / 'activity_pca60_svm.joblib',
        'rf_pipeline': OUTPUT_DIR / 'activity_rf.joblib',
        'label_encoder': OUTPUT_DIR / 'label_encoder.joblib',
        'feature_names': OUTPUT_DIR / 'feature_names.json',
        'metadata': OUTPUT_DIR / 'metadata.json'
    }

    print('[INFO] Guardando artefactos en', OUTPUT_DIR)
    joblib.dump(pca_svm_pipeline, artefacts['pca_svm_pipeline'])
    joblib.dump(rf_pipeline, artefacts['rf_pipeline'])
    joblib.dump(label_encoder, artefacts['label_encoder'])

    with open(artefacts['feature_names'], 'w', encoding='utf-8') as fp:
        json.dump(feature_names, fp, indent=2)

    metadata = {
        'dataset': str(DATASET_PATH.relative_to(ROOT)),
        'n_samples': len(df),
        'n_features': len(feature_names),
        'pca_components': 60,
        'rf_estimators': 400,
        'class_labels': list(label_encoder.classes_)
    }
    with open(artefacts['metadata'], 'w', encoding='utf-8') as fp:
        json.dump(metadata, fp, indent=2)

    print('[INFO] Exportación completada:')
    for key, path in artefacts.items():
        print(f' - {key}: {path}')


if __name__ == '__main__':
    main()
