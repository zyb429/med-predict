import sys
import os

from MedicalApp import MedicalApp

os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
os.environ["QT_SCALE_FACTOR"] = "1"

def main():
    try:
        app = MedicalApp()
        sys.exit(app.run())
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    main()
