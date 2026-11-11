# YHHYPy — 手机上的 Python 代码编辑器

一个跑在 Android 上的 Python **编辑器 + CPython 3.12 运行环境 + 纯 Python 包管理器**。
核心（词法高亮、符号索引、补全、语法检查、撤销、查找替换）用 **C++** 写成并通过 JNI 提供；
界面是**自绘的 Android 视图**（不用 EditText，所以滚动、彩色文本、行号都不会卡）。
当前版本 **5.6.8**（versionCode 91），APK 9.25 MB（8.82 MiB），应用名 **YHHYPy**，包名 `com.yhhy.pyeditor`，支持 Android 7.0+（arm64-v8a）。
下面「需求对照」是最初的定位（只编辑）；2.x 起已内置 CPython 3.12 运行环境与 pip 包管理，4.9 起移除 MicroPython。

## 需求对照

| 需求 | 实现 |
|---|---|
| 用 C++ / Python 写 | 核心引擎 `native/*.cpp`（**2,897 行 C++**）+ **16,863 行 Java** 外壳；JNI 47 个方法 |
| 只要编辑，不需要运行 | *（最初定位）* 纯编辑器；2.x 起已内置 CPython 运行与 pip，4.9 起只留 CPython |
| 补全：变量、函数名、自定义函数名、类名、自定义类名 | 每行增量提取符号：`def` / `class` / 赋值左值 / 参数 / `for` 目标 / `as` / `import` / `self.xxx` 属性；再合并 Python 关键字、内置函数、常量。按"精确 > 前缀 > 忽略大小写前缀 > 子串 > 子序列"排序，带类型标签 |
| 显示行号 | 左侧行号栏，当前行高亮；点行号可直接选中整行 |
| 语法高亮 | 15 种记号（关键字/内置/常量/字符串/注释/数字/运算符/def名/class名/装饰器/self/参数/自定义函数/自定义类/普通文本）；三引号字符串支持跨行 |
| 自定义关键字、函数名、文本等的字体与颜色 | 设置里 15 类记号逐项配色 + **B/I**（粗体/斜体）；另有背景/行号栏/当前行/选区/光标/错误线颜色；字号、行距、字体族（等宽/无衬线/衬线/**载入 .ttf**）；**4 套预设主题 + 任意多个自定义主题**；配色改动有实时预览 |
| 简单语法检查 | 5.5.4 起 24 类：括号/冒号/引号、缩进、赋值目标、缺右值、`def/class` 名字、参数重名/默认值顺序、调用参数顺序、import、数字字面量、模块级 await/yield、星号右值、孤立子句、`type` 缺 `=`、f-string、`except*`、单行字符串未闭合；规则对齐 CPython，标准库/ dist-packages 0 误报；错误处画红色波浪线，状态栏显示数量，点开可跳转 |
| 最好不卡顿 | 自绘视图 + 原生缓冲；每帧只做 1 次 JNI 取可见行记号，行文本按 revision 缓存；词法按行缓存并增量重算（改一行通常只重算 1–3 行）；语法检查防抖（输入后 400 ms、空闲 800 ms） |
| 支持横屏 | `configChanges` 处理旋转不重建、不丢内容；布局自适应 |

## 用法

* **工具栏**：`☰` 菜单 · 文件名（脏标记 ●）· `▶` 运行 · `常用`（含状态栏切换）· `↶` 撤销 · `↷` 重做 · 补全 · `+`（新建编辑区 / 解释器 / 终端，可选右侧/下方拆分）
* **手势**：点按定位光标；拖动滚动（带惯性）；长按选词，继续拖动扩选；点行号选整行；
  **双击块头 / 单行集合赋值 = 折叠**；横向到最左向右滑 = 抽屉；横向到最右向左滑 = 右侧大纲
* **折叠**：`def/class/if/elif/else/for/while/try/except/finally/with/match/case` 块、连续 import、
  多行签名、多行/单行的列表·字典·元组·集合字面量、连续赋值、连续同名调用都能折；
  折叠后显示 `▸ def f ...` / `▸ cfg = dict[str, int] ...` 这样的摘要（按 token 上色、保留缩进）；
  **子块可单独折**，父块折叠不丢子块状态；抽屉「折叠 ▸」还能按类别批量折（所有 / 关键字 / 赋值与函数 / 展开全部）
* **补全**：输入字母/`_`/`.` 自动弹出，点选插入；`Tab` 或回车选第一个，方向键上下移动；`. ` 后按属性补全
* **状态栏**：行/列、总行数、问题数；有问题时点状态栏可看清单并跳转
* **状态栏位置与开关**：设置 → 编辑器里横屏 / 竖屏各有「显示」复选框 + 「顶部 / 底部」位置，另有「在常用栏中显示」；快捷切换在 `常用` 菜单里（状态栏：底部/顶部/隐藏）
* **多区**：顶栏 `+` 选「编辑区 / 解释器 / 终端」+「在右侧 / 在下方拆分」，任意布局都能拼（上1下2、左2中1右2…），最多 6 个区；长按分割线换位、拖分割线挤掉；设置里的 1×2…1×6 只是「一键重排」
* **主题**：深色 / 浅色 / 午夜蓝 / 品红·浅蓝 + **自定义主题**（`＋ 保存当前配色` 起名存进 App，点切换、长按删除）
* **菜单**：新建 / 打开 / 保存 / 另存为 / 最近文件 / 全选 / 缩进·反缩进 / 语法检查 / 字体与配色 / 关于
* **文件**：走系统文件选择器（SAF），无需存储权限；退出时若有未保存修改会提示；切到后台会对已打开的文件自动保存

## 安装 / 下载

1. 在 Release 页下载 `PyEditor-5.6.8.apk`（**9,249,903 B ≈ 8.82 MiB**）；
2. 允许「安装未知来源应用」，点开安装；**只支持 arm64-v8a**（Android 7.0 / API 24 及以上）；
3. 覆盖安装 **5.6.0 – 5.6.7** 不需要卸载，偏好、自定义主题、已装的包都在；
   从 5.5.x 及更早版本升级也建议直接覆盖（会保留偏好；第一次启动多区布局可能退回网格，重新拆一次即可）；
4. 校验：
   * APK SHA-256 `a5c6153abffb1c54b367b63d4d1eb22749dbf3af7b1849e16e663f03b06ca6ff`
   * 签名证书 SHA-256 `e31569a9dcee6c2434c6bf15a6304b68cd71bc885122460808dc8815ba213ca0`（v1+v2+v3，与历史版本同一把）
5. 首次启动会解压标准库（约 6.2 MB，1–2 秒），之后启动不必再等。

## 文档

| 文件 | 用途 |
|---|---|
| `README.md` | **仓库主页**（本文件，长期维护） |
| `功能说明.md` | 详细功能说明（逐项、含实现方式与限制） |
| `release/功能说明-超详细版-5.6.8.md` | 超详细版（约 100 KB，30 章 + 4 附录；含折叠的显示/嵌套/边界全表） |
| `release/版本速览-<版本>.md` | 每个版本一页的更新摘要（发布 Release 时用） |
| `交接.md` | 开发者交接：架构、本轮改动、踩坑、发布流程、已知问题 |

> GitHub 主页 README 与 Release 页面 README 是两份：每个版本的发布目录里放一份 README 用来更新
> **仓库主页**；`项目概要/README.md` 是**发布 Release 资源**时用的那份（见 `项目概要/README.md` 顶部说明）。

## 目录

```
pyeditor/
├── AndroidManifest.xml
├── build.sh                 # 一条命令出 APK（不用 Gradle）
├── native/
│   ├── engine.h             # 数据结构 / 记号类型 / 接口
│   ├── lexer.cpp            # Python 词法分析 + 符号提取
│   ├── doc.cpp              # 缓冲、编辑、撤销、语法检查、补全、取记号
│   └── jni.cpp              # JNI 桥
├── java/com/yhhy/pyeditor/
│   ├── Native.java          # native 方法声明
│   ├── EditorView.java      # 自绘编辑器：绘制/触摸/IME/补全/折叠/行分隔线
│   ├── MainActivity.java    # 工具栏、文件读写、状态栏、多编辑区调度
│   ├── PaneLayout.java      # 多区容器（格子 + 边段网格）：拆分 / 按段拖动 / 十字圆点 / 磁吸 / 挤掉 / 换位
│   ├── PaneTiling.java      # 多区几何约束：拖动区间求解 + 重叠校验（纯 Java，可 JVM 单测）
│   ├── PaneCodec.java       # 多区快照编解码（ZL2：段表 + 每格四个段下标）
│   ├── PaneHost.java        # 一个编辑区：EditorView + 右侧 MiniMap（挤压布局）
│   ├── CustomThemes.java    # 自定义主题仓库（多命名、存 App 内）
│   ├── MiniMapView.java     # 右侧大纲小地图：只画色块 / 错误红点 / 可见框
│   ├── DocOutline.java      # 顶层 def/class + 方法的大纲扫描（纯 Java，可单测）
│   ├── FoldScan.java        # 集合字面量折叠 + 类型推断
│   ├── AssignScan.java      # 连续简单赋值折叠（N Value = 类型）
│   ├── CallScan.java        # 连续同名调用折叠（print() * 3）
│   ├── SymbolStats.java     # 函数引用 / 类成员统计
│   ├── SettingsActivity.java# 设置（含实时预览 / 页栈 / 预测返回）
│   ├── PreviewView.java     # 设置页预览
│   ├── Theme.java           # 配色/字体/行为配置 + 4 套预设 + 行分隔线 + 自定义主题序列化
│   ├── Immersive.java       # 横竖屏隐藏系统状态栏 + 刘海安全区
│   ├── BackCompat.java      # 预测性返回封装（API 33 / 34 分档）
│   ├── Messages.java        # 原生错误码 → 中文消息
│   ├── Lang.java            # 中英文字典（中文源码 + 运行时翻译）
│   ├── Prefs.java / Snippets.java / FindBar.java
│   ├── TerminalPanel.java / RunPanel.java / PipActivity.java
│   ├── CompilerStore.java / CBuilder.java / PyHeaders.java / SitePkgs.java
│   ├── CompletionPopup.java / ColorPickDialog.java / SnippetTemplate.java
│   ├── ShellBridge.java     # Shizuku / root / 本应用身份三通道
│   └── App.java             # 崩溃日志落盘
├── test/                    # 单测：native CheckTest 90 + SyntaxTest 91；JVM ScanTest 49 + SnippetAssignTest 31
│                            #      + MiniMapTest 13 + PaneTilingTest 36 = 129
├── res/mipmap-xxxhdpi/ic_launcher.png
└── dist/PyEditor.apk
```

## 重新构建

```bash
./build.sh
# 产物：dist/PyEditor.apk
```

依赖（都已在本机装好）：clang-19、`/opt/asysroot` 里的 Android sysroot + libc++ 头文件、
JDK 17、`/opt/android-sdk/build-tools-tmp`（d8 / apksigner）、`aapt`（apt 包，arm64 原生）。

**libc++ 静态库**：`libpyedit.so` 现在把 libc++ 静态链进来（不再打包 `libc++_shared.so`），
用到的 4 个静态库 + 1 个 libdl stub 放在 `/opt/asysroot/ndk-r30-clibs/`（可用 `CXXLIB=…` 覆盖）。
它们从 NDK r30 提取（clang 21，与 `/opt/asysroot/inc-cxx` 的 libc++ 21 头文件同版本、同为 `__ndk1` ABI 命名空间）：

```bash
curl -O https://dl.google.com/android/repository/android-ndk-r30-linux.zip
mkdir -p /opt/asysroot/ndk-r30-clibs
unzip -j android-ndk-r30-linux.zip \
  '*/sysroot/usr/lib/aarch64-linux-android/libc++_static.a' \
  '*/sysroot/usr/lib/aarch64-linux-android/libc++abi.a' \
  '*/lib/clang/21/lib/linux/aarch64/libunwind.a' \
  '*/lib/clang/21/lib/linux/libclang_rt.builtins-aarch64-android.a' \
  '*/sysroot/usr/lib/aarch64-linux-android/24/libdl.so' \
  -d /opt/asysroot/ndk-r30-clibs
