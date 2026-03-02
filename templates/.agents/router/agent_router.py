#!/usr/bin/env python3
import os, sys, json, argparse, re
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

BASE = ".agents"
DEFAULT_RUNTIME_DIR = os.path.join(BASE, "runtime")
NOW_ISO = datetime.now(timezone.utc).isoformat() + "Z"

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: str, obj: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str) -> List[str]:
    text = normalize(text)
    return re.findall(r"[a-z0-9]+(?:/[a-z0-9]+)?", text)

def read_task(task_arg: str | None) -> str:
    if task_arg and task_arg.strip():
        return task_arg.strip()
    if not sys.stdin.isatty():
        return sys.stdin.read().strip()
    raise SystemExit("❌ Informe --task ou passe texto via stdin.")

def resolve_runtime_dir(cli_runtime: str | None) -> str:
    return cli_runtime or os.getenv("AGENTS_RUNTIME_DIR") or DEFAULT_RUNTIME_DIR

def resolve_paths(runtime_dir: str) -> Dict[str, str]:
    return {
        "registry": os.path.join(BASE, "agents", "registry.json"),
        "confidence_log": os.path.join(BASE, "swarm", "confidence_log.json"),
        "products": os.path.join(runtime_dir, "products.json"),
        "hardware": os.path.join(runtime_dir, "hardware_profile.json"),
        "products_example": os.path.join(runtime_dir, "products.example.json"),
        "hardware_example": os.path.join(runtime_dir, "hardware_profile.example.json"),
    }

RISK_PROFILE_BOOST = {
    "high_security": {"security/appsec-engineer.md": 22, "testing/qa-strategist.md": 8},
    "privacy_sensitive": {"security/appsec-engineer.md": 18, "testing/qa-strategist.md": 6},
    "compliance_sensitive": {"security/appsec-engineer.md": 24, "testing/qa-strategist.md": 10},
    "medium_security": {"security/appsec-engineer.md": 8},
}

PHASE_KEYWORDS = {
    "plan": {"mvp","backlog","prioritize","sprint","scope","roi"},
    "design": {"architecture","arquitetura","adr","c4","schema","boundary"},
    "build": {"endpoint","api","component","ui","rag","docker","implement"},
    "test": {"test","qa","contract","load","benchmark","latency","perf"},
    "release": {"deploy","release","ci/cd","pipeline","monitoring","observability"},
}

def detect_phase(tokens: List[str]) -> str:
    s = set(tokens)
    scores = {k: len(v.intersection(s)) for k, v in PHASE_KEYWORDS.items()}
    best = max(scores.items(), key=lambda x: x[1])
    return best[0] if best[1] > 0 else "build"

def compute_node_capacity(node: Dict[str, Any]) -> Dict[str, float]:
    gpu_count = float(node.get("gpu_count", 0) or 0)
    vram = float(node.get("gpu_vram_gb", 0) or 0)
    ram = float(node.get("ram_gb", 0) or 0)
    cpu = float(node.get("cpu_cores", 0) or 0)
    return {"gpu_capacity": gpu_count * vram, "ram": ram, "cpu": cpu}

def choose_preferred_node(tokens: List[str], hardware: Dict[str, Any]) -> str:
    nodes = hardware.get("nodes", {})
    if not nodes:
        return "unknown"
    heavy = {"rag","embedding","inference","benchmark","latency","train","vision","cv"}
    is_heavy = any(t in heavy for t in tokens)
    scored = []
    for node_name, node_meta in nodes.items():
        role = node_meta.get("role", "unknown")
        cap = compute_node_capacity(node_meta)
        score = 0.0
        if is_heavy:
            score += (50.0 if role == "production" else 0.0)
            score += cap["gpu_capacity"] * 2.0
            score += cap["ram"] * 0.2
        else:
            score += (30.0 if role == "development" else 0.0)
            score += cap["cpu"] * 0.2
            score += cap["ram"] * 0.1
        scored.append((node_name, score))
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0]

