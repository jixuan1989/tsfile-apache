# Windows/Linux footer property order audit — PR #1024

**The original Windows query gate remains uncleared. No necessary query cost is proved; no production change or new timing was made.**

The dense (169,559 bytes) and sparse (392,839 bytes) Windows/Linux fixtures each differ at exactly 69 byte positions. All differences lie in the final 78-byte property block. The entire prefix before that block and the 10-byte footer after it are identical, including all data pages, chunk headers, metadata and Bloom filter bytes. Within each platform, baseline/fixed writer products are already byte-identical.

| Property | Raw value in all eight files |
| --- | --- |
| `encryptLevel` | `0` |
| `encryptType` | `org.apache.tsfile.encrypt.UNENCRYPTED` |
| `encryptKey` | NULL (signed varint length −1) |

Windows serializes `encryptLevel, encryptType, encryptKey`; Linux serializes `encryptKey, encryptType, encryptLevel`. Sorting the three entries in memory makes the whole files byte-identical; reordering either side to the other side's order exactly reconstructs the other's original bytes. No input was rewritten. `TsFileProperties` is a C++ `std::unordered_map`; serialization traverses it and deserialization inserts by key. The default properties are inserted by `TsFileIOWriter::write_file_index`. These writer/metadata/reader sources are unchanged between the exact PR base and head; hashes and offsets are recorded in `analysis.json`. This is a property ordering difference, not a data encoding difference or demonstrated new format defect.

Java independently decoded all eight raw property blocks using its varint/string utilities, then opened all eight files through `TsFileSequenceReader.getTsFileProperties()`. Both orders passed. **Raw NULL and API values differ by documented source behavior here:** `TsFileMetadata.deserializeFrom` normalizes the reserved encryption key to empty bytes for encryption level 0. The initial audit incorrectly expected the API to retain NULL and failed on the first file. Its source and logs are retained in `initial-null-expectation/`; the corrected audit checks raw NULL and the normalized API value separately and emits both actual maps. This was an audit expectation error, not evidence of a production regression.

The C++ getter returns a keyed map. Different insertion order could affect metadata allocation/cache behavior; this audit does not assert zero timing effect. Because the original Windows baseline/fixed files are identical, the cross-platform permutation cannot explain their within-Windows comparison. Compiler, OS/virtualization, linker context and filesystem factors still cannot be isolated by the separate GCC run. The original Windows performance observations and adverse controls stand.

Reproduce after extracting the companion evidence ZIP:

```text
python verify.py
python run_java.py "<TsFile Java runtime classpath>"
```

The first command uses Python standard libraries only and validates every frozen file/hash, property bound, canonical whole-file equality and saved Java result. The second requires `java`/`javac` on PATH and the same Java metadata API (checkout/class hashes in `provenance.json`); it compiles and repeats only the metadata checks. The full earlier GCC benchmark and event ZIPs remain immutable. No new full-value Java matrix, Java→C++ run, coverage, sanitizer, write throughput or query timing is claimed.

## 中文译稿

**原 Windows 查询门槛仍未通过，必要代价未证明；本轮未修改生产代码、未新增计时。** 稠密和稀疏文件分别为169559和392839字节，每组跨平台文件均有69字节不同，全部位于最后78字节的属性块。此前全部字节和此后10字节footer一致，包含数据页、chunk头、元数据和Bloom filter。同一平台内baseline/fixed产物原本就逐字节一致。

上表三个原始属性值在八份文件中相同；Windows顺序为`encryptLevel, encryptType, encryptKey`，Linux为`encryptKey, encryptType, encryptLevel`。仅在内存中排序属性即可使整份文件完全一致；改为另一方的顺序则精确重建另一方原始字节。原文件没有改写。C++使用`std::unordered_map`，按迭代顺序写出、按键读取；相关源码相对本PR基线未改。这不是数据编码差异，也没有证明新的格式缺陷。

Java使用自身工具独立解析八个原始属性块，再经元数据接口读取八份文件，两种排列均通过。需要区分原始NULL与接口规范化：未加密等级0时，Java将保留密钥变为空字节数组。第一次核对误要求接口仍返回NULL，在第一份文件断言失败；失败源码/日志完整保留，修正后分别检查并输出实际原始值与接口值。这是核对脚本预期错误，不能据此报告生产缺陷。

不同插入顺序可能影响元数据分配和缓存，本轮不宣称计时影响为零；但原Windows两版输入字节一致，因此跨平台属性排列无法解释Windows内部两版的差异。编译器、OS/虚拟化、链接上下文与文件系统的影响仍未独立辨识，原Windows退化及相反对照均保留。上面的两条命令可离线核对与重复Java元数据检查；所需Java类/源码哈希见provenance记录。旧GCC与事件证据包保持不变；没有新增完整Java值矩阵、Java→C++、覆盖率、sanitizer、写入吞吐或查询计时通过声明。
