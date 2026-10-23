#!/bin/bash

# Shopping Benchmark Runner. Optional external runtime variables:
#   DEEPPLANNING_RUN_DIR=/absolute/per-run/directory
#   DEEPPLANNING_TASK_IDS=1,7
#   BENCHMARK_TASK_SUBSET=standard|full|<name>   (default: standard; ignored
#       when DEEPPLANNING_TASK_IDS is set — explicit IDs win)

set -e
export PYTHONDONTWRITEBYTECODE=1

cd "$(dirname "$0")"
BASE_DIR=$(pwd -P)

TEST_LEVELS="${BENCHMARK_LEVELS:-${SHOPPING_LEVELS:-1 2 3}}"
WORKERS="${BENCHMARK_WORKERS:-${SHOPPING_WORKERS:-50}}"
MAX_LLM_CALLS="${BENCHMARK_MAX_LLM_CALLS:-${SHOPPING_MAX_LLM_CALLS:-400}}"
SHOPPING_AGENT_MODEL="${BENCHMARK_MODEL:-${SHOPPING_AGENT_MODEL:-qwen-plus}}"
SHOPPING_LANGUAGE="${DEEPPLANNING_LANGUAGE:-${BENCHMARK_LANGUAGE:-english}}"
export BENCHMARK_VERSION="${BENCHMARK_VERSION:-v8}"

TASK_SELECTOR_SET=0
TASK_SELECTOR=""
if [ "${DEEPPLANNING_TASK_IDS+x}" = x ]; then
    TASK_SELECTOR_SET=1
    TASK_SELECTOR="${DEEPPLANNING_TASK_IDS}"
fi

# Named frozen case subset (identical across languages). Resolved per level
# below into the same selector plumbing DEEPPLANNING_TASK_IDS uses.
TASK_SUBSET="${BENCHMARK_TASK_SUBSET:-standard}"

EXTERNAL_RUNTIME=0
if [ "${DEEPPLANNING_RUN_DIR+x}" = x ]; then
    if [ -z "${DEEPPLANNING_RUN_DIR}" ] || [ "${DEEPPLANNING_RUN_DIR#/}" = "${DEEPPLANNING_RUN_DIR}" ]; then
        echo "❌ DEEPPLANNING_RUN_DIR must be a nonempty absolute path" >&2
        exit 2
    fi
    if [ "${DEEPPLANNING_RUN_DIR}" = "/" ]; then
        echo "❌ DEEPPLANNING_RUN_DIR must not be the filesystem root" >&2
        exit 2
    fi
    EXTERNAL_RUNTIME=1
    RUN_ROOT="${DEEPPLANNING_RUN_DIR%/}"
    INFERRED_ROOT="${RUN_ROOT}/database_infered"
    REPORT_ROOT="${RUN_ROOT}/result_report/${BENCHMARK_VERSION}"
    mkdir -p "${INFERRED_ROOT}" "${REPORT_ROOT}"
fi

generate_run_id() {
    echo "$(date +%Y%m%d%H%M%S)_$$_${RANDOM}"
}

# Score + materialize whatever levels DID land, for the model currently in
# flight. This used to sit inline after the level loop, which meant `set -e`
# (line 9) plus a single killed level threw the script out before it ran, so a
# language that finished levels 1-2 and died in level 3 published NOTHING --
# the finished levels sat orphaned in database_infered/ and had to be salvaged
# by hand. It now runs from an EXIT trap
# so a crash, a SIGTERM, or a watchdog kill of a child still publishes the
# completed levels. Both steps already tolerate missing levels: score_statistics
# and organize_results build from whatever latest-timestamp folders exist.
FINALIZE_DONE=1   # nothing in flight before the first model

