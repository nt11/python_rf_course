
from pathlib import Path

# Create some paths
base_dir = Path.cwd() / Path("my_project")
data_dir = base_dir / "data"
images_dir = data_dir / "images"
config_file = base_dir / "config.txt"

# Create directory structure
images_dir.mkdir(parents=True, exist_ok=True)

# Create and write to a file using with open
with open(config_file, 'w') as f:
    f.write("Hello from pathlib!")

# Create some image files
(images_dir / "image1.jpg").touch()
(images_dir / "image2.png").touch()
(images_dir / "document.txt").touch()

# Read file content using with open
with open(config_file, 'r') as f:
    content = f.read()
print(f"Config content: {content}")

# List all files in images directory
print("\nFiles in images directory:")
for file in images_dir.iterdir():
    print(f"- {file.name}")

# Find only image files using glob
print("\nImage files only:")
for image in images_dir.glob("*.jpg"):
    print(f"- {image.name}")

# Get file information
if config_file.exists():
    print(f"\nConfig file info:")
    print(f"Parent directory: {config_file.parent}")
    print(f"File name: {config_file.name}")
    print(f"Stem: {config_file.stem}")
    print(f"Suffix: {config_file.suffix}")
    print(f"Absolute path: {config_file.resolve()}")