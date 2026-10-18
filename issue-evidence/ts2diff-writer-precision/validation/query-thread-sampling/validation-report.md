# PR #1024: unprivileged stack sampling and WPR permission result

Source head: `75592b89d1523a96090e8bca1dcb4cd2180162e5`. Production source remains clean and unchanged. **The query gate remains uncleared. No hardware counters have been captured.**

## What completed

Exactly eight position-balanced rounds × four original mixed-program payloads (two baseline and two fixed copies), 1024 queries/child: **32 children and32768 fully checked queries**. Two excluded256-query smoke children checked512 additional queries. All timestamps, types, values, NULLs, row counts, ordering and checksums pass. Separate image-copy preflights are excluded from timing/profile totals. Input is the prior dense aligned DOUBLE precision2, four-field1024-row batch scan; baseline/fixed writer products are byte identical and retain their earlier Java audit. No new Java/coverage/unit/ASan/write-throughput run is claimed.

The private sampler inspects only its own child main thread. It uses `SuspendThread`, `GetThreadContext` and `StackWalk64`, then resumes the thread. A high-resolution timer requests fixed-seed0.5..1.5ms waits. The parent is pinned to mask16, the child to mask12 before its initial resume; pool2, parallel=false, warmed filesystem cache, uncontrolled host background/power. Image payloads rotate over the same four paths each round. All32 actual main executable bases differ; this observation does not establish ASLR causality. Modules are inventoried after the loader exposes the CRT; modules loaded later can be unresolved. Per-process QPC intervals and module/RVA stack frames are retained, but exact per-query QPC boundaries are not instrumented.

The run produced **66168 snapshots**, with the `read_fixture` PE runtime-function interval present in **66158 stacks (99.985%)**. Symbol attribution uses linker maps plus loaded module bases; these are nearest public function names, not PDB source lines or complete inline frames. There are no CPU event counts in this dataset. Wall-time samples may include off-CPU/blocked time.

## Critical measurement limitation

The median per-child summed suspension interval is **26.64% of process wall time**. This is too intrusive to attribute an approximately1% production regression. It is only a hotspot discovery tool. Profiled native full-latency descriptive F/B median is 1.013294; whole main-thread lifetime cycle F/B is 1.027947. Neither is acceptance evidence or a query-only hardware count; initialization, output and exit affect lifetime cycles. Within-version negative controls and every sample remain available. There is no resampling, trimming, margin change or pass claim.

## Hotspots for the next investigation

| Nearest leaf function/module | Baseline query-frame samples % | Fixed query-frame samples % |
|---|---:|---:|
| query consumption and verifier (`read_fixture`) | 37.098 | 36.465 |
| aligned batch decode (`multi_DECODE_TV_BATCH`) | 6.819 | 8.318 |
| TS2DIFF INT64 batch decode | 8.648 | 9.006 |
| TS2DIFF DOUBLE batch decode | 7.754 | 7.300 |
| ntdll module (not a resolved internal function) | 12.790 | 12.423 |

These are descriptive sample shares, not a causal decomposition. The aligned batch function is a candidate for hardware-counter attribution: its share rises from about6.82% to8.32% in this perturbed run. However, its **5608 original COFF code bytes and every (offset,type,target-symbol) relocation tuple match exactly** between baseline/fixed. Earlier selected query/verifier code also matched. No added reader operation has been demonstrated. No production layout/padding change or unrelated reader optimization is proposed from these samples.

## WPR could not collect PMU data

The profile requests TotalCycles, InstructionRetired, IcacheMisses, DcacheMisses and BranchMispredictions on context switches, plus sampled-profile call stacks. `wpr -profiles tsfile.wprp` successfully lists the custom profile (configuration parsing only), but actual start failed with:

```text
Failed to enable the policy to profile system performance.
Error code: 0xc5585011
```

