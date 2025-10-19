import streamlit as st
import cv2
import numpy as np
from scipy import stats
import kociemba
import time
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, ClientSettings
import streamlit_rotate  # Import the adapted rotate functions
import av # Required by streamlit_webrtc

# --- Configuration for Webcam ---
# Use ClientSettings to potentially reduce latency if needed, but defaults are often fine.
# client_settings = ClientSettings(
#     rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
#     media_stream_constraints={"video": True, "audio": False},
# )

# --- Session State Initialization ---
# This is crucial for Streamlit apps to remember data between reruns
if 'current_frame' not in st.session_state:
    st.session_state.current_frame = None
if 'up_face' not in st.session_state:
    st.session_state.up_face = None
if 'right_face' not in st.session_state:
    st.session_state.right_face = None
if 'front_face' not in st.session_state:
    st.session_state.front_face = None
if 'down_face' not in st.session_state:
    st.session_state.down_face = None
if 'left_face' not in st.session_state:
    st.session_state.left_face = None
if 'back_face' not in st.session_state:
    st.session_state.back_face = None
if 'scan_stage' not in st.session_state:
    st.session_state.scan_stage = "Front" # Start by asking for Front face
if 'solution_str' not in st.session_state:
    st.session_state.solution_str = ""
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""
if 'cube_definition' not in st.session_state:
    st.session_state.cube_definition = ""


