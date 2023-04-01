import os
import cv2
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For static images:
cwd = os.path.join(os.getcwd(), "images")
IMAGE_FILES = [os.path.join(cwd, file) for file in os.listdir("images")]
print(IMAGE_FILES)

with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Draw face detections of each face.
        if not results.detections:
            print("No face detected for image", idx)
            continue
        annotated_image = image.copy()
        for detection in results.detections:
            # print('Nose tip:')
            # print(mp_face_detection.get_key_point(
            #     detection, mp_face_detection.FaceKeyPoint.NOSE_TIP))
            mp_drawing.draw_detection(annotated_image, detection)
        cv2.imwrite('/tmp/annotated_image' +
                    str(idx) + '.png', annotated_image)