```

标准库裁剪（可选，改完直接覆盖 `assets/stdlib.tar.xz`）：

```bash
tar xJf assets/stdlib.tar.xz -C /tmp/stdlib-src          # 或从 Python-3.12.8/Lib 准备
python3 tools/trim_stdlib.py /tmp/stdlib-src /tmp/stdlib-trim
python3 tools/pack_stdlib.py /tmp/stdlib-trim assets/stdlib.tar.xz
```

构建流程：clang 交叉编译 `libpyedit.so`（静态 libc++）→ `aapt` 处理资源 → `javac`（bootclasspath 用 API 30 android.jar）
→ `d8` 生成 dex → 自写 `tools/pack.py` 按 `resources.arsc` 4 字节、`.so` 16 KB 对齐重新打包 → `apksigner` 签名。

## 说明 / 限制

* 语法检查只是轻量的结构检查（不是完整 Python 语法分析）；代码运行由「▶」或菜单显式触发。
* 只打包了 `arm64-v8a`。
* 撤销按输入批次合并（连续打字算一步）。
* 中文输入法合成文本有下划线提示，跨行合成会退化成逐行删除（实际很少遇到）。

## 更新记录

**5.6.8**

* **标准库外科手术**：删掉 `unittest/ doctest.py pydoc.py pydoc_data/ venv/ turtle.py cgitb.py
  xmlrpc/`（tkinter/turtledemo/ensurepip/lib2to3/idlelib/distutils 本来就不在包里）；
  其余 494 个 `.py` 用 `tools/trim_stdlib.py` 去掉全部注释/空行/docstring（`compile()` 逐个校验，
  失败保留原文件），`this.py` 原样保留。
* `assets/stdlib.tar.xz` **1,688,784 → 793,312 B（-53%）**，标准库解压后 12 MB → 6.2 MB，
  APK 10,156,396 → **9,249,903 B（8.82 MiB，-906 KB）**。
* 打包用 `tools/pack_stdlib.py`（GNU tar + LZMA2 preset 6，和原来 `tar cJf` 格式一致）。

**5.6.7**

* **修单区状态存不下来**：单区没有分隔线（0 段），`saveLayout` 之前直接返回 null，日志里是
  `save desync … why=no segs`；ZL2 现在允许 0 段，关掉多区后的单区状态能正常落盘。
* **修恢复时读错字段**：`restoreZones` 把 ZL2 的第 4 个字段（段数）当成格子数，2/3/5 个区会被
  误判成「区数不一致」退回网格（4 个区时 4 段恰巧相等，所以之前没暴露）。改用 `PaneCodec.decode().n`。
* **关掉「启用多区域」不再丢布局**：关掉时不 clean、也不落盘单区状态，并把多区布局备份到
  `zone_multi_state/zone_multi_panes`；重新打开后下次启动自动恢复上次的多区布局。
* `PaneTilingTest` 35 → 36（单区 0 段快照往返）。

**5.6.6**

* **修「多区重开就粘一块」**：分区快照改成 ZL2（段表 + 每格四个段下标），同一坐标上的上下两根竖线 /
  左右两根横线恢复后仍是独立对象；旧 ZL1 快照恢复时按「格子覆盖范围」自动拆回（2×2 → 4 段，
  合并单元格保持共享）。根因是 5.6.1 起快照只存坐标、恢复按坐标取段，**新建不合并、重开才合并**。
* **设置 → 多区布局**新增「启用多区域」复选框：关掉后回主界面强制单区——除第一个区外全部关闭、
  清掉分区记忆、隐藏 `+`；启动时也不再恢复多区布局（直接打开上次的文件）。
* `PaneTilingTest` 27 → 35（ZL2 往返、同坐标两段独立、坏数据拒绝、`extentGroups` 拆分规则）。

**5.6.5**

* **libc++ 改为静态链接，APK 11.49 → 10.16 MB（-1.27 MiB）**：删掉 `libc++_shared.so`
  （1,423,696 B，stored 不压缩），把 libc++ / libc++abi / libunwind / compiler-rt 静态链进
  `libpyedit.so`（179,040 → 273,720 B）。静态库来自 NDK r30（clang 21，与项目 libc++ 头文件同版本）。
* **首装踩坑并修复**：只 `NEEDED libdl.so` 时真机 `dlopen` 报 `cannot locate symbol "__sF"` ——
  旧版是靠 `libc++_shared.so → libc.so` 的依赖链才找到 libc 符号的。现在显式 `NEEDED libc.so/libm.so/libdl.so`，
  链接改用 `-z defs`，并在 `build.sh` 里断言 NEEDED 三件套 + 静态 C++ 符号，防回归。

**5.6.4**

* **分区记忆改为「同步落盘 + 一变就存」**：`SharedPreferences.apply()` 在被划掉/被杀时会丢写，
  重开读到的是更早的旧快照（真机日志：store 6 区 → restore 读回 7 条旧记录）。
  现在 `commit()` 同步写 + 每次保存额外用 `fsync` 写一份 `files/zone-state.txt`（恢复优先读它）；
  焦点切换、区里换文件也会存（400ms 防抖）；恢复成功后立刻回写当前真实界面。
* 恢复容错：记录数超过上限只取前 6 条；形状数据不可用退回网格但保留区数/类型/文件/光标。

**5.6.3**

* **修「关掉软件不保存」**：5.6.2 的保存/恢复链路会静默失败——`saveLayout()` 拿不到区和格子的
  对应关系时直接返回 null，`saveZoneState()` 就悄悄不存了；恢复侧几个失败分支也不留痕迹。
  现在保存前先做一次「区 ↔ 格子」一致性自愈（清掉残留格子、给没格子的区补一个），
  失败原因写进 `files/zone.txt`；每次保存额外落一份 `files/zone-state.txt` 纯文本并在恢复时兜底；
  恢复时形状不可用不再丢整块，而是退回网格把区数/类型/文件/光标都恢复出来。
* `onDestroy` 再存一次；挤掉一个区的瞬间不再保存中间态。


**5.6.2**

* **修 5.6.1 真机反馈的「区域穿透 + 一片空地 + 拖不动」**：根因是「挤掉 / 关区」把被删格子的空间
  交给某一侧邻居时只改了对面那条边，邻居在另一个方向不等宽时那条边会悬空 —— 格子伸进隔壁、
  另一侧漏出空洞，坏布局还被「分区记忆」存了下来。现在新增 `PaneTiling.valid()/score()/repair()`：
  把容器切成单位格逐格数覆盖数（>1 重叠、0 空洞），用「把某条线挪到某个已有边界」的下降搜索
  把布局修成合法划分（空洞被邻居吃掉、悬空的边拉回对齐）；加区/挤掉/关区/均分/拖动松手/
  恢复分区/保存前都会调用，修不好就退回网格 —— 界面永远能用、永远拖得动。
* **恢复分区会先修再恢复**：5.6.1 存坏的分区不再整块丢弃，而是修好后原样回来；保存前也校验。
* **长按误入换位模式**：手指移动 > 2dp 就取消长按；换位/待替换模式给所有区铺一层淡色底，
  一眼能看出当前模式。
* 单测 `PaneTilingTest` 扩到 27 条（含用真机坏布局坐标复现 + 修复、空洞填充、合法阶梯不变）。


**5.6.1**

* **修「区域穿透」**：拖动分割线时不再只夹紧自己的最小尺寸，而是把全部格子放进约束
  （新 `PaneTiling.java`，纯 Java）：任何不引用这段线的格子都不能被碰到，夹紧位置正好落在
  隔壁那条线的坐标上（= 完美对齐，缝隙仍是一个 gap）。单独拖在本次方向被挡住、而整条相连的线
  一起动就能走时，自动升级成整线拖动；能独立拖的方向仍然只动这一段。每帧落子后还做一次
  重叠兜底校验，任何时刻都不会有两个区叠在一起。
* **马赛克整理更靠谱**：边界先按 ±2dp 聚类吸附再判定「完美网格」；同侧均分改用坐标判定
  （矩形范围相同即同一行/列），写入事务化、重叠整体回滚 —— 3×2 这类构图更容易一次对齐。
* **记住上次的分区**（新功能）：区数、拆分形状、每条分割线位置、每个区是编辑区/终端/解释器、
  每个编辑区打开的文件与光标、焦点区，全部在布局变化和进后台时保存；启动时恢复并等比缩放到
  当前屏幕，数据非法时自动退回网格排版。
* 新增 JVM 单测 `test/PaneTilingTest.java`（19 条：穿透复现 / 夹紧=对齐 / 整线更宽 /
  200+ 落子扫描 / 十字节点 / 快照编解码）。


**1.1**

* 文本宽度改为用 `Paint.getTextWidths()` 取真实字形步进，并按 token 的画笔分别测量：
  中文（双宽）、比例字体、粗体/斜体都不会再让光标、选区、波浪线错位。
* 每行宽度与行文本按「行版本号」缓存；只重算真正改动的那一行，打字时不再整屏重排。
* 撤销快照改为整篇扁平字符串（一次拷贝），回车/Backspace 不再逐行深拷贝。
* 语法检查防抖 260ms → 800ms，且同一 revision 不重复检查。
* 修复非等宽字体仍走等宽快路径的问题（不再依赖字体族猜等宽）。

**1.2.1**

* 配色只保留 RGB（取色器 6 位十六进制，保存/载入都按 RGB，透明度一律不透明）——
  旧版本存的 8 位 ARGB 值仍能正确读入。
* 修复输入法打字时括号/引号不自动配对：以前只有硬件键盘走 `insertTyped`，软键盘走
  `commitText` 直接插入原文。现在单字符提交统一走带配对的路径，回车仍保留自动缩进。
* 修复切换字体/字号后整屏宽度错乱（要再敲一个字才恢复）：主题变更时清掉所有已缓存的
  行宽数据，重新按新字体重算。

**1.3**

* 新增「品红·浅蓝」主题：关键词/类名用品红，内置函数/函数名/光标用浅蓝 rgb(50,200,255)。
* 取色器调色板加入 `#32C8FF` 浅蓝。
* 关于页显示签名「雨萱之华」。
* **签名证书换成 CN=雨萱之华, O=萱意永恒**（keystore.jks，别名 yuxuan；
  旧证书备份为 keystore-old-1.0.jks）。因为换了签名，从旧版本升级必须先卸载。

