import cv2
import sys
import time
import math
import numpy as np
import random as rng
from scipy import stats
import kociemba
from datetime import datetime
import os

# -----------------------------------------------------------------
# ALL THE FUNCTIONS YOU PROVIDED
# (I have completed the 'down_ccw' function at the end)
# -----------------------------------------------------------------

def rotate_cw(face):
    final = np.copy(face)
    final[0, 0] = face[0, 6]
    final[0, 1] = face[0, 3]
    final[0, 2] = face[0, 0]
    final[0, 3] = face[0, 7]
    final[0, 4] = face[0, 4]
    final[0, 5] = face[0, 1]
    final[0, 6] = face[0, 8]
    final[0, 7] = face[0, 5]
    final[0, 8] = face[0, 2]
    return final

def rotate_ccw(face):
    final = np.copy(face)
    final[0, 8] = face[0, 6]
    final[0, 7] = face[0, 3]
    final[0, 6] = face[0, 0]
    final[0, 5] = face[0, 7]
    final[0, 4] = face[0, 4]
    final[0, 3] = face[0, 1]
    final[0, 2] = face[0, 8]
    final[0, 1] = face[0, 5]
    final[0, 0] = face[0, 2]
    return final

def right_cw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: R Clockwise")
    temp = np.copy(front_face)
    front_face[0, 2] = down_face[0, 2]
    front_face[0, 5] = down_face[0, 5]
    front_face[0, 8] = down_face[0, 8]
    down_face[0, 2] = back_face[0, 6]
    down_face[0, 5] = back_face[0, 3]
    down_face[0, 8] = back_face[0, 0]
    back_face[0, 0] = up_face[0, 8]
    back_face[0, 3] = up_face[0, 5]
    back_face[0, 6] = up_face[0, 2]
    up_face[0, 2] = temp[0, 2]
    up_face[0, 5] = temp[0, 5]
    up_face[0, 8] = temp[0, 8]
    right_face = rotate_cw(right_face)
    
    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp) == True:
                    centroid1 = blob_colors[8]
                    centroid2 = blob_colors[2]
                    point1 = (int(centroid1[5]+(centroid1[7]/2)), int(centroid1[6]+(centroid1[7]/2)))
                    point2 = (int(centroid2[5]+(centroid2[8]/2)), int(centroid2[6]+(centroid2[8]/2)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def right_ccw(video, videoWriter, up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: R CounterClockwise")
    temp = np.copy(front_face)
    front_face[0, 2] = up_face[0, 2]
    front_face[0, 5] = up_face[0, 5]
    front_face[0, 8] = up_face[0, 8]
    up_face[0, 2] = back_face[0, 6]
    up_face[0, 5] = back_face[0, 3]
    up_face[0, 8] = back_face[0, 0]
    back_face[0, 0] = down_face[0, 8]
    back_face[0, 3] = down_face[0, 5]
    back_face[0, 6] = down_face[0, 2]
    down_face[0, 2] = temp[0, 2]
    down_face[0, 5] = temp[0, 5]
    down_face[0, 8] = temp[0, 8]
    right_face = rotate_ccw(right_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours

        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp) == True:
                    centroid1 = blob_colors[2]
                    centroid2 = blob_colors[8]
                    point1 = (int(centroid1[5]+(centroid1[7]/2)), int(centroid1[6]+(centroid1[7]/2)))
                    point2 = (int(centroid2[5]+(centroid2[8]/2)), int(centroid2[6]+(centroid2[8]/2)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def left_cw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: L Clockwise")
    temp = np.copy(front_face)
    front_face[0, 0] = up_face[0, 0]
    front_face[0, 3] = up_face[0, 3]
    front_face[0, 6] = up_face[0, 6]
    up_face[0, 0] = back_face[0, 8]
    up_face[0, 3] = back_face[0, 5]
    up_face[0, 6] = back_face[0, 2]
    back_face[0, 2] = down_face[0, 6]
    back_face[0, 5] = down_face[0, 3]
    back_face[0, 8] = down_face[0, 0]
    down_face[0, 0] = temp[0, 0]
    down_face[0, 3] = temp[0, 3]
    down_face[0, 6] = temp[0, 6]
    left_face = rotate_cw(left_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp) == True:
                    centroid1 = blob_colors[0]
                    centroid2 = blob_colors[6]
                    point1 = (int(centroid1[5]+(centroid1[7]/2)), int(centroid1[6]+(centroid1[7]/2)))
                    point2 = (int(centroid2[5]+(centroid2[8]/2)), int(centroid2[6]+(centroid2[8]/2)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def left_ccw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: L CounterClockwise")
    temp = np.copy(front_face)
    front_face[0, 0] = down_face[0, 0]
    front_face[0, 3] = down_face[0, 3]
    front_face[0, 6] = down_face[0, 6]
    down_face[0, 0] = back_face[0, 8]
    down_face[0, 3] = back_face[0, 5]
    down_face[0, 6] = back_face[0, 2]
    back_face[0, 2] = up_face[0, 6]
    back_face[0, 5] = up_face[0, 3]
    back_face[0, 8] = up_face[0, 0]
    up_face[0, 0] = temp[0, 0]
    up_face[0, 3] = temp[0, 3]
    up_face[0, 6] = temp[0, 6]
    left_face = rotate_ccw(left_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp) == True:
                    centroid1 = blob_colors[6]
                    centroid2 = blob_colors[0]
                    point1 = (int(centroid1[5]+(centroid1[7]/2)), int(centroid1[6]+(centroid1[7]/2)))
                    point2 = (int(centroid2[5]+(centroid2[8]/2)), int(centroid2[6]+(centroid2[8]/2)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def front_cw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: F Clockwise")
    temp1 = np.copy(front_face)
    temp = np.copy(up_face)
    front_face = rotate_cw(front_face)
    temp2 = np.copy(front_face)
    if np.array_equal(temp2, temp1) == True:
        [up_face, right_face, front_face, down_face, left_face, back_face] = turn_to_right(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        [up_face, right_face, front_face, down_face, left_face, back_face] = left_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        [up_face, right_face, front_face, down_face, left_face, back_face] = turn_to_front(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        return up_face, right_face, front_face, down_face, left_face, back_face
    up_face[0, 8] = left_face[0, 2]
    up_face[0, 7] = left_face[0, 5]
    up_face[0, 6] = left_face[0, 8]
    left_face[0, 2] = down_face[0, 0]
    left_face[0, 5] = down_face[0, 1]
    left_face[0, 8] = down_face[0, 2]
    down_face[0, 2] = right_face[0, 0]
    down_face[0, 1] = right_face[0, 3]
    down_face[0, 0] = right_face[0, 6]
    right_face[0, 0] = temp[0, 6]
    right_face[0, 3] = temp[0, 7]
    right_face[0, 6] = temp[0, 8]

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp1) == True:
                    centroid1 = blob_colors[8]
                    centroid2 = blob_colors[6]
                    centroid3 = blob_colors[0]
                    centroid4 = blob_colors[2]
                    point1 = (int(centroid1[5] + (centroid1[7] / 4)), int(centroid1[6] + (centroid1[7] / 2)))
                    point2 = (int(centroid2[5] + (3 * centroid2[8] / 4)), int(centroid2[6] + (centroid2[8] / 2)))
                    point3 = (int(centroid2[5] + (centroid2[7] / 2)), int(centroid2[6] + (centroid2[7] / 4)))
                    point4 = (int(centroid3[5] + (centroid3[8] / 2)), int(centroid3[6] + (3 * centroid3[8] / 4)))
                    point5 = (int(centroid3[5] + (3 * centroid3[8] / 4)), int(centroid3[6] + (centroid3[8] / 2)))
                    point6 = (int(centroid4[5] + (centroid4[8] / 4)), int(centroid4[6] + (centroid4[8] / 2)))
                    point7 = (int(centroid4[5] + (centroid4[8] / 2)), int(centroid4[6] + (3 * centroid4[8] / 4)))
                    point8 = (int(centroid1[5] + (centroid1[8] / 2)), int(centroid1[6] + (centroid1[8] / 4)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point3, point4, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point5, point6, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point7, point8, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
                    cv2.arrowedLine(bgr_image_input, point3, point4, (0, 0, 255), 4, tipLength=0.2)
                    cv2.arrowedLine(bgr_image_input, point5, point6, (0, 0, 255), 4, tipLength=0.2)
                    cv2.arrowedLine(bgr_image_input, point7, point8, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def front_ccw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: F CounterClockwise")
    temp = np.copy(up_face)
    temp1 = np.copy(front_face)
    front_face = rotate_ccw(front_face)
    temp2 = np.copy(front_face)
    if np.array_equal(temp2,temp1) == True:
            [up_face, right_face, front_face, down_face, left_face, back_face] = turn_to_right(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face)
            [up_face, right_face, front_face, down_face, left_face, back_face] = left_ccw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face)
            [up_face, right_face, front_face, down_face, left_face, back_face] = turn_to_front(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face)
            return up_face,right_face,front_face,down_face,left_face,back_face
    up_face[0, 6] = right_face[0, 0]
    up_face[0, 7] = right_face[0, 3]
    up_face[0, 8] = right_face[0, 6]
    right_face[0, 0] = down_face[0, 2]
    right_face[0, 3] = down_face[0, 1]
    right_face[0, 6] = down_face[0, 0]
    down_face[0, 0] = left_face[0, 2]
    down_face[0, 1] = left_face[0, 5]
    down_face[0, 2] = left_face[0, 8]
    left_face[0, 8] = temp[0, 6]
    left_face[0, 5] = temp[0, 7]
    left_face[0, 2] = temp[0, 8]

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp1) == True:
                    centroid1 = blob_colors[2]
                    centroid2 = blob_colors[0]
                    centroid3 = blob_colors[6]
                    centroid4 = blob_colors[8]
                    point1 = (int(centroid1[5] + (centroid1[7] / 4)), int(centroid1[6] + (centroid1[7] / 2)))
                    point2 = (int(centroid2[5] + (3 * centroid2[8]/4)), int(centroid2[6] + (centroid2[8] / 2)))
                    point3 = (int(centroid2[5] + (centroid2[7] / 2)), int(centroid2[6] + (3 * centroid2[7] / 4)))
                    point4 = (int(centroid3[5] + (centroid3[8] / 2)), int(centroid3[6] + (centroid3[8] / 4)))
                    point5 = (int(centroid3[5] + (3 * centroid3[8] / 4)), int(centroid3[6] + (centroid3[8] / 2)))
                    point6 = (int(centroid4[5] + (centroid4[8] / 4)), int(centroid4[6] + (centroid4[8] / 2)))
                    point7 = (int(centroid4[5] + (centroid4[8] / 2)), int(centroid4[6] + (centroid4[8] / 4)))
                    point8 = (int(centroid1[5] + (centroid1[8] / 2)), int(centroid1[6] + (3 * centroid1[8] / 4)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point3, point4, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point5, point6, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point7, point8, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
                    cv2.arrowedLine(bgr_image_input, point3, point4, (0, 0, 255), 4, tipLength=0.2)
                    cv2.arrowedLine(bgr_image_input, point5, point6, (0, 0, 255), 4, tipLength=0.2)
                    cv2.arrowedLine(bgr_image_input, point7, point8, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def back_cw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: B Clockwise")
    temp = np.copy(up_face)
    up_face[0, 0] = right_face[0, 2]
    up_face[0, 1] = right_face[0, 5]
    up_face[0, 2] = right_face[0, 8]
    right_face[0, 8] = down_face[0, 6]
    right_face[0, 5] = down_face[0, 7]
    right_face[0, 2] = down_face[0, 8]
    down_face[0, 6] = left_face[0, 0]
    down_face[0, 7] = left_face[0, 3]
    down_face[0, 8] = left_face[0, 6]
    left_face[0, 0] = temp[0, 2]
    left_face[0, 3] = temp[0, 1]
    left_face[0, 6] = temp[0, 0]
    back_face = rotate_cw(back_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def back_ccw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: B CounterClockwise")
    temp = np.copy(up_face)
    up_face[0, 2] = left_face[0, 0]
    up_face[0, 1] = left_face[0, 3]
    up_face[0, 0] = left_face[0, 6]
    left_face[0, 0] = down_face[0, 6]
    left_face[0, 3] = down_face[0, 7]
    left_face[0, 6] = down_face[0, 8]
    down_face[0, 6] = right_face[0, 8]
    down_face[0, 7] = right_face[0, 5]
    down_face[0, 8] = right_face[0, 2]
    right_face[0, 2] = temp[0, 0]
    right_face[0, 5] = temp[0, 1]
    right_face[0, 8] = temp[0, 2]
    back_face = rotate_ccw(back_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def up_cw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: U Clockwise")
    temp = np.copy(front_face)
    front_face[0, 0] = right_face[0, 0]
    front_face[0, 1] = right_face[0, 1]
    front_face[0, 2] = right_face[0, 2]
    right_face[0, 0] = back_face[0, 0]
    right_face[0, 1] = back_face[0, 1]
    right_face[0, 2] = back_face[0, 2]
    back_face[0, 0] = left_face[0, 0]
    back_face[0, 1] = left_face[0, 1]
    back_face[0, 2] = left_face[0, 2]
    left_face[0, 0] = temp[0, 0]
    left_face[0, 1] = temp[0, 1]
    left_face[0, 2] = temp[0, 2]
    up_face = rotate_cw(up_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp) == True:
                    centroid1 = blob_colors[2]
                    centroid2 = blob_colors[0]
                    point1 = (int(centroid1[5]+(centroid1[7]/2)), int(centroid1[6]+(centroid1[7]/2)))
                    point2 = (int(centroid2[5]+(centroid2[8]/2)), int(centroid2[6]+(centroid2[8]/2)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def up_ccw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: U CounterClockwise")
    temp = np.copy(front_face)
    front_face[0, 0] = left_face[0, 0]
    front_face[0, 1] = left_face[0, 1]
    front_face[0, 2] = left_face[0, 2]
    left_face[0, 0] = back_face[0, 0]
    left_face[0, 1] = back_face[0, 1]
    left_face[0, 2] = back_face[0, 2]
    back_face[0, 0] = right_face[0, 0]
    back_face[0, 1] = right_face[0, 1]
    back_face[0, 2] = right_face[0, 2]
    right_face[0, 0] = temp[0, 0]
    right_face[0, 1] = temp[0, 1]
    right_face[0, 2] = temp[0, 2]
    up_face = rotate_ccw(up_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp) == True:
                    centroid1 = blob_colors[0]
                    centroid2 = blob_colors[2]
                    point1 = (int(centroid1[5]+(centroid1[7]/2)), int(centroid1[6]+(centroid1[7]/2)))
                    point2 = (int(centroid2[5]+(centroid2[8]/2)), int(centroid2[6]+(centroid2[8]/2)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

def down_cw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: D Clockwise")
    temp = np.copy(front_face)
    front_face[0, 6] = left_face[0, 6]
    front_face[0, 7] = left_face[0, 7]
    front_face[0, 8] = left_face[0, 8]
    left_face[0, 6] = back_face[0, 6]
    left_face[0, 7] = back_face[0, 7]
    left_face[0, 8] = back_face[0, 8]
    back_face[0, 6] = right_face[0, 6]
    back_face[0, 7] = right_face[0, 7]
    back_face[0, 8] = right_face[0, 8]
    right_face[0, 6] = temp[0, 6]
    right_face[0, 7] = temp[0, 7]
    right_face[0, 8] = temp[0, 8]
    down_face = rotate_cw(down_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp) == True:
                    centroid1 = blob_colors[6]
                    centroid2 = blob_colors[8]
                    point1 = (int(centroid1[5]+(centroid1[7]/2)), int(centroid1[6]+(centroid1[7]/2)))
                    point2 = (int(centroid2[5]+(centroid2[8]/2)), int(centroid2[6]+(centroid2[8]/2)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

# -----------------------------------------------------------------
#
#  VVV   CODE AFTER THIS IS NEW   VVV
#
# -----------------------------------------------------------------

# (You were missing the end of this function)
def down_ccw(video,videoWriter,up_face,right_face,front_face,down_face,left_face,back_face):
    print("Next Move: D CounterClockwise")
    temp = np.copy(front_face)
    front_face[0, 6] = right_face[0, 6]
    front_face[0, 7] = right_face[0, 7]
    front_face[0, 8] = right_face[0, 8]
    right_face[0, 6] = back_face[0, 6]
    right_face[0, 7] = back_face[0, 7]
    right_face[0, 8] = back_face[0, 8]
    back_face[0, 6] = left_face[0, 6]
    back_face[0, 7] = left_face[0, 7]
    back_face[0, 8] = left_face[0, 8]
    left_face[0, 6] = temp[0, 6]
    left_face[0, 7] = temp[0, 7]
    left_face[0, 8] = temp[0, 8]
    down_face = rotate_ccw(down_face)

    faces = []
    while True:
        is_ok, bgr_image_input = video.read()

        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors) # Draw contours
        
        if len(face) == 9:
            faces.append(face)
            if len(faces) == 10:
                face_array = np.array(faces)
                detected_face = stats.mode(face_array)[0]
                up_face = np.asarray(up_face)
                front_face = np.asarray(front_face)
                detected_face = np.asarray(detected_face)
                faces = []
                if np.array_equal(detected_face, front_face) == True:
                    print("MOVE MADE")
                    return up_face,right_face,front_face,down_face,left_face,back_face
                elif np.array_equal(detected_face,temp) == True:
                    centroid1 = blob_colors[8]
                    centroid2 = blob_colors[6]
                    point1 = (int(centroid1[5]+(centroid1[7]/2)), int(centroid1[6]+(centroid1[7]/2)))
                    point2 = (int(centroid2[5]+(centroid2[8]/2)), int(centroid2[6]+(centroid2[8]/2)))
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 0), 7, tipLength = 0.2)
                    cv2.arrowedLine(bgr_image_input, point1, point2, (0, 0, 255), 4, tipLength=0.2)
        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            break
    return up_face,right_face,front_face,down_face,left_face,back_face # Added return

# (These functions were called in front_cw but not defined)
def turn_to_right(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face):
    """
    Simulates physically turning the cube to the right (Y rotation).
    The Front face becomes the Left face.
    The Right face becomes the Front face.
    """
    print("Please turn the cube to the right")
    temp_front = np.copy(front_face)
    temp_right = np.copy(right_face)
    temp_left = np.copy(left_face)
    temp_back = np.copy(back_face)

    front_face = temp_right
    right_face = temp_back
    back_face = temp_left
    left_face = temp_front

    up_face = rotate_cw(up_face)
    down_face = rotate_ccw(down_face)

    # Wait for user to physically turn the cube
    while True:
        is_ok, bgr_image_input = video.read()
        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors, "Turn cube right ->")

        if len(face) == 9:
            detected_face = np.asarray(stats.mode(np.array([face]))[0])
            if np.array_equal(detected_face, front_face):
                print("Cube turned right")
                return up_face, right_face, front_face, down_face, left_face, back_face

        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            sys.exit()

def turn_to_front(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face):
    """
    Simulates physically turning the cube from Right back to Front (Y' rotation).
    The Front face becomes the Right face.
    The Left face becomes the Front face.
    """
    print("Please turn the cube back to the front (left)")
    temp_front = np.copy(front_face)
    temp_right = np.copy(right_face)
    temp_left = np.copy(left_face)
    temp_back = np.copy(back_face)

    front_face = temp_left
    left_face = temp_back
    back_face = temp_right
    right_face = temp_front

    up_face = rotate_ccw(up_face)
    down_face = rotate_cw(down_face)

    # Wait for user to physically turn the cube
    while True:
        is_ok, bgr_image_input = video.read()
        if not is_ok:
            print("Cannot read video source")
            sys.exit()

        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors, "Turn cube left <-")

        if len(face) == 9:
            detected_face = np.asarray(stats.mode(np.array([face]))[0])
            if np.array_equal(detected_face, front_face):
                print("Cube turned back to front")
                return up_face, right_face, front_face, down_face, left_face, back_face

        videoWriter.write(bgr_image_input)
        cv2.imshow("Output Image", bgr_image_input)
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == 27 or key_pressed == ord('q'):
            sys.exit()


# -----------------------------------------------------------------
# NEW CRITICAL FUNCTIONS FOR COMPUTER VISION
# -----------------------------------------------------------------

def get_color_name(hsv):
    """ Get the name of the color based on HSV value """
    h, s, v = hsv

    # Define HSV color ranges
    # These might need tuning for your camera and lighting
    if (h < 10 or h > 170) and s > 120 and v > 120:
        return 'R' # Red
    elif h in range(11, 30) and s > 120 and v > 120:
        return 'B' # Orange (Kociemba uses B for Back/Orange)
    elif h in range(31, 80) and s > 100 and v > 100:
        return 'U' # Green (Kociemba uses U for Up/Green)
    elif h in range(81, 100) and s > 100 and v > 100:
        return 'F' # Blue (Kociemba uses F for Front/Blue)
    elif h in range(101, 140) and s > 100 and v > 100:
        return 'D' # Yellow (Kociemba uses D for Down/Yellow)
    elif h < 180 and s < 50 and v > 200:
        return 'L' # White (Kociemba uses L for Left/White)
    
    return '' # No color detected

def detect_face(image):
    """
    Detects the 9 stickers on a face of a Rubik's Cube.
    Returns an array of 9 color names and the contour info.
    """
    face = []
    blob_colors = []
    
    # Convert to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Blur the image to reduce noise
    blurred_image = cv2.medianBlur(hsv_image, 5)

    # --- Define HSV ranges for all 6 colors ---
    # These ranges are common, but you may need to adjust them
    color_ranges = {
        'R': [((0, 120, 120), (10, 255, 255)), ((170, 120, 120), (180, 255, 255))], # Red
        'B': [((11, 120, 120), (30, 255, 255))], # Orange (B for Back)
        'U': [((31, 100, 100), (80, 255, 255))], # Green (U for Up)
        'F': [((81, 100, 100), (100, 255, 255))], # Blue (F for Front)
        'D': [((101, 100, 100), (140, 255, 255))], # Yellow (D for Down)
        'L': [((0, 0, 200), (180, 50, 255))] # White (L for Left)
    }

    all_contours = []
    
    for color, hsv_range_list in color_ranges.items():
        for hsv_range in hsv_range_list:
            lower_bound = np.array(hsv_range[0])
            upper_bound = np.array(hsv_range[1])
            
            # Create a mask for the color
            mask = cv2.inRange(blurred_image, lower_bound, upper_bound)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for cnt in contours:
                area = cv2.contourArea(cnt)
                # Filter by area to remove small noise
                if area > 1000: # This threshold might need tuning
                    x, y, w, h = cv2.boundingRect(cnt)
                    # Filter by aspect ratio (stickers are squarish)
                    if 0.8 < (w / h) < 1.2:
                        all_contours.append((x, y, w, h, color))

    # We should have 9 stickers
    if len(all_contours) == 9:
        # Sort contours by position (top-to-bottom, then left-to-right)
        # Sort by y-coordinate first (row)
        all_contours.sort(key=lambda c: c[1])
        
        # Sort each row by x-coordinate (column)
        sorted_contours = []
        for i in range(0, 9, 3):
            row = sorted(all_contours[i:i+3], key=lambda c: c[0])
            sorted_contours.extend(row)
        
        # Now sorted_contours is in order 0, 1, 2, 3, 4, 5, 6, 7, 8
        for i, (x, y, w, h, color) in enumerate(sorted_contours):
            face.append(color)
            # Store info needed for drawing arrows
            # [x, y, w, h, color, center_x, center_y, width, height]
            blob_colors.append([x, y, w, h, color, x, y, w, h]) 
            
    return face, blob_colors

def draw_contours(image, blob_colors, text=""):
    """ Draws the detected sticker contours and text on the image """
    for i, (x, y, w, h, color, _, _, _, _) in enumerate(blob_colors):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f"{i}:{color}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Put instructional text
    if text:
        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
    return image


# -----------------------------------------------------------------
# NEW MAIN() FUNCTION TO RUN THE PROGRAM
# -----------------------------------------------------------------

def main():
    # --- 1. Initialize Camera and Video Writer ---
    video = cv2.VideoCapture(0) # Use 0 for built-in webcam
    if not video.isOpened():
        print("Error: Could not open webcam.")
        sys.exit()

    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    
    # Create a unique video filename
    datestr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_filename = f"cube_solve_{datestr}.mp4"
    
    # Make sure 'output' directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    video_filepath = os.path.join(output_dir, video_filename)
    
    # Use 'mp4v' codec for .mp4 files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    videoWriter = cv2.VideoWriter(video_filepath, fourcc, fps, (width, height))
    print(f"Saving video to: {video_filepath}")

    # --- 2. Initialize Cube State ---
    # We will scan each face
    up_face = []
    right_face = []
    front_face = []
    down_face = []
    left_face = []
    back_face = []
    
    faces_to_scan = {
        'U (Green)': 'up_face',
        'R (Red)': 'right_face',
        'F (Blue)': 'front_face',
        'D (Yellow)': 'down_face',
        'L (White)': 'left_face',
        'B (Orange)': 'back_face'
    }
    
    cube_state_list = []
    scanned_faces = {}

    # --- 3. Scan All 6 Faces ---
    for face_name, var_name in faces_to_scan.items():
        print(f"Scanning {face_name}...")
        while True:
            is_ok, bgr_image_input = video.read()
            if not is_ok:
                print("Cannot read video source")
                break
                
            face, blob_colors = detect_face(bgr_image_input)
            
            # Draw instructions
            text = f"Show {face_name}. Press 'S' to scan."
            bgr_image_input = draw_contours(bgr_image_input, blob_colors, text)

            cv2.imshow("Output Image", bgr_image_input)
            videoWriter.write(bgr_image_input)
            
            key_pressed = cv2.waitKey(1) & 0xFF
            
            if key_pressed == ord('s'):
                if len(face) == 9:
                    print(f"Scanned {face_name}: {face}")
                    scanned_faces[var_name] = np.array([face])
                    cube_state_list.extend(face)
                    break
                else:
                    print(f"Could not detect 9 stickers for {face_name}. Please try again.")
            
            if key_pressed == 27 or key_pressed == ord('q'):
                video.release()
                videoWriter.release()
                cv2.destroyAllWindows()
                sys.exit()

    # Assign scanned faces to the variables
    up_face = scanned_faces['up_face']
    right_face = scanned_faces['right_face']
    front_face = scanned_faces['front_face']
    down_face = scanned_faces['down_face']
    left_face = scanned_faces['left_face']
    back_face = scanned_faces['back_face']

    # --- 4. Get Kociemba Solution ---
    cubestring = "".join(cube_state_list)
    print(f"\nKociemba String (U-R-F-D-L-B): {cubestring}")
    
    try:
        solution_moves = kociemba.solve(cubestring)
        print(f"Solution: {solution_moves}")
    except Exception as e:
        print(f"Error solving cube: {e}")
        print("Please rescan the cube. Make sure colors are correct.")
        video.release()
        videoWriter.release()
        cv2.destroyAllWindows()
        return

    # --- 5. Parse and Execute Solution ---
    moves = solution_moves.split()
    
    for move in moves:
        if move == "R":
            up_face, right_face, front_face, down_face, left_face, back_face = right_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "R'":
            up_face, right_face, front_face, down_face, left_face, back_face = right_ccw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "R2":
            up_face, right_face, front_face, down_face, left_face, back_face = right_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
            up_face, right_face, front_face, down_face, left_face, back_face = right_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        
        elif move == "L":
            up_face, right_face, front_face, down_face, left_face, back_face = left_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "L'":
            up_face, right_face, front_face, down_face, left_face, back_face = left_ccw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "L2":
            up_face, right_face, front_face, down_face, left_face, back_face = left_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
            up_face, right_face, front_face, down_face, left_face, back_face = left_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)

        elif move == "U":
            up_face, right_face, front_face, down_face, left_face, back_face = up_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "U'":
            up_face, right_face, front_face, down_face, left_face, back_face = up_ccw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "U2":
            up_face, right_face, front_face, down_face, left_face, back_face = up_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
            up_face, right_face, front_face, down_face, left_face, back_face = up_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)

        elif move == "D":
            up_face, right_face, front_face, down_face, left_face, back_face = down_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "D'":
            up_face, right_face, front_face, down_face, left_face, back_face = down_ccw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "D2":
            up_face, right_face, front_face, down_face, left_face, back_face = down_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
            up_face, right_face, front_face, down_face, left_face, back_face = down_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)

        elif move == "F":
            up_face, right_face, front_face, down_face, left_face, back_face = front_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "F'":
            up_face, right_face, front_face, down_face, left_face, back_face = front_ccw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "F2":
            up_face, right_face, front_face, down_face, left_face, back_face = front_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
            up_face, right_face, front_face, down_face, left_face, back_face = front_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)

        elif move == "B":
            up_face, right_face, front_face, down_face, left_face, back_face = back_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "B'":
            up_face, right_face, front_face, down_face, left_face, back_face = back_ccw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
        elif move == "B2":
            up_face, right_face, front_face, down_face, left_face, back_face = back_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)
            up_face, right_face, front_face, down_face, left_face, back_face = back_cw(video, videoWriter, up_face, right_face, front_face, down_face, left_face, back_face)

    # --- 6. Clean Up ---
    print("\nCube Solved!")
    
    # Show final "Solved" message on video for 5 seconds
    end_time = time.time() + 5
    while time.time() < end_time:
        is_ok, bgr_image_input = video.read()
        if not is_ok:
            break
        
        face, blob_colors = detect_face(bgr_image_input)
        bgr_image_input = draw_contours(bgr_image_input, blob_colors, "SOLVED!")
        
        cv2.imshow("Output Image", bgr_image_input)
        videoWriter.write(bgr_image_input)
        if cv2.waitKey(1) & 0xFF == 27:
            break
            
    video.release()
    videoWriter.release()
    cv2.destroyAllWindows()

# --- Call the main function to run the program ---
if __name__ == "__main__":
    main()