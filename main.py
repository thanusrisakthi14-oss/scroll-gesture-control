import cv2
import mediapipe as mp
import pyautogui

cap=cv2.VideoCapture(0)
mp_hands=mp.solutions.hands
hands=mp_hands.Hands(max_num_hands=1)
mp_draw=mp.solutions.drawing_utils

prev_y=None
while True:
    rect, frame=cap.read()
    if not rect:
        break
    frame=cv2.flip(frame,1)
    rgb=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results=hands.process(rgb)
    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand,mp_hands.HAND_CONNECTIONS)
        h,w,_=frame.shape
        x=int(hand.landmark[8].x*w)
        y=int(hand.landmark[8].y*h)
        cv2.circle(frame,(x,y),10,(0,255,0),-1)
        if prev_y is not None:
            diff=y-prev_y
            if prev_y>20:
                pyautogui.scroll(-100)
            elif diff<-20:
                pyautogui.scroll(100)
        prev_y=y
    cv2.imshow("Gesture scrolling",frame)
    if cv2.waitKey(1)& 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()