**1.4**

* 软键盘（输入法工具栏/Gboard 剪贴板面板）的复制、剪切、粘贴、全选、撤销、重做现在可用：
  实现了 `InputConnection.performContextMenuAction()`，并补上 `getSelectedText()`，
  否则输入法会认为"没有选中任何内容"而不显示复制按钮。
* 长按选词后弹出系统浮动工具条：复制 / 剪切 / 粘贴 / 全选 / 撤销 / 重做。
* `☰` 菜单新增 复制 / 剪切 / 粘贴。
* 硬件键盘支持 Ctrl+C / Ctrl+X / Ctrl+V。

**1.5**

* 滑动/惯性滚动、长按选词、点行号栏都不再弹出软键盘；只有点按正文才会调起键盘并定位光标。
* 括号未闭合期间的缩进不再报错：位于 `(` `[` `{` 续行内的行，跳过"缩进不是设定值倍数"
  与"缩进含 Tab"检查（Python 本来允许括号内自由对齐）；语句头检查也只在
  括号深度 0 的行生效，避免把括号内的 `class` 等词误判成缺少冒号。

**1.6.1**

* 行号栏不再被正文覆盖：正文（含选区、波浪线、光标）整体裁剪到行号栏右侧，
  横向滚动时文字从行号栏边缘"滑入消失"，行号始终固定在最上层。
