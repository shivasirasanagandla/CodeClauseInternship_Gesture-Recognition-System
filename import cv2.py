import cv2 
import mediapipe as mp
import pyautogui
import time
import streamlit as st

def count_fingers(lst):
    cnt = 0

    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2

    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt += 1

    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt += 1

    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt += 1

    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt += 1

    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 6:
        cnt += 1

    return cnt 

st.title("Gesture Control")

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=1)

prev = -1

st.sidebar.write("Use the buttons to control the actions:")
button_right = st.sidebar.button("Right")
button_left = st.sidebar.button("Left")
button_up = st.sidebar.button("Up")
button_down = st.sidebar.button("Down")
button_space = st.sidebar.button("Space")

while True:
    end_time = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:

        hand_keyPoints = res.multi_hand_landmarks[0]

        cnt = count_fingers(hand_keyPoints)

        if not(prev==cnt):
            if (cnt == 1):
                if button_right:
                    pyautogui.press("right")
                
            elif (cnt == 2):
                if button_left:
                    pyautogui.press("left")

            elif (cnt == 3):
                if button_up:
                    pyautogui.press("up")

            elif (cnt == 4):
                if button_down:
                    pyautogui.press("down")

            elif (cnt == 5):
                if button_space:
                    pyautogui.press("space")

            prev = cnt

        drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)

    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
