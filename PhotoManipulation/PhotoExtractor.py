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
import re # Added for parsing filenames
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk, UnidentifiedImageError

# --- Helper Functions ---
# IoU and NMS functions remain largely the same, they operate on bounding boxes
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
        remaining_boxes_area = (boxes_xyxy[idxs[:last], 2] - boxes_xyxy[idxs[:last], 0]) * (boxes_xyxy[idxs[:last], 3] - boxes_xyxy[idxs[:last], 1])
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

    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    """
    Applies a four point perspective transform to a region defined by points pts.
    """
    rect = order_points(pts)
    if rect is None:
        return None # Return None if points ordering failed

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

    if maxWidth < 20 or maxHeight < 20: # Prevent errors/tiny outputs
        # print("Warning: Calculated very small dimensions for perspective transform.")
        return None

    dst = np.array([
        [buffer, buffer],
        [maxWidth - buffer -1 , buffer],
        [maxWidth - buffer -1, maxHeight - buffer -1],
        [buffer, maxHeight - buffer -1]], dtype = "float32")

    rect = rect.astype("float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # Crop the buffer added at the start/end
    warped = warped[buffer:maxHeight-buffer, buffer:maxWidth-buffer]

    return warped

def calculate_rotated_rect_points(x_min, y_min, x_max, y_max, angle_degrees):
    """
    Calculates the 4 corner points of an axis-aligned rectangle defined by
    (x_min, y_min) and (x_max, y_max), rotated by angle_degrees around its center.

    Returns points in original image coordinates.
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
    # We want positive angle on slider to mean clockwise rotation on screen, so use -angle
    M = cv2.getRotationMatrix2D((center_x, center_y), -angle_degrees, 1.0)

    # Apply the rotation matrix to the corners
    # Need to add a column of ones to the corners for matrix multiplication
    corners_homogeneous = np.c_[corners, np.ones(4)] # Add a column of 1s
    rotated_corners = np.dot(M, corners_homogeneous.T).T # Apply matrix, then transpose back

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
    if image_crop is None or image_crop.shape[0] < 10 or image_crop.shape[1] < 10: # Minimum size for crop
        # print("find_photo_rect_in_roi: Image crop too small or None.")
        return None

    crop_height, crop_width = image_crop.shape[:2]
    crop_area = crop_height * crop_width
    crop_diagonal = math.sqrt(crop_width**2 + crop_height**2)


    if crop_area == 0:
        # print("find_photo_rect_in_roi: Crop area is zero.")
        return None

    # Convert parameters from scaled slider values (integers) to floats if necessary
    # Ensure keys exist and values are numbers
    canny_low = params.get('canny_low', 50)
    canny_high = params.get('canny_high', 150)
    min_area_ratio = params.get('min_area_ratio_scaled', 5) / 1000.0 # Scale back, default 0.005
    max_area_ratio = params.get('max_area_ratio_scaled', 950) / 1000.0 # Scale back, default 0.95
    min_aspect_ratio_val = params.get('min_aspect_ratio_scaled', 30) / 100.0 # Scale back, default 0.3
    max_aspect_ratio_val = params.get('max_aspect_ratio_scaled', 300) / 100.0 # Scale back, default 3.0
    min_perimeter_ratio = params.get('min_perimeter_ratio_scaled', 20) / 1000.0 # Scale back, default 0.02
    nms_iou_threshold = params.get('nms_iou_threshold_scaled', 30) / 100.0 # Scale back, default 0.3
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
            continue # Skip this contour if minAreaRect fails

        (center_crop, (width, height), angle) = rect

        if width < 5 or height < 5: # Minimum dimension in pixels for a potential photo
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
            continue # Skip this rect

        box_points_int = np.intp(box_points) # Convert to integer points for boundingRect
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
                  break # Found match, move to next picked box


    if best_rect_crop is None:
        # print("No best rectangle found after filtering and NMS")
        return None # No suitable rectangle found

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
        os.makedirs(self.output_dir, exist_ok=True) # Ensure output dir exists

        self.image_files = []
        self.current_image_index = 0
        self.original_image = None
        self.tk_image = None # Stores the ImageTk.PhotoImage for the canvas
        self.display_scale = 1.0 # Scale factor for displaying image on canvas
        self.display_offset_x = 0
        self.display_offset_y = 0

        # Drawing state (Red ROI)
        self.drawing = False
        self.roi_start_canvas = None # (x, y) on canvas
        self.roi_end_canvas = None # (x, y) on canvas
        # axis-aligned bounds of the *initially drawn* ROI in original image coords (min/max)
        self.roi_axis_aligned_bounds_orig = None # (x_min, y_min, x_max, y_max)
        self.roi_rectangle_id = None # Canvas item ID for the drawn ROI (now a polygon)

        # Detected rectangle state (Green)
        self.detected_rect_orig = None # The single best rotated rect in original image coords
        self.detected_rectangle_id = None # Canvas item ID for the detected outline

        # self.photo_save_counter = 0 # Counter for sequential saving across all images # MODIFIED: Removed
        # MODIFICATION: Store determined output file extension for the current image
        self.output_file_extension_for_current_image = ".jpg" # Default, updated in load_current_image


        # --- Parameters with Default Values ---
        self.params = {
            'canny_low': tk.IntVar(value=50),
            'canny_high': tk.IntVar(value=150),
            'min_area_ratio_scaled': tk.IntVar(value=int(0.005 * 1000)), # 0.005
            'max_area_ratio_scaled': tk.IntVar(value=int(0.95 * 1000)), # 0.95
            'min_aspect_ratio_scaled': tk.IntVar(value=int(0.3 * 100)), # 0.3
            'max_aspect_ratio_scaled': tk.IntVar(value=int(3.0 * 100)), # 3.0
            'min_perimeter_ratio_scaled': tk.IntVar(value=int(0.02 * 1000)), # 0.02
            'nms_iou_threshold_scaled': tk.IntVar(value=int(0.3 * 100)), # 0.3
            'min_contour_area_px': tk.IntVar(value=100), # Minimum contour area in pixels (applied before minAreaRect)
             'roi_buffer_px': tk.IntVar(value=10) # Buffer added to ROI crop
        }
        # Ranges for scaled parameters (min, max)
        self.param_ranges = {
            'canny_low': (0, 255),
            'canny_high': (0, 255),
            'min_area_ratio_scaled': (0, 500), # 0 to 0.5 (scaled to 1000)
            'max_area_ratio_scaled': (500, 1000), # 0.5 to 1.0 (scaled to 1000)
            'min_aspect_ratio_scaled': (10, 100), # 0.1 to 1.0 (scaled to 100)
            'max_aspect_ratio_scaled': (100, 500), # 1.0 to 5.0 (scaled to 100)
            'min_perimeter_ratio_scaled': (0, 200), # 0 to 0.2 (scaled to 1000)
            'nms_iou_threshold_scaled': (0, 100), # 0.0 to 1.0 (scaled to 100)
            'min_contour_area_px': (0, 5000), # 0 to 5000 pixels
            'roi_buffer_px': (0, 50) # 0 to 50 pixels buffer
        }

        # --- Manual Save Options ---
        self.rotation_angle_var = tk.DoubleVar(value=0.0) # Stores rotation angle for red ROI save


        # --- GUI Layout ---
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Image display area (Canvas)
        self.canvas_frame = ttk.Frame(self.main_frame)
        self.canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        self.main_frame.columnconfigure(0, weight=3) # Canvas area takes more space
        self.main_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.canvas_frame, bg="gray", bd=0, highlightthickness=0) # Set background for empty space
        self.canvas.pack(expand=True, fill=tk.BOTH) # Use pack for canvas within frame

        # Bind mouse events for drawing
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        # Bind configure event to handle resizing
        self.canvas.bind("<Configure>", self.on_canvas_configure)


        # Controls area
        self.controls_frame = ttk.Frame(self.main_frame, padding="10")
        self.controls_frame.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W), padx=10, pady=5) # Sticky E+W allows cols to expand
        self.main_frame.columnconfigure(1, weight=1) # Controls area takes less space
        self.controls_frame.columnconfigure(1, weight=1) # Make the scale/entry column expand
        self.controls_frame.columnconfigure(2, weight=0) # Value column doesn't expand

        # Current file label
        self.file_label = ttk.Label(self.controls_frame, text="File: N/A")
        self.file_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Parameter sliders
        param_grid_row_start = 1
        self._create_parameter_controls(self.controls_frame, starting_row=param_grid_row_start)
        last_param_row = param_grid_row_start + len(self.params) -1


        # --- Manual Save Options Group ---
        manual_save_frame = ttk.LabelFrame(self.controls_frame, text="Manual Save Options", padding="10")
        # Place below parameters
        manual_save_frame.grid(row=last_param_row + 1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        manual_save_frame.columnconfigure(1, weight=1) # Make entry/scale column expand

        # Rotation Slider and Label
        ttk.Label(manual_save_frame, text="Rotation (°):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.rotation_scale = ttk.Scale(
            manual_save_frame,
            from_=-10.0, # Sensitive range
            to_=10.0,
            variable=self.rotation_angle_var,
            orient=tk.HORIZONTAL,
            command=self.on_rotation_change, # Call update display when slider changes
            length=150
            # Removed resolution=0.1 as it's not supported by ttk.Scale
        )
        self.rotation_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.rotation_scale.config(state=tk.DISABLED) # Start disabled

        # Label to display current rotation value (always 2 decimal places)
        self.rotation_value_var = tk.StringVar()
        self.rotation_value_var.set("0.00") # Initial value
        ttk.Label(manual_save_frame, textvariable=self.rotation_value_var).grid(row=0, column=2, sticky=tk.W, padx=5, pady=2)
        # Trace the rotation variable to update the display label
        self.rotation_angle_var.trace_add("write", lambda v,i,m: self.rotation_value_var.set(f"{self.rotation_angle_var.get():.2f}"))


        # Manual Save Button
        self.save_red_button = ttk.Button(manual_save_frame, text="Save Red Selection", command=self.save_red_selection, state=tk.DISABLED)
        self.save_red_button.grid(row=1, column=0, columnspan=3, pady=5)


        # --- Action Buttons ---
        self.button_frame = ttk.Frame(self.controls_frame)
        # Place below manual save options
        self.button_frame.grid(row=last_param_row + 2, column=0, columnspan=3, pady=10)

        self.save_green_button = ttk.Button(self.button_frame, text="Save Auto-Detected Photo", command=self.save_detected_photo, state=tk.DISABLED)
        self.save_green_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear Selection", command=self.clear_selection, state=tk.DISABLED)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(self.button_frame, text="Next Image (Discard)", command=self.load_next_image)
        self.next_button.pack(side=tk.LEFT, padx=5)


        # --- Initial Setup ---
        self.load_image_files()
        # MODIFICATION: Ensure initial image loads after GUI elements are ready
        if self.image_files:
            self.root.update_idletasks() # Allow Tkinter to process initial layout
            self.load_current_image()
        else:
            # If no images found by load_image_files, it will show an error and exit.
            # This part is for safety, in case load_image_files doesn't exit for some reason.
            if not self.image_files: # Re-check as load_image_files might destroy root
                 if self.root.winfo_exists(): # Check if root window still exists
                    messagebox.showerror("No Images", "No images found to load.")
                    self.root.destroy()

    def _get_next_save_number(self):
        """
        Determines the next available integer for saving a file in self.output_dir.
        Scans for files named like '1.jpg', '002.png', etc.
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir) # Should be created in __init__ but good to be safe
            return 1

        max_num = 0
        # Regex to find numbers at the beginning of the filename (before extension)
        # It will match "1.jpg", "002.png", "123.jpeg" but not "photo_1.jpg"
        # To match "photo_1.jpg" style, regex would need to be more complex,
        # for now, sticking to simple numeric names.
        numeric_file_pattern = re.compile(r"^(\d+)\.(jpg|jpeg|png|tiff|bmp)$", re.IGNORECASE)

        try:
            for f in os.listdir(self.output_dir):
                match = numeric_file_pattern.match(f)
                if match:
                    num = int(match.group(1))
                    if num > max_num:
                        max_num = num
        except Exception as e:
            print(f"Error scanning output directory for next save number: {e}")
            # Fallback or re-raise, for now, just prints and continues to return max_num + 1
            pass #This will default to 1 if directory was empty or unreadable

        return max_num + 1


    def _create_parameter_controls(self, parent_frame, starting_row):
        """Creates labels and scales for each parameter with value display."""
        row = starting_row

        # Mapping of internal param key to display name and scaling factor
        param_info = [
            ('canny_low', 'Canny Low', 1, "int"),
            ('canny_high', 'Canny High', 1, "int"),
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
            label = ttk.Label(parent_frame, text=display_name)
            label.grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)

            # Determine scale range based on key
            min_val, max_val = self.param_ranges[key]

            scale = ttk.Scale(
                parent_frame,
                from_=min_val,
                to=max_val,
                variable=self.params[key],
                orient=tk.HORIZONTAL,
                command=self.on_parameter_change, # Call update logic when slider changes
                length=150 # Adjust length as needed
            )
            scale.grid(row=row, column=1, sticky=(tk.W, tk.E), pady=2, padx=5)

            # Label to display current value (always 2 decimal places)
            display_value_var = tk.StringVar()
            # Function to update the StringVar when the parameter variable changes
            def update_display_value(var_name, index, mode, param_key=key, factor=scale_factor, display_var=display_value_var, p_type=param_type):
                try:
                    val = self.params[param_key].get()
                    if p_type == "float":
                        float_val = val / factor
                        display_var.set(f"{float_val:.2f}") # Always show 2 decimal places
                    else: # int type
                        display_var.set(f"{val:.2f}") # Format as float with 2 decimal places
                except Exception:
                    display_var.set("Err") # Handle potential errors during get()
            # Trace the variable to update the display label
            self.params[key].trace_add("write", update_display_value)
            # Set initial value
            update_display_value(None, None, None)

            value_label = ttk.Label(parent_frame, textvariable=display_value_var)
            value_label.grid(row=row, column=2, sticky=tk.W, pady=2, padx=5)

            row += 1

    def load_image_files(self):
        """Finds all image files in the input directory."""
        image_patterns = ["*.png", "*.jpg", "*.jpeg", "*.tiff", "*.bmp"] # Common image formats
        self.image_files = []
        for pattern in image_patterns:
            self.image_files.extend(glob.glob(os.path.join(self.input_dir, pattern)))

        self.image_files.sort() # Sort alphabetically/numerically

        if not self.image_files:
            # Check if root window still exists before showing messagebox
            if self.root.winfo_exists():
                messagebox.showerror("No Images Found", f"No image files found in {self.input_dir}")
                self.root.destroy() # Close app if no images
            return # Exit early


    def load_current_image(self):
        """Loads the image at the current index and updates the display."""
        if not self.image_files or self.current_image_index >= len(self.image_files):
            if self.root.winfo_exists():
                messagebox.showinfo("Finished", "All images processed!")
                self.root.destroy() # Close app when done
            return

        image_path = self.image_files[self.current_image_index]
        self.file_label.config(text=f"File: {os.path.basename(image_path)} ({self.current_image_index + 1}/{len(self.image_files)})")

        # MODIFICATION: Determine and store the output file extension based on the input image
        _, input_ext = os.path.splitext(image_path)
        if input_ext.lower() == ".png":
            self.output_file_extension_for_current_image = ".png"
        else:
            # For other formats (jpg, jpeg, tiff, bmp), default to saving as JPG
            self.output_file_extension_for_current_image = ".jpg"


        try:
            # Use PIL to handle potential format issues, then convert to OpenCV
            pil_img = Image.open(image_path)
            # Ensure image is in RGB format if it has an alpha channel or is grayscale
            if pil_img.mode != 'RGB':
                 pil_img = pil_img.convert('RGB')
            self.original_image = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        except (FileNotFoundError, UnidentifiedImageError, Exception) as e:
            if self.root.winfo_exists():
                messagebox.showwarning("Error Loading Image", f"Could not read image {image_path}: {e}. Skipping.")
            self.current_image_index += 1
            # Avoid infinite loop if only bad files exist
            if self.current_image_index < len(self.image_files):
                 self.load_current_image() # Try loading the next one
            elif self.root.winfo_exists():
                 messagebox.showinfo("Finished", "No more images could be loaded.")
                 self.root.destroy()
            return

        # Clear any previous selection and drawing
        self.clear_selection()
        # The image will be displayed when the canvas is configured for the first time by the system,
        # or if already configured, by calling display_image_on_canvas().
        # We call it explicitly here to ensure image is shown immediately if canvas is ready.
        if self.canvas.winfo_width() > 1 and self.canvas.winfo_height() > 1:
             self.display_image_on_canvas()
        # else:
            # print(f"Canvas not ready for image display: {self.canvas.winfo_width()}x{self.canvas.winfo_height()}")
            # It will be called by on_canvas_configure when ready


    def on_canvas_configure(self, event):
        """Handle window/canvas resizing."""
        # print(f"Canvas configured: {event.width}x{event.height}")
        if self.original_image is not None:
            self.display_image_on_canvas()
            # If an ROI was drawn, redraw it scaled and rotated
            if self.roi_axis_aligned_bounds_orig is not None:
                 self.draw_roi_on_canvas()
                 # If a detection was made, redraw it scaled
                 if self.detected_rect_orig is not None:
                      self.draw_detected_rect_on_canvas()


    def display_image_on_canvas(self):
        """Resizes the original image for display and puts it on the canvas."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1 or self.original_image is None:
            # print(f"Display condition not met: CW:{canvas_width}, CH:{canvas_height}, Img:{self.original_image is not None}")
            return

        original_height, original_width = self.original_image.shape[:2]

        # Calculate scaling factor to fit image while maintaining aspect ratio
        scale_w = canvas_width / original_width
        scale_h = canvas_height / original_height
        self.display_scale = min(scale_w, scale_h)
        if self.display_scale <= 0: self.display_scale = 1.0 # Safety for tiny canvas

        display_width = int(original_width * self.display_scale)
        display_height = int(original_height * self.display_scale)

        # Calculate offsets to center the image
        self.display_offset_x = (canvas_width - display_width) // 2
        self.display_offset_y = (canvas_height - display_height) // 2

        # Resize the image using OpenCV
        resized_img_cv2 = cv2.resize(self.original_image, (display_width, display_height), interpolation=cv2.INTER_AREA)

        # Convert OpenCV image (BGR) to RGB for PIL
        resized_img_cv2_rgb = cv2.cvtColor(resized_img_cv2, cv2.COLOR_BGR2RGB)

        # Convert to PIL Image and then Tkinter PhotoImage
        pil_image = Image.fromarray(resized_img_cv2_rgb)
        self.tk_image = ImageTk.PhotoImage(pil_image)

        # Clear previous canvas content (image and overlays)
        self.canvas.delete("all")
        self.roi_rectangle_id = None
        self.detected_rectangle_id = None

        # Display the image on the canvas, centered
        self.canvas.create_image(self.display_offset_x, self.display_offset_y,
                                 anchor=tk.NW, image=self.tk_image)
        # print(f"Image displayed at ({self.display_offset_x},{self.display_offset_y}) with scale {self.display_scale}")


    def canvas_to_original(self, x_canvas, y_canvas):
        """Converts canvas coordinates to original image coordinates."""
        if self.display_scale == 0 or self.original_image is None: return None, None # Avoid division by zero

        # Calculate relative position within the displayed image area
        x_relative = x_canvas - self.display_offset_x
        y_relative = y_canvas - self.display_offset_y

        # Convert relative display coords to original image coords
        x_orig = int(x_relative / self.display_scale)
        y_orig = int(y_relative / self.display_scale)

        # Clamp coordinates to image boundaries
        h, w = self.original_image.shape[:2]
        x_orig = max(0, min(x_orig, w - 1))
        y_orig = max(0, min(y_orig, h - 1))
        return x_orig, y_orig

    def original_to_canvas(self, x_orig, y_orig):
        """Converts original image coordinates to canvas coordinates."""
        if self.original_image is None: return None, None

        x_canvas = int(x_orig * self.display_scale + self.display_offset_x)
        y_canvas = int(y_orig * self.display_scale + self.display_offset_y)
        return x_canvas, y_canvas

    def on_button_press(self, event):
        """Start drawing ROI."""
        # Ignore if image not loaded
        if self.original_image is None:
            return

        # Ensure press was within the displayed image area
        canvas_x, canvas_y = event.x, event.y
        img_disp_w = int(self.original_image.shape[1] * self.display_scale)
        img_disp_h = int(self.original_image.shape[0] * self.display_scale)

        if not (self.display_offset_x <= canvas_x <= self.display_offset_x + img_disp_w and
                self.display_offset_y <= canvas_y <= self.display_offset_y + img_disp_h):
             # print("Click outside image area")
             return # Ignore clicks outside the displayed image

        # Clear previous selection when starting a new draw
        self.clear_selection()

        self.drawing = True
        # Store start point in original image coordinates
        self.roi_start_orig = self.canvas_to_original(event.x, event.y)
        self.roi_start_canvas = (event.x, event.y)
        self.roi_end_canvas = (event.x, event.y) # Initialize end point


    def on_mouse_drag(self, event):
        """Update and redraw ROI polygon while dragging."""
        if not self.drawing or self.original_image is None:
            return

        self.roi_end_canvas = (event.x, event.y)

        # Redraw the current axis-aligned rectangle shape while dragging
        # This is simpler than calculating rotated points during drag
        self.draw_roi_on_canvas(is_dragging=True)


    def on_button_release(self, event):
        """Finalize ROI, perform detection within ROI, and display result."""
        if not self.drawing or self.original_image is None:
            return

        self.drawing = False
        self.roi_end_canvas = (event.x, event.y)
        end_orig = self.canvas_to_original(event.x, event.y) # Get end in original coords

        if self.roi_start_orig is None or end_orig is None: # Should not happen if drawing started correctly
            self.clear_selection()
            return

        # Ensure start and end are ordered min to max for calculating axis-aligned bounds
        x1_orig, y1_orig = self.roi_start_orig
        x2_orig, y2_orig = end_orig
        x_min_orig, x_max_orig = min(x1_orig, x2_orig), max(x1_orig, x2_orig)
        y_min_orig, y_max_orig = min(y1_orig, y2_orig), max(y1_orig, y2_orig)

        # Store the normalized axis-aligned original coordinates
        self.roi_axis_aligned_bounds_orig = (x_min_orig, y_min_orig, x_max_orig, y_max_orig)

        # Ensure ROI is large enough for detection or manual save
        min_roi_size = 20 # Pixels
        if x_max_orig - x_min_orig < min_roi_size or y_max_orig - y_min_orig < min_roi_size:
            # print("ROI too small, clearing selection.")
            self.clear_selection()
            return

        # Reset rotation angle to 0 for the new ROI
        self.rotation_angle_var.set(0.0)
        self.rotation_scale.config(state=tk.NORMAL) # Enable rotation slider

        # Draw the initial (0 rotation) red ROI polygon
        self.draw_roi_on_canvas()

        # Enable manual save button and clear button
        self.save_red_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)


        # Perform detection within the finalized ROI
        self.run_detection_in_roi()


    def draw_roi_on_canvas(self, is_dragging=False):
        """Draws the red ROI polygon on the canvas."""
        if self.original_image is None: return
        if not is_dragging and self.roi_axis_aligned_bounds_orig is None:
            # print("draw_roi_on_canvas: Missing ROI bounds for final draw, returning.")
            return
        if is_dragging and (self.roi_start_canvas is None or self.roi_end_canvas is None):
            # print("draw_roi_on_canvas: Missing drag points, returning.")
            return


        # Delete previous rectangle/polygon if it exists
        self.canvas.delete("roi_rect")
        self.roi_rectangle_id = None # Reset ID

        if is_dragging:
             # Draw a simple rectangle based on initial and current canvas points while dragging
             x1_c, y1_c = self.roi_start_canvas
             x2_c, y2_c = self.roi_end_canvas # Use live end point from drag
             points_canvas = [x1_c, y1_c, x2_c, y2_c]
             # Draw the rectangle
             self.roi_rectangle_id = self.canvas.create_rectangle(
                points_canvas, outline='red', width=2, tags="roi_rect"
            )
        else:
            # For the final display (after release or on parameter/rotation change), calculate rotated points
            x_min_orig, y_min_orig, x_max_orig, y_max_orig = self.roi_axis_aligned_bounds_orig
            rotation_angle = self.rotation_angle_var.get()
            rotated_points_orig = calculate_rotated_rect_points(x_min_orig, y_min_orig, x_max_orig, y_max_orig, rotation_angle)

            # Convert original image points to canvas coordinates
            canvas_points = []
            for point_orig in rotated_points_orig:
                x_c, y_c = self.original_to_canvas(point_orig[0], point_orig[1])
                if x_c is None or y_c is None: # Should not happen if image is loaded
                    # print("Warning: original_to_canvas returned None during ROI draw")
                    return
                canvas_points.append((x_c, y_c))

            # Draw the polygon outline
            # Canvas create_polygon expects a flat list of points [x1, y1, x2, y2, ...]
            flat_canvas_points = [coord for point in canvas_points for coord in point]

            self.roi_rectangle_id = self.canvas.create_polygon(
                flat_canvas_points,
                outline='red', fill='', width=2, tags="roi_rect"
            )

        # Ensure ROI drawing is on top
        self.canvas.tag_raise("roi_rect")
        if self.detected_rectangle_id: # Keep green below red
             self.canvas.tag_lower("detected_rect", "roi_rect")


    def draw_detected_rect_on_canvas(self):
        """Draws the green detected polygon on the canvas based on self.detected_rect_orig."""
        # Delete previous detection drawing if it exists
        self.canvas.delete("detected_rect")
        self.detected_rectangle_id = None # Reset ID

        if self.detected_rect_orig is None or self.original_image is None:
            self.save_green_button.config(state=tk.DISABLED)
            # Clear button state is managed by ROI presence
            return

        # Get the points of the detected rectangle in original image coordinates
        box_points_orig = cv2.boxPoints(self.detected_rect_orig)
        box_points_orig = np.intp(box_points_orig) # Convert to integer points

        # Convert original image points to canvas coordinates
        canvas_points = []
        for point_orig in box_points_orig:
            x_c, y_c = self.original_to_canvas(point_orig[0], point_orig[1])
            if x_c is None or y_c is None: # Should not happen if image is loaded
                # print("Warning: original_to_canvas returned None during detected_rect draw")
                return
            canvas_points.append((x_c, y_c))

        # Draw the polygon outline
        flat_canvas_points = [coord for point in canvas_points for coord in point]

        self.detected_rectangle_id = self.canvas.create_polygon(
            flat_canvas_points,
            outline='lime green', fill='', width=2, tags="detected_rect"
        )

        # Ensure detection outline is drawn below the ROI if both exist
        self.canvas.tag_raise("detected_rect")
        if self.roi_rectangle_id: # Keep green below red
             self.canvas.tag_lower("detected_rect", "roi_rect")


        self.save_green_button.config(state=tk.NORMAL)
        # Clear button state is managed by ROI presence


    def run_detection_in_roi(self):
        """
        Crops the original image based on the axis-aligned ROI bounds and runs
        photo detection within the cropped region. Updates self.detected_rect_orig.
        """
        if self.original_image is None or self.roi_axis_aligned_bounds_orig is None:
            # print("run_detection_in_roi: Missing ROI or image, clearing detection.")
            self.detected_rect_orig = None
            self.draw_detected_rect_on_canvas() # Clear any previous detection drawing
            return

        # Use the *axis-aligned* ROI bounds for the initial crop
        x_min_orig, y_min_orig, x_max_orig, y_max_orig = self.roi_axis_aligned_bounds_orig

        # Add a buffer to the ROI crop region
        buffer = self.params['roi_buffer_px'].get()
        h_orig, w_orig = self.original_image.shape[:2]

        crop_x_min = max(0, x_min_orig - buffer)
        crop_y_min = max(0, y_min_orig - buffer)
        crop_x_max = min(w_orig, x_max_orig + buffer)
        crop_y_max = min(h_orig, y_max_orig + buffer)

        # Ensure minimum crop size even with buffer
        min_crop_dim = 20 # Pixels
        if crop_x_max - crop_x_min < min_crop_dim or crop_y_max - crop_y_min < min_crop_dim:
             # print("Crop region too small even with buffer.")
             self.detected_rect_orig = None
        else:
            # Crop the image
            image_crop = self.original_image[crop_y_min:crop_y_max, crop_x_min:crop_x_max].copy() # Use copy

            # Get current parameters from the GUI variables
            current_params = {key: var.get() for key, var in self.params.items()}

            # Find the best rectangle in the cropped region
            # Pass the offset of the crop in original image coords
            self.detected_rect_orig = find_photo_rect_in_roi(
                image_crop, (crop_x_min, crop_y_min), current_params
            )

        # Update the display with the new detection result and update button state
        self.draw_detected_rect_on_canvas()


    def on_parameter_change(self, *args):
        """Callback for parameter slider changes. Re-runs detection if ROI exists."""
        # If an ROI is currently drawn, re-run detection with new parameters
        if self.roi_axis_aligned_bounds_orig is not None:
            self.run_detection_in_roi()
        # Value labels are updated automatically via trace_add

    def on_rotation_change(self, *args):
        """Callback for rotation slider changes. Updates the red ROI polygon display."""
        if self.roi_axis_aligned_bounds_orig is not None:
             # Only redraw the ROI polygon with the new rotation
             self.draw_roi_on_canvas()
             # The rotation value label is updated automatically via trace_add

    def save_detected_photo(self):
        """Saves the currently auto-detected photo (green) using perspective transform."""
        if self.original_image is None or self.detected_rect_orig is None:
            messagebox.showinfo("Nothing to Save", "No auto-detected photo found to save.")
            return

        # Create output directory if it doesn't exist (should be done in __init__ too)
        os.makedirs(self.output_dir, exist_ok=True)


        # Save the detected photo using perspective transform
        try:
            # cv2.boxPoints needs rect format ((center_x, center_y), (width, height), angle)
            # self.detected_rect_orig is already in this format and in original image coords
            box_points_orig = cv2.boxPoints(self.detected_rect_orig)
            box_points_orig = np.float32(box_points_orig) # Ensure float32 for four_point_transform

            cropped_image = four_point_transform(self.original_image, box_points_orig)

            if cropped_image is not None and cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
                # MODIFICATION: Get next available save number
                save_number = self._get_next_save_number()
                # MODIFICATION: Use determined output file extension
                output_filename = f"{save_number}{self.output_file_extension_for_current_image}"
                output_path = os.path.join(self.output_dir, output_filename)

                cv2.imwrite(output_path, cropped_image)
                # MODIFICATION: Updated print statement for clarity
                print(f"Saved auto-detected photo {save_number} from {os.path.basename(self.image_files[self.current_image_index])} as {output_filename}")

            else:
                messagebox.showwarning("Save Warning", "Could not crop auto-detected area (too small/invalid).")

        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving auto-detected photo: {e}")

    def save_red_selection(self):
        """Saves the image region defined by the red ROI, transformed according to rotation."""
        if self.original_image is None or self.roi_axis_aligned_bounds_orig is None:
            messagebox.showinfo("Nothing to Save", "No red selection found to save.")
            return

        # Create output directory if it doesn't exist (should be done in __init__ too)
        os.makedirs(self.output_dir, exist_ok=True)

        try:
            # Get the rotation angle from the slider
            rotation_angle = self.rotation_angle_var.get()

            # Get the axis-aligned bounds of the drawn ROI
            x_min_orig, y_min_orig, x_max_orig, y_max_orig = self.roi_axis_aligned_bounds_orig

            # Calculate the 4 corner points of the red ROI *rotated* by the current angle
            rotated_roi_points_orig = calculate_rotated_rect_points(
                x_min_orig, y_min_orig, x_max_orig, y_max_orig, rotation_angle
            )

            # Use four_point_transform with these rotated points to get the deskewed image
            # This crops and straightens the image based on the visible rotated red polygon
            cropped_image = four_point_transform(self.original_image, rotated_roi_points_orig)

            if cropped_image is not None and cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
                # MODIFICATION: Get next available save number
                save_number = self._get_next_save_number()
                # MODIFICATION: Use determined output file extension
                output_filename = f"{save_number}{self.output_file_extension_for_current_image}"
                output_path = os.path.join(self.output_dir, output_filename)

                cv2.imwrite(output_path, cropped_image)
                # MODIFICATION: Updated print statement for clarity and consistency
                print(f"Saved red selection photo {save_number} from {os.path.basename(self.image_files[self.current_image_index])} as {output_filename}")

            else:
                messagebox.showwarning("Save Warning", "Could not crop red selection (too small/invalid transformed area).")


        except Exception as e:
            messagebox.showerror("Save Error", f"Error saving red selection: {e}")


    def clear_selection(self):
        """Clears the drawn ROI (red) and detected photo (green) overlays."""
        # Reset drawing state
        self.drawing = False
        self.roi_start_canvas = None
        self.roi_end_canvas = None
        # Clear the stored axis-aligned ROI bounds
        self.roi_axis_aligned_bounds_orig = None

        # Reset detection state
        self.detected_rect_orig = None

        # Reset rotation slider and disable it
        self.rotation_angle_var.set(0.0)
        self.rotation_scale.config(state=tk.DISABLED)
        # The trace will update the value label

        # Remove drawings from canvas
        self.canvas.delete("roi_rect")
        self.canvas.delete("detected_rect")
        self.roi_rectangle_id = None # Reset IDs just in case
        self.detected_rectangle_id = None

        # Disable buttons
        self.save_green_button.config(state=tk.DISABLED)
        self.save_red_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)


    def load_next_image(self):
        """Increments the image index and loads the next image."""
        self.current_image_index += 1
        self.load_current_image()


    def run(self):
        """Starts the Tkinter main loop."""
        self.root.mainloop()

# --- Main Execution ---
if __name__ == "__main__":
    root = tk.Tk()

    # --- Configuration ---
    input_directory = "./OriginalDescriptions" # Default input dir
    output_directory = "./Extracted" # Default output dir

    # Ask user to select input directory if default not found or empty
    needs_input_prompt = True
    if os.path.exists(input_directory):
         image_files_check = []
         # MODIFICATION: Added ".bmp", ".tiff" to the check to align with load_image_files patterns
         for pattern in ["*.png", "*.jpg", "*.jpeg", "*.tiff", "*.bmp"]:
             image_files_check.extend(glob.glob(os.path.join(input_directory, pattern)))
         if image_files_check:
              needs_input_prompt = False # Directory exists and has images, use it

    if needs_input_prompt:
        # Temporarily hide the root window for the dialog
        root.withdraw()
        selected_input_dir = filedialog.askdirectory(
            title="Select Input Directory Containing Scans",
            initialdir=input_directory if os.path.exists(input_directory) else "."
            )
        if not selected_input_dir:
            print("No input directory selected. Exiting.")
            # root.destroy() # Don't destroy, let it be handled by app if no images
            # exit() # Replaced with a return or a flag that app init handles
            input_directory = None # Flag that no directory was selected
        else:
            input_directory = selected_input_dir
        root.deiconify() # Show the root window again

    if input_directory is None: # If user cancelled input directory selection
        if root.winfo_exists(): root.destroy()
        exit()


    # Ask user to select output directory or create default
    # Temporarily hide the root window for the dialogs
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
                      messagebox.showwarning("Output Dir Error", "No output directory selected and default couldn't be created. Using current directory '.' as fallback.")
                      output_directory = "." # Fallback
                      os.makedirs(output_directory, exist_ok=True)
         else: # User chose not to create the default
             selected_output_dir = filedialog.askdirectory(title="Select Output Directory", initialdir=".")
             if selected_output_dir:
                 output_directory = selected_output_dir
             else: # User cancelled selection after choosing not to create default
                 messagebox.showwarning("Output Dir Warning", "No output directory selected. Using default './Extracted' (will be created if needed by app).")
                 # output_directory remains "./Extracted", app will try to create it
    root.deiconify() # Show the root window again


    # --- Create and Run the GUI App ---
    app = PhotoExtractorGUI(root, input_directory, output_directory)
    # If app.image_files is empty after init (e.g., directory had no valid images), app's load_image_files would have exited.
    # We check here again if the root window was destroyed by those early exits.
    if root.winfo_exists():
        app.run()
