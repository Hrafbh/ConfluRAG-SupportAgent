import os
import json
import csv
import re
import argparse
from datetime import datetime

from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "data/index/chroma"
COLLECTION_NAME = "routepilot_kb"
DEFAULT_EVAL_SET = "eval/eval_set.json"
DEFAULT_REPORT_MD = "reports/rag_eval_report.md"
DEFAULT_DETAILS_CSV = "reports/rag_eval_details.csv"


def normalize(s):
    s = (s or "").lower()
    s = re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿñæœ\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_routing(path="config/intent_routing.json"):
    if not os.path.exists(path):
        return {}
    return load_json(path)


def detect_intent(question, routing):
    q = normalize(question)
    best_intent = None
    best_score = 0

    for intent_name, cfg in routing.items():
        kws = cfg.get("keywords", [])
        score = 0
        for kw in kws:
            if normalize(kw) in q:
                score += 1
        if score > best_score:
            best_score = score
            best_intent = intent_name

    category = routing.get(best_intent, {}).get("category") if best_intent else None
    return best_intent, best_score, category


def keyword_bonus(question, meta, doc):
    q = normalize(question)
    title = normalize(meta.get("title", ""))
    tags = normalize(meta.get("tags", ""))
    category = normalize(meta.get("category", ""))

    bonus = 0

    # Overlap titre
    q_words = set(q.split())
    t_words = set(title.split())
    bonus += min(4, len(q_words.intersection(t_words)))

    # Bonus tags
    for w in ["pdf", "csv", "export", "mfa", "login", "vpn", "proxy", "incident", "runbook"]:
        if w in q and w in tags:
            bonus += 1

    # Bonus si doc contient le mot-clé
    for w in ["export", "pdf", "csv", "mfa", "vpn", "incident", "runbook"]:
        if w in q and w in normalize(doc):
            bonus += 1

    # Bonus category (léger)
    if "incident" in q and "incidents" in category:
        bonus += 1

    return bonus


def rerank(question, docs, metas, dists):
    scored = []
    for i in range(len(docs)):
        dist = dists[i] if dists and i < len(dists) else 0.0
        score = (-dist) + keyword_bonus(question, metas[i], docs[i])
        scored.append((score, i))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [i for _, i in scored]


def dedup_by_page_id(indices, metas):
    seen = set()
    out = []
    for i in indices:
        pid = metas[i].get("page_id", "")
        if pid in seen:
            continue
        seen.add(pid)
        out.append(i)
    return out


def hit_at_k(ranked_kb_ids, expected, k):
    expected_set = set(expected)
    return any(x in expected_set for x in ranked_kb_ids[:k])


