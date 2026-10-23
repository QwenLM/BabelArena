#!/usr/bin/env python3
"""Materialize a clean, travel-style per-language result tree for shopping.

The core shopping pipeline writes flat, timestamped folders:
    database_infered/database_<model>_<lang>_level<N>_<ts>_<runid>/case_*/{messages,cart,...}.json
    result_report/<ver>/database_<model>_<lang>_level<N>_<ts>_<runid>/{case_*_report,summary_report}.json
    result_report/<ver>/<model>_<lang>_statistics.json
`score_statistics.py` picks the LATEST-timestamp folder per (model, lang, level).
This script mirrors that selection and copies the *winning* folder's artifacts into
a per-language tree that parallels travelplanning/results:

    results/<ver>/<model>_<lang>/
        level<N>/
            trajectories/   case_<i>.json   (<- messages.json, the agent trajectory)
            carts/          case_<i>.json   (<- cart.json, the structured result/plan)
            reports/        case_<i>.json   (<- case_<i>_report.json, the score)
            summary_report.json             (per-level summary)
        statistics.json                     (language-level, all levels)
        MANIFEST.json                       (provenance: source folder + ts + valid per level)

The flat source folders are left untouched, so scoring / re-runs are unaffected.
Re-running this script rebuilds a language subtree from scratch (idempotent).
Seed inputs (products.jsonl / user_info.json / validation_cases.json) are NOT copied;
they live in the seed DBs, not in the model's results.
"""
import argparse
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from evaluation.score_statistics import parse_folder_name  # noqa: E402

CASE_RE = re.compile(r'^case_(\d+)$')
REPORT_RE = re.compile(r'^case_(\d+)_report\.json$')


def find_winners(infered_root, report_root, model_filter, lang_filter):
    """Return {(model, lang, level): (folder_name, timestamp)} keeping latest ts."""
    winners = {}
    if not os.path.isdir(infered_root):
        return winners
    for name in os.listdir(infered_root):
        if not os.path.isdir(os.path.join(infered_root, name)):
            continue
        parsed = parse_folder_name(name)
        if not parsed:
            continue
        model, level, ts, lang = parsed
        if model_filter and model != model_filter:
            continue
        if lang_filter and lang != lang_filter:
            continue
        # require the matching report folder to exist too
        if not os.path.isdir(os.path.join(report_root, name)):
            continue
        key = (model, lang, level)
        if key not in winners or ts > winners[key][1]:
            winners[key] = (name, ts)
    return winners


def copy_json(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def organize_level(infered_root, report_root, folder, out_level_dir):
    inf_dir = os.path.join(infered_root, folder)
    rep_dir = os.path.join(report_root, folder)
    n_traj = n_cart = n_rep = 0

    for entry in os.listdir(inf_dir):
        m = CASE_RE.match(entry)
        if not m:
            continue
        cid = m.group(1)
        case_dir = os.path.join(inf_dir, entry)
        msg = os.path.join(case_dir, 'messages.json')
        cart = os.path.join(case_dir, 'cart.json')
        if os.path.isfile(msg):
            copy_json(msg, os.path.join(out_level_dir, 'trajectories', f'case_{cid}.json'))
            n_traj += 1
        if os.path.isfile(cart):
            copy_json(cart, os.path.join(out_level_dir, 'carts', f'case_{cid}.json'))
            n_cart += 1

    if os.path.isdir(rep_dir):
        for entry in os.listdir(rep_dir):
            m = REPORT_RE.match(entry)
            if m:
                cid = m.group(1)
                copy_json(os.path.join(rep_dir, entry),
                          os.path.join(out_level_dir, 'reports', f'case_{cid}.json'))
                n_rep += 1
        summ = os.path.join(rep_dir, 'summary_report.json')
        if os.path.isfile(summ):
            copy_json(summ, os.path.join(out_level_dir, 'summary_report.json'))
    return n_traj, n_cart, n_rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--version', default=os.environ.get('BENCHMARK_VERSION', 'v8'))
    ap.add_argument('--model', default=None, help='only this model (e.g. qwen3.7-max-think)')
    ap.add_argument('--language', default=None, help='only this language short code (e.g. ar)')
    ap.add_argument('--base', default=HERE, help='shoppingplanning dir')
    args = ap.parse_args()

    infered_root = os.path.join(args.base, 'database_infered')
    report_root = os.path.join(args.base, 'result_report', args.version)
    out_root = os.path.join(args.base, 'results', args.version)

    winners = find_winners(infered_root, report_root, args.model, args.language)
    if not winners:
        print(f"⚠️  No winning folders found (model={args.model}, lang={args.language})")
        return 0

    # group by (model, lang)
    by_lang = {}
    for (model, lang, level), (folder, ts) in winners.items():
        by_lang.setdefault((model, lang), {})[level] = (folder, ts)

    for (model, lang), levels in sorted(by_lang.items()):
        out_lang_dir = os.path.join(out_root, f'{model}_{lang}')
        # rebuild from scratch for idempotency
        if os.path.isdir(out_lang_dir):
            shutil.rmtree(out_lang_dir)
        manifest = {'model': model, 'language': lang, 'version': args.version, 'levels': {}}
        for level in sorted(levels):
            folder, ts = levels[level]
            out_level_dir = os.path.join(out_lang_dir, f'level{level}')
            nt, nc, nr = organize_level(infered_root, report_root, folder, out_level_dir)
            # pull per-level validity out of the statistics file later; record source now
            manifest['levels'][f'level{level}'] = {
                'source_folder': folder, 'timestamp': ts,
                'trajectories': nt, 'carts': nc, 'reports': nr,
            }
            print(f"  {model}_{lang} level{level}: {nt} traj / {nc} carts / {nr} reports  <- {folder}")

        # language-level statistics.json
        stats_src = os.path.join(report_root, f'{model}_{lang}_statistics.json')
        if os.path.isfile(stats_src):
            shutil.copy2(stats_src, os.path.join(out_lang_dir, 'statistics.json'))
            # enrich manifest with per-level valid flag + score
            try:
                st = json.load(open(stats_src))
                for lk, lv in st.get('levels', {}).items():
                    if lk in manifest['levels']:
                        manifest['levels'][lk]['valid'] = lv.get('valid')
                        manifest['levels'][lk]['average_case_score'] = lv.get('average_case_score')
                        manifest['levels'][lk]['incomplete_rate'] = lv.get('incomplete_rate')
            except Exception:
                pass

        os.makedirs(out_lang_dir, exist_ok=True)
        with open(os.path.join(out_lang_dir, 'MANIFEST.json'), 'w') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"✅ {model}_{lang} -> {out_lang_dir}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
