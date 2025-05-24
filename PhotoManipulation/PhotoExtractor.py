# -*- coding: utf-8 -*-
"""
Interactive Photo Extractor with ROI selection and manual save/rotate.

Allows users to draw a rectangle Region of Interest (ROI) on a scanned image,
rotates the displayed ROI based on a slider, detects potential photos
within that ROI using adjustable parameters (green outline), allows saving
the automatically detected photo using perspective transform, OR allows saving
the drawn and rotated red ROI using perspective transform.
"""

import cv2
import numpy as np
import os
import glob
import math
import re  # Added for parsing filenames
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, UnidentifiedImageError


# --- Helper Functions ---

def rotate_polygon_around_point(polygon_points, pivot_point, angle_degrees):
    """
    Rotates a list of 2D points (polygon) around a given pivot point.

    Args:
        polygon_points (list of tuples): List of (x, y) coordinates for the polygon.
        pivot_point (tuple): (px, py) coordinates of the pivot.
        angle_degrees (float): The angle of rotation in degrees.
                               Positive angle means clockwise rotation.

    Returns:
        list of tuples: List of rotated (x, y) coordinates.
    """
    angle_rad = math.radians(angle_degrees)  # Negative for clockwise with standard math functions
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    rotated_polygon = []
    pivot_x, pivot_y = pivot_point

    for x, y in polygon_points:
        # Translate point relative to pivot
        translated_x = x - pivot_x
        translated_y = y - pivot_y

        # Rotate point
        rotated_x = translated_x * cos_a - translated_y * sin_a
        rotated_y = translated_x * sin_a + translated_y * cos_a

        # Translate point back
        final_x = rotated_x + pivot_x
        final_y = rotated_y + pivot_y
        rotated_polygon.append((final_x, final_y))

    return rotated_polygon


def iou(box1, box2):
    """Calculates the Intersection over Union (IoU) of two axis-aligned bounding boxes."""
    # box1 and box2 are (x, y, w, h)
    x1_tl, y1_tl, w1, h1 = box1
    x1_br, y1_br = x1_tl + w1, y1_tl + h1

    x2_tl, y2_tl, w2, h2 = box2
    x2_br, y2_br = x2_tl + w2, y2_tl + h2

    x_inter_tl = max(x1_tl, x2_tl)
    y_inter_tl = max(y1_tl, y2_tl)
    x_inter_br = min(x1_br, x2_br)
    y_inter_br = min(y1_br, y2_br)

    inter_w = max(0, x_inter_br - x_inter_tl)
    inter_h = max(0, y_inter_br - y_inter_tl)
    inter_area = inter_w * inter_h

    box1_area = w1 * h1
    box2_area = w2 * h2

    union_area = float(box1_area + box2_area - inter_area)
    iou_val = inter_area / union_area if union_area > 0 else 0
    return iou_val


def apply_non_max_suppression(boxes, overlap_threshold):
    """Applies Non-Maximum Suppression (NMS) to a list of axis-aligned bounding boxes (x, y, w, h)."""
    if len(boxes) == 0:
        return []

    boxes_np = np.array(boxes)
    # Convert (x, y, w, h) to (x1, y1, x2, y2)
    boxes_xyxy = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes_np])

    # Sort by the bottom-right y-coordinate of the bounding boxes
    idxs = np.lexsort((boxes_xyxy[:, 2], boxes_xyxy[:, 3]))

    pick = []
    while len(idxs) > 0:
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        xx1 = np.maximum(boxes_xyxy[i, 0], boxes_xyxy[idxs[:last], 0])
        yy1 = np.maximum(boxes_xyxy[i, 1], boxes_xyxy[idxs[:last], 1])
        xx2 = np.minimum(boxes_xyxy[i, 2], boxes_xyxy[idxs[:last], 2])
        yy2 = np.minimum(boxes_xyxy[i, 3], boxes_xyxy[idxs[:last], 3])

        w = np.maximum(0, xx2 - xx1)
        h = np.maximum(0, yy2 - yy1)

        overlap_area = w * h
        box_area_i = (boxes_xyxy[i, 2] - boxes_xyxy[i, 0]) * (boxes_xyxy[i, 3] - boxes_xyxy[i, 1])
        remaining_boxes_area = (boxes_xyxy[idxs[:last], 2] - boxes_xyxy[idxs[:last], 0]) * (
                    boxes_xyxy[idxs[:last], 3] - boxes_xyxy[idxs[:last], 1])
        union_area = box_area_i + remaining_boxes_area - overlap_area

        overlap = np.zeros_like(overlap_area, dtype=float)
        non_zero_union_mask = union_area > 0
        overlap[non_zero_union_mask] = overlap_area[non_zero_union_mask] / union_area[non_zero_union_mask]

        idxs = np.delete(idxs, np.concatenate(([last],
                                               np.where(overlap > overlap_threshold)[0])))

    picked_boxes_wh = [boxes[idx] for idx in pick]
    picked_boxes_wh.sort(key=lambda b: (b[1], b[0]))
    return picked_boxes_wh