* 行号栏与正文之间加一条细分隔线（取背景与行号色的混合，随主题变化）。
* 行号栏不再参与横向滚动，点它仍然是选中整行、不弹键盘。

**1.7 · 内置终端（Shizuku）**

* `☰ → 终端 / Shell…` 打开底部终端面板：可执行 `sh` 命令、看输出、按退出码提示，
  支持历史（↑）、快捷 `cd /sdcard`、清屏、收起、运行中"中断"。
* **命令优先经 Shizuku 以 shell（uid 2000）身份执行**，因此能直接读写 `/sdcard` 全盘；
  Shizuku 未连接或未授权时自动退回本应用身份（工作目录为 App 外部目录），面板标题会显示当前身份。
* 集成 Shizuku API 12.2.0（client / aidl / shared / provider 四个 jar 手打进 dex），
  manifest 增加 `moe.shizuku.manager.permission.API_V23`、`ShizukuProvider` 与 V3 支持标记。
* 终端是独立面板：打开时弹键盘、按返回键先收面板。

**1.8 · 菜单整理**

* 菜单只留常用：新建 / 打开 / 保存 / 另存为 / 最近文件 / **编辑 ▸**（全选、复制、剪切、粘贴、
  缩进、查看语法问题）/ 终端 / 设置。
* 设置页扩成真正的配置中心，新增：
  * 编辑器：语法检查开关、后台自动保存开关
  * 终端 · Shizuku：当前身份显示、请求授权、刷新状态、默认工作目录
  * 关于：版本号（读自 PackageManager）、签名、实现说明（原来菜单里的「关于」并入这里）
* 「字体与配色」入口并入「设置…」，不再单独占菜单项。

**1.9 · 远程自检**

* 长按标题栏（文件名）可把当前界面渲染成 PNG（半分辨率）、base64 写到
  `files/shot.b64`，README 里不用提功能入口 —— 仅用于开发期远程确认布局。

**2.0 · 可运行（内置 MicroPython）**

* 打包 MicroPython 1.24.1 **standard** 变体（交叉编译为 `lib/arm64-v8a/libmpyrun.so`，约 500 KB），
  工具栏 ▶ / 菜单「运行 ▶」把当前缓冲区写到 `cache/run/main.py`，用独立进程执行。
* 独立进程而不是嵌入：死循环可以「停止」杀掉，不会把 App 卡死。
* 运行面板：彩色输出、退出码、用时、清屏、收起、停止。
* **支持 `input()` 交互**：面板底部有输入行，回车/发送即写入程序 stdin。
* 修复：最初误用 `minimal` 变体导致浮点被裁掉，任何小数都报
  `decimal numbers not supported`，已换 standard（浮点/math/json/re/os/sys/time 全部可用）。
* 相对 CPython 的差异：标准库是精简版，没有 pip/numpy/requests/ssl；语法基本兼容 3.4+。

**2.1 · 双引擎（MicroPython / CPython 3.12）**

* 设置 → 运行引擎 可切换：MicroPython（默认，快、小）或 CPython 3.12（完整语法，支持 `match`）。
* CPython 3.12.8 交叉编译为 `lib/arm64-v8a/libcpython.so`（7.6 MB），标准库 530 个模块打成
  `assets/stdlib.zip`（2.6 MB），首次运行解到 `files/python/lib/python3.12`，用 `PYTHONPATH` 指过去。
* 交叉编译踩的 Android 坑（都写进 `tools/build_cpython.sh`）：
  * bionic 缺 glibc/BSD 符号：sem_clockwait、close_range、fdwalk、posix_spawn、chflags、
    fexecve、preadv2/pwritev2、copy_file_range、confstr、getloadavg、explicit_bzero/memset…
  * `pwd.getpwall()` / `grp.getgrall()` 依赖的 setpwent/getpwent 在 Android 上没有
  * clang 对 Android 目标默认「模拟 TLS」，要加 `-fno-emulated-tls`
  * Bionic 要求可执行文件 PT_TLS 段 64 字节对齐且 skew=0（`tools/fix_tls_align.py` + 一个
    `aligned(64)` 的 TLS 变量）
  * 静态内建模块只保留能编的 24 个（math/cmath/json/struct/array/datetime/select/哈希族…），
    没有 ssl/ctypes/sqlite/pip

**2.2 · 侧边栏 / 折叠 / 页签 / 片段**

* ☰ 改为打开左侧抽屉（整条不透明面板 + 编辑区半透明黑遮罩），点击遮罩或返回键关闭
* 顶栏快捷按钮：文件 / ▶ 运行 / 撤销 / 重做 / 保存（补全移入抽屉）
* 抽屉内：新建、保存、打开、另存为、最近、撤销、重做、补全、全选、粘贴、缩进、语法问题、
  展开/折叠全部、终端、设置，以及「打开的文件」列表（单击切换、长按关闭）
* 打开的文件按页签对象保存（文本 + 光标 + 脏标记），任意文本文件按 **UTF-8** 打开；
  只有 `.py` 走高亮 / 折叠 / 语法检查 / 补全，其它文件是纯文本（状态栏显示 `纯文本 · UTF-8`）
* 补全条数可设（3/5/8/12，默认 5），并且按类别配额：先每类出一个，再按分数补齐
* 常用片段补全：21 个内置片段（while / try / for / def / class / if / main / elif / else / tryf / trye / with /
  match / async / lambda / comp / dcomp / decor / prop / init / fori）；可在 **设置 → 代码片段** 改内置模板 /
  恢复默认 / 删除后恢复，也能新增自定义片段。模板支持**多个光标位**：`${cursor}`、`${cursor1}`、`${cursor2}`…
  插入后光标在第一个位，右下角出现 ↓ 跳转按钮，点一下跳到下一个位（跳转时落撤销快照）
* 代码折叠（原生侧按缩进 + 子句识别）：
  * if/elif/else → `if ... elif ... else ...`
  * while + try/except + else → `while ... else ...`
  * try/except/finally → `try ... except ...`
  * 连续 import / from ... import 合并为 `import ...`
  * 双击关键字折叠/展开；行号按可见行跳跃

**2.3 · 折叠修复 / 菜单收敛**

* 展开折叠时连带展开外层（否则展开了也看不见内容）；子层折叠状态保留（记忆）
* 顶栏去掉「文件」按钮，改为「常用」弹出菜单：保存 / 另存为 / 缩进 / 反缩进
* 抽屉收窄到 228dp；文件类命令收进「文件 ▸」分组，展开才显示
* 抽屉内不再重复 保存 / 另存为 / 缩进（已在「常用」里）

**2.4 · 折叠范围修正 / 菜单去重**