def mrr(ranked_kb_ids, expected):
    expected_set = set(expected)
    for i, kb in enumerate(ranked_kb_ids, start=1):
        if kb in expected_set:
            return 1.0 / i
    return 0.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval_set", default=DEFAULT_EVAL_SET)
    parser.add_argument("--k", type=int, default=10)
    parser.add_argument("--use_routing", action="store_true")
    args = parser.parse_args()

    load_dotenv()
    os.environ["ANONYMIZED_TELEMETRY"] = "False"

    if not os.path.exists(CHROMA_DIR):
        print(" Index introuvable. Lancez d'abord: python scripts/rag_build_index.py")
        return
    if not os.path.exists(args.eval_set):
        print(f" Eval set introuvable: {args.eval_set}")
        return

    tests = load_json(args.eval_set)
    routing = load_routing() if args.use_routing else {}

    model_name = os.getenv("RAG_EMBED_MODEL", "all-MiniLM-L6-v2")
    model = SentenceTransformer(model_name)

    client = chromadb.PersistentClient(path=CHROMA_DIR)
    collection = client.get_collection(name=COLLECTION_NAME)

    os.makedirs("reports", exist_ok=True)

    details_rows = []
    hits_1 = hits_3 = hits_5 = 0
    mrr_sum = 0.0

    for t in tests:
        tid = t.get("id", "")
        query = t.get("query", "")
        expected = t.get("expected_kb_ids", [])

        intent, intent_score, category = (None, 0, None)
        if args.use_routing and routing:
            intent, intent_score, category = detect_intent(query, routing)

        q_vec = model.encode([query])[0].tolist()

        # Query Chroma (avec filtre category si possible)
        try:
            if category:
                res = collection.query(
                    query_embeddings=[q_vec],
                    n_results=args.k,
                    where={"category": category},
                    include=["documents", "metadatas", "distances"],
                )
            else:
                res = collection.query(
                    query_embeddings=[q_vec],
                    n_results=args.k,
                    include=["documents", "metadatas", "distances"],
                )
        except Exception:
            # fallback sans filtre
            res = collection.query(
                query_embeddings=[q_vec],
                n_results=args.k,
                include=["documents", "metadatas", "distances"],
            )

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        dists = res.get("distances", [[]])[0]

        if not docs:
            ranked_kb_ids = []
        else:
            order = rerank(query, docs, metas, dists)
            order = dedup_by_page_id(order, metas)
            ranked_kb_ids = [metas[i].get("kb_id", "") for i in order]

        # metrics
        h1 = hit_at_k(ranked_kb_ids, expected, 1)
        h3 = hit_at_k(ranked_kb_ids, expected, 3)
        h5 = hit_at_k(ranked_kb_ids, expected, 5)
        rr = mrr(ranked_kb_ids, expected)

        hits_1 += 1 if h1 else 0
        hits_3 += 1 if h3 else 0
        hits_5 += 1 if h5 else 0
        mrr_sum += rr

        top5 = ranked_kb_ids[:5]
        details_rows.append({
            "test_id": tid,
            "query": query,
            "expected": "|".join(expected),
            "intent": intent or "",
            "intent_score": intent_score,
            "category_filter": category or "",
            "top1": ranked_kb_ids[0] if ranked_kb_ids else "",
            "top3": "|".join(ranked_kb_ids[:3]),
            "top5": "|".join(top5),
            "hit@1": int(h1),
            "hit@3": int(h3),
            "hit@5": int(h5),
            "mrr": round(rr, 4),
        })

    n = max(1, len(tests))
    acc1 = hits_1 / n
    acc3 = hits_3 / n
    acc5 = hits_5 / n
    mrr_avg = mrr_sum / n

    # Write CSV details
    with open(DEFAULT_DETAILS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(details_rows[0].keys()))
        writer.writeheader()
        writer.writerows(details_rows)

    # Write Markdown report
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append(f"# RAG Evaluation Report\n\n")
    lines.append(f"- Date: {ts}\n")
    lines.append(f"- Model: `{model_name}`\n")
    lines.append(f"- Tests: **{n}**\n")
    lines.append(f"- Routing: **{'ON' if args.use_routing else 'OFF'}**\n\n")
    lines.append("## Metrics\n\n")
    lines.append(f"- Hit@1: **{acc1:.2%}**\n")
    lines.append(f"- Hit@3: **{acc3:.2%}**\n")
    lines.append(f"- Hit@5: **{acc5:.2%}**\n")
    lines.append(f"- MRR: **{mrr_avg:.4f}**\n\n")
    lines.append("## Outputs\n\n")
    lines.append(f"- Details CSV: `{DEFAULT_DETAILS_CSV}`\n")
    lines.append(f"- This report: `{DEFAULT_REPORT_MD}`\n\n")
    lines.append("## Notes\n\n")
    lines.append("- Le scoring combine distance vectorielle + bonus mots-clés (titre/tags/doc).\n")
    lines.append("- Déduplication par `page_id` pour éviter les doublons dans le top-k.\n")

    with open(DEFAULT_REPORT_MD, "w", encoding="utf-8") as f:
        f.write("".join(lines))

    print("\n Evaluation terminée")
    print(f"Hit@1={acc1:.2%} | Hit@3={acc3:.2%} | Hit@5={acc5:.2%} | MRR={mrr_avg:.4f}")
    print(f"Report:  {DEFAULT_REPORT_MD}")
    print(f"Details: {DEFAULT_DETAILS_CSV}")


if __name__ == "__main__":
    main()
