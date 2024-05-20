from flask import Flask, render_template, request, redirect, url_for, flash
from ultralytics import YOLO
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'sdlkégmjsdéklgjsdlékjmlkdsgjnlknsld.m,fnáéaskldasd'
UPLOAD_FOLDER = 'static/uploads'
DETECTED_FOLDER = 'static/detected'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_descriptions(descriptions):
    with open('descriptions.json', 'w') as f:
        json.dump(descriptions, f)


def load_descriptions():
    try:
        with open('descriptions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


# Load descriptions when the app starts
descriptions = load_descriptions()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    file = request.files['image']
    description = request.form['description']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        descriptions[filename] = description  # Store the description
        save_descriptions(descriptions)  # Save descriptions after updating
        return redirect(url_for('detect_image', filename=filename))
    else:
        flash('Only JPG, JPEG, or PNG files can be uploaded.')
        return redirect(url_for('index'))


@app.route('/display/<filename>')
def display_image(filename):
    return render_template('display_image.html', filename=filename,
                           image_url=url_for('static', filename=os.path.join('uploads', filename)))


@app.route('/images')
def list_images():
    images = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    return render_template('images.html', images=images)


@app.route('/detect/<filename>')
def detect_image(filename):
    source_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    model = YOLO('yolov8n.pt')  # Ensure the model file path is correct
    results = model.predict(source_path, project=DETECTED_FOLDER, name='results', exist_ok=True, save=True)
    names = model.names  # Get the model names dictionary

    car_id = None
    for key, value in names.items():
        if value == 'car':
            car_id = key
            break

    if car_id is not None:
        car_count = sum(1 for box in results[0].boxes if box.cls == car_id)
        if results:
            descriptions[filename] += f" | Detected cars: {car_count}"  # Update the description
            save_descriptions(descriptions)  # Save descriptions after updating
            flash('Detection completed successfully.')
        else:
            flash('Detection failed.')
    else:
        flash('Car class not found in model.')

    return redirect(url_for('display_image', filename=filename))


@app.route('/detected/results')
def detected_images():
    image_files = os.listdir('static/detected/results')
    return render_template('detected_images.html', images=image_files, descriptions=descriptions)


@app.route('/admin')
def admin():
    images = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    return render_template('admin.html', images=images, descriptions=descriptions)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