finalize_model() {
    if [ "${FINALIZE_DONE}" -eq 1 ]; then
        return 0
    fi
    FINALIZE_DONE=1
    cd "$BASE_DIR" || return 0

    echo ""
    echo "<<<< Calculating Overall Statistics for ${SHOPPING_AGENT_MODEL} (language=${SHOPPING_LANGUAGE}) >>>>"
    STATISTICS_ARGS=(
        python evaluation/score_statistics.py
        --model_name "$SHOPPING_AGENT_MODEL"
        --language "$SHOPPING_LANGUAGE"
    )
    if [ "$EXTERNAL_RUNTIME" -eq 1 ]; then
        STATISTICS_ARGS+=(--result_report_dir "$REPORT_ROOT")
    fi
    if ! "${STATISTICS_ARGS[@]}"; then
        echo "⚠️  Warning: Statistics calculation failed for model ${SHOPPING_AGENT_MODEL}, continuing..."
    else
        echo "✅ Statistics calculation completed for ${SHOPPING_AGENT_MODEL}"
    fi
    echo ""

    # Materialize a clean, travel-style per-language result tree from the winning
    # (latest-timestamp) folders. Non-fatal; the flat pipeline dirs are untouched.
    echo "<<<< Organizing per-language result tree for ${SHOPPING_AGENT_MODEL} (language=${SHOPPING_LANGUAGE}) >>>>"
    ORGANIZE_ARGS=(
        python organize_results.py
        --model "$SHOPPING_AGENT_MODEL"
        --language "$SHOPPING_LANGUAGE"
        --version "$BENCHMARK_VERSION"
    )
    if [ "$EXTERNAL_RUNTIME" -eq 1 ]; then
        ORGANIZE_ARGS+=(--base "$RUN_ROOT")
    fi
    if ! "${ORGANIZE_ARGS[@]}"; then
        echo "⚠️  Warning: Result organization failed for model ${SHOPPING_AGENT_MODEL}, continuing..."
    else
        echo "✅ Result tree organized for ${SHOPPING_AGENT_MODEL}"
    fi
    echo ""
    return 0
}

# The trap must not itself abort under `set -e`, hence the `|| true`.
trap 'finalize_model || true' EXIT
trap 'finalize_model || true; exit 143' TERM
trap 'finalize_model || true; exit 130' INT

read -r -a MODELS <<< "$SHOPPING_AGENT_MODEL"
read -r -a LEVELS <<< "$TEST_LEVELS"

