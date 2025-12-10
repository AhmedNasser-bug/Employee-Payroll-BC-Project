import os
import subprocess
import sys

# Constants
VALIDATION_FILE = "feature_validation.txt"

def run_cmd(args, cwd=None):
    if cwd is None:
        cwd = os.getcwd()
    try:
        result = subprocess.run(
            args, 
            cwd=cwd, 
            text=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            check=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()

def start_feature(modifier_func, validation_steps):
    branch_name = modifier_func.__name__
    print(f"\n--- Starting Feature: {branch_name} ---")

    # 1. Create/Switch Branch
    print(f"[*] Creating branch '{branch_name}'...")
    success, _ = run_cmd(["git", "checkout", "-b", branch_name])
    if not success:
        print(f"    Branch might exist, switching to '{branch_name}'...")
        success, _ = run_cmd(["git", "checkout", branch_name])
        if not success:
            print("[!] Failed to switch branch.")
            return

    # 2. Execute Modifier
    print(f"[*] Executing modification function: {branch_name}()")
    try:
        modifier_func()
    except Exception as e:
        print(f"[!] Function execution failed: {e}")
        return

    # 3. Save Validation Steps
    print(f"[*] Saving validation instructions...")
    with open(VALIDATION_FILE, "w", encoding="utf-8") as f:
        f.write(validation_steps)

    # 4. Commit
    print("[*] Committing changes...")
    run_cmd(["git", "add", "."])
    success, msg = run_cmd(["git", "commit", "-m", f"Feature: {branch_name} implemented"])
    
    if success:
        print(f"[SUCCESS] Feature '{branch_name}' ready.")
        print(f"[*] Validation steps saved to '{VALIDATION_FILE}'")
    else:
        print(f"[!] Commit failed: {msg}")

def finish_feature():
    print("\n--- Finalizing Feature ---")

    # 1. Identify Branch
    success, current_branch = run_cmd(["git", "branch", "--show-current"])
    if not success or current_branch == "master":
        print("[!] You are on 'master' or detection failed. Switch to feature branch first.")
        return

    # 2. Read Validation
    if not os.path.exists(VALIDATION_FILE):
        print(f"[!] '{VALIDATION_FILE}' not found.")
        return

    with open(VALIDATION_FILE, "r", encoding="utf-8") as f:
        steps = f.read()

    print(f"\n[?] VALIDATION FOR '{current_branch}':")
    print("-" * 40)
    print(steps)
    print("-" * 40)

    # 3. Merge
    if input("\nDid these checks pass? (yes/no): ").strip().lower() == "yes":
        print(f"[*] Switching to master...")
        run_cmd(["git", "checkout", "master"])
        
        print(f"[*] Merging '{current_branch}'...")
        success, msg = run_cmd(["git", "merge", current_branch])
        
        if success:
            print(f"[SUCCESS] Merged {current_branch} into master.")
            print(f"[*] Deleting branch '{current_branch}'...")
            run_cmd(["git", "branch", "-d", current_branch])
        else:
            print(f"[!] Merge conflict:\n{msg}")
    else:
        print("[*] Merge aborted.")