* 折叠前强制把整篇 lex 一遍——此前未 lex 的行 `blank` 默认为 true，导致缩进 4 的块把缩进 0 的后续行整段吞掉
* 折叠区间不再包含尾部空行（`def a():` 折到 `[1..4]` 而不是 `[1..5]`）
* 顶栏去掉「保存」按钮（「常用」里已有），抽屉去掉「撤销 / 重做」（顶栏已有）
* 原则：别处能点到的主菜单不再重复

**2.5 · 折叠改在 Java 侧计算**

* 真机仍出现「折 def 把后面 if 也吞掉」：native 折叠库与安装包 md5 一致，说明区间没问题，
  问题出在跨 JNI 的折叠缓存/行映射。2.5 起折叠**完全在 Java 里按行文本计算**：
  去注释 → 取缩进 → 判断行尾冒号的关键字 → 按缩进和子句（else/elif/except/finally/case）确定区间，
  import 连续段单独合并。native 的 folds 接口保留但不再使用。

**2.6 · 折叠规则收紧（按用户建议）**

* 折叠时行文本改走 `nativeLineText`，不再用带缓存的 `line()`（缓存里没取到的行会返回空串，
  被当成空行 → 整篇被吞进折叠区，这才是"一路吞到末尾"的真凶）
* 规则：空行 / 注释行不算断块；缩进更小的**非注释非空行**立刻结束；子句必须同缩进

**2.8 · 折叠后内容变空的真因**

* 区间一直是对的（logcat：`n=21 folds=18-20 4-7 10-15 11-12 14-15`），坏在渲染：
  每帧向 native 取 [起始行..结束行] 的 token 记录后，行循环是按**可见行**走的；
  折叠隐藏的行不会进循环，它们的记录没人消费 → `runBuf` 游标卡在被隐藏的行上，
  后面所有行都匹配不到 → 整片空白。
* 修法：进入每行绘制前先 `while (runBuf[idx] < i) idx += 4;`，把隐藏行的记录跳过。

**3.4–4.5 · 摘要**

* 3.4 撤销合并时间窗、参考线按块渐变、查找/替换雏形
* 3.5–3.8 缩进参考线的空行规则逐步收紧（最终：空行看块是否延续）
* 4.x 解释器 REPL、pip 依赖自动安装（读 `Requires-Dist`）、C 编译器仓库设置页（下载/本地导入/探活）

**4.6 · 查找替换补齐 / pip 增强 / 参考线可配色**

* 查找 / 替换重写（4.6 先做成弹窗 `FindReplaceDialog`，4.6.2 改为底部常驻查找栏 `FindBar`）：
  * 实时结果计数「共 N 处」，定位时显示「第 n / 共 N 处」
  * 查找与替换串支持 `\n` / `\t`（可跨行匹配、可插入多行）
  * 新增「正则」开关：MULTILINE、可选忽略大小写，替换支持 `$1` / `\1` 分组；「全词」会加词边界
  * 全部替换改成整篇一次写回（新原生接口 `nativeReplaceWholeText`），**一个撤销步骤**即可全恢复；替换后自动统计剩余匹配
  * 修掉替换提示被截断、以及输入即统计的防抖
* 包管理：
  * 列表拆出「包名 + 版本」两行，本地 `.py` 标「本地模块」
  * 每个包可展开**递归依赖树**（深度 ≤ 3、防环），未安装依赖标红并汇总「缺 N 项」
  * 复选框多选 +「全选 / 清空 / 卸载选中 (n)」，确认框列出将删除的目录；依赖只装不级联删
  * 修掉安装日志无限变高把包列表挤成 0 高度的问题（日志区固定 110dp 并自动滚到底）
* 编辑器外观：
  * 参考线颜色可自定义（第 1 层 → 最深层两段颜色线性过渡），新增「显示缩进参考线」开关，设置页预览同步绘制参考线
  * 片段从 7 个扩到 21 个（elif / else / tryf / trye / with / match / async / lambda / comp / dcomp / decor / prop / init / fori）
* 修复：
  * 设置子页返回时，上层旧 Activity 的 `onPause` 用旧主题整篇覆盖 → 新改的颜色丢失（去掉覆盖保存，改为 `Theme.saveCount` 变化时按需重载）
  * 切主题后底部状态栏与抽屉不换色
  * 「编辑器」页里显示行号 / 参考线的开关会因 `preview == null` 空指针崩溃

**4.6.1 · 回车卡顿 / 行号不刷新**

* Enter 走硬件键或 IME `sendKeyEvent` 时，`onKeyDown` 里只改了缓冲、没有 `refreshAfterEdit()`：
  行号与底部「行/列」要等 530ms 光标闪烁那次重绘才更新，看起来就是「换行后不刷新」→ 补上刷新调用
* 回车卡顿的主因是折叠/参考线扫描：`ensureFolds()` 每行一次 JNI（`nativeLineText`），后面还有 3 轮同样逐行 JNI，
  3000 行文件按一次回车就是上万次跨 JNI 调用 → 改成整篇一次 `nativeGetText()` 后在 Java 里 `split("\n")`，
  后续遍历全部复用该数组；同时删掉每次重算都拼字符串写 logcat 的 `PYE_FOLD` 调试日志
* 空白行取下一段缩进（`nextCodeIndent`）改走按行版本缓存的 `line()`
* `Doc::newline()` 的 `snap(false)` 改为 `snap(true)`：回车不再每次整篇拷贝快照，与连续输入合并成一批撤销

**4.6.2 · 查找替换改成底部查找栏**

* 不再弹对话框，改成贴在编辑区下方、状态栏上方的常驻栏（与终端面板同风格）：
  * 标题行：`查找 / 替换` + 右侧实时状态（共 N 处 / 第 n 共 N 处）+ `收起`
  * 查找行：输入框 + `Aa`（忽略大小写）/ `W`（全词）/ `.*`（正则）三个小开关 + `↑` `↓`
  * 替换行：输入框 + `替换` / `全部`
  * 按钮 26dp 高、标签尽量短；返回键先收栏，`收起` 同时收键盘
* 查找栏非模态：改完编辑区再点查找会检测 revision 自动重算匹配；主题切换时整栏跟着换色

**4.6.3 · 开关文案 + 发布目录约定**

* 查找栏小开关改名：`Aa`（忽略大小写）/ `全词`（完整单词，原 `W`）/ `Re`（正则，原 `.*`），长按弹一句解释
* 发布约定：每个版本放到 `Download/PyEditor/`，里面放 `PyEditor-<版本号>.apk` 和 `版本速览-<版本号>.md`

**4.7 · C 扩展编译（Shizuku）**

* 设置 → 编译器新增：
  * **Python 头文件**：不打包进 APK，用户「从本地导入」`pyinclude-3.12.tgz` 或填地址下载；解到 `files/pyinclude/Include`
  * **编译 C 扩展**：选 `.c` + 模块名 → 用 Shizuku(shell) 在 `/data/local/tmp` 编译 → `.so` 装到 `site-packages/<模块>-c/` → 自动 `import` 验证
* 传输方式：App 把源码/头文件/编译器放到 App 外部目录（shell 可读），shell 复制到 `/data/local/tmp` 并 `chmod 755`；产物写回外部目录
* 编译参数：`-shared -fPIC -O2 -Wl,-z,max-page-size=16384 -Wl,--allow-shlib-undefined`；Zig 用 `zig cc -target aarch64-linux-android24`，不认该 target 时自动退回 `aarch64-linux-android`
* 头文件包由 `tools/make_pyinclude.sh` 从 CPython 3.12.8 源码生成（含 `Include/cpython`、`Include/internal`、Android `pyconfig.h`），约 270 KB，随版本发布在 `Download/PyEditor/`