The current token is not elevated, and `wpr -status` confirms no recording. [Microsoft documents the same error when WPR is started without administrator rights](https://learn.microsoft.com/en-us/windows/apps/performance/disk-memory). [Microsoft's PMU recording documentation](https://learn.microsoft.com/en-us/windows-hardware/test/wpt/recording-pmu-events) distinguishes listing a source from collecting counters. The profile being listed is not evidence that the five counters will successfully allocate or produce valid events.

## Ready-to-run administrator capture

Local script: `work/query-backfill/pmu/capture-admin.ps1`. It does not elevate itself or modify security policy. It reads the current state/backlog, checks the precision PR head and clean source, verifies exact original binaries and the identical input, and checks every native result. Its query preflight passed12 queries and its PowerShell syntax parsed. Actual elevated capture remains **unexecuted/unverified**.

Run from an **administrator PowerShell**:

```powershell
& 'C:/Users/hxd/Documents/Codex/2026-10-17/new-chat-2/work/query-backfill/pmu/capture-admin.ps1'
```

The script refuses to disturb an existing WPR recording. It uses a uniquely named capture directory and its own `TsFileQueryDiag` instance; it runs8 balanced rounds of4 original children ×1024 queries, records PID/main-TID/QPC intervals and all native outputs, bounds workload execution to10 minutes with per-child limits, and saves/stops its own trace in `finally`, including partial failures. PMCs apply to process/thread intervals; query-only attribution still requires validated sample/call-stack boundaries. WPR overhead and the elevated child token differ from acceptance conditions, so this remains diagnosis.

**The system-wide ETL must stay local.** The script performs no upload, Git push, source edit or policy change. Only future target-PID/TID-filtered evidence may be published after validation. The current public archive contains only the private child sampler's data, normalized to module/RVA (absolute loaded bases stay local), native query outputs, source, maps, plans and errors. No sample is dropped during address normalization; unmapped addresses use per-process opaque tokens. Original absolute-address files and failed development smoke logs remain local. The failed smoke iterations exposed helper teardown and early-loader inventory races; both were repaired before the completed fixed run, and no failed iteration is treated as a valid profile.

## Existing quality evidence and limits

The earlier corrected32-case matrix/7 independent confirmations/3 residual query signals remain unchanged. The earlier write, Java interoperability and coverage results retain their exact scope. This one-case sampling exercise is not the full query matrix and cannot fill the earlier cold-cache/P99/compressed/sparse/native-FIELD/parallel-scaling gaps. All original production binaries still have the same SHA-256. New issue04 remains unpublished and unapproved.

## 中文说明

本轮源码没有修改或推送，查询门槛仍未通过。完成32个原程序子进程、32768次完整核对查询，采集66168个快照，其中66158个调用栈包含查询函数。采样只操作自身子进程的主线程；每次暂停、读取上下文和调用栈后立即恢复。主线程暂停时间中位占比达26.64%，对约1%的退化来说干扰过大，因此只用于发现热点，不作为性能验收或硬件事件计数。

对齐批量解码的采样占比约从6.82%升到8.32%，但该函数5608字节机器码以及全部重定位目标在两版中完全一致，尚未证明新增读取操作，也未确定根因。保留所有采样和异常，不据此添加生产 padding/排列或无关的读取优化。

WPR实际启动报错0xc5585011，当前进程未提升为管理员；没有产生有效PMU采集。自定义配置可以被工具列出，不等于五项计数器已能成功采集。管理员采集脚本已准备完成，其12次查询预检和PowerShell语法检查通过，真正的管理员录制尚未执行。需在管理员PowerShell执行上面的命令。脚本不自行提权、不修改策略、不干扰已有录制，固定轮数并核对全部结果，在finally中停止并保存自身录制，失败样本保留。系统ETL只保存在本地，不上传；后续只能发布目标进程过滤后的数据。

原兼容性、覆盖率、写入和查询矩阵证据继续保留，不冒充本轮重测；第4条issue仍待独立批准。

**AI disclosure:** The implementation, tests and description in this pull request were written by an AI coding agent (OpenAI Codex), which also performed the reported local validation.

**AI 使用说明：** 本 PR 的代码修改、测试和正文由 AI 编程代理（OpenAI Codex）编写，文中报告的本地验证也由该 AI 代理执行。
