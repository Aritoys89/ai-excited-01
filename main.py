"""ai-excited-01 entry: write the entry image to /output/entry.png."""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "art.jpg"), "/output/entry.png")

if __name__ == "__main__":
    main()
