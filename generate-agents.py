#!/usr/bin/env python3
import os, argparse, shutil

BASE = ".agents"
TEMPLATES_DIR = "templates/.agents"

def ensure_dir(p): os.makedirs(p, exist_ok=True)

def copy_tree(src, dst, force: bool):
    if not os.path.exists(src):
        raise SystemExit(f"Missing templates dir: {src}")
    for root, _, files in os.walk(src):
        for f in files:
            s = os.path.join(root, f)
            rel = os.path.relpath(s, src)
            d = os.path.join(dst, rel)
            ensure_dir(os.path.dirname(d))
            if os.path.exists(d) and not force:
                continue
            shutil.copy2(s, d)

def main():
    ap = argparse.ArgumentParser(description="Generate Inteligens Agents Framework (hybrid)")
    ap.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = ap.parse_args()

    # Copy baseline framework (router/swarm) from templates
    copy_tree(TEMPLATES_DIR, BASE, force=args.force)

    # If personas/registry already exist, keep them unless --force
    # This repo ships with a default squad; users may customize after generation.

    print("✅ Generated/updated .agents from templates.")
    print("Next: python .agents/router/agent_router.py --task \"...\"")

if __name__ == "__main__":
    main()
