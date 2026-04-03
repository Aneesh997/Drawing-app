from flask import Flask, render_template, request, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename
import uuid

# Import from utils folder
from utils.image_processing import convert_to_grayscale

app = Flask(__name__)
app.secret_key = "your-secret-key-here-change-in-production"

# ── Configuration ────────────────────────────────────────────
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16 MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def unique_filename(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return f"{uuid.uuid4().hex}.{ext}" if ext else uuid.uuid4().hex


# ── Routes ───────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
def index():
    image_path = None
    gray_image_path = None

    # 👉 ADD THESE (important)
    mean = None
    min_val = None
    max_val = None
    std = None
    hist = None

    if request.method == "POST":
        if 'image' not in request.files:
            flash('No file part in the request.', 'error')
            return redirect(request.url)

        file = request.files["image"]

        if file.filename == '':
            flash('No file selected.', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            try:
                # Save original image
                fname = unique_filename(secure_filename(file.filename))
                save_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
                file.save(save_path)

                # ── Grayscale + Brightness Analysis ──
                gray_path, mean, min_val, max_val, std , hist = convert_to_grayscale(
                    save_path,
                    app.config["UPLOAD_FOLDER"],
                    fname
                )

                image_path = save_path
                gray_image_path = gray_path

                flash('Image processed successfully!', 'success')

            except Exception as e:
                app.logger.error(f"Upload error: {e}")
                flash('Error processing file. Please try again.', 'error')
        else:
            flash('Invalid file type. Accepted: PNG, JPG, JPEG, GIF, WEBP.', 'error')

    return render_template(
        "index.html",
        image=image_path,
        gray_image=gray_image_path,
        mean=mean,
        min_val=min_val,
        max_val=max_val,
        std=std,
        hist=hist.tolist() if hist is not None else None
    )

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16 MB.', 'error')
    return redirect(url_for('index')), 413


if __name__ == "__main__":
    app.run(debug=True)