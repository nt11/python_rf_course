from pathlib import Path


if __name__ == "__main__":
   print("Results")
   print("-------")

   # Current directory and files
   current = Path.cwd()
   print(f"Current directory: {current}")

   # Create some paths
   data_dir = Path("data")
   file_path = data_dir / "test.txt"

   # Create directory and file
   data_dir.mkdir(exist_ok=True)
   file_path.write_text("Hello from pathlib!")

   # Show structure and content
   print("\nDirectory contents:")
   for item in data_dir.iterdir():
      print(f"- {item.name}")