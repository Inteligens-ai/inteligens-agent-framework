import os
import sys
import json
import argparse
import re
from datetime import datetime, timezone
from typing import Dict, Any, List, Tuple

BASE = ".agents"
DEFAULT_RUNTIME_DIR = os.path.join(BASE, "runtime")

NOW_ISO = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


# =========================
# IO helpers
# =========================
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
    raise SystemExit("❌ Informe --task ou use stdin.")

def safe_getenv(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    return v if v else default


# =========================
# Paths (runtime overlay)
# =========================
def resolve_runtime_dir(cli_runtime: str | None, public_mode: bool) -> str:
    # priority: CLI > ENV > default
    runtime_dir = cli_runtime or safe_getenv("AGENTS_RUNTIME_DIR", DEFAULT_RUNTIME_DIR)

    if public_mode:
        # In public mode we strongly prefer example configs.
        return runtime_dir

    return runtime_dir


def resolve_paths(runtime_dir: str) -> Dict[str, str]:
    registry_path = os.path.join(BASE, "agents", "registry.json")
    routing_rules_path = os.path.join(BASE, "agents", "routing_rules.md")
    confidence_log_path = os.path.join(BASE, "swarm", "confidence_log.json")

    products_path = os.path.join(runtime_dir, "products.json")
    hardware_path = os.path.join(runtime_dir, "hardware_profile.json")

    # examples fallback
    products_example = os.path.join(runtime_dir, "products.example.json")
    hardware_example = os.path.join(runtime_dir, "hardware_profile.example.json")

    return {
        "registry": registry_path,
        "routing_rules": routing_rules_path,
        "confidence_log": confidence_log_path,
        "products": products_path,
        "hardware": hardware_path,
        "products_example": products_example,
        "hardware_example": hardware_example,
    }


# =========================
# Risk profile weights
# =========================
RISK_PROFILE_BOOST = {
    "high_security": {"security/appsec-engineer.md": 22, "testing/qa-strategist.md": 8},
    "privacy_sensitive": {"security/appsec-engineer.md": 18, "testing/qa-strategist.md": 6},
    "compliance_sensitive": {"security/appsec-engineer.md": 24, "testing/qa-strategist.md": 10},
    "medium_security": {"security/appsec-engineer.md": 8},
}

# =========================
# Phase detection
# =========================
PHASE_KEYWORDS = {
    "plan": {"mvp", "backlog", "prioritize", "sprint", "scope", "roi"},
    "design": {"architecture", "arquitetura", "adr", "c4", "boundary", "schema"},
    "build": {"endpoint", "api", "component", "ui", "rag", "docker"},
    "test": {"test", "quality", "contract", "load", "benchmark", "latency"},
    "release": {"deploy", "release", "ci/cd", "pipeline", "monitoring", "observability"},
}

def detect_phase(tokens: List[str]) -> str:
    s = set(tokens)
    scores = {k: len(v.intersection(s)) for k, v in PHASE_KEYWORDS.items()}
    best = max(scores.items(), key=lambda x: x[1])
    return best[0] if best[1] > 0 else "build"


# =========================
# Capacity-aware node selection (V6)
# =========================
def compute_node_capacity(node: Dict[str, Any]) -> Dict[str, float]:
    gpu_count = float(node.get("gpu_count", 0) or 0)
    vram = float(node.get("gpu_vram_gb", 0) or 0)
    ram = float(node.get("ram_gb", 0) or 0)
    cpu = float(node.get("cpu_cores", 0) or 0)

    gpu_capacity = gpu_count * vram  # simple proxy
    return {
        "gpu_capacity": gpu_capacity,
        "ram": ram,
        "cpu": cpu,
    }

def choose_preferred_node(tokens: List[str], hardware: Dict[str, Any]) -> str:
    nodes = hardware.get("nodes", {})
    if not nodes:
        return "unknown"

    heavy = {"rag", "embedding", "inference", "benchmark", "latency", "train", "vision", "cv"}
    is_heavy = any(t in heavy for t in tokens)

    # rank nodes by role + capacity
    scored = []
    for node_name, node_meta in nodes.items():
        role = node_meta.get("role", "unknown")
        cap = compute_node_capacity(node_meta)

        score = 0.0
        if is_heavy:
            # prefer production + GPU capacity
            score += (50.0 if role == "production" else 0.0)
            score += cap["gpu_capacity"] * 2.0
            score += cap["ram"] * 0.2
        else:
            # prefer development + responsiveness
            score += (30.0 if role == "development" else 0.0)
            score += cap["cpu"] * 0.2
            score += cap["ram"] * 0.1

        scored.append((node_name, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[0][0]


# =========================
# Scoring agents (Mode B+)
# =========================
def score_agents(task: str, registry: Dict[str, Any], product_meta: Dict[str, Any] | None) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    tokens = tokenize(task)
    s = set(tokens)
    phase = detect_phase(tokens)

    agents = registry["agents"]
    scores = {k: 0.0 for k in agents}
    reasons = {k: [] for k in agents}

    # tag overlap
    for a, meta in agents.items():
        tags = set(meta.get("tags", []))
        overlap = len(tags.intersection(s))
        if overlap:
            scores[a] += overlap * 6.0
            reasons[a].append(f"tag_overlap:{overlap}")

    # phase bias
    phase_bias = {
        "plan": {"product/product-owner.md": 12, "project-management/scrum-master.md": 8},
        "design": {"engineering/staff-architect.md": 12, "engineering/tech-lead.md": 6},
        "build": {"engineering/backend-engineer.md": 6, "engineering/frontend-engineer.md": 6, "engineering/ai-engineer.md": 6},
        "test": {"testing/qa-strategist.md": 12, "testing/api-tester.md": 8, "testing/performance-benchmarker.md": 8},
        "release": {"engineering/devops-sre.md": 12, "testing/qa-strategist.md": 6, "security/appsec-engineer.md": 4},
    }
    for a, bonus in phase_bias.get(phase, {}).items():
        if a in scores:
            scores[a] += bonus
            reasons[a].append(f"phase_bias:{phase}")

    # product risk boost
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


# =========================
# Redaction (privacy safe publishing)
# =========================
def redact_runtime(runtime: Dict[str, Any]) -> Dict[str, Any]:
    if not runtime:
        return runtime
    rt = json.loads(json.dumps(runtime))  # deep copy

    # redact node names and any detailed fields
    nodes = rt.get("nodes")
    if isinstance(nodes, dict):
        redacted_nodes = {}
        for i, (_name, meta) in enumerate(nodes.items(), 1):
            alias = f"node-{i}"
            # keep only coarse data
            redacted_nodes[alias] = {
                "role": meta.get("role"),
                "gpu_available": meta.get("gpu_available"),
                "gpu_count": meta.get("gpu_count"),
                "gpu_vram_gb": meta.get("gpu_vram_gb"),
                "gpu_class": meta.get("gpu_class"),
                "cpu_cores": meta.get("cpu_cores"),
                "ram_gb": meta.get("ram_gb"),
            }
        rt["nodes"] = redacted_nodes

    return rt


# =========================
# Confidence log
# =========================
def append_confidence_log(path: str, entry: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        data = load_json(path)
    else:
        data = {"runs": []}
    data.setdefault("runs", []).append(entry)
    save_json(path, data)


# =========================
# Main
# =========================
def main():
    p = argparse.ArgumentParser(description="Inteligens Router v6 (capacity-aware, runtime overlay, redaction)")
    p.add_argument("--task", type=str, default=None, help="Task text; if omitted reads stdin.")
    p.add_argument("--product", type=str, default=None, help="Product key (from runtime/products.json)")
    p.add_argument("--top", type=int, default=6, help="Top N agents to print")
    p.add_argument("--format", choices=["md", "json"], default="md")
    p.add_argument("--runtime-dir", type=str, default=None, help="Override runtime directory (AGENTS_RUNTIME_DIR)")
    p.add_argument("--public", action="store_true", help="Public mode: prefer example configs; redact runtime output")
    p.add_argument("--no-redact", action="store_true", help="Disable redaction (private usage)")
    args = p.parse_args()

    task = read_task(args.task)

    runtime_dir = resolve_runtime_dir(args.runtime_dir, args.public)
    paths = resolve_paths(runtime_dir)

    if not os.path.exists(paths["registry"]):
        raise SystemExit(f"❌ Missing registry: {paths['registry']} (run generator first)")

    registry = load_json(paths["registry"])

    # load runtime (private or example)
    products = None
    hardware = None

    def load_with_fallback(primary: str, fallback: str) -> Dict[str, Any]:
        if os.path.exists(primary):
            return load_json(primary)
        if os.path.exists(fallback):
            return load_json(fallback)
        raise SystemExit(f"❌ Missing runtime config: {primary} and fallback {fallback}")

    products = load_with_fallback(paths["products"], paths["products_example"])
    hardware = load_with_fallback(paths["hardware"], paths["hardware_example"])

    product_meta = None
    if args.product:
        product_meta = products.get("products", {}).get(args.product)

    results, meta = score_agents(task, registry, product_meta)
    tokens = tokenize(task)

    preferred_node = choose_preferred_node(tokens, hardware)

    # redact if public (default)
    redact_on = args.public and (not args.no_redact)
    hardware_out = redact_runtime(hardware) if redact_on else hardware
    product_out = None
    if product_meta:
        # safe: product itself may be sensitive; in public mode, show only risk_profile + stack summary
        if args.public and not args.no_redact:
            product_out = {
                "risk_profile": product_meta.get("risk_profile"),
                "primary_stack": product_meta.get("primary_stack", [])[:6],
            }
        else:
            product_out = product_meta

    # confidence log entry (safe)
    log_entry = {
        "timestamp": NOW_ISO,
        "mode": "v6",
        "phase": meta["phase"],
        "product": args.product if not args.public else ("public" if args.product else None),
        "preferred_node": ("redacted" if args.public else preferred_node),
        "top_agents": [r["agent"] for r in results[: max(1, args.top)]],
    }
    append_confidence_log(paths["confidence_log"], log_entry)

    out = {
        "generated": NOW_ISO,
        "router_version": "6.0.0",
        "task": task,
        "product": args.product,
        "phase": meta["phase"],
        "preferred_node": ("redacted" if args.public else preferred_node),
        "top": results[: max(1, args.top)],
        "runtime": {
            "runtime_dir": runtime_dir,
            "hardware": hardware_out,
            "product": product_out,
        },
    }

    if args.format == "json":
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # markdown
    lines = []
    lines.append("# 🧭 Router v6 Result\n")
    lines.append(f"**Product:** `{args.product or 'N/A'}`")
    lines.append(f"**Phase:** `{meta['phase']}`")
    lines.append(f"**Preferred node:** `{out['preferred_node']}`")
    lines.append("")
    lines.append("## 🧩 Top Agents")
    for r in out["top"]:
        lines.append(f"- **`{r['agent']}`** | score={r['score']} | conf={r['confidence']}")
        if r.get("reasons"):
            lines.append(f"  - reasons: {', '.join(r['reasons'])}")
        if r.get("commands"):
            lines.append(f"  - commands: {', '.join(r['commands'])}")
    lines.append("")
    lines.append("✅ Logged run to swarm/confidence_log.json")
    print("\n".join(lines))


if __name__ == "__main__":
    main()