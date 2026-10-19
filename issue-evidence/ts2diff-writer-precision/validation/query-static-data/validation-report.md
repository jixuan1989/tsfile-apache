# Static data/reference audit — PR #1024

**The original Windows query gate is still UNCLEARED; necessary cost is not proved. This audit contains no new query timing or production change.**

The prior link-boundary hypothesis was stopped: loading `tsfile_writer.obj` for `libtsfile_init/destroy` does not retain all writer functions. Four exact-image sidecar guards pass (`.text`/`.pdata` identical to their original images; only debug timestamps differ in `.rdata`). The two APIs are separate 45/76-byte COMDATs with identical code across versions. The selected precision-related symbols appear37/37 times in mixed images and0/0 in reader-only images. A file split is not justified as removing new precision execution from queries.

The remaining31 changed reader-only instructions reference10 vtables. All57 actual method-pointer slots match **byte-for-byte**, including their function RVAs and order. Starting at those tables,72 reachable TsFile vtable/RTTI data nodes (2,656 bytes) match after normalizing171 named address relocations per image. Every relocated value was checked against the original PE bytes and selected MAP binding. One explicit external boundary remains: the CRT `type_info` vtable, with the same named provider/RVA; its implementation was not recursively audited. Initial writable RTTI cache fields are not a proof of identical runtime state.

Additional original-image accounting:

| Section | Differing bytes | Result |
| --- | ---: | --- |
| `.text` |60 | Earlier instruction decoding:52 same operations, same named bindings;21 import references plus31 vtable references. |
| `.rdata` |719 | All differences classified:56 import-table/name-storage bytes and663 bytes in verified literal/vtable/RTTI ranges. No unexplained byte is silently excluded. |
| `.data`, `.pdata`, `.rsrc` |0 | Exact on-disk byte equality. |
| `.reloc` |69 | One removed and one added DIR64 location, exactly matching the shifted audited data slot. |

Both reader images import the same184 DLL/name pairs. Six IAT slots reorder but stay within their old64-byte RVA blocks; same binding is not a cache/latency claim. Forty owner-qualified non-COMDAT literal pools per image match their contributing COFF bytes. All100 shared owner-qualified constant symbols have equal payloads after explicitly excluding trailing NUL/padding. One anonymous-namespace symbol has a different compiler-mangled name but identical raw value. Owner qualification matters because internal names repeat across object files. A preliminary NUL-terminated byte-pattern search is only a locator; it must not be read as evidence that a constexpr array/copy was removed.

All15 CRT pointer arrays match in order, including482 `.CRT$XCU` entries (497 pointer cells across the arrays, including sentinels/runtime entries). This rules out changed stored initialization order in these images, not changed runtime cache/allocator state. GNU binutils objdump2.38 independently decoded both original images and verified every72-node byte snapshot,57 method slots,171 relocated values,40 literal pools and497 CRT cells per image.

The archive contains target data snapshots, full GNU data dumps, selected MAP rows, structured COFF-derived records, analyzers and retained helper corrections. Full original executables, COFF objects, native COFF dumps and full MAPs remain local with pinned hashes; **this is not a self-contained original binary/build archive**. Run `python verify_snapshot.py` after extraction for portable offline snapshot checks. Re-running `analyze.py`/the dependency relinks requires the existing pinned workspace/compiler artifacts. It does not run a runtime benchmark. The literal-pool helper's initial set-union typo and original partial classification (520 bytes then unclassified) are preserved; only offline analysis was extended, no measurement was rerun/replaced.

No virtual target change or constant-value difference was found in the checked scope. Static equality/normalization does not establish identical runtime heap/cache state, all address-sensitive behavior, or necessary performance cost. The original mixed-image regressions, contradictory sessions and scope limits remain; this reader-only audit cannot clear them. No new Java compatibility, coverage, sanitizer or write/query performance pass is claimed. PR source remains at `75592b89d1523a96090e8bca1dcb4cd2180162e5`.

## 中文译稿

**原Windows查询门槛仍未通过，必要代价未证明；本轮没有新增查询计时或生产代码修改。** 上轮核查停止了拆分初始化文件方向：对象被加载不等于所有writer函数保留。四份旁路重链保持原代码/展开信息逐字节一致，只读段仅debug时间戳改变；两个入口是45/76字节的独立COMDAT，前后代码相同。固定选取的精度writer符号在混合程序各37项，仅读程序均0项，不能声称拆分会移除新增查询执行路径。

剩余31条变址指令指向10张vtable，57个实际方法指针的字节、函数RVA及顺序全部相同。继续追踪72个TsFile vtable/RTTI节点（2656字节），每版171个地址重定位均按原PE实际值和MAP绑定核对；规范化地址后非地址数据和目标顺序一致。唯一外部边界是CRT的type_info vtable，名字/提供者/RVA相同，但没有递归验证其实现；初始可写RTTI缓存也不代表运行时状态一致。

上表列出全部原reader段差异：代码60字节已由既有52条指令分析覆盖；只读段719字节全部归类为导入存储56字节及已核对的常量/vtable/RTTI范围663字节。可写数据、展开信息、资源段字节一致。重定位表69个差异字节对应1处DIR64位置移除和1处增加，与已核对数据槽位的移动精确对应；没有把未解释字节排除后宣称全等。

两版reader的184个DLL/函数导入对相同，六个IAT槽位重排但未跨原64字节RVA块，这不是缓存或耗时等价。每版40个非COMDAT常量池按对象限定的MAP锚点核对COFF原字节；100个共享常量符号在明确去除尾部NUL/填充后内容一致，一个匿名命名空间的修饰名不同但原始值相同。内部符号会跨对象重名，不能用全局名字字典误选副本。初步带NUL的字节模式搜索只用于定位，不能据此声称constexpr数组或副本被删除。

全部15组CRT指针数组顺序一致，包括482个XCU槽位；连同sentinel/运行时条目共497个指针单元。独立GNU objdump2.38对原PE数据解码，再次核对每版72节点、57方法槽位、171地址值、40常量池及497个CRT单元。初始化表顺序相同不证明运行时分配/缓存状态相同。

快照包保存目标数据、GNU完整数据转储、MAP摘录、COFF派生记录、复核器及工具更正。原exe/COFF对象、完整MAP与原生COFF转储留在本地并记录哈希；它不是可独立重建原二进制的整包。解压后运行上面的Python命令可离线核对快照，重做COFF遍历/链接还需原固定工作区及编译器。首次常量池辅助脚本的集合运算笔误和最初尚未归类520字节的中间记录均保留，只扩展离线分析，没有重跑/替换性能样本。

已查范围内没有发现虚函数目标或常量值变化，但不能由此推导运行时堆/缓存、全部地址敏感行为或性能等价。原混合程序退化、相反轮次及未测范围保留，查询门槛未通过；没有新增Java互通、覆盖率、sanitizer、写入或查询通过声明。源码head保持上面的原提交。只有发现具体活跃路径差异或新的有效审阅要求后才设计下一项修改/固定测量，不为取得通过而继续排列、padding或追加跑分。
