#!/usr/bin/env python3
"""
Capstone test: runs everything criteria.md's capstone criteria need, three times.

    python capstone_eval.py              three runs (the default)
    python capstone_eval.py --runs 1     one run

Each run does three sessions against fresh `serve.py` processes, cache off:

  A  real key — 5 matching, 5 impossible, 5 empty requests   → criteria 1, 2, 3
  B  same server — matching queries until 10 come back ok     → criterion 5
  C  broken key — 5 rounds of matching / impossible / health  → criterion 4

Nothing in serve.py or the agent changes between runs. Every response, every
new log line and the server's own output are saved to results/capstone/runN/,
and the scores go to results/capstone/summary.md. Verdicts are left to me.
"""

import argparse
import json
import os
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
LOG_FILE = ROOT / "logs" / "runs.jsonl"
OUT = ROOT / "results" / "capstone"
PY = sys.executable

MATCHING = [
    "vintage graphic tee under $30",
    "denim jacket under $50",
    "platform sneakers",
    "y2k baby tee",
    "cargo pants under $40",
    "band tee",
    "mesh top",
    "vintage jeans under $50",
    "cardigan",
    "black boots",
]
IMPOSSIBLE = [
    "designer ballgown size XXS under $5",
    "wedding dress under $2",
    "ski boots size 15 under $3",
    "tuxedo size XXXL under $1",
    "ballet slippers size 2 under $4",
]
REQUIRED_FIELDS = ["timestamp", "status", "query", "seconds",
                   "model_calls", "cache_hits", "prompt_tokens", "output_tokens"]


# ── talking to the server ─────────────────────────────────────────────────────

