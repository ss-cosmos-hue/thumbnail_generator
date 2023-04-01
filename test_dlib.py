import dlib
import cv2
import matplotlib as plt

face_detect = dlib.get_frontal_face_detector()

rects = face_detect(gray, 1)

for (i, rect) in enumerate(rects):
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 255, 255), 3)

plt.figure(figsize=(12, 8))
plt.imshow(gray, cmap='gray')
plt.show()
