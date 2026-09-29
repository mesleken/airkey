import math
import mediapipe as mp

def get_distance(p1, p2):
    # MediaPipe Z koordinatını da kullanarak 3 boyutlu mesafe ölçümü
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)

class HandFeatures:
    def __init__(self, hand_landmarks):
        self.landmarks = hand_landmarks.landmark
        self.mp_hands = mp.solutions.hands

    def get_index_tip(self):
        tip = self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        return tip.x, tip.y
        
    def get_thumb_tip(self):
        tip = self.landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        return tip.x, tip.y

    def get_thumb_mcp(self):
        mcp = self.landmarks[self.mp_hands.HandLandmark.THUMB_MCP]
        return mcp.x, mcp.y

    def get_index_mcp(self):
        mcp = self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        return mcp.x, mcp.y

    def get_wrist(self):
        wrist = self.landmarks[self.mp_hands.HandLandmark.WRIST]
        return wrist.x, wrist.y

    def get_hand_size(self):
        # Palm width (index_mcp to pinky_mcp) in 3D
        index_mcp = self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        pinky_mcp = self.landmarks[self.mp_hands.HandLandmark.PINKY_MCP]
        return get_distance(index_mcp, pinky_mcp)

    def get_normalized_thumb_distance(self):
        # Distance from thumb tip to index mcp in 3D
        thumb_tip = self.landmarks[self.mp_hands.HandLandmark.THUMB_TIP]
        index_mcp = self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        dist = get_distance(thumb_tip, index_mcp)
        size = self.get_hand_size()
        if size > 0:
            return dist / size
        return 0

    def is_index_extended(self):
        # If the tip is further from the wrist than the PIP joint, it's extended.
        # When curled into a fist, the tip is much closer to the wrist than the PIP.
        tip = self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        pip = self.landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_PIP]
        wrist = self.landmarks[self.mp_hands.HandLandmark.WRIST]
        
        dist_tip = get_distance(tip, wrist)
        dist_pip = get_distance(pip, wrist)
        
        return dist_tip > dist_pip
