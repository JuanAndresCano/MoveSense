import argparse
import json
from collections import deque
from pathlib import Path
from typing import Dict, List, Tuple

import cv2
import joblib
import mediapipe as mp
import numpy as np
import pandas as pd

FRAME_TEXT_COLOR = (40, 220, 90)
ALERT_TEXT_COLOR = (0, 0, 255)
BACKGROUND_COLOR = (15, 15, 15)
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.6
THICKNESS = 2


def load_artifacts(models_dir: Path):
    pipeline = joblib.load(models_dir / 'activity_pca60_svm.joblib')
    encoder = joblib.load(models_dir / 'label_encoder.joblib')

    feature_names_path = models_dir / 'feature_names.json'
    if not feature_names_path.exists():
        raise FileNotFoundError('No se encontró feature_names.json en el directorio de modelos.')
    with open(feature_names_path, 'r', encoding='utf-8') as fp:
        feature_names = json.load(fp)

    metadata_path = models_dir / 'metadata.json'
    metadata = None
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as fp:
            metadata = json.load(fp)

    return pipeline, encoder, feature_names, metadata


def empty_feature_row(feature_names: List[str]) -> Dict[str, float]:
    return {name: np.nan for name in feature_names}


def extract_features(result_pose, feature_names: List[str]) -> pd.DataFrame:
    row = empty_feature_row(feature_names)
    if result_pose and result_pose.pose_landmarks:
        for idx, landmark in enumerate(result_pose.pose_landmarks.landmark):
            prefix = f'{idx}_'
            row[f'{prefix}x'] = landmark.x
            row[f'{prefix}y'] = landmark.y
            row[f'{prefix}z'] = landmark.z
            row[f'{prefix}v'] = landmark.visibility
    return pd.DataFrame([row])


def calc_angle(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    ba = a - b
    bc = c - b
    norm_ba = np.linalg.norm(ba)
    norm_bc = np.linalg.norm(bc)
    if norm_ba == 0 or norm_bc == 0:
        return float('nan')
    cosine = np.dot(ba, bc) / (norm_ba * norm_bc)
    cosine = np.clip(cosine, -1.0, 1.0)
    angle = np.degrees(np.arccos(cosine))
    return angle


def get_point(landmarks, index: int) -> np.ndarray:
    lm = landmarks[index]
    return np.array([lm.x, lm.y, lm.z])


def compute_pose_angles(landmarks) -> Dict[str, float]:
    left_hip, left_knee, left_ankle = 23, 25, 27
    right_hip, right_knee, right_ankle = 24, 26, 28
    left_shoulder, right_shoulder = 11, 12
    left_elbow, left_wrist = 13, 15
    right_elbow, right_wrist = 14, 16

    def safe_angle(p1, p2, p3):
        return calc_angle(get_point(landmarks, p1), get_point(landmarks, p2), get_point(landmarks, p3))

    angles = {
        'left_knee': safe_angle(left_hip, left_knee, left_ankle),
        'right_knee': safe_angle(right_hip, right_knee, right_ankle),
        'left_elbow': safe_angle(left_shoulder, left_elbow, left_wrist),
        'right_elbow': safe_angle(right_shoulder, right_elbow, right_wrist)
    }

    spine_vector = get_point(landmarks, left_shoulder) + get_point(landmarks, right_shoulder)
    spine_vector /= 2
    pelvis_vector = get_point(landmarks, left_hip) + get_point(landmarks, right_hip)
    pelvis_vector /= 2
    vertical = np.array([0, -1, 0])
    body_vec = spine_vector - pelvis_vector
    tilt = calc_angle(pelvis_vector + vertical, pelvis_vector, spine_vector)
    angles['trunk_inclination'] = tilt

    return angles


def overlay_info(frame: np.ndarray, label: str, confidence: float, angles: Dict[str, float], fps: float):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (350, 180), BACKGROUND_COLOR, thickness=-1)
    alpha = 0.4
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    y = 30
    cv2.putText(frame, f'Actividad: {label}', (10, y), FONT, FONT_SCALE, FRAME_TEXT_COLOR, THICKNESS)
    y += 30
    cv2.putText(frame, f'Confianza aprox: {confidence:.2f}', (10, y), FONT, FONT_SCALE, FRAME_TEXT_COLOR, 1)
    y += 30
    cv2.putText(frame, f'FPS: {fps:.1f}', (10, y), FONT, FONT_SCALE, FRAME_TEXT_COLOR, 1)
    y += 30

    for name, value in angles.items():
        text = f'{name}: {value:.1f}°' if not np.isnan(value) else f'{name}: N/A'
        cv2.putText(frame, text, (10, y), FONT, FONT_SCALE, FRAME_TEXT_COLOR, 1)
        y += 25


def smooth_prediction(history: deque, new_label: str, maxlen: int = 8) -> str:
    history.append(new_label)
    if len(history) > maxlen:
        history.popleft()
    values, counts = np.unique(history, return_counts=True)
    return values[counts.argmax()]


def main():
    parser = argparse.ArgumentParser(description='MoveSense real-time inference demo')
    parser.add_argument('--models-dir', type=str, default='Entrega 3/deployment/models', help='Directorio con artefactos joblib')
    parser.add_argument('--camera-index', type=int, default=0, help='Índice de la cámara a utilizar')
    parser.add_argument('--confidence-history', type=int, default=8, help='Tamaño de la ventana para suavizado de etiquetas')
    args = parser.parse_args()

    models_dir = Path(args.models_dir)
    if not models_dir.exists():
        raise FileNotFoundError(f'No se encontró el directorio de modelos en {models_dir}')

    pipeline, label_encoder, feature_names, metadata = load_artifacts(models_dir)
    print('[INFO] Artefactos cargados. Etiquetas:', list(label_encoder.classes_))
    if metadata:
        print('[INFO] Metadata:', metadata)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False, smooth_landmarks=True)
    drawer = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(args.camera_index)
    if not cap.isOpened():
        raise RuntimeError('No se pudo abrir la cámara. Verifica el índice o permisos.')

    prediction_history = deque(maxlen=args.confidence_history)
    prev_time = cv2.getTickCount()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print('[WARN] No se recibió frame de la cámara. Reiniciando...')
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            if results.pose_landmarks:
                drawer.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            features_df = extract_features(results, feature_names)
            classifier = pipeline.named_steps['classifier']
            probs = pipeline.predict_proba(features_df) if hasattr(classifier, 'predict_proba') else None
            pred_encoded = pipeline.predict(features_df)[0]
            pred_label = label_encoder.inverse_transform([pred_encoded])[0]

            smooth_label = smooth_prediction(prediction_history, pred_label, args.confidence_history)
            history_list = list(prediction_history)
            if probs is not None:
                confidence = float(np.max(probs))
            elif history_list:
                confidence = history_list.count(smooth_label) / len(history_list)
            else:
                confidence = 1.0

            angles = {}
            if results.pose_landmarks:
                angles = compute_pose_angles(results.pose_landmarks.landmark)

            curr_time = cv2.getTickCount()
            fps = cv2.getTickFrequency() / (curr_time - prev_time)
            prev_time = curr_time

            overlay_info(frame, smooth_label, confidence, angles, fps)

            cv2.imshow('MoveSense — Clasificación en Tiempo Real', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    finally:
        cap.release()
        pose.close()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
