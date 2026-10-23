# data/

This directory holds no benchmark data in git. What is committed here are the
frozen `standard` task lists, one task ID per line:

```
tau3/task_subsets/standard/<domain>/base.txt
vitabench/task_subsets/standard/<domain>.txt
deepplanning/task_subsets/standard/<domain>.txt
```

They fix which tasks `standard` runs, the same IDs in every language. ClawEval's
lists live in `benchmarks/claw/task_subsets/standard/`.

The task data itself (per-language tasks, policies, databases and environments,
about 14 GB) is not in the repository. `./bench fetch-data` fills it in here,
next to the lists, and ClawEval's into `benchmarks/claw/tasks/`. See the
Data section of the [README](../README.md) and [docs/RUNNING.md](../docs/RUNNING.md#setup-and-data).
