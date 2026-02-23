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
    print("--- Setting up directory junctions for asset resolution ---")
    base_dirs = [
        'chapters',
        'chapters/part1',
        'chapters/part2',
        'chapters/part3',
        'chapters/part4',
        'chapters/epilogue',
        'chapters/prologue'
    ]
    
    for d in base_dirs:
        target = os.path.join(d, 'assets')
        if not os.path.exists(target):
            # mklink /J <link> <target>
            # Note: Relative target path for junction should be correct relative to the link location
            # But here we use absolute or relative to root for simplicity
            run_command(f'cmd /c "mklink /J {target} assets"', f"Creating junction for {target}")

def main():
    # 1. ジャンクション作成（Markdownファイルを書き換えずにパスを解決するため）
    setup_junctions()

    # 2. Vivliostyle ビルド
    # --output dist/ でWeb出版形式を出力
    if not run_command("vivliostyle build --output dist/", "Running Vivliostyle build"):
        sys.exit(1)

    # 3. HTML修正とナビゲーション付与
    if not run_command("python scripts/fix_web_dist.py", "Running post-process script"):
        sys.exit(1)

    print("
========================================")
    print("Build Complete! Open 'dist/index.html' to view the book.")
    print("========================================
")

if __name__ == "__main__":
    main()
