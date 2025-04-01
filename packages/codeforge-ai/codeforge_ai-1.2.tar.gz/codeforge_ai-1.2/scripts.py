import threading
import subprocess
import signal
import sys
import os
import shutil
from pathlib import Path
from app.main import main

def frontend_start():
    subprocess.run(["npm", "run", "start"], cwd="frontend")

def frontend_install():
    subprocess.run(["npm", "install"], cwd="frontend")

def frontend_build():
    subprocess.run(["npm", "run", "build"], cwd="frontend")

def codeforge_ai():
    main()

def signal_handler(sig, frame):
    print('Interrupt received, shutting down...')
    sys.exit(0)

def build_and_archive():
    archive_dir = Path("archive")
    archive_dir.mkdir(exist_ok=True)
    try:
        subprocess.run(["poetry", "build"], check=True)
        dist_dir = Path("dist")
        dist_files = list(dist_dir.glob("*"))
        if not dist_files:
            print("No distribution files found in the dist directory.")
            return
        for file in dist_files:
            shutil.copy2(file, archive_dir)
            print(f"Distribution file {file.name} copied to {archive_dir}")
        print("Build and archive process completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during build process: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def dev():
    frontend_thread = threading.Thread(target=frontend_start)
    signal.signal(signal.SIGINT, signal_handler)
    frontend_thread.start()
    try:
        main()
    except KeyboardInterrupt:
        print("Main process interrupted.")
    finally:
        frontend_thread.join()
