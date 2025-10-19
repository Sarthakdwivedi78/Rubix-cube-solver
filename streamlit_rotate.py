import numpy as np

# --- Face Rotation (Same as before) ---
def rotate_cw(face):
    if face is None: return None
    final = np.copy(face)
    # Clockwise sticker reassignment (indices 0-8)
    final[0] = face[6]
    final[1] = face[3]
    final[2] = face[0]
    final[3] = face[7]
    final[4] = face[4] # Center stays
    final[5] = face[1]
    final[6] = face[8]
    final[7] = face[5]
    final[8] = face[2]
    return final

def rotate_ccw(face):
    if face is None: return None
    final = np.copy(face)
    # Counter-clockwise sticker reassignment
    final[8] = face[6]
    final[7] = face[3]
    final[6] = face[0]
    final[5] = face[7]
    final[4] = face[4] # Center stays
    final[3] = face[1]
    final[2] = face[8]
    final[1] = face[5]
    final[0] = face[2]
    return final


# --- Move Simulation Functions (NO webcam verification or arrow drawing) ---
# These functions now ONLY update the internal numpy arrays representing the cube state.

def right_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, front_face, down_face, back_face]:
        print("Error: One or more faces are None in right_cw")
        return up_face, right_face, front_face, down_face, left_face, back_face # Return unchanged

    temp = np.copy(front_face)
    front_face[2] = down_face[2]
    front_face[5] = down_face[5]
    front_face[8] = down_face[8]
    down_face[2] = back_face[6] # Note: Indices adjusted for 1D array access
    down_face[5] = back_face[3]
    down_face[8] = back_face[0]
    back_face[0] = up_face[8]
    back_face[3] = up_face[5]
    back_face[6] = up_face[2]
    up_face[2] = temp[2]
    up_face[5] = temp[5]
    up_face[8] = temp[8]
    right_face = rotate_cw(right_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def right_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, front_face, down_face, back_face]:
         print("Error: One or more faces are None in right_ccw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(front_face)
    front_face[2] = up_face[2]
    front_face[5] = up_face[5]
    front_face[8] = up_face[8]
    up_face[2] = back_face[6]
    up_face[5] = back_face[3]
    up_face[8] = back_face[0]
    back_face[0] = down_face[8]
    back_face[3] = down_face[5]
    back_face[6] = down_face[2]
    down_face[2] = temp[2]
    down_face[5] = temp[5]
    down_face[8] = temp[8]
    right_face = rotate_ccw(right_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def left_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, left_face, front_face, down_face, back_face]:
         print("Error: One or more faces are None in left_cw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(front_face)
    front_face[0] = up_face[0]
    front_face[3] = up_face[3]
    front_face[6] = up_face[6]
    up_face[0] = back_face[8]
    up_face[3] = back_face[5]
    up_face[6] = back_face[2]
    back_face[2] = down_face[6]
    back_face[5] = down_face[3]
    back_face[8] = down_face[0]
    down_face[0] = temp[0]
    down_face[3] = temp[3]
    down_face[6] = temp[6]
    left_face = rotate_cw(left_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def left_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, left_face, front_face, down_face, back_face]:
         print("Error: One or more faces are None in left_ccw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(front_face)
    front_face[0] = down_face[0]
    front_face[3] = down_face[3]
    front_face[6] = down_face[6]
    down_face[0] = back_face[8]
    down_face[3] = back_face[5]
    down_face[6] = back_face[2]
    back_face[2] = up_face[6]
    back_face[5] = up_face[3]
    back_face[8] = up_face[0]
    up_face[0] = temp[0]
    up_face[3] = temp[3]
    up_face[6] = temp[6]
    left_face = rotate_ccw(left_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def front_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, front_face, down_face, left_face]:
         print("Error: One or more faces are None in front_cw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(up_face)
    front_face = rotate_cw(front_face)
    up_face[8] = left_face[2]
    up_face[7] = left_face[5]
    up_face[6] = left_face[8]
    left_face[2] = down_face[0]
    left_face[5] = down_face[1]
    left_face[8] = down_face[2]
    down_face[2] = right_face[0]
    down_face[1] = right_face[3]
    down_face[0] = right_face[6]
    right_face[0] = temp[6]
    right_face[3] = temp[7]
    right_face[6] = temp[8]
    return up_face, right_face, front_face, down_face, left_face, back_face

def front_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, front_face, down_face, left_face]:
         print("Error: One or more faces are None in front_ccw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(up_face)
    front_face = rotate_ccw(front_face)
    up_face[6] = right_face[0]
    up_face[7] = right_face[3]
    up_face[8] = right_face[6]
    right_face[0] = down_face[2]
    right_face[3] = down_face[1]
    right_face[6] = down_face[0]
    down_face[0] = left_face[2]
    down_face[1] = left_face[5]
    down_face[2] = left_face[8]
    left_face[8] = temp[6]
    left_face[5] = temp[7]
    left_face[2] = temp[8]
    return up_face, right_face, front_face, down_face, left_face, back_face

# --- Back, Up, Down moves follow the same pattern... ---
# (Implement back_cw, back_ccw, up_cw, up_ccw, down_cw, down_ccw similarly,
# just updating the numpy arrays without the verification loop)

def up_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, front_face, left_face, back_face]:
         print("Error: One or more faces are None in up_cw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(front_face)
    front_face[0] = right_face[0]
    front_face[1] = right_face[1]
    front_face[2] = right_face[2]
    right_face[0] = back_face[0]
    right_face[1] = back_face[1]
    right_face[2] = back_face[2]
    back_face[0] = left_face[0]
    back_face[1] = left_face[1]
    back_face[2] = left_face[2]
    left_face[0] = temp[0]
    left_face[1] = temp[1]
    left_face[2] = temp[2]
    up_face = rotate_cw(up_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def up_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, front_face, left_face, back_face]:
         print("Error: One or more faces are None in up_ccw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(front_face)
    front_face[0] = left_face[0]
    front_face[1] = left_face[1]
    front_face[2] = left_face[2]
    left_face[0] = back_face[0]
    left_face[1] = back_face[1]
    left_face[2] = back_face[2]
    back_face[0] = right_face[0]
    back_face[1] = right_face[1]
    back_face[2] = right_face[2]
    right_face[0] = temp[0]
    right_face[1] = temp[1]
    right_face[2] = temp[2]
    up_face = rotate_ccw(up_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def down_cw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [down_face, right_face, front_face, left_face, back_face]:
         print("Error: One or more faces are None in down_cw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(front_face)
    front_face[6] = left_face[6]
    front_face[7] = left_face[7]
    front_face[8] = left_face[8]
    left_face[6] = back_face[6]
    left_face[7] = back_face[7]
    left_face[8] = back_face[8]
    back_face[6] = right_face[6]
    back_face[7] = right_face[7]
    back_face[8] = right_face[8]
    right_face[6] = temp[6]
    right_face[7] = temp[7]
    right_face[8] = temp[8]
    down_face = rotate_cw(down_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def down_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [down_face, right_face, front_face, left_face, back_face]:
         print("Error: One or more faces are None in down_ccw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(front_face)
    front_face[6] = right_face[6]
    front_face[7] = right_face[7]
    front_face[8] = right_face[8]
    right_face[6] = back_face[6]
    right_face[7] = back_face[7]
    right_face[8] = back_face[8]
    back_face[6] = left_face[6]
    back_face[7] = left_face[7]
    back_face[8] = left_face[8]
    left_face[6] = temp[6]
    left_face[7] = temp[7]
    left_face[8] = temp[8]
    down_face = rotate_ccw(down_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def back_cw(up_face,right_face,front_face,down_face,left_face,back_face):
     if None in [up_face, right_face, back_face, down_face, left_face]:
         print("Error: One or more faces are None in back_cw")
         return up_face, right_face, front_face, down_face, left_face, back_face

     temp = np.copy(up_face)
     up_face[0] = right_face[2]
     up_face[1] = right_face[5]
     up_face[2] = right_face[8]
     right_face[8] = down_face[6]
     right_face[5] = down_face[7]
     right_face[2] = down_face[8]
     down_face[6] = left_face[0]
     down_face[7] = left_face[3]
     down_face[8] = left_face[6]
     left_face[0] = temp[2]
     left_face[3] = temp[1]
     left_face[6] = temp[0]
     back_face = rotate_cw(back_face)
     return up_face, right_face, front_face, down_face, left_face, back_face

def back_ccw(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, back_face, down_face, left_face]:
         print("Error: One or more faces are None in back_ccw")
         return up_face, right_face, front_face, down_face, left_face, back_face

    temp = np.copy(up_face)
    up_face[2] = left_face[0]
    up_face[1] = left_face[3]
    up_face[0] = left_face[6]
    left_face[0] = down_face[6]
    left_face[3] = down_face[7]
    left_face[6] = down_face[8]
    down_face[6] = right_face[8]
    down_face[7] = right_face[5]
    down_face[8] = right_face[2]
    right_face[2] = temp[0]
    right_face[5] = temp[1]
    right_face[8] = temp[2]
    back_face = rotate_ccw(back_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

# --- Whole Cube Turn Simulation (NO webcam) ---
# These functions just update the internal state based on turning the whole cube.

def turn_to_right(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, front_face, down_face, left_face, back_face]: return up_face, right_face, front_face, down_face, left_face, back_face
    temp = np.copy(front_face)
    front_face = np.copy(right_face)
    right_face = np.copy(back_face)
    back_face = np.copy(left_face)
    left_face = np.copy(temp)
    up_face = rotate_cw(up_face)
    down_face = rotate_ccw(down_face)
    return up_face, right_face, front_face, down_face, left_face, back_face

def turn_to_front(up_face,right_face,front_face,down_face,left_face,back_face):
    if None in [up_face, right_face, front_face, down_face, left_face, back_face]: return up_face, right_face, front_face, down_face, left_face, back_face
    temp = np.copy(front_face)
    front_face = np.copy(left_face)
    left_face = np.copy(back_face)
    back_face = np.copy(right_face)
    right_face = np.copy(temp)
    up_face = rotate_ccw(up_face)
    down_face = rotate_cw(down_face)
    return up_face, right_face, front_face, down_face, left_face, back_face