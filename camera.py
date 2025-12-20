import cv2
from fer import FER

class CameraEmotionDetector:
    def __init__(self):
        self.detector = FER(mtcnn=True)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def read_emotion(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None

        detections = self.detector.detect_emotions(frame)
        if not detections:
            return None, frame

        emotions = detections[0]["emotions"]
        return emotions, frame




    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()
