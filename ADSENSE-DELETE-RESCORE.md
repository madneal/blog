# Delete 列表：扩写后保留结论

已对原 26 篇全部扩写（补背景、步骤、坑点、小结；修正明显标题错误）。

## 结论一览

| 原 units | 现 prose | 现 full* | 判定 | 标题 |
|--------:|---------:|---------:|------|------|
| 12 | 544 | 546 | `DROP` | 米哈游内推（历史记录） |
| 131 | 209 | 338 | `KEEP_WEAK` | MATLAB：批量 load 后按文件名重命名变量 |
| 137 | 223 | 256 | `KEEP_WEAK` | 每日一练：直接插入排序（C++） |
| 251 | 224 | 313 | `KEEP_WEAK` | 一道简单却易错的数组输入输出题 |
| 155 | 253 | 313 | `KEEP_WEAK` | 常用颜色的 RGB 值速查与色彩模型笔记 |
| 121 | 257 | 324 | `KEEP_WEAK` | 验证歌德巴赫猜想：偶数拆成两素数且乘积最大 |
| 113 | 268 | 349 | `KEEP_WEAK` | LaTeX 画一张简单三线表 |
| 267 | 285 | 328 | `KEEP_WEAK` | OpenCV：IplImage 与 Mat 该用哪个？ |
| 298 | 288 | 338 | `KEEP_WEAK` | 剑指 Offer：二维数组中的查找 |
| 177 | 335 | 434 | `KEEP` | 简易车道线检测 Demo：OpenCvSharp 与 C++ OpenCV |
| 231 | 343 | 380 | `KEEP` | LaTeX 中 \large 的作用域：为什么第一种写法会「污染」后面全文 |
| 82 | 345 | 600 | `KEEP` | 原生 JS 实现图片轮播：结构、样式与交互 |
| 62 | 346 | 462 | `KEEP` | LaTeX 算法环境：去掉 algorithmic 自动行号 |
| 63 | 369 | 549 | `KEEP` | 单链表线性表：初始化、插入、遍历与有序合并 |
| 23 | 383 | 509 | `KEEP` | LaTeX 表格脚注：用 threeparttable 给表格加注释 |
| 32 | 412 | 521 | `KEEP` | WinForms DataGridView：CheckBox 列的全选与取消全选 |
| 110 | 426 | 604 | `KEEP` | WinForms 里用 HTTP POST 上传文件的正确姿势 |
| 70 | 428 | 491 | `KEEP` | 如何查找 Django 的安装路径与版本信息 |
| 84 | 519 | 615 | `KEEP` | HTTP 状态码速览：从 2xx 成功到 5xx 服务器错误 |
| 63 | 531 | 563 | `KEEP` | 柯西分布：密度、标准型与为何「均值不存在」 |
| 0 | 592 | 814 | `KEEP` | 如何将网络流转化为内存流（C#） |
| 42 | 668 | 814 | `KEEP` | 差分进化（DE）算法原理与 MATLAB 示例 |
| 105 | 818 | 839 | `KEEP` | 用 Burp MCP 把代理能力接进 Claude CLI |
| 104 | 840 | 885 | `KEEP` | SameSite 的七八事：Chrome 默认 Lax 之后，SSO iframe 为什么挂了 |
| 23 | 855 | 856 | `KEEP` | 安全与开发常用在线工具清单（持续整理） |
| 20 | 1079 | 1171 | `KEEP` | Jenkins SAML SSO 插件中的 XXE 与 SSRF（CVE-2023-32991 / CVE-2023-32992） |

\* full ≈ 含代码的汉字+标识符，反映技术文真实体积。

## 详细说明

### 米哈游内推（历史记录）

- 路径：`content/post/mihoyo.md`
- 原 → 现：`12` → prose **544** / full **546**
- **判定：`DROP`** — 内推二维码页，无长期技术价值；已改成归档说明，仍建议 draft/下线

### MATLAB：批量 load 后按文件名重命名变量

- 路径：`content/post/matlab批量修改变量的名称.md`
- 原 → 现：`131` → prose **209** / full **338**
- **判定：`KEEP_WEAK`** — 能留，但建议继续加案例或并入系列

### 每日一练：直接插入排序（C++）

- 路径：`content/post/每日一练--直接插入排序.md`
- 原 → 现：`137` → prose **223** / full **256**
- **判定：`KEEP_WEAK`** — 能留，但建议继续加案例或并入系列

### 一道简单却易错的数组输入输出题

- 路径：`content/post/一个简单的输入输出算法题.md`
- 原 → 现：`251` → prose **224** / full **313**
- **判定：`KEEP_WEAK`** — 能留，但建议继续加案例或并入系列

### 常用颜色的 RGB 值速查与色彩模型笔记

- 路径：`content/post/常用颜色的RGB分布.md`
- 原 → 现：`155` → prose **253** / full **313**
- **判定：`KEEP_WEAK`** — 能留，但建议继续加案例或并入系列

### 验证歌德巴赫猜想：偶数拆成两素数且乘积最大

- 路径：`content/post/歌德巴赫猜想.md`
- 原 → 现：`121` → prose **257** / full **324**
- **判定：`KEEP_WEAK`** — 能留，但建议继续加案例或并入系列