**4.8 · 下拉来源 / 引擎按钮**

* 编译器与 Python 头文件来源都改成 Spinner 下拉：
  * 编译器：Zig 0.15.2 / Zig 0.17.0 / NDK r27c / LLVM 19 / TinyCC / 自定义
  * 头文件：本地 pyinclude / 华为云 / 阿里云 / python.org 官方 CPython 3.12.8 / 自定义
* 官方源码（20 MB tar.xz）只提取 `Include/`，再补 App 内置的 Android `pyconfig.h`（56 KB）
* 运行引擎 `MPy` / `CPy` 按钮移到终端面板标题栏，设置里的「运行」页移除
* 明确 C 扩展目前只支持 `.c`，`.cxx/.cpp` 暂不支持

**4.8.1 · 面板多级高度 / 多行签名折叠**

* 终端与解释器（RunPanel）标题栏新增 `0` `1` `3` `5` `全` `收`：
  * 0 只留标题按钮；1 输入行 + 1 行输出；3/5 多行输出；全 = 吞掉编辑区（同时只允许一个面板全屏）；收 = 关闭
  * 全屏由 MainActivity 协调：一个面板全屏时把另一个从全屏挤下来，并隐藏编辑区；退出/关闭后恢复
* 修复括号跨行的块头无法折叠：
  * `def foo(` / `a,` / `b` / `):` 会按括号配平拼成逻辑行，最终以 `:` 结尾就折叠
  * 同样适用于 `class` / `if` / `for` / `while` / `with` / `match` / `async def`

**4.9 · 移除 MicroPython，只留 CPython 3.12**

* 删除 `libs/micropython/libmpyrun.so` 与 `build.sh` 的打包行，APK 从 12.83 MB 降到 12.30 MB（少 519 KB）
* 终端标题栏去掉 `MPy` / `CPy` 切换按钮；运行引擎固定 CPython 3.12
* 清理全部引擎分支/环境注入：`Prefs.runEngine`、`MICROPYPATH`、MicroPython 启动参数（`-X heapsize`）、双引擎试 import
* `RunPanel` 标题固定显示 `(CPython 3.12)`；设置里的「运行」页只留说明

**4.9.1 · 标准库改 tar.xz**

* `assets/stdlib.zip`（2,622,760 B）→ `assets/stdlib.tar.xz`（1,688,784 B，LZMA2 preset 6），删掉 zip 解压代码
* `ensureStdlib()` 复用 `CompilerStore.extract()` 的 tar.xz 解压器，首次运行解到 `files/python/lib/python3.12`
* APK 12,301,064 → 11,395,762 B（少 905,302 B ≈ 884 KB）

**4.9.2 · R8 代码混淆**

* `build.sh` 先把 `java/com/dsh/pyedit` 复制到 `build/obfuscated_java`，用 `tools/strip_java_comments.py` 删除注释再编译
* dex 从 D8 改成 **R8**，`tools/proguard-rules.pro` 白名单：
  * keep `App / MainActivity / SettingsActivity / PipActivity`（清单/反射）
  * keep `Native` 与所有 `native` 方法（JNI 符号名）
  * keep 所有 `on*` 方法（生命周期/回调）
  * keep Shizuku / XZ 外部库
* 其余类名/方法名/字段名重命名、死代码删除；`classes.dex` 387,084 → 315,516 B
* 没用源码逐字替换：会误伤回调/JNI/字符串，R8 在字节码层等价且安全

**源码备份（4.9.2）**

* `tools/minify_java.py`：删注释、去缩进/空行、每个 .java 合并成单行；已用 javac 验证编译通过
* 原始版 + 压缩版各存三处：`Download/DSHA/PyEditor-src-4.9.2/`、`/sdcard/临时/`、`/sdcard/代码/编程/`
* 另有 `Download/PyEditor/PyEditor-4.9.2-src.tar.gz`

**5.0.0 · 返回手势 / 预测性返回**

* `AndroidManifest.xml` 开启 `android:enableOnBackInvokedCallback="true"`
* 新增 `BackCompat`：Android 13+ 用平台 `OnBackInvokedDispatcher` 注册回调，低版本走 `onBackPressed`（不引入 AndroidX，避免 Kotlin/AndroidX 体积）
* 分层返回：查找栏 → 抽屉 → 终端 → 运行/解释器 → 补全 → 未保存确认 → 退出
* 设置/编译器子页返回目录页；抽屉沿用滑出动画
* 编辑区最左 + 光标行首时右滑打开抽屉
* R8 keep：`BackCompat`、`OnBackInvokedCallback` 实现与 `onBackInvoked()`
* 构建改用 build-tools 的 aapt2（x86_64 经 qemu）处理 API 35 的 `enableOnBackInvokedCallback`

**5.0.1 · 预测性返回跟手动画**

* `BackCompat.registerAnimated()`：API 34+ 注册 `OnBackAnimationCallback`，替代普通 `OnBackInvokedCallback`
* 返回手势进行中按 `BackEvent.getProgress()` 驱动视觉：
  * 抽屉 `translationX = -width * progress`、遮罩淡出
  * 查找栏 / 终端 / 运行面板下滑 + 淡出
  * 取消时 140ms 复位；完成时关闭对应层并复位
* API 33 无跟手进度，仍只做手势结束关闭；R8 增加 `OnBackAnimationCallback` keep

**5.0.2 · 设置页单 Activity 重做**

* 目录页点条目不再 `startActivity` 新的 SettingsActivity，而是在同一 Activity 内 `goPage()`：
  * 直接清空当前内容、拼对应子页、标题栏同步
  * 返回：子页 → 目录页，目录页 → 关闭设置（预测性返回回调同一套）
* 解决了子页标题总是“设置”、返回层级依赖 Activity 堆叠的问题

**5.0.3 · 设置 View 栈**

* 单 Activity：固定顶栏 + FrameLayout 容器；主页 View 隐藏保留，子页动态生成压栈
* 返回出栈并恢复上一页/标题；栈深 1 关闭设置
* 压栈/出栈 180ms 横向滑动；API 34+ 预测返回按 progress 跟手右移
* R8 keep `SettingsActivity`、`BackCompat$**`、`OnBack*Callback` 与全部回调方法

**5.0.4 · 预测返回修复：手势中能看见上级页**

* 问题：`pushPage()` 进子页时立刻把上一页 `GONE`，`predictiveProgress()` 只移动当前页，
  子页右移后下面是容器背景 → 预测性返回看不到上级内容
* `predictiveStart()`：手势开始先让上一页 `VISIBLE`（z 序在下），当前页右移时露出真实内容
* `predictiveProgress()`：当前页 `translationX = w * progress`、`alpha = 1 - 0.15p`；
  上一页 `translationX = -0.18w * (1 - p)` 做层叠视差
* `predictiveCancel()`：140ms 回弹后才重新隐藏上一页（`pageGen` 防止收尾误伤新页面）
* 压栈也改成“滑完再隐藏上一页”；新增 `syncPageVisibility()` / `removeOrphanPages()`
* 修掉手势打断压栈/出栈动画后 `pageAnimating` 永远为 true、返回全失效的隐患

**5.1.0 · 任意文本 + 多行字面量折叠 + 可编辑片段**

* 任意文本文件按 UTF-8 打开：`*/*` 选择器 + `text/*`/json/xml/js 外部打开；SAF 用
  `OpenableColumns.DISPLAY_NAME` 取真实文件名判断扩展名
