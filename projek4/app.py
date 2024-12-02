from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

# Fungsi normalisasi vektor
def normalize(vector):
    magnitude = np.linalg.norm(vector)
    return np.array(vector) / magnitude

# Fungsi dot product
def dot_product(v1, v2):
    return np.dot(v1, v2)

# Fungsi shading
def calculate_shading(light_dir, normal, light_intensity):
    diffuse = max(dot_product(normal, light_dir), 0) * light_intensity
    return diffuse

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    # Baca parameter dari form
    data = request.json
    light_intensity = float(data['intensity'])
    cmap = data['cmap']
    light_dir = normalize([
        float(data['light_x']),
        float(data['light_y']),
        float(data['light_z'])
    ])
    
    size = 100
    image = np.zeros((size, size))

    # Generate shading
    for y in range(size):
        for x in range(size):
            nx = (x - size / 2) / (size / 2)
            ny = (y - size / 2) / (size / 2)
            if nx**2 + ny**2 >= 1:
                continue
            nz = np.sqrt(max(0, 1 - nx**2 - ny**2))
            normal = normalize([nx, ny, nz])
            shading = calculate_shading(light_dir, normal, light_intensity)
            image[y, x] = shading

    # Simpan gambar ke buffer
    fig, ax = plt.subplots()
    ax.imshow(image, cmap=cmap)
    ax.axis('off')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return jsonify({"image": image_base64})

if __name__ == "__main__":
    app.run(debug=True)
