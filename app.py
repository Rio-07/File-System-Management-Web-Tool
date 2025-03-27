from flask import Flask, render_template, request, jsonify
import os
import shutil
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename="filesystem_tool.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def scan_filesystem(directory):
    """Scans the filesystem and lists all files in the given directory."""
    if not os.path.exists(directory):
        return {"error": f"Directory '{directory}' not found!"}
    
    try:
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        return {"files": files}
    except Exception as e:
        return {"error": f"Error scanning filesystem: {e}"}

def recover_files(directory, backup_directory):
    """Recovers files from a backup directory into the main filesystem."""
    if not os.path.exists(backup_directory):
        return {"error": "Backup directory not found!"}

    os.makedirs(directory, exist_ok=True)
    
    try:
        files = [f for f in os.listdir(backup_directory) if os.path.isfile(os.path.join(backup_directory, f))]
        for file in files:
            shutil.copy2(os.path.join(backup_directory, file), os.path.join(directory, file))
        return {"message": f"Recovered {len(files)} files!"}
    except Exception as e:
        return {"error": f"Error recovering files: {e}"}

def optimize_filesystem(directory):
    """Optimizes the filesystem by renaming files systematically."""
    if not os.path.exists(directory):
        return {"error": f"Directory '{directory}' not found!"}
    
    try:
        files = sorted([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        for index, file in enumerate(files):
            old_path = os.path.join(directory, file)
            new_path = os.path.join(directory, f"optimized_{index}_{file}")
            os.rename(old_path, new_path)
        return {"message": f"Optimized {len(files)} files!"}
    except Exception as e:
        return {"error": f"Error optimizing filesystem: {e}"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scan", methods=["POST"])
def scan():
    directory = request.form.get("directory")
    return jsonify(scan_filesystem(directory))

@app.route("/recover", methods=["POST"])
def recover():
    directory = request.form.get("directory")
    backup_directory = request.form.get("backup_directory")
    return jsonify(recover_files(directory, backup_directory))

@app.route("/optimize", methods=["POST"])
def optimize():
    directory = request.form.get("directory")
    return jsonify(optimize_filesystem(directory))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
