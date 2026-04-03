import cv2
import os
import numpy as np

def convert_to_grayscale(input_path, output_folder, filename):
    # ── Step 1: Read image ─────────────────────────────
    img = cv2.imread(os.path.abspath(input_path))

    if img is None:
        raise ValueError("Image not loaded properly")

    # ── Step 2: Convert to grayscale ───────────────────
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ── Step 3: Brightness Analysis (Week 3) ───────────
    pixels = gray.flatten()

    mean_val = np.mean(pixels)
    min_val = np.min(pixels)
    max_val = np.max(pixels)
    std_val = np.std(pixels)

    # ── Step 3.1: Histogram Calculation ────────────────
    hist = np.histogram(pixels, bins=256, range=[0,256])[0]

    # Print results (for testing/demo)
    print("\n--- Brightness Analysis ---")
    print(f"Mean Brightness: {mean_val}")
    print(f"Minimum Intensity: {min_val}")
    print(f"Maximum Intensity: {max_val}")
    print(f"Contrast (Std Dev): {std_val}")
    print("---------------------------\n")

    # ── Step 4: Save grayscale image ───────────────────
    gray_name = f"gray_{filename}"
    gray_path = os.path.join(output_folder, gray_name)

    cv2.imwrite(gray_path, gray)

    # ── Step 5: Return everything ──────────────────────
    return gray_path, mean_val, min_val, max_val, std_val, hist