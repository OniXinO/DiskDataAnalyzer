"""
Build script для створення Windows executable з PyInstaller
"""

import subprocess
import sys
import os


def build_exe():
    """Збірка Windows executable з PyInstaller"""
    print("🔨 Building DiskDataAnalyzer.exe...")

    # Перевіряємо що PyInstaller встановлено
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not installed!")
        print("Install with: pip install pyinstaller>=5.10.0")
        sys.exit(1)

    # Запускаємо PyInstaller
    cmd = [
        sys.executable,
        '-m', 'PyInstaller',
        '--clean',
        '--noconfirm',
        'diskanalyzer.spec'
    ]

    build_dir = os.path.dirname(__file__)
    result = subprocess.run(cmd, cwd=build_dir)

    if result.returncode == 0:
        print("\n✅ Build successful!")
        print(f"Executable: {os.path.join(build_dir, 'dist', 'DiskDataAnalyzer.exe')}")
    else:
        print("\n❌ Build failed!")
        sys.exit(1)


if __name__ == '__main__':
    build_exe()