def order_points(pts):
    """
    Order the points in top-left, top-right, bottom-right, bottom-left order.
    This is necessary for perspective transform.
    """
    # Ensure pts is a numpy array of shape (4, 2)
    pts = np.array(pts, dtype="float32")
    if pts.shape != (4, 2):
        # Attempt to handle slightly different input formats if possible
        pts = pts.reshape(-1, 2)
        if pts.shape != (4, 2):
            # print(f"Warning: order_points received points with shape {pts.shape}. Expected (4, 2).")
            return None

    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_point_transform(image, pts):
    """
    Applies a four point perspective transform to a region defined by points pts.
    """
    rect = order_points(pts)
    if rect is None:
        return None  # Return None if points ordering failed

    (tl, tr, br, bl) = rect

    # Calculate dimensions based on rectangle points
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    # Add small buffer to dimensions to avoid black lines at edges after warp
    buffer = 1
    maxWidth += 2 * buffer
    maxHeight += 2 * buffer

    if maxWidth < 20 or maxHeight < 20:  # Prevent errors/tiny outputs
        # print("Warning: Calculated very small dimensions for perspective transform.")
        return None

    dst = np.array([
        [buffer, buffer],
        [maxWidth - buffer - 1, buffer],
        [maxWidth - buffer - 1, maxHeight - buffer - 1],
        [buffer, maxHeight - buffer - 1]], dtype="float32")

    rect = rect.astype("float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # Crop the buffer added at the start/end
    warped = warped[buffer:maxHeight - buffer, buffer:maxWidth - buffer]

    return warped


def calculate_rotated_rect_points(x_min, y_min, x_max, y_max, angle_degrees):
    """
    Calculates the 4 corner points of an axis-aligned rectangle defined by
    (x_min, y_min) and (x_max, y_max), rotated by angle_degrees around its center.
    The input and output points are in the same coordinate system.
    Returns points as a NumPy array of shape (4, 2).
    """
    # Get original corners (top-left, top-right, bottom-right, bottom-left)
    corners = np.array([
        [x_min, y_min],
        [x_max, y_min],
        [x_max, y_max],
        [x_min, y_max]
    ], dtype=np.float32)

    # Calculate center of the rectangle
    center_x = (x_min + x_max) / 2.0
    center_y = (y_min + y_max) / 2.0

    # Create rotation matrix
    # OpenCV getRotationMatrix2D expects angle in degrees, positive is counter-clockwise
    # We want positive angle on slider to mean clockwise rotation on screen, so use -angle_degrees
    M = cv2.getRotationMatrix2D((center_x, center_y), -angle_degrees, 1.0)

    # Apply the rotation matrix to the corners
    # Need to add a column of ones to the corners for matrix multiplication
    corners_homogeneous = np.c_[corners, np.ones(4)]  # Add a column of 1s
    rotated_corners = np.dot(M, corners_homogeneous.T).T  # Apply matrix, then transpose back

    return rotated_corners.astype(np.float32)


# --- Core Detection Logic (modified for ROI) ---
def find_photo_rect_in_roi(image_crop, roi_offset_orig, params):
    """
    Finds the best potential rotated photo rectangle within the cropped ROI.

    Args:
        image_crop (np.ndarray): The cropped image (ROI).
        roi_offset_orig (tuple): (x, y) offset of the crop's top-left corner
                                 in the original image coordinates.
        params (dict): Dictionary of parameters.

    Returns:
        tuple: A single best rotated rectangle tuple (center, size, angle)
               in original image coordinates, or None if none found.
    """
    if image_crop is None or image_crop.shape[0] < 10 or image_crop.shape[1] < 10:  # Minimum size for crop
        # print("find_photo_rect_in_roi: Image crop too small or None.")
        return None

    crop_height, crop_width = image_crop.shape[:2]
    crop_area = crop_height * crop_width
    crop_diagonal = math.sqrt(crop_width ** 2 + crop_height ** 2)

    if crop_area == 0:
        # print("find_photo_rect_in_roi: Crop area is zero.")
        return None

    # Convert parameters from scaled slider values (integers) to floats if necessary
    # Ensure keys exist and values are numbers
    canny_low = params.get('canny_low', 50)
    canny_high = params.get('canny_high', 150)
    min_area_ratio = params.get('min_area_ratio_scaled', 5) / 1000.0  # Scale back, default 0.005
    max_area_ratio = params.get('max_area_ratio_scaled', 950) / 1000.0  # Scale back, default 0.95
    min_aspect_ratio_val = params.get('min_aspect_ratio_scaled', 30) / 100.0  # Scale back, default 0.3
    max_aspect_ratio_val = params.get('max_aspect_ratio_scaled', 300) / 100.0  # Scale back, default 3.0
    min_perimeter_ratio = params.get('min_perimeter_ratio_scaled', 20) / 1000.0  # Scale back, default 0.02
    nms_iou_threshold = params.get('nms_iou_threshold_scaled', 30) / 100.0  # Scale back, default 0.3
    min_contour_area_px = params.get('min_contour_area_px', 100)

    gray = cv2.cvtColor(image_crop, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, canny_low, canny_high)

    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    potential_rotated_rects_crop = []
    potential_axis_aligned_boxes_crop_for_nms = []

    for contour in contours:
        # Filter small contours early
        if cv2.contourArea(contour) < min_contour_area_px:
            continue

        # minAreaRect needs at least 5 points (or sometimes 6?) - let's check contour length
        if len(contour) < 5:
            continue

        try:
            rect = cv2.minAreaRect(contour)
        except cv2.error as e:
            # print(f"Warning: minAreaRect failed for a contour: {e}")
            continue  # Skip this contour if minAreaRect fails

        (center_crop, (width, height), angle) = rect

        if width < 5 or height < 5:  # Minimum dimension in pixels for a potential photo
            continue

        rotated_rect_area = width * height

        # Filter based on parameters relative to crop size/area
        if rotated_rect_area < crop_area * min_area_ratio or \
                rotated_rect_area > crop_area * max_area_ratio:
            continue

        rotated_rect_perimeter = 2 * (width + height)
        if crop_diagonal > 0 and rotated_rect_perimeter / crop_diagonal < min_perimeter_ratio:
            continue

        # Ensure width and height are positive before calculating aspect ratio
        if min(width, height) <= 0:
            # print("Warning: Detected rectangle with non-positive dimension.")
            continue
        aspect_ratio = max(width, height) / min(width, height)
        if aspect_ratio < min_aspect_ratio_val or aspect_ratio > max_aspect_ratio_val:
            continue

        potential_rotated_rects_crop.append(rect)

        # Get axis-aligned box in crop coordinates for NMS
        # Ensure boxPoints returns a valid shape before converting to int
        box_points = cv2.boxPoints(rect)
        if box_points.shape != (4, 2):
            # print(f"Warning: cv2.boxPoints did not return 4 points ({box_points.shape}) for rect {rect}")
            continue  # Skip this rect

        box_points_int = np.intp(box_points)  # Convert to integer points for boundingRect
        x, y, w, h = cv2.boundingRect(box_points_int)
        potential_axis_aligned_boxes_crop_for_nms.append((x, y, w, h))

    # Apply NMS in crop coordinates
    picked_axis_aligned_boxes_crop = apply_non_max_suppression(
        potential_axis_aligned_boxes_crop_for_nms, nms_iou_threshold
    )

    # Find the best rectangle among the NMS results.
    # A simple approach is to take the one with the largest area within the ROI.
    best_rect_crop = None
    max_area = 0

    original_pairs_crop = list(zip(potential_axis_aligned_boxes_crop_for_nms, potential_rotated_rects_crop))

    for picked_box_crop in picked_axis_aligned_boxes_crop:
        # Find the corresponding original rotated rect
        # Need to match based on (x,y,w,h) tuple equality
        for original_bbox_crop, original_rotated_rect_crop in original_pairs_crop:
            if original_bbox_crop == picked_box_crop:
                area = original_rotated_rect_crop[1][0] * original_rotated_rect_crop[1][1]
                if area > max_area:
                    max_area = area
                    best_rect_crop = original_rotated_rect_crop
                break  # Found match, move to next picked box

    if best_rect_crop is None:
        # print("No best rectangle found after filtering and NMS")
        return None  # No suitable rectangle found

    # Convert the best rectangle's coordinates from crop coordinates to original image coordinates
    (center_crop, size, angle) = best_rect_crop
    center_orig_x = center_crop[0] + roi_offset_orig[0]
    center_orig_y = center_crop[1] + roi_offset_orig[1]

    # Return the rectangle definition in original image coordinates
    # Note: minAreaRect angle is in [-90, 0) or [-90, 90) depending on orientation.
    # The perspective transform handles this angle correctly.
    return ((center_orig_x, center_orig_y), size, angle)


# --- GUI Application Class ---
class PhotoExtractorGUI:
    def __init__(self, root, input_dir=".", output_dir="./Extracted"):
        self.root = root
        root.title("Interactive Photo Extractor")

        self.input_dir = input_dir
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)  # Ensure output dir exists

        self.image_files = []
        self.current_image_index = 0
        self.original_image = None
        self.tk_image = None  # Stores the ImageTk.PhotoImage for the canvas
        self.display_scale = 1.0  # Scale factor for displaying image on canvas
        self.display_offset_x = 0
        self.display_offset_y = 0

        # Drawing state (Red ROI)
        self.drawing = False
        self.roi_start_canvas = None  # (x, y) on canvas where mouse button was pressed
        self.roi_end_canvas = None  # (x, y) on canvas current mouse position during drag / on release
        self.roi_start_orig = None  # (x, y) in original image coords, corresponding to roi_start_canvas
        # axis-aligned bounds of the *unrotated* ROI in original image coords
        self.roi_axis_aligned_bounds_orig = None  # (x_min, y_min, x_max, y_max)
        self.roi_rectangle_id = None  # Canvas item ID for the drawn ROI (now a polygon)

        # Detected rectangle state (Green)
        self.detected_rect_orig = None  # The single best rotated rect in original image coords
        self.detected_rectangle_id = None  # Canvas item ID for the detected outline

        # MODIFICATION: Store determined output file extension for the current image
        self.output_file_extension_for_current_image = ".jpg"  # Default, updated in load_current_image

        # --- Parameters with Default Values ---
        self.params = {
            'canny_low': tk.IntVar(value=50),
            'canny_high': tk.IntVar(value=150),
            'min_area_ratio_scaled': tk.IntVar(value=int(0.005 * 1000)),  # 0.005
            'max_area_ratio_scaled': tk.IntVar(value=int(0.95 * 1000)),  # 0.95
            'min_aspect_ratio_scaled': tk.IntVar(value=int(0.3 * 100)),  # 0.3
            'max_aspect_ratio_scaled': tk.IntVar(value=int(3.0 * 100)),  # 3.0
            'min_perimeter_ratio_scaled': tk.IntVar(value=int(0.02 * 1000)),  # 0.02
            'nms_iou_threshold_scaled': tk.IntVar(value=int(0.3 * 100)),  # 0.3
            'min_contour_area_px': tk.IntVar(value=100),  # Minimum contour area in pixels (applied before minAreaRect)
            'roi_buffer_px': tk.IntVar(value=10)  # Buffer added to ROI crop
        }
        # Ranges for scaled parameters (min, max)
        self.param_ranges = {
            'canny_low': (0, 255),
            'canny_high': (0, 255),
            'min_area_ratio_scaled': (0, 500),  # 0 to 0.5 (scaled to 1000)
            'max_area_ratio_scaled': (500, 1000),  # 0.5 to 1.0 (scaled to 1000)
            'min_aspect_ratio_scaled': (10, 100),  # 0.1 to 1.0 (scaled to 100)
            'max_aspect_ratio_scaled': (100, 500),  # 1.0 to 5.0 (scaled to 100)
            'min_perimeter_ratio_scaled': (0, 200),  # 0 to 0.2 (scaled to 1000)
            'nms_iou_threshold_scaled': (0, 100),  # 0.0 to 1.0 (scaled to 100)
            'min_contour_area_px': (0, 5000),  # 0 to 5000 pixels
            'roi_buffer_px': (0, 50)  # 0 to 50 pixels buffer
        }

        # --- Manual Save Options ---
        self.rotation_angle_var = tk.DoubleVar(value=0.0)

        # --- GUI Layout ---
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Image display area (Canvas)
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        self.main_frame.columnconfigure(0, weight=3)
        self.main_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.canvas_frame, bg="gray", bd=0, highlightthickness=0)
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Controls area
        self.controls_frame = ttk.Frame(self.main_frame, padding="10")
        self.controls_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=5)
        self.main_frame.columnconfigure(1, weight=1)
        self.controls_frame.columnconfigure(1, weight=1)
        self.controls_frame.columnconfigure(2, weight=0)

        self.file_label = ttk.Label(self.controls_frame, text="File: N/A")
        self.file_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)

        param_grid_row_start = 1
        self._create_parameter_controls(self.controls_frame, starting_row=param_grid_row_start)
        last_param_row = param_grid_row_start + len(self.params) - 1

        manual_save_frame = ttk.LabelFrame(self.controls_frame, text="Manual Save Options", padding="10")
        manual_save_frame.grid(row=last_param_row + 1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        manual_save_frame.columnconfigure(1, weight=1)

        ttk.Label(manual_save_frame, text="Rotation (°):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.rotation_scale = ttk.Scale(
            manual_save_frame, from_=-10.0, to_=10.0, variable=self.rotation_angle_var,
            orient=tk.HORIZONTAL, command=self.on_rotation_change, length=150
        )
        self.rotation_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.rotation_scale.config(state=tk.DISABLED)

        self.rotation_value_var = tk.StringVar()
        self.rotation_value_var.set(f"{self.rotation_angle_var.get():.2f}")
        ttk.Label(manual_save_frame, textvariable=self.rotation_value_var).grid(row=0, column=2, sticky=tk.W, padx=5,
                                                                                pady=2)
        self.rotation_angle_var.trace_add("write", lambda v, i, m: self.rotation_value_var.set(
            f"{self.rotation_angle_var.get():.2f}"))

        self.save_red_button = ttk.Button(manual_save_frame, text="Save Red Selection", command=self.save_red_selection,
                                          state=tk.DISABLED)
        self.save_red_button.grid(row=1, column=0, pady=5, padx=(0, 2), sticky=tk.EW)

        self.reset_rotation_button = ttk.Button(manual_save_frame, text="Reset Rotation", command=self.reset_rotation,
                                                state=tk.DISABLED)
        self.reset_rotation_button.grid(row=1, column=1, pady=5, padx=(2, 0), sticky=tk.EW)

        manual_save_frame.columnconfigure(0, weight=1)
        manual_save_frame.columnconfigure(1, weight=1)

        self.button_frame = ttk.Frame(self.controls_frame)
        self.button_frame.grid(row=last_param_row + 2, column=0, columnspan=3, pady=10)

        self.save_green_button = ttk.Button(self.button_frame, text="Save Auto-Detected Photo",
                                            command=self.save_detected_photo, state=tk.DISABLED)
        self.save_green_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear Selection", command=self.clear_selection,
                                       state=tk.DISABLED)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.button_frame, text="Next Image (Discard)", command=self.load_next_image)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.load_image_files()
        if self.image_files:
            self.root.update_idletasks()
            self.load_current_image()
        else:
            if not self.image_files:
                if self.root.winfo_exists():
                    messagebox.showerror("No Images", "No images found to load.")
                    self.root.destroy()

    def _get_next_save_number(self):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            return 1
        max_num = 0
        numeric_file_pattern = re.compile(r"^(\d+)\.(jpg|jpeg|png|tiff|bmp)$", re.IGNORECASE)
        try:
            for f in os.listdir(self.output_dir):
                match = numeric_file_pattern.match(f)
                if match:
                    num = int(match.group(1))
                    if num > max_num: max_num = num
        except Exception as e:
            print(f"Error scanning output directory for next save number: {e}")
        return max_num + 1

    def _create_parameter_controls(self, parent_frame, starting_row):
        row = starting_row
        param_info = [
            ('canny_low', 'Canny Low', 1, "int"), ('canny_high', 'Canny High', 1, "int"),
            ('min_area_ratio_scaled', 'Min Area Ratio (*1000)', 1000, "float"),
            ('max_area_ratio_scaled', 'Max Area Ratio (*1000)', 1000, "float"),
            ('min_aspect_ratio_scaled', 'Min Aspect Ratio (*100)', 100, "float"),
            ('max_aspect_ratio_scaled', 'Max Aspect Ratio (*100)', 100, "float"),
            ('min_perimeter_ratio_scaled', 'Min Perimeter Ratio (*1000)', 1000, "float"),
            ('nms_iou_threshold_scaled', 'NMS IoU Threshold (*100)', 100, "float"),
            ('min_contour_area_px', 'Min Contour Area (px)', 1, "int"),
            ('roi_buffer_px', 'ROI Buffer (px)', 1, "int"),
        ]
        for key, display_name, scale_factor, param_type in param_info:
            ttk.Label(parent_frame, text=display_name).grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
            min_val, max_val = self.param_ranges[key]
            ttk.Scale(parent_frame, from_=min_val, to=max_val, variable=self.params[key],
                      orient=tk.HORIZONTAL, command=self.on_parameter_change, length=150
                      ).grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)
            display_value_var = tk.StringVar()

            def update_display_value(var_name, index, mode, param_key=key, factor=scale_factor,
                                     display_var=display_value_var, p_type=param_type):
                try:
                    val = self.params[param_key].get()
                    if p_type == "float":
                        display_var.set(f"{val / factor:.2f}")
                    else:
                        display_var.set(f"{val:.2f}")
                except Exception:
                    display_var.set("Err")

            self.params[key].trace_add("write", update_display_value)
            update_display_value(None, None, None)
            ttk.Label(parent_frame, textvariable=display_value_var).grid(row=row, column=2, sticky=tk.W, pady=2, padx=5)
            row += 1

    def load_image_files(self):
        image_patterns = ["*.png", "*.jpg", "*.jpeg", "*.tiff", "*.bmp"]
        self.image_files = []
        for pattern in image_patterns:
            self.image_files.extend(glob.glob(os.path.join(self.input_dir, pattern)))
        self.image_files.sort()
        if not self.image_files:
            if self.root.winfo_exists():
                messagebox.showerror("No Images Found", f"No image files found in {self.input_dir}")
                self.root.destroy()
            return

    def load_current_image(self):
        if not self.image_files or self.current_image_index >= len(self.image_files):
            if self.root.winfo_exists():
                messagebox.showinfo("Finished", "All images processed!")
                self.root.destroy()
            return
        image_path = self.image_files[self.current_image_index]
        self.file_label.config(
            text=f"File: {os.path.basename(image_path)} ({self.current_image_index + 1}/{len(self.image_files)})")
        _, input_ext = os.path.splitext(image_path)
        if input_ext.lower() == ".png":
            self.output_file_extension_for_current_image = ".png"
        else:
            self.output_file_extension_for_current_image = ".jpg"
        try:
            pil_img = Image.open(image_path)
            if pil_img.mode != 'RGB': pil_img = pil_img.convert('RGB')
            self.original_image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except (FileNotFoundError, UnidentifiedImageError, Exception) as e:
            if self.root.winfo_exists():
                messagebox.showwarning("Error Loading Image", f"Could not read image {image_path}: {e}. Skipping.")
            self.current_image_index += 1
            if self.current_image_index < len(self.image_files):
                self.load_current_image()
            elif self.root.winfo_exists():
                messagebox.showinfo("Finished", "No more images could be loaded.")
                self.root.destroy()
            return
        self.clear_selection()
        if self.canvas.winfo_width() > 1 and self.canvas.winfo_height() > 1:
            self.display_image_on_canvas()

    def on_canvas_configure(self, event):
        if self.original_image is not None:
            self.display_image_on_canvas()
            if self.roi_axis_aligned_bounds_orig is not None:
                # When resizing, if an ROI exists, redraw it.
                # Default to center pivot for consistency if slider was used.
                # Or, could try to remember last pivot mode, but this is simpler.
                self.draw_roi_on_canvas(is_dragging=False, use_center_pivot_for_finalized_roi=True)
                if self.detected_rect_orig is not None:
                    self.draw_detected_rect_on_canvas()

    def display_image_on_canvas(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1 or canvas_height <= 1 or self.original_image is None: return
        original_height, original_width = self.original_image.shape[:2]
        scale_w = canvas_width / original_width
        scale_h = canvas_height / original_height
        self.display_scale = min(scale_w, scale_h)
        if self.display_scale <= 0: self.display_scale = 1.0
        display_width = int(original_width * self.display_scale)
        display_height = int(original_height * self.display_scale)
        self.display_offset_x = (canvas_width - display_width) // 2
        self.display_offset_y = (canvas_height - display_height) // 2
        resized_img_cv2 = cv2.resize(self.original_image, (display_width, display_height), interpolation=cv2.INTER_AREA)
        resized_img_cv2_rgb = cv2.cvtColor(resized_img_cv2, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(resized_img_cv2_rgb)
        self.tk_image = ImageTk.PhotoImage(pil_image)
        self.canvas.delete("all")
        self.roi_rectangle_id = None
        self.detected_rectangle_id = None
        self.canvas.create_image(self.display_offset_x, self.display_offset_y, anchor=tk.NW, image=self.tk_image)

    def canvas_to_original(self, x_canvas, y_canvas):
        if self.display_scale == 0 or self.original_image is None: return None, None
        x_relative = x_canvas - self.display_offset_x
        y_relative = y_canvas - self.display_offset_y
        x_orig = int(x_relative / self.display_scale)
        y_orig = int(y_relative / self.display_scale)
        h, w = self.original_image.shape[:2]
        x_orig = max(0, min(x_orig, w - 1))
        y_orig = max(0, min(y_orig, h - 1))
        return x_orig, y_orig

    def original_to_canvas(self, x_orig, y_orig):
        if self.original_image is None: return None, None
        x_canvas = int(x_orig * self.display_scale + self.display_offset_x)
        y_canvas = int(y_orig * self.display_scale + self.display_offset_y)
        return x_canvas, y_canvas

    def on_button_press(self, event):
        if self.original_image is None: return
        canvas_x, canvas_y = event.x, event.y
        img_disp_w = int(self.original_image.shape[1] * self.display_scale)
        img_disp_h = int(self.original_image.shape[0] * self.display_scale)
        if not (self.display_offset_x <= canvas_x <= self.display_offset_x + img_disp_w and
                self.display_offset_y <= canvas_y <= self.display_offset_y + img_disp_h):
            return
        self.clear_selection()
        self.drawing = True
        self.roi_start_canvas = (event.x, event.y)
        self.roi_start_orig = self.canvas_to_original(event.x, event.y)  # Store original start point
        self.roi_end_canvas = (event.x, event.y)

    def on_mouse_drag(self, event):
        if not self.drawing or self.original_image is None: return
        self.roi_end_canvas = (event.x, event.y)
        self.draw_roi_on_canvas(is_dragging=True)  # Default for use_center_pivot_for_finalized_roi is False

    def on_button_release(self, event):
        if not self.drawing or self.original_image is None: return
        self.drawing = False

        if self.roi_start_orig is None:
            self.clear_selection()
            return

        start_orig_x, start_orig_y = self.roi_start_orig
        # Use self.roi_end_canvas as it's the most up-to-date end point from the drag
        end_orig_x, end_orig_y = self.canvas_to_original(*self.roi_end_canvas)

        if end_orig_x is None:
            self.clear_selection()
            return

        x_min_orig = min(start_orig_x, end_orig_x)
        y_min_orig = min(start_orig_y, end_orig_y)
        x_max_orig = max(start_orig_x, end_orig_x)
        y_max_orig = max(start_orig_y, end_orig_y)

        self.roi_axis_aligned_bounds_orig = (x_min_orig, y_min_orig, x_max_orig, y_max_orig)

        min_roi_size = 20
        if x_max_orig - x_min_orig < min_roi_size or y_max_orig - y_min_orig < min_roi_size:
            self.clear_selection()
            return

        self.rotation_scale.config(state=tk.NORMAL)
        # Initial draw after release should pivot around the start point
        self.draw_roi_on_canvas(is_dragging=False, use_center_pivot_for_finalized_roi=False)
        self.save_red_button.config(state=tk.NORMAL)
        self.reset_rotation_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)
        self.run_detection_in_roi()

    def draw_roi_on_canvas(self, is_dragging=False, use_center_pivot_for_finalized_roi=False):
        if self.original_image is None: return

        self.canvas.delete("roi_rect")
        self.roi_rectangle_id = None
        rotation_angle = self.rotation_angle_var.get()
        flat_canvas_points = []

        if is_dragging:
            if self.roi_start_canvas is None or self.roi_end_canvas is None: return

            start_x_c, start_y_c = self.roi_start_canvas
            end_x_c, end_y_c = self.roi_end_canvas
            unrotated_corners_canvas = [
                (start_x_c, start_y_c), (end_x_c, start_y_c),
                (end_x_c, end_y_c), (start_x_c, end_y_c)
            ]
            pivot_point_canvas = self.roi_start_canvas
            rotated_canvas_points_list = rotate_polygon_around_point(
                unrotated_corners_canvas, pivot_point_canvas, rotation_angle
            )
            flat_canvas_points = [coord for point in rotated_canvas_points_list for coord in point]
        else:  # Finalized ROI (not dragging)
            if self.roi_axis_aligned_bounds_orig is None: return

            x_min_orig, y_min_orig, x_max_orig, y_max_orig = self.roi_axis_aligned_bounds_orig
            rotated_orig_points_list = []

            if use_center_pivot_for_finalized_roi:
                # Rotate around the center of the unrotated original bounds
                rotated_orig_points_np = calculate_rotated_rect_points(
                    x_min_orig, y_min_orig, x_max_orig, y_max_orig, rotation_angle
                )
                rotated_orig_points_list = [tuple(p) for p in rotated_orig_points_np]
            else:
                # Rotate around self.roi_start_orig (initial click point in original coords)
                if self.roi_start_orig is None: return
                unrotated_corners_orig = [
                    (x_min_orig, y_min_orig), (x_max_orig, y_min_orig),
                    (x_max_orig, y_max_orig), (x_min_orig, y_max_orig)
                ]
                pivot_point_orig = self.roi_start_orig
                rotated_orig_points_list = rotate_polygon_around_point(
                    unrotated_corners_orig, pivot_point_orig, rotation_angle
                )

            canvas_points_for_display = []
            for point_orig in rotated_orig_points_list:
                x_c, y_c = self.original_to_canvas(point_orig[0], point_orig[1])
                if x_c is None or y_c is None: return
                canvas_points_for_display.append((x_c, y_c))
            flat_canvas_points = [coord for point in canvas_points_for_display for coord in point]

        if flat_canvas_points:
            self.roi_rectangle_id = self.canvas.create_polygon(
                flat_canvas_points, outline='red', fill='', width=2, tags="roi_rect"
            )
            self.canvas.tag_raise("roi_rect")
            if self.detected_rectangle_id:
                self.canvas.tag_lower("detected_rect", "roi_rect")

    def draw_detected_rect_on_canvas(self):
        self.canvas.delete("detected_rect")
        self.detected_rectangle_id = None
        if self.detected_rect_orig is None or self.original_image is None:
            self.save_green_button.config(state=tk.DISABLED)
            return
        box_points_orig = cv2.boxPoints(self.detected_rect_orig)
        box_points_orig = np.intp(box_points_orig)
        canvas_points = []
        for point_orig in box_points_orig:
            x_c, y_c = self.original_to_canvas(point_orig[0], point_orig[1])
            if x_c is None or y_c is None: return
            canvas_points.append((x_c, y_c))
        flat_canvas_points = [coord for point in canvas_points for coord in point]
        self.detected_rectangle_id = self.canvas.create_polygon(
            flat_canvas_points, outline='lime green', fill='', width=2, tags="detected_rect"
        )
        self.canvas.tag_raise("detected_rect")
        if self.roi_rectangle_id: self.canvas.tag_lower("detected_rect", "roi_rect")
        self.save_green_button.config(state=tk.NORMAL)

    def run_detection_in_roi(self):
        if self.original_image is None or self.roi_axis_aligned_bounds_orig is None:
            self.detected_rect_orig = None
            self.draw_detected_rect_on_canvas()
            return
        x_min_orig, y_min_orig, x_max_orig, y_max_orig = self.roi_axis_aligned_bounds_orig
        buffer = self.params['roi_buffer_px'].get()
        h_orig, w_orig = self.original_image.shape[:2]
        crop_x_min = max(0, x_min_orig - buffer)
        crop_y_min = max(0, y_min_orig - buffer)
        crop_x_max = min(w_orig, x_max_orig + buffer)
        crop_y_max = min(h_orig, y_max_orig + buffer)
        min_crop_dim = 20
        if crop_x_max - crop_x_min < min_crop_dim or crop_y_max - crop_y_min < min_crop_dim:
            self.detected_rect_orig = None
        else:
            image_crop = self.original_image[crop_y_min:crop_y_max, crop_x_min:crop_x_max].copy()
            current_params = {key: var.get() for key, var in self.params.items()}
            self.detected_rect_orig = find_photo_rect_in_roi(
                image_crop, (crop_x_min, crop_y_min), current_params
            )
        self.draw_detected_rect_on_canvas()

    def on_parameter_change(self, *args):
        if self.roi_axis_aligned_bounds_orig is not None:
            self.run_detection_in_roi()

    def on_rotation_change(self, *args):
        if self.roi_axis_aligned_bounds_orig is not None:
            # When slider changes an existing ROI, rotate around its center
            self.draw_roi_on_canvas(is_dragging=False, use_center_pivot_for_finalized_roi=True)

    def reset_rotation(self):
        self.rotation_angle_var.set(0.0)
        if self.roi_axis_aligned_bounds_orig is not None:
            # When resetting rotation of an existing ROI, rotate around its center
            self.draw_roi_on_canvas(is_dragging=False, use_center_pivot_for_finalized_roi=True)

    def save_detected_photo(self):
        if self.original_image is None or self.detected_rect_orig is None:
            messagebox.showinfo("Nothing to Save", "No auto-detected photo found to save.")
            return
        os.makedirs(self.output_dir, exist_ok=True)
        try:
            box_points_orig = cv2.boxPoints(self.detected_rect_orig)
            box_points_orig = np.float32(box_points_orig)
            cropped_image = four_point_transform(self.original_image, box_points_orig)
            if cropped_image is not None and cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
                save_number = self._get_next_save_number()
                output_filename = f"{save_number}{self.output_file_extension_for_current_image}"
                output_path = os.path.join(self.output_dir, output_filename)
                cv2.imwrite(output_path, cropped_image)
                print(
                    f"Saved auto-detected photo {save_number} from {os.path.basename(self.image_files[self.current_image_index])} as {output_filename}")
            else:
                messagebox.showwarning("Save Warning", "Could not crop auto-detected area (too small/invalid).")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving auto-detected photo: {e}")

    def save_red_selection(self):
        if self.original_image is None or self.roi_axis_aligned_bounds_orig is None:
            messagebox.showinfo("Nothing to Save", "No red selection found to save.")
            return
        os.makedirs(self.output_dir, exist_ok=True)
        try:
            rotation_angle = self.rotation_angle_var.get()
            x_min_orig, y_min_orig, x_max_orig, y_max_orig = self.roi_axis_aligned_bounds_orig

            rotated_roi_points_for_save = calculate_rotated_rect_points(
                x_min_orig, y_min_orig, x_max_orig, y_max_orig, rotation_angle
            )
            cropped_image = four_point_transform(self.original_image, rotated_roi_points_for_save)

            if cropped_image is not None and cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
                save_number = self._get_next_save_number()
                output_filename = f"{save_number}{self.output_file_extension_for_current_image}"
                output_path = os.path.join(self.output_dir, output_filename)
                cv2.imwrite(output_path, cropped_image)
                print(
                    f"Saved red selection photo {save_number} from {os.path.basename(self.image_files[self.current_image_index])} as {output_filename}")
            else:
                messagebox.showwarning("Save Warning",
                                       "Could not crop red selection (too small/invalid transformed area).")
        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving red selection: {e}")

    def clear_selection(self):
        self.drawing = False
        self.roi_start_canvas = None
        self.roi_end_canvas = None
        self.roi_start_orig = None
        self.roi_axis_aligned_bounds_orig = None
        self.detected_rect_orig = None

        self.rotation_scale.config(state=tk.DISABLED)
        self.canvas.delete("roi_rect")
        self.canvas.delete("detected_rect")
        self.roi_rectangle_id = None
        self.detected_rectangle_id = None
        self.save_green_button.config(state=tk.DISABLED)
        self.save_red_button.config(state=tk.DISABLED)
        self.reset_rotation_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)

    def load_next_image(self):
        self.current_image_index += 1
        self.load_current_image()

    def run(self):
        self.root.mainloop()


# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    input_directory = "./OriginalDescriptions"
    output_directory = "./Extracted"
    needs_input_prompt = True
    if os.path.exists(input_directory):
        image_files_check = []
        for pattern in ["*.png", "*.jpg", "*.jpeg", "*.tiff", "*.bmp"]:
            image_files_check.extend(glob.glob(os.path.join(input_directory, pattern)))
        if image_files_check: needs_input_prompt = False

    if needs_input_prompt:
        root.withdraw()
        selected_input_dir = filedialog.askdirectory(
            title="Select Input Directory Containing Scans",
            initialdir=input_directory if os.path.exists(input_directory) else "."
        )
        if not selected_input_dir:
            print("No input directory selected. Exiting.")
            input_directory = None
        else:
            input_directory = selected_input_dir
        root.deiconify()

    if input_directory is None:
        if root.winfo_exists(): root.destroy()
        exit()

    root.withdraw()
    if not os.path.exists(output_directory):
        create_output = messagebox.askyesno(
            "Output Directory",
            f"Output directory '{os.path.abspath(output_directory)}' does not exist. Create it?",
            default="yes"
        )
        if create_output:
            try:
                os.makedirs(output_directory, exist_ok=True)
            except OSError as e:
                messagebox.showerror("Directory Creation Error", f"Could not create directory {output_directory}: {e}")
                selected_output_dir = filedialog.askdirectory(title="Select Output Directory", initialdir=".")
                if selected_output_dir:
                    output_directory = selected_output_dir
                else:
                    messagebox.showwarning("Output Dir Error",
                                           "No output directory selected and default couldn't be created. Using current directory '.' as fallback.")
                    output_directory = "."
                    os.makedirs(output_directory, exist_ok=True)
        else:
            selected_output_dir = filedialog.askdirectory(title="Select Output Directory", initialdir=".")
            if selected_output_dir:
                output_directory = selected_output_dir
            else:
                messagebox.showwarning("Output Dir Warning",
                                       "No output directory selected. Using default './Extracted' (will be created if needed by app).")
    root.deiconify()

    app = PhotoExtractorGUI(root, input_directory, output_directory)
    if root.winfo_exists():
        app.run()