* 只有 `.py` 才高亮 / 折叠 / 语法检查 / 补全；其它文本整行单色、无波浪线、无折叠，状态栏 `纯文本 · UTF-8`
* 多行 list / dict / tuple / set 折叠，摘要 `cfg = dict ...` / `items = list ...` / `pt = tuple ...` /
  `tags = set ...`（`{…}` 看直接内容层有无 `:`/`**` 区分 dict/set；支持 `self.x =`、类型标注、
  `dict(`/`list(`/`set(`/`tuple(` 构造；`==`/`+=`/`print([`/`return [`/未闭合不折；字符串与注释里的括号不干扰）
* 片段系统重做：内置 21 个可改模板 / 恢复默认 / 删除后恢复；自定义片段（名称 + 模板 + `${cursor}` 最终光标）；
  补全改由 `Snippets` 注册表统一提供（原生片段名在 Java 侧过滤），改完立即生效
* 新增 `FoldScan.java`（纯 Java，可 JVM 单测，32 例全过）与 `Snippets.java`（SharedPreferences 持久化）

**5.2.0 · 行尾标注（集合类型 / 函数引用 / 类成员）**

* 集合字面量：单行行尾标注类型（`items = [1, 2]  list[int]`），多行折叠摘要带类型
  （`cfg = dict[str, int] ...`）；元素种类最多写两种，超过写 `Any`；dict 键、值两侧各自判断
* 自定义函数：行尾 `被使用 N 次`，点这段字打开查找/替换栏并自动填好函数名
* 自定义类：行尾 `N 个属性 · M 个方法`（`self.x =` / 类体同级 `x =`；类体同级 `def` 计方法）
* 新增 `SymbolStats.java`（纯 Java 标识符统计，跳过字符串/注释/三引号）；`FoldScan` 扩展单行 + 类型推断
* JVM 单测 49 例全过

**5.2.1 · 单行集合也能折叠**

* `items = [1, 2, 3]` 这类单行字面量现在双击也能折叠，折叠后整行显示 `items = list[int] ...`
  （行数不变，只隐藏元素）；`展开/折叠全部` 也包含它们
* 单行折叠期间一编辑就自动展开，不会改到看不见的正文
* 折叠摘要统一带元素类型（单行与多行同一套推断）
* 单测源码放进 `test/ScanTest.java`（49 例）

**5.3.0 · 中英双语**

* 新增 `Lang`：字符串仍以中文书写，显示时查字典翻译成英文（400+ 条），
  设置 → 语言 / Language 可切「跟随系统 / 简体中文 / English」，切换后自动重启界面
* 清单 label 用 `res/values` + `res/values-zh` 资源，随系统语言
* 英文模式下欢迎文档、状态栏、行尾标注、补全标签、语法问题、对话框与 toast 全部为英文

**5.4.0 · 多编辑区 + 手势修复 + 应用名 YHHYPy**

* 多编辑区：设置 → 编辑器 → 开启多编辑区；手机最多 2 个、平板 4 个；顶栏 + 新建；抽屉点文件在多区时进入
  「点哪个区替换哪个」的待替换状态（各区微亮）；无 × 按钮——拖分割线把区挤到 < max(40dp,10%) 松手销毁并重排；
  长按分割线进入换位模式，拖/点两个区交换 View 实例（文件、滚动、折叠都跟着走）
* 布局算法：1 全屏 / 2 左右 / 3 左主 50% + 右上下 25% / 4 2x2；每区独立 native 文档与 scrollX/scrollY，永不折行；
  底部行/列状态栏由「显示状态栏」按钮独立开关（默认显示；不再随多编辑区自动隐藏）
* 修右侧滑：先 32dp 死区，之后按 (dx−32dp)/240dp 阻尼跟手，不再一碰就弹开抽屉
* 修设置预测返回：当前页保持不透明只位移，上一页从 −22% 跟出、0.72→1 变亮，两层不再文字叠影
* 应用名改为 **YHHYPy**

**5.4.1 · 抽屉可滚动 + 竖屏上下分屏 + 设置页返回不再叠影**

* 抽屉菜单整列放进 `ScrollView`：菜单项和「打开的文件」一起滚，不再被屏幕高度截断（之前文件列表点不到）
* 多编辑区按屏幕方向切换：竖屏 2 个上下、3 个上主下双；横屏 2 个左右、3 个左主右双；4 个始终 2x2
* 设置子页的页面 View 铺 `theme.bg` 不透明背景；推入/弹出动画去掉 alpha 交叉；
  预测返回时上一页固定不动、当前页只做位移 —— 两层不再文字重叠

**5.4.2 · 横屏去掉常驻状态栏**

* 横屏时隐藏顶部状态栏、代码区使用整个高度；竖屏恢复普通窗口
* 设置 `LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES` 并按刘海安全区补左右内边距，横屏文字不会被挖孔盖住
* 旋转时由 `onConfigurationChanged` 重新应用，主界面 / 设置页都生效

**5.4.3 · 片段多光标 + 更多折叠 + 关于页更新**

* 片段模板支持多个光标位：`${cursor}` / `${cursor1}` / `${cursor2}`…（带数字按数字顺序，不带数字按出现顺序排在后面）；
  插入后光标停在第一个位，光标右下出现 ↓ 悬浮按钮，点击跳到下一个，没有后续位时按钮消失
* 输入、回车、退格、中文组合输入时动态平移后续占位符的位置；插入片段、每次点跳转按钮都各落一个撤销快照
* 折叠：连续的同名函数（中间空行/注释不断开）合成一个折叠块；连续简单赋值折叠成 `5 Value = int` 这样的摘要
* 关于页改成「Python 3.12 编辑器 + 运行环境」的介绍（能运行代码、pip、C 扩展编译）

**5.4.4 · 连续同名调用折叠 + 片段页兜底**

* 连续同名函数调用折叠：`print(a,b,c)` / `print("gbjj")` / `print(bool)` → `print() * 3`
  （允许空行/注释间隔；赋值、def、行尾还有别的语句都不算）
* 设置页/片段页加了加载兜底：某页构建异常时提示「该页加载失败：…」，不再整页崩溃退回编辑区

**5.4.5 · 片段页修复（正则转义）**

* 修复设置 → 代码片段 打不开：`Snippets.preview` 里的 `replaceAll("\$\{cursor[0-9]*}")` 在 Java 里 `}` 被当成量词结尾报
  `PatternSyntaxException`；改用 `SnippetTemplate.preview()` 手写扫描，不再编译正则
* 片段页的加载兜底保留（异常会提示「该页加载失败：…」而不是退回编辑区）

**5.4.6 · 片段占位符顺序修正**

* `${cursor}`（不带数字）= 默认位置，**先跳**，多个按出现顺序；之后 `${cursor1}`、`${cursor2}` 按数字从小到大
  （5.4.3 把不带数字的排到最后，导致初始光标和 ↓ 按钮顺序都不对）
* 片段页提示文案同步改成「不带数字的默认位置先跳，再按数字从小到大」

**5.5.0 · 行分隔线 + 右侧大纲导航（MiniMap）**

* 行分隔线：设置 → 个性化 → 「显示行分隔线」开关 + 取色器（默认极淡灰 `#DCE1E7`，约 30% 不透明度绘制）；
  按可见行（折叠后的 row）画在文字下沿，滚动 / 折叠都不错位；设置页预览同步
* 右侧大纲导航 MiniMap：设置 → 编辑器 → 「启用右侧大纲导航（MiniMap）」（默认开）。
  （5.5.0 原为「右边缘 20dp + 手势排除」，5.5.1 已改成「横向到最右后任意位置左滑」，见下）
  打开时通过 `PaneHost` 把 EditorView **挤压** 56dp，不悬浮遮盖正文；点正文 / 其它区 / 抽屉 / 面板 / 返回即收起