for MODEL in "${MODELS[@]}"; do
    FINALIZE_DONE=0   # this model now has levels that must be published
    export SHOPPING_AGENT_MODEL="$MODEL"

    if [ "$EXTERNAL_RUNTIME" -eq 1 ] && [[ "$MODEL" == *[!A-Za-z0-9._+-]* ]]; then
        echo "❌ Model name is unsafe for deterministic runtime paths: $MODEL" >&2
        exit 2
    fi

    for TEST_LEVEL in "${LEVELS[@]}"; do
        cd "$BASE_DIR"

        SHOPPING_DB_CODE=$(cd .. && python -c 'import sys; sys.path.insert(0, "."); from languages import resolve_language; print(resolve_language(sys.argv[1]).shopping_canonical_db_code)' "$SHOPPING_LANGUAGE")
        # Seed DBs live under DEEPPLANNING_DATA_DIR when set (the suite shares one
        # top-level data/ across benchmarks), otherwise in-tree as upstream ships.
        SEED_ROOT="${DEEPPLANNING_DATA_DIR:-$(cd .. && pwd)}/shoppingplanning"
        if [ "$SHOPPING_DB_CODE" = "en" ]; then
            SRC_DIR="${SEED_ROOT}/database_level${TEST_LEVEL}"
        else
            SRC_DIR="${SEED_ROOT}/database_level${TEST_LEVEL}_${SHOPPING_DB_CODE}"
        fi
        if [ ! -d "$SRC_DIR" ]; then
            echo "❌ Seed DB not found: $SRC_DIR (language=${SHOPPING_LANGUAGE}, code=${SHOPPING_DB_CODE})"
            echo "   Check the data download; DEEPPLANNING_DATA_DIR=${DEEPPLANNING_DATA_DIR:-<unset>}"
            exit 1
        fi

        # Per-level case selector: explicit DEEPPLANNING_TASK_IDS wins; else
        # resolve the named task subset ('full' resolves to no selector).
        LEVEL_SELECTOR_SET=$TASK_SELECTOR_SET
        LEVEL_SELECTOR="$TASK_SELECTOR"
        if [ "$LEVEL_SELECTOR_SET" -eq 0 ]; then
            if ! LEVEL_SELECTOR=$(cd .. && python scripts/resolve_task_subset.py "shopping_level${TEST_LEVEL}" --name "$TASK_SUBSET"); then
                echo "❌ Failed to resolve task subset '${TASK_SUBSET}' for level ${TEST_LEVEL}" >&2
                exit 2
            fi
            if [ -n "$LEVEL_SELECTOR" ]; then
                LEVEL_SELECTOR_SET=1
            fi
        fi

        RESUME_EVAL_ONLY=0
        if [ "$EXTERNAL_RUNTIME" -eq 1 ]; then
            DATABASE_RUN_DIR="${RUN_ROOT}/database_run"
            OUTPUT_FOLDER="database_${MODEL}_${SHOPPING_LANGUAGE}_level${TEST_LEVEL}"
            INFERRED_DATABASE="${INFERRED_ROOT}/${OUTPUT_FOLDER}"
            REPORT_DIRECTORY="${REPORT_ROOT}/${OUTPUT_FOLDER}"
            # Resume. A run directory belongs to one trial of one run, so whatever
            # is already in it came from an earlier attempt at this same level. A
            # level with a summary is finished. One whose inference finished
            # needs only evaluation: the staged copy is moved to INFERRED_DATABASE
            # only after run.py succeeds. Anything else is redone. This used to
            # abort the script instead, so an interrupted `bench run` could never
            # be completed under the same run id.
            if [ -f "${REPORT_DIRECTORY}/summary_report.json" ]; then
                echo "⏭️  Level ${TEST_LEVEL} already evaluated for ${MODEL}, skipping (${REPORT_DIRECTORY})"
                continue
            elif [ -d "$INFERRED_DATABASE" ]; then
                echo "↻  Level ${TEST_LEVEL}: inference already done for ${MODEL}, re-running evaluation only"
                RESUME_EVAL_ONLY=1
                rm -rf "$REPORT_DIRECTORY"
            else
                rm -rf "$DATABASE_RUN_DIR" "$REPORT_DIRECTORY"
            fi
        else
            RUN_ID=$(generate_run_id)
            DATABASE_RUN_DIR="database_run_${MODEL}_level${TEST_LEVEL}_${RUN_ID}"
            OUTPUT_FOLDER="database_${MODEL}_${SHOPPING_LANGUAGE}_level${TEST_LEVEL}_$(date +%Y%m%d%H%M)_${RUN_ID}"
            INFERRED_ROOT="${BASE_DIR}/database_infered"
            INFERRED_DATABASE="${INFERRED_ROOT}/${OUTPUT_FOLDER}"
            REPORT_ROOT="${BASE_DIR}/result_report/${BENCHMARK_VERSION}"
            REPORT_DIRECTORY="${REPORT_ROOT}/${OUTPUT_FOLDER}"
        fi

        echo ""
        echo "🚀 Starting Shopping Benchmark"
        echo "   Level: ${TEST_LEVEL}"
        echo "   Model: ${SHOPPING_AGENT_MODEL}"
        echo "   Language: ${SHOPPING_LANGUAGE}"
        if [ "$TASK_SELECTOR_SET" -eq 1 ]; then
            echo "   Task selection: explicit DEEPPLANNING_TASK_IDS (${TASK_SELECTOR})"
        else
            echo "   Task subset: ${TASK_SUBSET}"
        fi
        echo "   Workers: $WORKERS"
        echo "   Max LLM calls: $MAX_LLM_CALLS"
        echo "   Database: ${DATABASE_RUN_DIR}"
        echo ""

        PREPARE_ARGS=(
            python prepare_database.py
            --source "$SRC_DIR"
            --destination "$DATABASE_RUN_DIR"
        )
        if [ "$LEVEL_SELECTOR_SET" -eq 1 ]; then
            PREPARE_ARGS+=(--task-ids "$LEVEL_SELECTOR")
        fi
        if [ "$RESUME_EVAL_ONLY" -eq 0 ] && ! "${PREPARE_ARGS[@]}"; then
            echo "❌ Failed to stage Shopping database" >&2
            exit 1
        fi

        # On an evaluation-only resume the cases are already in INFERRED_DATABASE.
        CASE_SOURCE="$DATABASE_RUN_DIR"
        if [ "$RESUME_EVAL_ONLY" -eq 1 ]; then
            CASE_SOURCE="$INFERRED_DATABASE"
        fi
        CASE_FILTER=()
        if [ "$LEVEL_SELECTOR_SET" -eq 1 ]; then
            while IFS= read -r case_name; do
                CASE_FILTER+=("$case_name")
            done < <(find "$CASE_SOURCE" -mindepth 1 -maxdepth 1 -type d -name 'case_*' -printf '%f\n' | sort -V)
            if [ "${#CASE_FILTER[@]}" -eq 0 ]; then
                echo "❌ Selected-task staging produced no case directories" >&2
                rm -rf "$DATABASE_RUN_DIR"
                exit 1
            fi
        fi

        RUN_ARGS=(
            python run.py
            --model "$SHOPPING_AGENT_MODEL"
            --workers "$WORKERS"
            --level "$TEST_LEVEL"
            --max-llm-calls "$MAX_LLM_CALLS"
            --database-dir "$DATABASE_RUN_DIR"
            --language "$SHOPPING_LANGUAGE"
        )
        if [ "$LEVEL_SELECTOR_SET" -eq 1 ]; then
            # The selector fully encodes the case set, so tell run.py to skip
            # its own subset resolution (its --rerun-ids path takes over).
            RUN_ARGS+=(--rerun-ids "$LEVEL_SELECTOR" --task-subset full)
        fi
        if [ "$RESUME_EVAL_ONLY" -eq 0 ]; then
            if ! "${RUN_ARGS[@]}"; then
                echo "❌ Inference failed for model ${SHOPPING_AGENT_MODEL} level ${TEST_LEVEL}"
                rm -rf "$DATABASE_RUN_DIR"
                exit 1
            fi

            echo "<<<< Starting Evaluation >>>>"
            mkdir -p "$INFERRED_ROOT"
            mv "$DATABASE_RUN_DIR" "$INFERRED_DATABASE"
            echo "<<<< Database saved to: ${INFERRED_DATABASE} >>>>"
        else
            echo "<<<< Starting Evaluation (resumed) >>>>"
        fi

        if [ "$EXTERNAL_RUNTIME" -eq 1 ]; then
            EVALUATION_ARGS=(
                python evaluation/evaluation_pipeline.py
                --database_dir "$INFERRED_DATABASE"
                --output_dir "$REPORT_DIRECTORY"
            )
        else
            # Preserve the legacy relative lookup and report layout.
            EVALUATION_ARGS=(
                python evaluation/evaluation_pipeline.py
                --database_dir "$OUTPUT_FOLDER"
            )
        fi
        if [ "$LEVEL_SELECTOR_SET" -eq 1 ]; then
            EVALUATION_ARGS+=(--case_filter "${CASE_FILTER[@]}")
        fi
        "${EVALUATION_ARGS[@]}"

        echo "✅ Model ${SHOPPING_AGENT_MODEL} Level ${TEST_LEVEL} finished."

        if [ "${TEST_LEVEL}" != "${LEVELS[-1]}" ]; then
            echo "Sleeping 10s before next level..."
            sleep 10
        fi
    done

    finalize_model

    if [ "${MODEL}" != "${MODELS[-1]}" ]; then
        echo "Sleeping 60s before next model..."
        sleep 60
    fi
done

echo ""
echo "✅ All models completed."
exit 0