# --- Video Frame Callback Class (for streamlit_webrtc) ---
class VideoProcessor(VideoProcessorBase):
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        # Convert the frame to an OpenCV BGR image (NumPy array)
        img = frame.to_ndarray(format="bgr24")
        # Store the latest frame in session state
        st.session_state.current_frame = img
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- Face Detection Logic (Adapted from your main.py) ---
# Note: Removed drawing functions, focus is on color detection
def detect_face_colors(bgr_image_input):
    if bgr_image_input is None:
        return None, "No image received"

    gray = cv2.cvtColor(bgr_image_input, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    gray = cv2.adaptiveThreshold(gray, 20, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0)

    try:
        contours, _ = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    except ValueError: # Handle OpenCV version difference
         _, contours, _ = cv2.findContours(gray, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)


    blob_colors = []
    processed_image = bgr_image_input.copy() # To draw contours on

    for contour in contours:
        A1 = cv2.contourArea(contour)
        if 1000 < A1 < 3000: # Adjusted thresholds might be needed
            perimeter = cv2.arcLength(contour, True)
            if perimeter > 0: # Avoid division by zero
                epsilon = 0.01 * perimeter
                approx = cv2.approxPolyDP(contour, epsilon, True)
                # Check for squareness more robustly
                is_square_like = len(approx) == 4 and abs(1 - w/h) < 0.2 if cv2.boundingRect(contour)[2] > 0 and cv2.boundingRect(contour)[3] > 0 else False
                x, y, w, h = cv2.boundingRect(contour)

                if cv2.isContourConvex(approx) and is_square_like: # Added convexity check
                   # Calculate stability metric - less sensitive than original
                    solidity = A1 / cv2.contourArea(cv2.convexHull(contour)) if cv2.contourArea(cv2.convexHull(contour)) > 0 else 0

                    if solidity > 0.9: # Check if contour is filled (likely a sticker)
                         cv2.drawContours(processed_image,[contour],0,(0, 255, 0),2) # Draw green contour

                         val = (50 * y) + (10 * x) # Positional sorting value
                         blob_color_mean = np.array(cv2.mean(bgr_image_input[y:y + h, x:x + w])[:3]).astype(int) # Get BGR mean

                         # Store BGR, sorting value, x, y, w, h
                         blob_data = np.append(blob_color_mean, [val, x, y, w, h])
                         blob_colors.append(blob_data)

    if len(blob_colors) != 9:
        st.warning(f"Detected {len(blob_colors)} potential stickers instead of 9. Adjust lighting/position.")
        return None, processed_image # Return image with contours for debugging

    # Sort based on the calculated positional value
    blob_colors = np.asarray(blob_colors)
    blob_colors = blob_colors[blob_colors[:, 3].argsort()] # Sort by 'val'

    face_colors = np.zeros(9, dtype=int)
    color_map = {1: 'Y', 2: 'O', 3: 'B', 4: 'G', 5: 'R', 6: 'W'} # Example mapping
    detected_color_chars = []

    for i in range(9):
        b, g, r = blob_colors[i][:3]
        color_code = 0
        # Color detection logic (NEEDS CAREFUL CALIBRATION for your lighting/camera)
        # This is a simplified example, you'll need to refine these ranges
        if r > 150 and g > 150 and b < 100: color_code = 1 # Yellow
        elif r > 180 and g > 80 and g < 150 and b < 100: color_code = 2 # Orange
        elif r < 100 and g < 100 and b > 150: color_code = 3 # Blue
        elif r < 100 and g > 150 and b < 100: color_code = 4 # Green
        elif r > 170 and g < 80 and b < 80: color_code = 5 # Red
        elif r > 150 and g > 150 and b > 150: color_code = 6 # White

        if color_code == 0:
            st.warning(f"Could not classify color for sticker {i+1} (BGR: {b},{g},{r}).")
            return None, processed_image # Failed classification

        face_colors[i] = color_code
        detected_color_chars.append(color_map.get(color_code, '?'))

        # Add text label to the image
        cx = int(blob_colors[i][4] + blob_colors[i][6] / 2)
        cy = int(blob_colors[i][5] + blob_colors[i][7] / 2)
        cv2.putText(processed_image, color_map.get(color_code, '?'), (cx - 10, cy + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 3, cv2.LINE_AA)
        cv2.putText(processed_image, color_map.get(color_code, '?'), (cx - 10, cy + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1, cv2.LINE_AA)


    if 0 in face_colors: # Check if any color failed
        return None, processed_image

    return face_colors, processed_image

# --- Concatenate Function (from main.py) ---
def concat_faces(up, right, front, down, left, back):
    if None in [up, right, front, down, left, back]:
        return None
    # Ensure they are numpy arrays before concatenating
    solution = np.concatenate((
        np.asarray(up), np.asarray(right), np.asarray(front),
        np.asarray(down), np.asarray(left), np.asarray(back)
    ), axis=None)
    return solution

# --- Convert to Kociemba String ---
def convert_to_kociemba_string(solution_array, face_centers):
    """ Converts the numeric array to Kociemba's URFDLB string format. """
    if solution_array is None or len(solution_array) != 54:
        return None, "Invalid array for conversion"
    if None in face_centers.values():
        return None, "Center colors not fully determined"

    center_map = {
        face_centers['U']: 'U', face_centers['R']: 'R', face_centers['F']: 'F',
        face_centers['D']: 'D', face_centers['L']: 'L', face_centers['B']: 'B'
    }
    kociemba_str = ""
    for color_code in solution_array:
        char = center_map.get(color_code)
        if char is None:
            return None, f"Unknown color code {color_code} encountered"
        kociemba_str += char
    return kociemba_str, None


# --- Streamlit UI ---
st.title("Rubik's Cube Solver - Webcam Scanner")

st.info("Hold the cube steady and ensure good, consistent lighting.")

# Start the webcam feed
webrtc_ctx = webrtc_streamer(
    key="webcam",
    video_processor_factory=VideoProcessor,
    # client_settings=client_settings, # Optional settings
    async_processing=True,
)

st.markdown("---")

# Display current scan stage and instructions
st.subheader(f"Scan Stage: {st.session_state.scan_stage} Face")
instruction_placeholder = st.empty()
if st.session_state.scan_stage != "Solved":
    instruction_placeholder.write(f"Position the **{st.session_state.scan_stage} face** towards the camera and click the button below.")
else:
     instruction_placeholder.write("Cube state scanned. Calculating solution...")


# --- Face Display Columns ---
col1, col2, col3 = st.columns(3)
with col1:
    st.write("**Up (U):**")
    st.write(st.session_state.up_face if st.session_state.up_face is not None else "Not Scanned")
    st.write("**Left (L):**")
    st.write(st.session_state.left_face if st.session_state.left_face is not None else "Not Scanned")
with col2:
    st.write("**Front (F):**")
    st.write(st.session_state.front_face if st.session_state.front_face is not None else "Not Scanned")
    st.write("**Down (D):**")
    st.write(st.session_state.down_face if st.session_state.down_face is not None else "Not Scanned")
with col3:
    st.write("**Right (R):**")
    st.write(st.session_state.right_face if st.session_state.right_face is not None else "Not Scanned")
    st.write("**Back (B):**")
    st.write(st.session_state.back_face if st.session_state.back_face is not None else "Not Scanned")

st.markdown("---")

# Area to display the processed image after scanning
image_placeholder = st.empty()

# --- Scan Button Logic ---
scan_button_disabled = st.session_state.scan_stage == "Solved"
if st.button(f"Scan {st.session_state.scan_stage} Face", disabled=scan_button_disabled):
    st.session_state.error_message = "" # Clear previous errors
    if st.session_state.current_frame is not None:
        face_colors, processed_img = detect_face_colors(st.session_state.current_frame)

        if processed_img is not None:
             # Display the image with detected contours/colors
            image_placeholder.image(processed_img, channels="BGR", caption=f"Processed {st.session_state.scan_stage} Face")

        if face_colors is not None:
            st.success(f"{st.session_state.scan_stage} face scanned successfully!")
            time.sleep(1) # Brief pause

            # Store the scanned face in session state
            if st.session_state.scan_stage == "Front":
                st.session_state.front_face = face_colors
                st.session_state.scan_stage = "Top" # Move to next stage
            elif st.session_state.scan_stage == "Top":
                st.session_state.up_face = face_colors
                st.session_state.scan_stage = "Down"
            elif st.session_state.scan_stage == "Down":
                st.session_state.down_face = face_colors
                st.session_state.scan_stage = "Right"
            elif st.session_state.scan_stage == "Right":
                st.session_state.right_face = face_colors
                st.session_state.scan_stage = "Left"
            elif st.session_state.scan_stage == "Left":
                st.session_state.left_face = face_colors
                st.session_state.scan_stage = "Back"
            elif st.session_state.scan_stage == "Back":
                st.session_state.back_face = face_colors
                st.session_state.scan_stage = "Solved" # All faces scanned

            # Rerun the script to update the UI (buttons, text, etc.)
            st.experimental_rerun()
        else:
            st.session_state.error_message = f"Failed to detect all 9 colors for {st.session_state.scan_stage} face. Please check lighting and cube position."
    else:
        st.session_state.error_message = "Webcam frame not available. Ensure webcam is active."

# Display errors if any occurred
if st.session_state.error_message:
    st.error(st.session_state.error_message)

# --- Solution Logic ---
if st.session_state.scan_stage == "Solved" and not st.session_state.solution_str:
    instruction_placeholder.write("All faces scanned. Calculating solution...")
    image_placeholder.empty() # Clear the last scanned image

    # Determine center colors (important for Kociemba string)
    face_centers = {}
    try:
        face_centers['F'] = st.session_state.front_face[4] if st.session_state.front_face is not None else None
        face_centers['U'] = st.session_state.up_face[4] if st.session_state.up_face is not None else None
        face_centers['D'] = st.session_state.down_face[4] if st.session_state.down_face is not None else None
        face_centers['R'] = st.session_state.right_face[4] if st.session_state.right_face is not None else None
        face_centers['L'] = st.session_state.left_face[4] if st.session_state.left_face is not None else None
        face_centers['B'] = st.session_state.back_face[4] if st.session_state.back_face is not None else None
    except IndexError:
        st.error("Error accessing center color. Please rescan.")
        st.session_state.scan_stage = "Front" # Reset scan stage
        # Reset faces
        st.session_state.front_face = None
        # ... reset others ...
        st.experimental_rerun()


    # Concatenate faces
    solution_array = concat_faces(
        st.session_state.up_face, st.session_state.right_face, st.session_state.front_face,
        st.session_state.down_face, st.session_state.left_face, st.session_state.back_face
    )

    if solution_array is not None and None not in face_centers.values():
        # Convert to Kociemba string
        cube_def_string, convert_err = convert_to_kociemba_string(solution_array, face_centers)
        st.session_state.cube_definition = cube_def_string # Store for display

        if convert_err:
             st.error(f"Error preparing cube string: {convert_err}. Please rescan.")
             # Optionally reset scan state here
        elif cube_def_string:
            st.write(f"Cube Definition String: `{cube_def_string}`") # Show the string
            try:
                # Solve using Kociemba
                st.session_state.solution_str = kociemba.solve(cube_def_string)
                st.success("Solution Found!")
                st.subheader("Solution Steps:")
                st.markdown(f"```\n{st.session_state.solution_str}\n```")
            except ValueError as e:
                st.error(f"Solver Error: {e}. The scanned colors might be incorrect or represent an impossible cube state. Please rescan carefully.")
                # Reset scan stage
                st.session_state.scan_stage = "Front"
                st.session_state.front_face = None
                st.session_state.up_face = None
                st.session_state.down_face = None
                st.session_state.right_face = None
                st.session_state.left_face = None
                st.session_state.back_face = None
                st.session_state.solution_str = ""
                st.session_state.cube_definition = ""
                st.button("Reset and Scan Again") # User clicks this to rerun
                st.stop() # Stop further execution until reset
            except Exception as e:
                st.error(f"An unexpected error occurred during solving: {e}")
                # Reset scan stage as above
                st.session_state.scan_stage = "Front"
                # ... reset faces ...
                st.session_state.solution_str = ""
                st.session_state.cube_definition = ""
                st.button("Reset and Scan Again")
                st.stop()
    else:
        st.warning("Could not solve. One or more faces were not scanned correctly.")
        # Optionally add a reset button here too

# Display final solution if already calculated
if st.session_state.solution_str and st.session_state.scan_stage == "Solved":
    instruction_placeholder.write("Solution Calculated!")
    image_placeholder.empty()
    st.subheader("Solution Steps:")
    st.markdown(f"Cube Definition String: `{st.session_state.cube_definition}`")
    st.markdown(f"```\n{st.session_state.solution_str}\n```")
    st.info("Follow the steps carefully. F=Front, B=Back, U=Up, D=Down, L=Left, R=Right. Apostrophe (') means counter-clockwise, '2' means 180 degrees.")
    if st.button("Scan Another Cube"):
         # Reset everything
         st.session_state.scan_stage = "Front"
         st.session_state.front_face = None
         st.session_state.up_face = None
         st.session_state.down_face = None
         st.session_state.right_face = None
         st.session_state.left_face = None
         st.session_state.back_face = None
         st.session_state.solution_str = ""
         st.session_state.error_message = ""
         st.session_state.cube_definition = ""
         st.experimental_rerun()