* 渲染：`DocOutline` 扫顶层 def/class 与内部方法（最多 400 块），按「行号 / 总行数」映射成彩色块
  （class 用类色、函数用函数色、方法压暗缩短）；语法错误行按比例画红点（最多 240 个）；另画当前可见区域框；
  **只画色块，不画文字**
* 导航：在侧边栏上下滑，`targetScrollY = touchY / sidebarHeight * totalScrollHeight`，正文 `scrollY` 实时跟手
* 多编辑区：每区一个 `PaneHost` / `MiniMapView`，开几个区各自独立，换位 / 挤掉后状态跟着区走；同时只展开一个
* 其它：`PaneLayout` 分割线命中区只向右/下扩展 10dp，把左/上区的最右边缘让给呼出手势；
  R8 keep `PaneHost` / `MiniMapView` / `DocOutline`；新增 `test/MiniMapTest.java` 13 例（总计 93 例全过）；
  APK 10.88 MiB（上限 11.5 MiB）

**5.5.1 · MiniMap 手势与菜单对齐 + 语法检查补赋值目标**

* 呼出 MiniMap 不再死磕屏幕右边缘：横向已经到最右（`scrollX >= maxScrollX`）时，编辑区**任意位置**向左滑
  >24dp 即可呼出 —— 与左侧菜单「横向到最左 + 向右滑」完全对称。删掉了右边缘 20dp 判定和
  `setSystemGestureExclusionRects`，系统返回手势不再被抢；短行文件 `maxScrollX==0`，等于随处可呼出
* 语法检查新增两类错误（原生 `runCheck`）：赋值目标非法（`4 = 1`、`x + 1 = 2`、`f() = 1`、`if x = 1:`、
  `None = 1`、`[1] = [1]`、`{a} = 1`、`4 += 1`、`a,,b = 1`、`= 1`）与缺少右值（`x =`），
  消息 id `M_INVALID_TARGET` / `M_MISSING_RHS`，中英文案同步
* 规则对齐 CPython：不误报关键字参数 / `def` 默认值 / 装饰器参数 / lambda 多个默认值 / 类型注解 /
  3.12 类型别名（含类型参数）/ 软关键字 `match`、`case` / 单行复合语句 `if x: y = 1` / 反斜杠续行 /
  空目标 `[] = x`、`() = x` / 字面量的属性与下标 `None.x`、`"s"[0]`、`1 .real` / 调用后属性 `f().x`
* 测试：`test/CheckTest.cpp` 85 例全过；新检查扫 CPython 3.12 标准库 + CPython `Lib/` + dist-packages
  （数千文件）**0 误报**；JVM 93 例（ScanTest/SnippetAssignTest/MiniMapTest）全过
* APK 10.89 MiB（上限 11.5 MiB），`5.5.1 / 77`

**5.5.2 · 注释缩进 / 状态栏 / 折叠菜单与子句**

* 语法检查：**三引号 / docstring 内部的行不再检查缩进**（`runCheck` 增加 `strStart == 0` 条件），
  注释里随手写的 Tab / 非 4 倍数缩进不再报波浪线；正文代码仍照常检查
* 竖屏偶发状态栏消失：API 30+ 改用 `WindowInsetsController`（横屏 `hide`、竖屏 `show`），
  不再和 legacy `IMMERSIVE_STICKY` 混用；`onResume` / `onWindowFocusChanged` / 设置页 `onResume`
  重新 apply，横屏切回、后台回来、对话框关闭后都能恢复竖屏状态栏；并按 `statusBg` 亮度切换状态栏图标明暗，
  浅色主题下不再“一片白像消失”
* 抽屉折叠范围：**折叠所有** / **折叠关键字**（控制流块 + 子句 + import 段）/
  **折叠多行赋值和函数**（`def`/`class` + 多行字面量 + 连续赋值 + 连续调用）；另有「展开全部」；
  `EditorView.foldKind` 记录每块类别（5.5.3 起入口改成抽屉内联子菜单）
* **子句可单独折叠**：`else / elif / except / finally / case` 各自有折叠区间，双击子句行只折该子句体
  （摘要 `else ...` 等），父块合并子句的旧行为保留
* 单测：`test/CheckTest.cpp` 90 例全过（新增 5 个注释缩进用例）；JVM 93 例全过；标准库扫描 0 误报
* APK 10.89 MiB（上限 11.5 MiB），`5.5.2 / 78`

**5.5.3 · 折叠入口改成抽屉内联子菜单**

* 5.5.2 的 `PopupMenu` 换成和「文件 ▸」一致的抽屉内联分组：**折叠 ▸** 原位展开
  「折叠所有 / 折叠关键字 / 折叠多行赋值和函数 / 展开全部」，箭头 `▸/▾` 切换，选中子项后收起抽屉
* 折叠粒度、`EditorView.foldKind`、子句折叠、docstring 缩进、竖屏状态栏修复均沿用 5.5.2
* APK 10.89 MiB（上限 11.5 MiB），`5.5.3 / 79`

**5.5.4 · 语法检查扩展 + 选区手柄**

* 语法检查新增 13 类（合计 24 类）：关键字当 def/class 名字、顶格后意外缩进、参数重名/默认值顺序、
  调用位置参数跟在关键字参数后、import/from、数字字面量（前导零/1.2.3/0x/0b102/0o8/1_/1e）、
  模块级 await/yield、`x = *[..]` / `x = **{..}`、孤立 else/elif/except/finally/case、
  `type Alias` 缺 `=`、f-string（`{}` / `{x` / `!z`，支持 PEP 701 嵌套引号）、`except* :`、
  单行字符串未闭合；`test/SyntaxTest.cpp` 91 例 + `CheckTest.cpp` 90 例全过，
  用户提供的 `py312_syntax_errors.py` 28 处 `#不通过` 全命中，标准库 0 误报
* 选区手柄：选中文字后两端各出现一个圆形手柄，拖动实时调整选区（另一端固定），
  拖到上下边缘自动滚动，松手后重新弹出复制/剪切/粘贴工具条
* APK 10.92 MiB（上限 11.5 MiB），`5.5.4 / 82`

**5.5.4 回退包（versionCode 82）**

* 删除 5.5.5 的「CPython compile 4.0」，恢复 24 类原生语法检查（含你那份 28 条用例）；版本名回到 5.5.4
* 设置 → 编辑器新增「显示状态栏」按钮，顶栏新增「状态栏」快捷按钮；多编辑区不再自动隐藏底部状态栏
* versionCode 82（覆盖已装的 5.5.5/81；没装过也能直接升），APK 10.92 MiB

**5.6.0 · 多区 / 自定义主题 / 竖屏沉浸**

* 多编辑区升级为**多区**：一个区可以是编辑区、Shell 终端或 CPython 解释器；
  顶栏 `+` 三选一；终端/解释器作为区时去掉 0/1/3/5/全 分级按钮（大小交给分割线）；
  换位方式不变，终端/解释器没有文件可换；`▶` 运行**当前焦点**编辑区的文件
* 多区改成**自由拆分**：`+` 选类型 + 右侧/下方，任意组合都能拼，上限 6 个区；
  设置里的 1×2…1×6 只是「一键重排」，每条分割线都能拖
* 「行/列 + 语法问题」状态栏：横屏 / 竖屏各有 **显示开关 + 顶部/底部位置**，另有「在常用栏中显示」；快捷切换在「常用」菜单
* **竖屏也隐藏 Android 系统状态栏**（以前只有横屏），刘海按 top 安全区内缩
* 删除 Monokai / Solarized 两个英文内置主题，新增**多命名自定义主题**（存 App 内，可切换/删除）
* APK 10.94 MiB（上限 11.5 MiB），`5.6.0 / 83`
