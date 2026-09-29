import cv2
import time
from capture.camera import CameraCapture
from vision.hand_tracker import HandTracker
from gestures.features import HandFeatures
from gestures.detectors import ClickDetector
from pointer.controller import CursorController

def main():
    print("Starting AirKey Phase 1: Pointer Control + Click Lock + Clutch")
    cam = CameraCapture(camera_index=0)
    if not cam.start():
        return

    tracker = HandTracker()
    # Eşikler: 0.8 açılma, 0.65 kapanma
    open_thresh = 0.8
    close_thresh = 0.65
    click_detector = ClickDetector(open_threshold=open_thresh, close_threshold=close_thresh)
    
    # Ekran boyutunu şimdilik sabit veriyoruz (Prototip ekranı)
    # Gerçek uygulamada Windows ekran çözünürlüğü olacak
    screen_w, screen_h = 1280, 720
    cursor_ctrl = CursorController(screen_w, screen_h)
    
    cv2.namedWindow("AirKey Phase 1", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AirKey Phase 1", screen_w, screen_h)
    
    last_click_time = 0
    click_count = 0

    try:
        while True:
            frame = cam.get_frame()
            if frame is None:
                time.sleep(0.01)
                continue
                
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (screen_w, screen_h)) # UI ile uyumlu olması için büyütüyoruz
            
            results = tracker.process(frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    features = HandFeatures(hand_landmarks)
                    idx_x, idx_y = features.get_index_tip()
                    hand_size = features.get_hand_size()
                    
                    # 1. Debriyaj (Clutch) Kontrolü
                    # İşaret parmağı kapalıysa (yumruk), imleç donar.
                    is_index_ext = features.is_index_extended()
                    is_clutched = not is_index_ext
                    
                    # 2. Tık Kontrolü
                    thumb_dist = features.get_normalized_thumb_distance()
                    click_event, is_thumb_open = click_detector.process(thumb_dist)
                    
                    if click_event:
                        click_count += 1
                        last_click_time = time.time()
                        print(f"Click! Total: {click_count}")

                    # 3. Tık Kilidi (Heisenberg) Durumu
                    # Baş parmak hareket halindeyse (açılmaya başladıysa veya açıksa) imleci kilitle
                    thumb_is_moving = is_thumb_open or thumb_dist > close_thresh
                    
                    # 4. İmleç Güncellemesi
                    t = time.time()
                    cx, cy, is_locked = cursor_ctrl.update(idx_x, idx_y, hand_size, is_clutched, thumb_is_moving, t)
                    
                    # Draw UI on frame
                    # İmleç rengi: Debriyaj = Gri, Kilitli (Tık) = Yeşil, Normal = Kırmızı
                    if is_clutched:
                        color = (150, 150, 150)
                    elif is_locked:
                        color = (0, 255, 0)
                    else:
                        color = (0, 0, 255)
                        
                    cv2.circle(frame, (cx, cy), 15, color, cv2.FILLED)
                    cv2.circle(frame, (cx, cy), 18, (255, 255, 255), 2) # Dış çerçeve
                    
                    state_text = f"Thumb: {'OPEN' if is_thumb_open else 'CLOSED'} | Clutch: {'ON' if is_clutched else 'OFF'}"
                    cv2.putText(frame, state_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                    cv2.putText(frame, f"Dist: {thumb_dist:.2f}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                    
                    # Görsel geri bildirim (Bar)
                    bar_max = 2.0
                    bar_w = 200
                    fill_w = int(min(thumb_dist / bar_max, 1.0) * bar_w)
                    cv2.rectangle(frame, (10, 90), (10 + bar_w, 110), (100, 100, 100), 2)
                    cv2.rectangle(frame, (10, 90), (10 + fill_w, 110), color, -1)
                    
                    open_x = int((open_thresh / bar_max) * bar_w)
                    close_x = int((close_thresh / bar_max) * bar_w)
                    cv2.line(frame, (10 + open_x, 85), (10 + open_x, 115), (0, 255, 0), 2) 
                    cv2.line(frame, (10 + close_x, 85), (10 + close_x, 115), (0, 0, 255), 2)
                    
                    if time.time() - last_click_time < 0.5:
                        cv2.putText(frame, "CLICK!", (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 3)

            # Draw landmarks (Opaklık düşürülebilir ama şimdilik doğrudan çiziyoruz)
            frame = tracker.draw_landmarks(frame, results)
            
            cv2.imshow("AirKey Phase 1", frame)
            
            if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("AirKey Phase 1", cv2.WND_PROP_VISIBLE) < 1:
                break
    finally:
        cam.stop()
        cv2.destroyAllWindows()
        print("Stopped.")

if __name__ == "__main__":
    main()
