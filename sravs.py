import cv2
import mediapipe as mp
import pyautogui  
import time
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
last_action_time = 0
def count_fingers(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    fingers = []
    if hand_landmarks.landmark[tips[0]].x < hand_landmarks.landmark[tips[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1, 5):
        if hand_landmarks.landmark[tips[i]].y < hand_landmarks.landmark[tips[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers)
while True:
    success, img = cap.read()
    if not success:
        break
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            fingers = count_fingers(handLms)
            current_time = time.time()
            if current_time - last_action_time > 1:
                if fingers == 1:
                    pyautogui.press('playpause')   # Play/Pause
                    action = "Play/Pause"
                elif fingers == 2:
                    pyautogui.press('volumeup')   # Volume Up
                    action = "Volume Up"
                elif fingers == 3:
                    pyautogui.press('volumedown') # Volume Down
                    action = "Volume Down"
                elif fingers == 4:
                    pyautogui.press('nexttrack')  # Next Song
                    action = "Next Track"
                elif fingers == 5:
                    pyautogui.press('prevtrack')  # Previous Song
                    action = "Previous Track"
                else:
                    action = "None"
                last_action_time = current_time
            else:
                action = ""
            cv2.putText(img, f'Fingers: {fingers}', (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(img, f'Action: {action}', (10, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Media Controller", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break
cap.release()
cv2.destroyAllWindows()