### LaTeX 画一张简单三线表

- 路径：`content/post/如何用latex画一个简单的表格.md`
- 原 → 现：`113` → prose **268** / full **349**
- **判定：`KEEP_WEAK`** — 能留，但建议继续加案例或并入系列

### OpenCV：IplImage 与 Mat 该用哪个？

- 路径：`content/post/Iplimage versus Mat.md`
- 原 → 现：`267` → prose **285** / full **328**
- **判定：`KEEP_WEAK`** — 能留，但建议继续加案例或并入系列

### 剑指 Offer：二维数组中的查找

- 路径：`content/post/剑指offer学习读书笔记--二维数组中的查找.md`
- 原 → 现：`298` → prose **288** / full **338**
- **判定：`KEEP_WEAK`** — 能留，但建议继续加案例或并入系列

### 简易车道线检测 Demo：OpenCvSharp 与 C++ OpenCV

- 路径：`content/post/道路识别demo.md`
- 原 → 现：`177` → prose **335** / full **434**
- **判定：`KEEP`** — 扩写后结构完整；厚度中等但可公开保留（非最优）

### LaTeX 中 \large 的作用域：为什么第一种写法会「污染」后面全文

- 路径：`content/post/latex中large的作用域问题.md`
- 原 → 现：`231` → prose **343** / full **380**
- **判定：`KEEP`** — 扩写后结构完整；厚度中等但可公开保留（非最优）

### 原生 JS 实现图片轮播：结构、样式与交互

- 路径：`content/post/使用js实现图片轮滑效果.md`
- 原 → 现：`82` → prose **345** / full **600**
- **判定：`KEEP`** — 扩写后结构完整；厚度中等但可公开保留（非最优）

### LaTeX 算法环境：去掉 algorithmic 自动行号

- 路径：`content/post/latex算法步骤如何去掉序号.md`
- 原 → 现：`62` → prose **346** / full **462**
- **判定：`KEEP`** — 扩写后结构完整；厚度中等但可公开保留（非最优）

### 单链表线性表：初始化、插入、遍历与有序合并

- 路径：`content/post/数据结构线性表相关操作.md`
- 原 → 现：`63` → prose **369** / full **549**
- **判定：`KEEP`** — 扩写后结构完整；厚度中等但可公开保留（非最优）

### LaTeX 表格脚注：用 threeparttable 给表格加注释

- 路径：`content/post/latex如何给表格添加注释.md`
- 原 → 现：`23` → prose **383** / full **509**
- **判定：`KEEP`** — 扩写后结构完整；厚度中等但可公开保留（非最优）

### WinForms DataGridView：CheckBox 列的全选与取消全选

- 路径：`content/post/datagridview里面的checkbox全选和取消全选.md`
- 原 → 现：`32` → prose **412** / full **521**
- **判定：`KEEP`** — 扩写后结构完整；厚度中等但可公开保留（非最优）

### WinForms 里用 HTTP POST 上传文件的正确姿势

- 路径：`content/post/winform中进行post上传文件.md`
- 原 → 现：`110` → prose **426** / full **604**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### 如何查找 Django 的安装路径与版本信息

- 路径：`content/post/如何查找django安装路径.md`
- 原 → 现：`70` → prose **428** / full **491**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### HTTP 状态码速览：从 2xx 成功到 5xx 服务器错误

- 路径：`content/post/http响应代码解释.md`
- 原 → 现：`84` → prose **519** / full **615**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### 柯西分布：密度、标准型与为何「均值不存在」

- 路径：`content/post/柯西分布.md`
- 原 → 现：`63` → prose **531** / full **563**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### 如何将网络流转化为内存流（C#）

- 路径：`content/post/如何将网络流转化为内存流 C#.md`
- 原 → 现：`0` → prose **592** / full **814**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### 差分进化（DE）算法原理与 MATLAB 示例

- 路径：`content/post/differential evolution代码实例（DE算法）.md`
- 原 → 现：`42` → prose **668** / full **814**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### 用 Burp MCP 把代理能力接进 Claude CLI

- 路径：`content/burp-mcp.md`
- 原 → 现：`105` → prose **818** / full **839**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### SameSite 的七八事：Chrome 默认 Lax 之后，SSO iframe 为什么挂了

- 路径：`content/samesite.md`
- 原 → 现：`104` → prose **840** / full **885**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### 安全与开发常用在线工具清单（持续整理）

- 路径：`content/checklist.md`
- 原 → 现：`23` → prose **855** / full **856**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

### Jenkins SAML SSO 插件中的 XXE 与 SSRF（CVE-2023-32991 / CVE-2023-32992）

- 路径：`content/CVE-2023-32991.md`
- 原 → 现：`20` → prose **1079** / full **1171**
- **判定：`KEEP`** — 已具备背景/步骤/坑点/小结，可作为独立技术文保留

## 最终建议

| 判定 | 篇数 | 动作 |
|------|-----:|------|
| KEEP | 17 | 保留公开 |
| KEEP_WEAK | 8 | 可保留，有空再加厚 |
| DROP | 1 | **draft 下线** |

**仅 1 篇建议下线：`content/post/mihoyo.md`（米哈游内推）。** 其余 25 篇扩写后均可保留。
