import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, List, Tuple
import time
import math

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Finger tip landmark indices
        self.finger_tips = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
        self.finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
        
        # Palm landmarks for calculating palm center and radius
        self.palm_landmarks = [0, 1, 5, 9, 13, 17]  # Key palm points
        
        # Gesture stability - balanced for accuracy and responsiveness
        self.gesture_history = []
        self.history_length = 4  # Reduced for less delay
        self.last_stable_gesture = 0
        self.stability_threshold = 0.75  # Balanced threshold
        
        # Camera setup
        self.cap = None
        
        # Palm circle parameters
        self.palm_radius_multiplier = 1.3  # Make circle 30% bigger than palm for better thumb detection
        
    def start_camera(self, camera_index: int = 0) -> bool:
        """Initialize camera capture"""
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {camera_index}")
            return False
        
        # Set camera properties for better performance
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        return True
    
    def stop_camera(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
    
    def calculate_palm_circle(self, landmarks) -> tuple:
        """Calculate palm center and radius based on hand landmarks"""
        # Get palm points
        palm_points = []
        for idx in self.palm_landmarks:
            palm_points.append([landmarks[idx].x, landmarks[idx].y])
        
        palm_points = np.array(palm_points)
        
        # Calculate palm center (centroid of palm points)
        palm_center_x = np.mean(palm_points[:, 0])
        palm_center_y = np.mean(palm_points[:, 1])
        
        # Calculate palm radius (distance from center to furthest palm point)
        distances = []
        for point in palm_points:
            dist = math.sqrt((point[0] - palm_center_x)**2 + (point[1] - palm_center_y)**2)
            distances.append(dist)
        
        palm_radius = max(distances) * self.palm_radius_multiplier
        
        return (palm_center_x, palm_center_y), palm_radius
    
    def is_finger_outside_palm_circle(self, finger_tip, palm_center, palm_radius, is_thumb=False) -> bool:
        """Check if finger tip is outside the palm circle"""
        distance = math.sqrt(
            (finger_tip.x - palm_center[0])**2 + 
            (finger_tip.y - palm_center[1])**2
        )
        # Use smaller threshold for thumb since it extends in different direction
        threshold_multiplier = 0.85 if is_thumb else 1.0
        return distance > (palm_radius * threshold_multiplier)
    
    def count_extended_fingers(self, landmarks, is_right_hand=True) -> int:
        """Count extended fingers using palm circle method"""
        # Calculate palm circle
        palm_center, palm_radius = self.calculate_palm_circle(landmarks)
        
        extended_fingers = 0
        
        # Check each finger tip
        for i, tip_id in enumerate(self.finger_tips):
            finger_tip = landmarks[tip_id]
            is_thumb = (i == 0)  # First finger is thumb
            
            # Check if finger tip is outside palm circle
            if self.is_finger_outside_palm_circle(finger_tip, palm_center, palm_radius, is_thumb):
                extended_fingers += 1
                print(f"{self.finger_names[i]}: Extended (outside palm circle)")
            else:
                print(f"{self.finger_names[i]}: Folded (inside palm circle)")
        
        return extended_fingers
    
    def is_right_hand(self, landmarks) -> bool:
        """Determine if the detected hand is the right hand"""
        # Compare thumb and pinky positions
        thumb_x = landmarks[4].x  # Thumb tip
        pinky_x = landmarks[20].x  # Pinky tip
        
        # For right hand, thumb should be on the right side of pinky
        return thumb_x > pinky_x
    
    def get_stable_gesture(self, current_fingers: int) -> int:
        """Apply stability filtering to gesture recognition"""
        self.gesture_history.append(current_fingers)
        
        # Keep only recent history
        if len(self.gesture_history) > self.history_length:
            self.gesture_history.pop(0)
        
        # Check if we have enough history
        if len(self.gesture_history) < self.history_length:
            return self.last_stable_gesture
        
        # Count occurrences of each gesture
        gesture_counts = {}
        for gesture in self.gesture_history:
            gesture_counts[gesture] = gesture_counts.get(gesture, 0) + 1
        
        # Find the most frequent gesture
        most_frequent_gesture = max(gesture_counts, key=gesture_counts.get)
        stability_ratio = gesture_counts[most_frequent_gesture] / len(self.gesture_history)
        
        # Update stable gesture if stability threshold is met
        if stability_ratio >= self.stability_threshold:
            self.last_stable_gesture = most_frequent_gesture
        
        return self.last_stable_gesture
    
    def draw_heart(self, frame, center_x, center_y, size=50):
        """Draw a cute hollow pink heart at the specified location"""
        # Light pink color (BGR format)
        pink = (203, 192, 255)  # Light pink
        thickness = 3
        
        # Heart shape using curves and lines
        # Calculate heart points
        heart_points = []
        for i in range(360):
            angle = math.radians(i)
            # Heart equation: x = 16*sin^3(t), y = 13*cos(t) - 5*cos(2t) - 2*cos(3t) - cos(4t)
            x = 16 * (math.sin(angle) ** 3)
            y = -(13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle))
            
            # Scale and translate
            x = int(center_x + (x * size / 40))
            y = int(center_y + (y * size / 40))
            heart_points.append((x, y))
        
        # Draw heart outline
        for i in range(len(heart_points)):
            start_point = heart_points[i]
            end_point = heart_points[(i + 1) % len(heart_points)]
            cv2.line(frame, start_point, end_point, pink, thickness)
    
    def process_frame(self) -> Tuple[Optional[np.ndarray], int]:
        """Process one frame and return the frame and detected finger count"""
        if not self.cap:
            return None, 0
        
        ret, frame = self.cap.read()
        if not ret:
            return None, 0
        
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        frame_height, frame_width = frame.shape[:2]
        
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        finger_count = 0
        
        if results.multi_hand_landmarks:
            # Priority: right hand first, then any hand
            right_hand = None
            any_hand = None
            
            for hand_landmarks in results.multi_hand_landmarks:
                if self.is_right_hand(hand_landmarks.landmark):
                    right_hand = hand_landmarks
                else:
                    any_hand = hand_landmarks
            
            # Use right hand if available, otherwise use any hand
            selected_hand = right_hand if right_hand is not None else any_hand
            
            if selected_hand:
                # Draw cute heart instead of hand skeleton
                # Calculate heart position (center of palm with upward offset)
                wrist = selected_hand.landmark[0]  # Wrist landmark
                middle_mcp = selected_hand.landmark[9]  # Middle finger MCP
                heart_x = int((wrist.x + middle_mcp.x) / 2 * frame_width)
                heart_y = int((wrist.y + middle_mcp.y) / 2 * frame_height)
                
                # Move heart up by 40 pixels for better positioning
                heart_y -= 40
                
                # Count extended fingers first
                is_right = (selected_hand == right_hand)
                raw_finger_count = self.count_extended_fingers(selected_hand.landmark, is_right)
                finger_count = self.get_stable_gesture(raw_finger_count)
                
                # Calculate hand size for base scaling
                middle_tip = selected_hand.landmark[12]  # Middle finger tip
                hand_span = math.sqrt(
                    ((middle_tip.x - wrist.x) * frame_width) ** 2 + 
                    ((middle_tip.y - wrist.y) * frame_height) ** 2
                )
                
                # Base heart size (smaller than before)
                base_size = max(60, min(120, int(hand_span * 0.6)))
                
                # Scale heart size based on number of extended fingers
                # 0 fingers = base size, 5 fingers = 2.5x base size
                finger_multiplier = 1.0 + (finger_count * 0.3)  # Grows by 30% per finger
                heart_size = int(base_size * finger_multiplier)
                
                # Draw heart
                self.draw_heart(frame, heart_x, heart_y, size=heart_size)
                
                # Indicate which hand is being used
                hand_type = "Right Hand" if selected_hand == right_hand else "Left Hand"
                cv2.putText(frame, f'{hand_type} - Fingers: {finger_count}', 
                          (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Draw chord indicator
                if finger_count > 0:
                    cv2.putText(frame, f'Chord {finger_count}', 
                              (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        return frame, finger_count
    
    def run_preview(self):
        """Run a preview window to test gesture recognition"""
        if not self.start_camera():
            return
        
        print("Hand Gesture Recognition Preview")
        print("Show your right hand to the camera")
        print("Press 'q' to quit")
        
        try:
            while True:
                frame, finger_count = self.process_frame()
                
                if frame is not None:
                    cv2.imshow('Hand Gesture Recognition', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                    
        except KeyboardInterrupt:
            print("Interrupted by user")
        finally:
            self.stop_camera()

if __name__ == "__main__":
    recognizer = GestureRecognizer()
    recognizer.run_preview()