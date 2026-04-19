import os
import subprocess
import sys

def run_command(command, description):
    print(f"--- {description} ---")
    try:
        # shell=True for Windows to support commands like mklink
        result = subprocess.run(command, shell=True, check=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error during {description}: {e}")
        return False

def setup_junctions():
    print("--- Setting up directory junctions/symlinks for asset resolution ---")
    base_dirs = [
        'chapters',
        'chapters/part1',
        'chapters/part2',
        'chapters/part3',
        'chapters/part4',
        'chapters/epilogue',
        'chapters/prologue',
        'chapters/appendix',
    ]

    abs_assets = os.path.abspath('assets')

    for d in base_dirs:
        target = os.path.join(d, 'assets')
        if not os.path.exists(target):
            if sys.platform == 'win32':
                run_command(f'cmd /c "mklink /J {target} {abs_assets}"', f"Creating junction for {target}")
            else:
                os.symlink(abs_assets, target)
                print(f"Created symlink: {target} -> {abs_assets}")

def main():
    # 1. ジャンクション作成
    setup_junctions()

    # 2. Vivliostyle ビルド
    if not run_command("vivliostyle build --output dist/", "Running Vivliostyle build"):
        sys.exit(1)

    # 3. HTML修正とナビゲーション付与
    if not run_command("python scripts/fix_web_dist.py", "Running post-process script"):
        sys.exit(1)

    print("\n========================================")
    print("Build Complete! Open 'dist/index.html' to view the book.")
    print("========================================\n")

if __name__ == "__main__":
    main()
