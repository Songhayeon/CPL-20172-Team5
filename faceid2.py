import cv2 

while True:
    ret, img = cap.read()

    input_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    detected = detector(input_img, 1)
    current_viewers = len(detected)
    if current_viewers > last_total_current_viewers:
        user_id += current_viewers - last_total_current_viewers
    last_total_current_viewers = current_viewers

    for i, d in enumerate(detected):
        x1, y1, x2, y2, w, h = d.left(), d.top(), d.right() + 1, d.bottom() + 1, d.width(), d.height()
        cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(img, 'user_' + str(i), (x1, y1), font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("result", img)
    key = cv2.waitKey(30)

    if key == 27:
        break