def score_agents(task: str, registry: Dict[str, Any], product_meta: Dict[str, Any] | None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    tokens = tokenize(task)
    s = set(tokens)
    phase = detect_phase(tokens)

    agents = registry["agents"]
    scores = {k: 0.0 for k in agents}
    reasons = {k: [] for k in agents}

    for a, meta in agents.items():
        tags = set(meta.get("tags", []))
        overlap = len(tags.intersection(s))
        if overlap:
            scores[a] += overlap * 6.0
            reasons[a].append(f"tag_overlap:{overlap}")

    phase_bias = {
        "plan": {"product/product-owner.md": 12, "project-management/scrum-master.md": 8},
        "design": {"engineering/staff-architect.md": 12, "engineering/tech-lead.md": 6},
        "build": {"engineering/backend-engineer.md": 6, "engineering/frontend-engineer.md": 6, "engineering/ai-engineer.md": 6, "engineering/data-engineer.md": 4},
        "test": {"testing/qa-strategist.md": 12, "testing/api-tester.md": 8, "testing/performance-benchmarker.md": 8, "security/appsec-engineer.md": 6},
        "release": {"engineering/devops-sre.md": 12, "testing/qa-strategist.md": 6, "security/appsec-engineer.md": 4},
    }
    for a, bonus in phase_bias.get(phase, {}).items():
        if a in scores:
            scores[a] += bonus
            reasons[a].append(f"phase_bias:{phase}")

    if product_meta:
        risk = product_meta.get("risk_profile")
        boosts = RISK_PROFILE_BOOST.get(risk, {})
        for a, bonus in boosts.items():
            if a in scores:
                scores[a] += float(bonus)
                reasons[a].append(f"risk_profile:{risk}")

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top = ranked[0][1] if ranked else 1.0

    results = []
    for a, sc in ranked:
        conf = 0.0 if top <= 0 else min(1.0, sc / top)
        results.append({
            "agent": a,
            "title": agents[a].get("title"),
            "score": round(sc, 2),
            "confidence": round(conf, 3),
            "reasons": reasons[a][:8],
            "commands": agents[a].get("commands", [])[:6],
        })
    return results, {"phase": phase, "tokens": tokens[:80]}

def append_confidence_log(path: str, entry: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        data = load_json(path)
    else:
        data = {"generated": NOW_ISO, "runs": []}
    data.setdefault("runs", []).append(entry)
    save_json(path, data)

def main():
    p = argparse.ArgumentParser(description="Inteligens Router (v6) — hybrid")
    p.add_argument("--task", type=str, default=None)
    p.add_argument("--product", type=str, default=None)
    p.add_argument("--top", type=int, default=8)
    p.add_argument("--format", choices=["md","json"], default="md")
    p.add_argument("--runtime-dir", type=str, default=None)
    args = p.parse_args()

    task = read_task(args.task)
    runtime_dir = resolve_runtime_dir(args.runtime_dir)
    paths = resolve_paths(runtime_dir)

    if not os.path.exists(paths["registry"]):
        raise SystemExit(f"❌ Missing registry: {paths['registry']} (run generator first)")

    registry = load_json(paths["registry"])

    def load_with_fallback(primary: str, fallback: str) -> Dict[str, Any]:
        if os.path.exists(primary):
            return load_json(primary)
        if os.path.exists(fallback):
            return load_json(fallback)
        return {}

    products = load_with_fallback(paths["products"], paths["products_example"])
    hardware = load_with_fallback(paths["hardware"], paths["hardware_example"])

    product_meta = None
    if args.product:
        product_meta = products.get("products", {}).get(args.product)

    results, meta = score_agents(task, registry, product_meta)
    preferred_node = choose_preferred_node(tokenize(task), hardware) if hardware else "unknown"

    append_confidence_log(paths["confidence_log"], {
        "timestamp": NOW_ISO,
        "router_version": "6.0.0",
        "phase": meta["phase"],
        "product": args.product,
        "preferred_node": preferred_node,
        "top_agents": [r["agent"] for r in results[: max(1, args.top)]],
    })

    out = {
        "generated": NOW_ISO,
        "router_version": "6.0.0",
        "task": task,
        "product": args.product,
        "phase": meta["phase"],
        "preferred_node": preferred_node,
        "top": results[: max(1, args.top)],
    }

    if args.format == "json":
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    lines = []
    lines.append("# 🧭 Router Result\n")
    lines.append(f"**Product:** `{args.product or 'N/A'}`")
    lines.append(f"**Phase:** `{meta['phase']}`")
    lines.append(f"**Preferred node:** `{preferred_node}`\n")
    lines.append("## 🧩 Top Agents")
    for r in out["top"]:
        lines.append(f"- **`{r['agent']}`** | score={r['score']} | conf={r['confidence']}")
        if r.get("reasons"):
            lines.append(f"  - reasons: {', '.join(r['reasons'])}")
        if r.get("commands"):
            lines.append(f"  - commands: {', '.join(r['commands'])}")
    lines.append("\n✅ Logged run to .agents/swarm/confidence_log.json")
    print("\n".join(lines))

if __name__ == "__main__":
    main()