def request(port, method, path, body=None):
    """One HTTP call. Returns (status code, parsed JSON or None, content type)."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"http://localhost:{port}{path}", data=data, method=method,
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            code, ctype, raw = r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        code, ctype, raw = e.code, e.headers.get("Content-Type", ""), e.read()
    try:
        parsed = json.loads(raw)
    except ValueError:
        parsed = None
    return code, parsed, ctype


def ask(port, query):
    body = {} if query is None else {"query": query}
    code, data, ctype = request(port, "POST", "/ask", body)
    return {"query": query, "http": code, "json": "json" in ctype,
            "error": (data or {}).get("error"),
            "fit_card": (data or {}).get("fit_card")}


def start_server(port, run_dir, name, extra_env):
    env = {**os.environ, "PORT": str(port), "AI201_CACHE": "0", **extra_env}
    out = open(run_dir / f"server_{name}.out", "w")
    proc = subprocess.Popen([PY, "serve.py"], cwd=ROOT, env=env,
                            stdout=out, stderr=subprocess.STDOUT)
    for _ in range(60):
        try:
            if request(port, "GET", "/health")[0] == 200:
                return proc
        except OSError:
            pass
        time.sleep(0.5)
    proc.kill()
    raise RuntimeError(f"server on port {port} never came up")


def stop_server(proc):
    proc.terminate()
    proc.wait(timeout=10)


# ── the log ───────────────────────────────────────────────────────────────────

def log_lines():
    if not LOG_FILE.exists():
        return []
    return [json.loads(l) for l in LOG_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]


def expected_status(resp):
    """What criterion 2 says the status should be, from the response alone."""
    if resp["http"] == 400:
        return "rejected"
    if resp["error"] is None and resp["fit_card"]:
        return "ok"
    if (resp["error"] or "").startswith("No listings matched"):
        return "no_match"
    return "model_unavailable"


# ── sessions ──────────────────────────────────────────────────────────────────

def session_a(port):
    """15 requests: 5 matching, 5 impossible, 5 empty."""
    before = len(log_lines())
    responses = [ask(port, q) for q in MATCHING[:5]]
    responses += [ask(port, q) for q in IMPOSSIBLE]
    responses += [ask(port, None) for _ in range(5)]
    return responses, log_lines()[before:]


def session_b(port):
    """Matching queries until 10 come back ok (at most 25 tries)."""
    before = len(log_lines())
    responses, ok = [], 0
    for i in range(25):
        r = ask(port, MATCHING[i % len(MATCHING)])
        responses.append(r)
        ok += expected_status(r) == "ok"
        if ok == 10:
            break
    return responses, log_lines()[before:]


def session_c(port):
    """Broken key: 5 rounds of matching query, impossible query, /health."""
    before = len(log_lines())
    rounds = []
    for i in range(5):
        m = ask(port, MATCHING[i])
        n = ask(port, IMPOSSIBLE[i])
        h_code, h_json, _ = request(port, "GET", "/health")
        rounds.append({"matching": m, "impossible": n,
                       "health": {"http": h_code, "body": h_json}})
    return rounds, log_lines()[before:]


# ── scoring, one criterion at a time ─────────────────────────────────────────

def score_1(responses, lines):
    """Exactly one line per request, in order, with every field."""
    if len(lines) != len(responses):
        return 0, f"{len(lines)} lines for {len(responses)} requests"
    passed = 0
    for resp, line in zip(responses, lines):
        if resp["query"] is None:
            passed += line.get("status") == "rejected"
        else:
            passed += line.get("query") == resp["query"] and all(f in line for f in REQUIRED_FIELDS)
    return passed, ""


def score_2(responses, lines):
    if len(lines) != len(responses):
        return 0, "line count mismatch, can't pair lines with requests"
    passed = sum(line.get("status") == expected_status(resp)
                 for resp, line in zip(responses, lines))
    return passed, ""


def score_3(lines):
    checked = passed = 0
    for line in lines:
        if line.get("status") == "ok":
            checked += 1
            passed += (line.get("model_calls") == 2 and line.get("cache_hits") == 0
                       and line.get("prompt_tokens", 0) > 0 and line.get("output_tokens", 0) > 0)
        elif line.get("status") == "no_match":
            checked += 1
            passed += all(line.get(f) == 0 for f in
                          ["model_calls", "cache_hits", "prompt_tokens", "output_tokens"])
    return passed, checked


def score_4(rounds, lines):
    """A round passes if the failure is JSON + logged, and the server still works."""
    unavailable = [l for l in lines if l.get("status") == "model_unavailable"]
    passed = 0
    for i, r in enumerate(rounds):
        m = r["matching"]
        logged = (i < len(unavailable)
                  and unavailable[i].get("query") == m["query"]
                  and m["error"] and unavailable[i].get("output") == m["error"])
        ok = (m["json"] and m["http"] != 500 and m["error"] and logged
              and expected_status(r["impossible"]) == "no_match"
              and r["health"]["http"] == 200
              and (r["health"]["body"] or {}).get("status") == "ok")
        passed += bool(ok)
    return passed


def score_5(lines):
    secs = [l["seconds"] for l in lines if l.get("status") == "ok"][:10]
    if not secs:
        return None, 0, secs
    return statistics.median(secs), sum(s < 30 for s in secs), secs


# ── one full run ──────────────────────────────────────────────────────────────

def one_run(n):
    run_dir = OUT / f"run{n}"
    run_dir.mkdir(parents=True, exist_ok=True)
    print(f"\n=== Run {n} ===", flush=True)

    proc = start_server(5061, run_dir, "real_key", {})
    try:
        print("  session A (15 mixed requests)…", flush=True)
        a_resp, a_lines = session_a(5061)
        print("  session B (until 10 ok)…", flush=True)
        b_resp, b_lines = session_b(5061)
    finally:
        stop_server(proc)

    proc = start_server(5062, run_dir, "broken_key", {"GEMINI_API_KEY": "not-a-real-key"})
    try:
        print("  session C (broken key)…", flush=True)
        c_rounds, c_lines = session_c(5062)
    finally:
        stop_server(proc)

    s1, s1_note = score_1(a_resp, a_lines)
    s2, s2_note = score_2(a_resp, a_lines)
    s3, s3_of = score_3(a_lines)
    s4 = score_4(c_rounds, c_lines)
    median, under30, secs = score_5(b_lines)

    scores = {
        "1": {"passed": s1, "of": 15, "note": s1_note},
        "2": {"passed": s2, "of": 15, "note": s2_note},
        "3": {"passed": s3, "of": s3_of},
        "4": {"passed": s4, "of": 5},
        "5": {"median_seconds": median, "under_30": under30, "ok_runs": len(secs),
              "seconds": secs,
              "model_unavailable_in_b": sum(l.get("status") == "model_unavailable" for l in b_lines)},
    }
    for name, obj in [("session_a_responses", a_resp), ("session_b_responses", b_resp),
                      ("session_c_rounds", c_rounds), ("scores", scores)]:
        (run_dir / f"{name}.json").write_text(json.dumps(obj, indent=2, ensure_ascii=False))
    for name, lines in [("a", a_lines), ("b", b_lines), ("c", c_lines)]:
        (run_dir / f"session_{name}_log.jsonl").write_text(
            "".join(json.dumps(l, ensure_ascii=False) + "\n" for l in lines))
    print(f"  scores: {json.dumps(scores)}", flush=True)
    return scores


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()

    all_scores = [one_run(n) for n in range(1, args.runs + 1)]

    def cell(s, k):
        if k == "5":
            m = s["5"]["median_seconds"]
            return f"median {m:.2f}s, {s['5']['under_30']}/{s['5']['ok_runs']} < 30s" if m else "no ok runs"
        note = f" ({s[k]['note']})" if s[k].get("note") else ""
        return f"{s[k]['passed']}/{s[k]['of']}{note}"

    rows = [
        ("1. Every request writes exactly one log line", "15 of 15"),
        ("2. Logged status matches the response", "15 of 15"),
        ("3. Cost fields count the right things", "100% of lines"),
        ("4. Model unreachable: logged, server keeps going", "5 of 5"),
        ("5. Real run under 20 s", "median < 20s, 8 of 10 < 30s"),
    ]
    head = "| Criterion | Target | " + " | ".join(f"Run {i}" for i in range(1, args.runs + 1)) + " | Verdict |"
    table = [head, "|" + "---|" * (args.runs + 3)]
    for i, (name, target) in enumerate(rows, start=1):
        table.append(f"| {name} | {target} | "
                     + " | ".join(cell(s, str(i)) for s in all_scores) + " |  |")
    (OUT / "summary.md").write_text("\n".join(table) + "\n")
    print("\n" + "\n".join(table))


if __name__ == "__main__":
    main()
