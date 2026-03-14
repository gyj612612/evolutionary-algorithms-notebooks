# CE310-6-__ : Evolutionary Computation and Genetic Programming

本文件合并了：

1) **CE310 coursework 2026.pdf** 全部可提取文本（尽量保持原样，不做删改）

2) 我在聊天中给你的 **完整技术报告/实现方案**（原样收录）

3) **Lecture 01–07** 每份 PDF 的全部可提取文本（尽量保持原样，不做删改）


> 说明：若 PDF 内含图片/扫描页/图中嵌字，纯文本提取可能无法包含这些“非可选中文本”。这不是我主动删改，而是 PDF 本身的文本层不可直接提取。


---

## A. 技术报告（聊天输出原样收录）

下面我给你一套**“按评分点逐条对齐、实现细节可直接落地到 notebook、实验与统计一条龙”**的完整方案。你在 VSCode 里配合 codex 写代码/调试即可；我这边负责**算法思路、数学/模型、可行性、实验设计、统计与写作结构**，确保覆盖所有得分点。

---

## 0. 先把“满分”最关键的两条护城河做对
### A) 必须“lab-style incremental development”
你每个 part 的 notebook 都要严格按“**小步 + 解释 + 测试 + 输出**”写（否则每 part 最多可被扣到 20%）。要求点包括：每个代码 cell 前有清晰解释；小步可测试；组件（初始化/选择/变异/交叉/适应度/主循环）先独立测试再集成；有 debug/改进证据；参数选择有理由。fileciteturn3file0L86-L97 fileciteturn3file0L342-L353  

### B) Responsible AI use（如果你用 AI）
要交 **AI log（Word）**，并且要有“挑战/质疑/纠错/调试”证据，否则也可能每 part 最多扣 20%，严重还可能触发学术调查。fileciteturn3file0L58-L60 fileciteturn3file0L73-L80 fileciteturn3file0L361-L369  

> 你现在的工作流正合适：你用 codex 写 + debug，我负责给你“每一步该怎么写、怎么测、怎么解释”，这些都能直接粘到 AI log 里当“负责使用 AI”的证据链。

---

## 1. 交付物与评分结构（你写 notebook 时要显式对齐）
- 提交 zip：Part1.ipynb、Part2.ipynb；若用 AI 再加 AI_log.docx。fileciteturn3file0L81-L103  
- 评分点（课程作业内部比例）：
  - Task1 GA 10%，Task2 10%，Task3 15%，Task4 15%
  - Task5 GP 10%，Task6 20%，Task7 10%，Task8 10% fileciteturn1file0L30-L81  

---

## 2. Part 1（GA）：实现方案与“写作-实验”模板

### Task 1：Binary Generational GA（用 OneMax 测）fileciteturn3file0L114-L131  
你要实现并**分别测试**：
1) 初始化  
2) 适应度评估  
3) Tournament selection（T≥2）  
4) Cloning  
5) Mutation（**独立算子**：不是在 XO 后再变异）  
6) Crossover  
7) 完整 generational loop（无世代重叠；clone 用于让父母“存活”）  

**推荐的“算子选择机制”（最容易对齐作业要求）**  
每产生 1 个 offspring 时，用一个随机数在三种方式里选一种（互斥）：
- clone：从锦标赛胜者复制
- crossover：从两次锦标赛得到两个父母做 1-point XO
- mutation：从锦标赛胜者复制后，按 bit-level rate 翻转（只在这个分支发生）

这样你会自然拥有：
- cloning probability \(p_{clone}\)
- crossover probability \(p_{xo}\)
- mutation operator probability \(p_{mutop}\)
并满足 \(p_{clone}+p_{xo}+p_{mutop}=1\)。  
此外 mutation 还需要 **bit mutation prob** \(p_{bit}\)。作业明确要求你给出“两个 mutation 概率：算子级 + bit级”。fileciteturn3file0L128-L130  

**你在 notebook 里要写出来的“每步测试”建议**
- 初始化：打印前 5 条 chromosome，检查长度、0/1 分布
- OneMax：手工构造 bitstring 测 expected
- Tournament：固定小 population + 固定 fitness，检查总是选到更优者（或在 tie 时的处理）
- Clone/XO/Mutation：  
  - XO：固定 cut point（先写可控版）验证拼接正确，再换随机 cut  
  - Mutation：固定 random seed，验证翻转位数期望范围
- 主循环：记录每代 best fitness 与 mean fitness（至少打印/plot 一次）

**参数初值（用于“有理由的 choice”）**  
你可以先用常见合理起点：T=3；\(p_{xo}=0.7\)、\(p_{clone}=0.2\)、\(p_{mutop}=0.1\)；\(p_{bit}=1/L_{bits}\)（平均每次 mutation 翻 1 bit）  
然后按作业要求用多次 runs 验证/调整（这一段就是你写 justification 的材料）。fileciteturn3file0L128-L131  

---

### Task 2：Genotype→Phenotype：两种编码 + 15-max fileciteturn3file0L132-L161  
目标：进化长度为 \(L\) 的整数序列，每个整数在 0..15。染色体仍是 bitstring，但评估前要 decode。

必须实现两种 decode：
1) **4-bit positional**：\(\;I=b_1+2b_2+4b_3+8b_4\)（注意这里 b1 是最低位）fileciteturn3file0L139-L146  
2) **15-bit non-positional**：\(\;I=\sum_{i=1}^{15} b_i\) fileciteturn3file0L153-L154  

然后实现 **15-max fitness**：  
- decode 得到 \(L\) 个整数  
- fitness = 其中等于 15 的个数（范围 0..L）fileciteturn3file0L155-L159  

**关键测试（写进 notebook）**
- decode4：`1111 -> 15`、`0000 -> 0`、`1000 -> 1`（验证位序）
- decode15：全 1 -> 15；全 0 -> 0；一半 1 -> 期望值
- 15-max：构造 phenotype 明确的 bitstring，看计数是否正确

**分析点（写 discussion 提分）**
- 15-bit sum 编码对中间值有组合数偏置（binomial），而极端值（0/15）很稀有 ⇒ 15-max 更难；4-bit positional 的 15 只有一种编码也稀有，但整体分布均匀。你后面 Task3/4 的对比就有理论依据。

---

### Task 3：调参 + 系统实验（必须 50 代 + 每条件 10 runs）fileciteturn3file0L162-L172  
要求分两段：

**(i) 调参（50 generations）**  
“尝试识别好的 population size 与 tournament size”。fileciteturn3file0L164-L168  
建议你用一个小网格（写得像科学实验）：
- Pop ∈ {20, 50, 100, 200}  
- T ∈ {2, 3, 5, 7}  
每组跑 5 次（调参阶段不强制 10 次，但你写清楚“先粗筛再做 10 次正式实验”很加分），指标用“第 50 代 best fitness 的均值/方差 + 收敛速度曲线”。

**(ii) 正式实验：4 个条件维度**  
对每种整数表示（两种编码）× 每个 L（10 与 30）× fitness（15-max 与 soft-15-max）  
都要做 10 个独立 runs，并记录 best-of-run best fitness（至少这个）。fileciteturn1file0L47-L51 fileciteturn3file0L166-L172  

soft-15-max 定义：返回 \(L\) 个整数的平均值（替代“数 15 的个数”）。fileciteturn3file0L169-L170  
并比较它是“帮助还是阻碍”解决 15-max（建议你：运行时用 soft-15-max 做选择压力，但评估结果时同时报告 **15-max 的 best-of-run**，这样能回答“是否更容易到达全 15”这个核心问题）。

**你应该输出的图/表（直接对齐 Task3 得分点）**  
- 表：每条件 10 次 best-of-run（以及 mean±std）  
- 图：每条件的“best fitness vs generation”平均曲线（带 std 阴影/误差棒也行）  
- 文字：解释差异（编码偏置、选择压力、L=30 更难等）

---

### Task 4：自创 deceptive（trap-style）+ 与 15-max 对比 fileciteturn3file0L173-L178  
你要做一个“15-trap”（或对应 soft 版本的 trap），并展示：
- GA 解变慢  
- 有时收敛到 deceptive local optimum fileciteturn1file0L53-L56  

**可直接用的 trap 设计（标准且解释最清晰）**  
对每个“整数块”先算该块的 unitation \(u=\#1s\)。块长度 \(k\)：
- 对 4-bit positional：k=4  
- 对 15-bit sum：k=15  

定义（经典 trap(k)）：
\[
trap(u;k)=egin{cases}
k, & u=k \
(k-1)-u, & 0\le u < k
\end{cases}
\]
性质：
- 全 1 是全局最优（k）
- 全 0 是局部最优（k-1），而且对“逐步爬山”具有欺骗性（因为从 0 往 1 走会先变差）

整体 fitness = 所有块 trap 值求和（或平均）。  
然后你用同样参数、同样代数、同样 runs 数去对比对应的 15-max/soft-15-max（作业也明确要求对比“对应版本”）。fileciteturn3file0L179-L181  

**你要展示“陷入局部最优”的证据**
- 曲线：best fitness 长期停在 \(L\cdot (k-1)\) 附近（全 0 块）  
- 或者：最终个体的 unitation 分布集中在 0（每块几乎全 0）  
- 再对比 15-max 最终能更常到达全 1（或至少更高）

---

## 3. Part 2（GP）：从 Part1 的 GA 变成 stack-based GP

### Task 5：表示与遗传算子（复用 GA 框架）fileciteturn3file0L186-L204  
你要选 Part1 中“你觉得最好”的 GA 版本来改（建议选你在 Task3 里表现最好、最稳定的那套参数与编码）。fileciteturn3file0L186-L187  

GP primitive set（8 条指令）：NOP、+、-、*、X、1、-1、0。fileciteturn3file0L188-L197  
程序长度固定 \(L=30\)，指令用整数表示，并用 bitstring 编码：  
- 3-bit positional：\(I=b_1+2b_2+4b_3\)（0..7）  
- 7-bit sum：\(I=\sum_{i=1}^{7}b_i\)（0..7） fileciteturn3file0L198-L202  

**重要：这里“复用”的意思是**  
初始化/选择/交叉/变异/主循环都沿用 Part1（因为仍是二进制串）。fileciteturn3file0L202-L204  
变化的是：fitness 现在要 decode 成“30 条指令”并用解释器执行。

> 强烈建议：两种编码都实现，但你可以把“主实验”放在 3-bit 上（因为它在随机初始化时更接近“指令均匀分布”，也更符合 Task8 里“12.5%”的直觉期望）。fileciteturn3file0L331-L334  
> 7-bit sum 编码初始分布会是 binomial（不均匀），你可以把它当“额外观察/扩展”，写清楚原因反而加分。

---

### Task 6：解释器 + 两个问题的 fitness function（20%大头）fileciteturn3file0L406-L411  
作业给了必须“纳入、测试、理解”的 postfix-stack 解释器 execute(program, x)。你要原样整合并写一堆测试。fileciteturn3file0L218-L254  

解释器关键点（写进你的文字说明里）：
- 使用 stack；自定义 pop()：空栈时返回 0，避免 runtime error（这是 closure 的一种工程实现）。fileciteturn3file0L231-L234  
- 指令映射（按给定代码）：  
  - 0:NOP，1:X，2:+，3:-，4:*，5:1，6:-1，7:0（else 分支）fileciteturn3file0L237-L252  
- 返回值是“最后一次压栈的结果”（最终 pop）。fileciteturn3file0L253-L254  
- 示例必须复现：execute([5,1,2],3)=4，并把它逐步执行过程解释出来（作业里给了步骤，你可以对照写测试输出）。fileciteturn3file0L255-L279  

#### Problem 1（两次 fitness case）
目标：x=-1 时输出尽可能负；x=1 时输出尽可能正。fileciteturn3file0L284-L288  
**建议 fitness（最大化）**：
\[
f_1(prog)=execute(prog,1)-execute(prog,-1)
\]
它等价于“让 x=1 大、x=-1 小（更负）”。  
你在说明里再补一句：由于 program length 固定、搜索空间有限，存在某个（未知的）最大值；我们以此为优化目标并报告 best-of-run、曲线与方差。

> “ideal solution reporting”这一点：Problem1 的全局最优通常不可解析求出。你可以把 **达到当前实验中观测到的最大值** 作为“经验 ideal”，并诚实说明“这是下界”。Task7 更关键的“ideal”其实 Problem2 有天然 ideal（误差=0）。fileciteturn1file0L73-L74  

#### Problem 2（21 次 fitness case：符号回归）
x = -1, -0.9, …, 1.0（共 21 个），目标逼近 5 次多项式：fileciteturn3file0L289-L296  
\[
y(x)=2x^5+4x^4+6x^3+8x^2+10x+1
\]
**建议 objective 与 fitness**
- 误差（越小越好）：
\[
U=\sum_{x\in\{-1,-0.9,\ldots,1\}} |execute(prog,x)-y(x)|
\]
- fitness（越大越好）：\(f_2=-U\)（课程里也常用 \(f=-U\) 这种映射；实现简单，统计也好做）

**ideal solution**：\(U=0\)（所有点完全拟合），这是你 Task7 “ideal-solution reporting”最稳的落脚点。fileciteturn1file0L73-L74  

---

### Task 7：实验协议 + 统计（必须 10 runs、50 代、不许提前停）fileciteturn3file0L309-L313  
你要做的是“系统实验 + 统计 + 解释”，目标是理解 population size 与 tournament size 的影响，以及计算代价。fileciteturn3file0L305-L308  

**硬性要求（写进 notebook 的实验设置框里）**
- 每个实验条件：至少 10 次独立 runs fileciteturn3file0L309-L311  
- 每 run：50 generations，不允许早停（即使出现 ideal）。fileciteturn3file0L311-L313  
- 每代统计：mean fitness、std fitness、best fitness（单次 run）fileciteturn3file0L316-L321  
- 跨 runs 聚合：对每代曲线做均值与 std，并关注 variability fileciteturn3file0L322-L325  
- 额外要看：ideal 命中率、首次命中 ideal 的平均代数（但仍继续跑满 50 代）fileciteturn3file0L326-L329  

**推荐实验矩阵（够用且信息量大）**
- Problem1 与 Problem2 分开做
- Pop ∈ {50, 100, 200}
- T ∈ {2, 3, 5, 7}
共 2×3×4=24 个条件，每条件 10 runs（你可按时间缩减，但至少要覆盖“低/中/高”的 pop 与 selection pressure 组合）

**计算代价（写进报告会很加分）**
- Problem1：每个个体评估需要 2 次 execute（x=-1 与 1）  
- Problem2：每个个体评估需要 21 次 execute  
所以理论 execute 调用次数：
\[
	ext{calls} = runs 	imes generations 	imes pop\_size 	imes n\_{cases}
\]
这能直接解释“为何更大 pop 更贵”以及“为何 Problem2 更慢”。fileciteturn3file0L305-L308  

---

### Task 8：primitive 频率演化（10%）fileciteturn3file0L331-L341  
你要追踪 8 个 primitive 在种群中的比例变化，并解释“为什么某些 primitive 会扩散”。

**实现要点**
- 每代：对整个人口的 decoded 指令（pop_size × 30 个整数）统计直方图（0..7）
- 频率 = count / (pop_size×30)
- 至少报告最终代；更好是画出“频率 vs generation”的 8 条曲线 fileciteturn3file0L331-L338  

**解释角度（写作模板）**
- 初始：理论上应接近 12.5%（特别是 3-bit positional 时更合理）fileciteturn3file0L331-L334  
- 演化后：  
  - Problem2（拟合多项式）通常会偏好能构造多项式项的 primitive（X、*、+、常数 1/0/-1）  
  - NOP 可能变多（“中性漂变/保护有用片段”直觉）或变少（如果浪费长度导致输出不佳），你用数据说话  
- 把频率趋势和“fitness 上升/停滞阶段”对齐解释，会很像一篇小论文。

---

## 4. 两个 Notebook 的“满分结构模板”（你照着写就不会跑偏）

### Part1.ipynb 推荐目录（每小节都按：解释→代码→测试/输出→小结）
1. 任务概览 + 评分点映射（Task1-4）  
2. Task1：逐步实现 GA  
   - init / one-max / selection / operators / loop / run logs & plots  
3. Task2：两种 decode + 15-max + 运行验证  
4. Task3：调参实验（50 代）→正式实验（10 runs）→表/图/讨论  
5. Task4：15-trap 定义 + 对比实验 + “陷入局部最优”证据  
6. 总结：表示差异、soft 的作用、选择压力与 premature convergence

### Part2.ipynb 推荐目录
1. 任务概览 + 评分点映射（Task5-8）  
2. Task5：GP 表示（bitstring→指令序列）+ 复用 GA 框架说明  
3. Task6：execute 解释器“逐行理解”+ 单元测试 + 两个 fitness 函数验证  
4. Task7：实验矩阵、10 runs、50 gens、统计与聚合图、ideal 命中率与代数  
5. Task8：primitive 频率曲线 + 解释  
6. 总结：参数影响、成本权衡、随机性/方差、与 EC 理论的连接

---

## 5. 你接下来最顺的落地方式（不需要我再问你任何信息）
1) 你先把 Part1 的 GA 框架按 Task1 小步写完（每步带测试），我可以根据你贴的某一段代码/输出，逐段帮你定位 bug 与补“解释文字”。  
2) Task2-4 都是“换 fitness/加 decoder/加实验循环 + 作图统计”，复用程度很高。  
3) Part2 直接复用 GA，只新增：decode→program、execute、fitness_case 循环、primitive 统计。fileciteturn3file0L202-L204 fileciteturn3file0L218-L254  

如果你现在已经在 VSCode 里开始写了：把你**当前项目结构/核心函数签名/一段跑不通的输出**贴出来（哪怕很短），我就按上面模板把“下一步该写什么、怎么测、怎么在 notebook 里解释”直接给你对齐到评分点。


---

## B. Coursework（PDF可提取全文）

```text

CE310: Evolutionary Computation and 
Genetic Programming 
Coursework Assignment, Prof Riccardo Poli, Spring Term 2025-26 

Table of Contents 
1  Overview ......................................................................................................... 2 

1.1  What needs to be done in the coursework ................................................... 2 

1.2 

1.3 

1.4 

1.5 

How you should develop your coursework ................................................... 2 

Format ...................................................................................................... 3 

Submission ............................................................................................... 3 

Clarifications and Recommendation ........................................................... 3 

2  GA implementation and solving problems (Part 1) ............................................... 4 

2.1 

2.2 

2.3 

2.4 

Task 1 - Implement a Binary Generational GA ............................................... 4 

Task 2 – Use your GA to Evolve Sequences of Integers ................................... 4 

Task 3 – Tune the GA and solve 15-max and soft-15-max problems ................ 5 

Task 4 – Invent a deceptive problem and compare with 15-max ..................... 5 

3  GP implementation and solving problems (Part 2) ............................................... 6 

3.1 

3.2 

3.3 

3.4 

Task 5 – Representation and Genetic Operators ........................................... 6 

Task 6 – Program Execution and Fitness Functions ....................................... 6 

Task 7 – Experiments and Analysis of Results ............................................... 9 

Task 8 – Evolution at the Level of Primitives .................................................. 9 

4  Marking Scheme ............................................................................................ 10 

4.1 

4.2 

4.3 

4.4 

4.5 

4.6 

4.7 

4.8 

4.9 

Incremental Development & Methodology ................................................. 10 

Responsible AI Use .................................................................................. 10 

Task 1 Binary GA (10%) ............................................................................. 11 

Task 2 Genotype–Phenotype Mapping & 15-max (10%) ............................... 11 

Task 3 Parameter Tuning & Experiments with 15-max and soft-15-max (15%)  11 

Task 4 Deceptive problem and 15-max Comparison (15%) .......................... 11 

Task 5 GP Representation & Operators (10%) ............................................. 11 

Task 6 Interpreter & Fitness Functions (20%) .............................................. 12 

Task 7 Experimental Protocol & Statistics (10%) ......................................... 12 

4.10  Task 8 Evolution of Primitives (10%) ........................................................... 12 

 
1  Overview 
1.1  What needs to be done in the coursework 
This coursework is worth 40% of the module overall (the other 60% being the exam). It 
consists of two parts, each carrying 50% of the marks for the coursework. 

Part 1 involves coding your own Genetic Algorithm in Python and using it to solve a 
small number of problems, documenting and discussing your work along the way. 

Part 2 involves turning the Genetic Algorithm developed in Part 1 into a Stack-based 
Genetic Programming system and using it to solve a small number of problems, 
recording the run behaviour and performance, and discussing the results obtained. 

The deadline for submitting the coursework on FASER is 2026-03-06 (Week 23) just 
before 2pm. 

1.2  How you should develop your coursework 
You are allowed to use AIs to help with some aspects of the coursework, but you do 
not have to do so. If you do, you must use AIs responsibly and prove that you did so. 

Whether or not you use AIs to help, you must make sure you fully understand the 
work you are submitting to the point that you could satisfactorily answer any questions 
I may have at the time of marking on the code or analysis done.1 

To promote this level of understanding, I am making it a requirement that you produce 
the coursework incrementally and you provide evidence that you did so. Basically, 
you need to follow the same small steps we have used in the CE310 labs/classes, the 
only difference being that, in your coursework, you need to describe and justify the 
sequence of small steps that eventually lead to implementing algorithms, solving 
problems, etc.,  while in the classes I provided this information.  

If you make use of AIs, you need to show the exact queries you submitted to the AIs 
and the AI outputs. You must also show evidence that you challenged the AIs, 
indicating how you identified logical errors and debugged the AI ideas and code.2  

Whether or not you use AIs to help, if you make use of concepts and techniques that 
were not presented in CE310, you must justify why you chose them over the 
alternatives that I presented. 

1 Be aware that I will myself feed this coursework description in multiple AIs (multiple times) and will 
record their outputs. So, if you decide to just do this to save time and effort, I will most likely find out. If I 
do, I don’t consider this a responsible use of AI. 
2 If you manually corrected an AI’s outputs, you need to resubmit such corrections into the AI, so it is 
aware of where you stand, in case of further interactions. Type into the AI prompt something like “Below is 
my current code. I don’t want any answer. Just making you aware of changes I made: ** YOUR CODE**”. 

 
 
 
 
 
 
 
 
 
 
AIs tend to produce the same or similar answers repeatedly and they write code in a 
very characteristic style. So, your coursework submission may be flagged up by our in-
house and commercial plagiarism detection systems. However, you will not be 
penalised for this, if your coursework shows clearly that you used the AIs 
responsibly.  

To reiterate: If you want to get help from AIs in producing the coursework, you must 
keep a log of the AI interactions performed and to submit it with the coursework. 
This should be in the form of a Word file where you copy and paste all AI interactions 
you have had in the order you had them.  

1.3  Format 
The required format for the coursework is a single Jupyter notebook for each part (that 
is: submit two notebooks), plus the AI log if you used AIs. 

In each notebook you will have multiple cells (text/markup, code and output). As I 
indicated before, you must proceed in very small steps, like we do in the labs. Follow 
this protocol: 
1.  Precede each code cell with a textual explanation of what you want to achieve 
with the code that immediately follows and why it is the next logical step towards 
the goal. 

2.  The code should just implement the target functionality, but it must also include 

tests and produce outputs, so one is sure it works as expected. If the code presents 
bugs, try to fix any issues yourself (preferred) or ask the AI for help.  

3.  Make sure the code does not only run, but you fully understand it. If you don’t, 
study it more, add more tests, or split the task into even smaller steps, until you do 
understand it all. 

4.  Then and only then, identify the next (smallest) element of functionality that 
makes sense to add, and repeat the steps above, until you achieve the target. 

1.4  Submission 
Please submit all your work as a single zip file on FASER by the above deadline. Inside 
the zip file, put:  

1.  a Jupyter notebook with your Part 1 work, 
2.  a Jupyter notebook with your Part 2 work, 
3.  if AIs were used, also include the AI Log in the form of a Word document. 

1.5  Clarifications and Recommendation 
Ask questions during the lectures and classes if any requirement in the assignment is 
not clear. Feel free to also contact me by email. 
You can assume that if you struggle, your fellow students will also struggle. Keep in 
mind that there are many ways how to address and complete the tasks. There is no 
single correct or best way to do this.  

Above all, start this process early(!), so that you have time to try things and make 
mistakes, and have still have time to learn from them. 

 
 
 
 
2  GA implementation and solving problems (Part 1) 
2.1  Task 1 - Implement a Binary Generational GA 
Incrementally develop, following the protocol mentioned above, a binary generational 
Genetic Algorithm. 

Your generational GA will need: 

1.  initialisation,  
2.  fitness evaluation (more on this below),  
3.  tournament selection (with any tournament size 𝑇 from 2 upward),  
4.  cloning,  
5.  mutation (used as an independent genetic operator, not on top of other genetic 

operators), and  

6.  crossover. 

All the above will need to be tested independently and integrated gradually within the 
GA’s main loop. 

Use the one-max function to test the GA.  

Choose meaningful settings for: the tournament size 𝑇, the cloning probability, the 
crossover probability and the two mutation probabilities: the probability of applying the 
mutation operator and the probability of mutating each bit.  

Verify or revise/tweak your choices using multiple runs of the GA. 

2.2  Task 2 – Use your GA to Evolve Sequences of Integers 
Now we need to use the binary GA to evolve sequences of 𝐿 integers, each in the range 0 
to 15 for a pre-assigned 𝐿.  

The chromosomes in your GA will still be binary. However, before fitness evaluation 
groups of contiguous bits are transformed into integers. This operation is a genotype-to-
phenotype transformation, where genotypes are bit strings/chromosomes, and 
phenotypes are sequence of 𝐿 integers. 

Important: two different forms of conversion from bits to integers must be explored:  

1.  the standard binary to decimal formula where each group of 4 contiguous bits 

(𝑏1, 𝑏2, 𝑏3, 𝑏4) is transformed into integers as follows: 

𝐼 = 𝑏1 + 2 × 𝑏2 + 4 × 𝑏3 + 8 × 𝑏4 

So, to evolve sequences of 𝐿 integers one needs chromosomes of 4 × 𝐿 bits. 

2.  the less usual non-positional binary to decimal conversion where each integer is 

encoded using a group of 15 contiguous bits (𝑏1, 𝑏2, . . . , 𝑏15) which are 
transformed into integers as follows:  

 
 
 
 
 
 
 
 
 
 
 
𝐼 = 𝑏1 + 𝑏2 +. . . +𝑏15 

So, to evolve sequences of 𝐿 integers one needs chromosomes of 15 × 𝐿 bits. 

To test everything is working, implement a 15-max fitness function, which is like one-
max but: 

1.  it first applies the appropriate genotype-to-phenotype conversion to get a 

sequence of 𝐿 integers and then  
2.  returns how many of them equal 15 

So, 15-max fitness values range between 0 and 𝐿 inclusive.  

Run the GA, with both binary representations for integers, to ensure all is working as 
expected. 

2.3  Task 3 – Tune the GA and solve 15-max and soft-15-max 

problems 

Perform runs, each lasting 50 generations, to try to identify the good values of 
population size and tournament size.  

With the good parameters found (and still 50 generations), for each representation for 
integers and for both 𝐿 =  10 and 𝐿  =  30 perform 10 independent runs (recording the 
best-of-run best fitness found in each) with the 15-max problem. 

Modify the 15-max fitness function, call it soft-15-max,  so that instead of counting how 
many integers are exactly 15, it returns the average of the 𝑳 integers.  

Repeat the experiments to find out whether this fitness function helps or hinders the 
ability of the GA to solve the 15-max problem. 

2.4  Task 4 – Invent a deceptive problem and compare with 15-max  

Based on the binary deceptive fitness function we have studied in the Unit 03 class 
(which is known in the GA literatures as trap function), define a deceptive version of 
the 15-max problem. Rerun your code to prove that the GA ability to solve the problem 
is slowed down and sometimes the population converges towards the deceptive local 
optimum.3 

3 Feel free to modify either the 15-max or soft-15-max functions to create your 15-trap function. Just make 
sure you compare the results obtained with your trap function with the corresponding version of the 15-
max function. 

 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
3  GP implementation and solving problems (Part 2)  
Part 2 requires transforming one of the GAs developed in Part 1 into a GP system. This 
will require changes to some, but not all, the elements of the GA.  

3.1  Task 5 – Representation and Genetic Operators 

Pick the GA which you feel worked best in Part 1.  

Assume that our GP primitive set only includes a very small number of instructions:  

-: which subtracts two values and returns their difference, 

•  NOP: that does nothing,  
•  +: which adds up two values and returns their sum, 
• 
•  *: which multiplies two values and returns their product, 
•  X: which returns the input value to the program,  
•  1: which returns the constant 1,  
• 
•  0: which returns the constant 0. 

-1: which returns the constant -1, and  

So, in total we have 8 instructions.  

Instructions will be represented as integers (NOP=0, +=1, -=2, etc.). Programs are just 
sequences of 𝑳 = 𝟑𝟎 integers, represented using bit strings of length 𝐿 × 3 or 𝐿 × 7 
bits depending on which formula you use to decode integers: 

𝐼 = 𝑏1 + 2 × 𝑏2 + 4 × 𝑏3 

OR  

𝐼 = 𝑏1 + 𝑏2 +. . . +𝑏7 

Because we are evolving programs represented as binary strings, in our GP system you 
are asked to reuse the initialisation, selection, crossover, mutation and main 
evolution loop used for the binary GA in Part 1. 

3.2  Task 6 – Program Execution and Fitness Functions 
We know that in GP, computing the fitness of a program often requires running the 
program multiple times with different inputs. The question is: how are the instructions 
sequenced and how do they know on which data to operate and where to place their 
results? 

We are used to seeing programs/expressions like: (X + 1) or (X * X – 1). This is called the 
infix notation as operations are in between their arguments (e.g., + is between X and 1 
in the first expression).  In lectures we will see the prefix notation where (X + 1) would 
be written as (+ X 1). In this assignment we will use another notation called the postfix 
notation (a form of Reverse Polish Notation) where the operations follow their 
arguments so (X + 1) would be written as (X 1 +). We do this as it leads to an extremely 
simple simulator of program execution. 

 
 
 
 
 
 
 
 
 
 
The operations are executed using the following simulator/interpreter which you need 
to incorporate, test and understand thoroughly, and, finally, use in your GP code:4 

# Simulator of program execution (GP interpreter) 
# program = sequence of integers 
# x = input variable 
def execute(program, x): 

    # A place where to get arguments for operations and  
    # for storing their results 
    stack = []  

    # If l = [1,2,3], l.pop() removes 3 from the list and returns it 
    # but if l = [], l.pop() gives an error 
    # Fixing the problem for stack by defining our own pop() 
    def pop(): 
        if not stack: 
            return 0 
        return stack.pop() 

    # Main execution loop 
    for instr in program: 
        if instr == 0:   # NOP 
            pass 
        elif instr == 1: # X 
            stack.append(x) 
        elif instr == 2: # + 
            stack.append(pop() + pop()) 
        elif instr == 3: # - 
            stack.append(pop() - pop()) 
        elif instr == 4: # * 
            stack.append(pop() * pop()) 
        elif instr == 5: # 1  
            stack.append(1) 
        elif instr == 6: # -1  
            stack.append(-1) 
        else:            # 0 
            stack.append(0) 

    # Returning the very last result appended to stack 
    return pop() 

So, from the point of view of this simulator/interpreter the individual [5, 1, 2] 
corresponds to [1, X, ADD], that is (1 X +) in postfix notation.  

So, running: 

execute([5, 1, 2], 3)  

4 The simulator presents some resemblance with the CPU simulator presented in the Unit 05 class. 
However, in that simulator instructions made use of registers, while here the instructions use a stack. 

 
 
 
 
 
 
 
 
 
 
performs the following steps: 

Input x = 3 

Initial State: 
      Stack: [] 

Step 1: Instruction 5 
      [Append] 1 
      Stack: [1] 

Step 2: Instruction 1 
      [Append] x (3) 
      Stack: [1, 3] 

Step 3: Instruction 2 
      [Pop]  -> 3 
      [Pop]  -> 1 
      [Calc] 1 + 3 = 4 
      Stack: [4] 

Return instruction: 
      [Pop]  -> 4 

Final Result: 4 

Turning to fitness functions: the details of your fitness functions will depend on the 
problem you need to solve, but they all will most certainly require invoking the function 
execute(prog, x) for multiple fitness cases, accumulating the contributions to fitness 
from each case, and finally returning the accumulated fitness. 

The problems you will need to solve are: 

1.  Problem 1: Evolve programs that when executed with x = -1 produce the 

smallest possible output (i.e., a value as negative as possible) and when 
executed with  x = 1 produce the largest possible output (i.e., a value as positive 
as possible). 

2.  Problem 2: Evolve a program that when executed 21 times with 𝑥  = -1, -0.9, … , 
1.0 produces outputs that are as close as possible to the 𝑦 values obtained from 
the function (5th order polynomial): 

𝑦  =  2 × 𝑥5   + 4 × 𝑥4   + 6 × 𝑥3   + 8 × 𝑥2  + 10  ×  𝑥 + 1 

You need to develop corresponding fitness functions for these two problems, 
making sure they achieve the high-level goals specified in the problem statements 
above.  

 
 
 
 
 
 
 
 
 
 
 
 
 
 
3.3  Task 7 – Experiments and Analysis of Results 
You are asked to perform a series of GP runs and describe the results of your runs in a 
report. In your experiments you will need to use GP in different configurations (i.e., 
problems and parameters).  

The aim of the experiments is to get an intuition on how the population and tournament 
size impacts on fitness of the evolved programs for different symbolic regression 
problems, and on the corresponding computational effort (based on how often the 
fitness function is being executed).  

Since GP is a stochastic searcher, you will see that performance varies from run to run. 
Therefore, to draw your conclusions, you should ensure you perform at least 10 runs in 
each experiment. IMPORTANT: Do not stop runs even if an ideal solution has been 
identified. So, they only stopping criterion for runs should be that the number of 
generations has reached the limit (50 generations). 

Once the runs are completed, analyse the output and behaviour of the system 
produced in different experiments. To do that you will need to look at statistics obtained 
in different experiments when solving the chosen problems. Statistics often used to 
describe individual GP runs include   

•  The average and standard deviation of the fitness of the programs in the 

population 

•  The fitness of the best program in the population 

Normally these are computed at each generation.  

Because you have 10 runs in each experiment, you need to aggregate results across 
runs. Typical averaging is sufficient for this purpose, but you should keep an eye also on 
variability of results across runs with the same configuration, so reporting also the 
standard deviation would be good.  

When performing multiple runs, it is also important to look at: 
•  The fraction of runs where an ideal solution was found 
•  The average generation at which such solution was found (given that we are not 

stopping runs until they reach the final generation). 

Study the results and report any conclusions. 

3.4  Task 8 – Evolution at the Level of Primitives  
After random initialisation, we expect to see each of our 8 primitives to be present in 
approximately equal proportions (12.5%) across all chromosomes in the population. 
However, the utility of the primitives may change generation after generation (in ways 
that depend also on the problem being tackled), and so their proportions in the 
population will not be equal anymore.  

Study these changes (in at least the final generation, or in all generations) and try to 
formulate an explanation for why certain primitives are significant more frequent than 

 
 
 
 
 
 
 
others. Why are such primitives spreading within the population? Why are they fitter 
than others? 

4  Marking Scheme 
4.1  Incremental Development & Methodology  

In both Part 1 and Part 2, I compliance with the required lab-style incremental development is 
required. Marks in each part can be reduced by up to 20% if the this has not been followed.  

No reduction of marks will be associated with: 

•  Each code cell is preceded by a clear explanation of what functionality is being added 

and why it is the next logical step. 

•  Functionality developed in small, testable steps. 
•  Each component (initialisation, selection, mutation, crossover, fitness, loop) tested 

independently before integration. 
•  Evidence of debugging and refinement. 
•  Clear justification of parameter choices. 

Medium reduction of marks will be associated with: 

•  Mostly incremental, but steps too large or poorly justified. 
•  Some but limited testing evidence. 
•  Weak justification of choices. 

High reduction of marks with be associated with: 

•  Large blocks of code with minimal explanation. 
•  Little evidence of stepwise reasoning or understanding. 

4.2  Responsible AI Use 

Marks in each part may be reduced by up to 20%, or an investigation into an academic 
offence5 can be initiated, based on the degree to which AI has been used irresponsibly (as 
described in the main text.  

No marks will be deducted AI not used or if: 

•  Full AI log submitted 
•  Evidence of critical engagement 
•  Evidence of debugging/challenging the AI output 

5 See https://www.essex.ac.uk/student/academic-offences/artificial-intelligence. 

 
 
4.3  Task 1 Binary GA (10%) 
Marks awarded for correct implementation of: 

Initialisation 

• 
•  Tournament selection 
•  Cloning 
•  Mutation (operator-level + bit-level probabilities) 
•  Crossover 
•  Fully working generational loop 
•  Testing on one-max 

4.4  Task 2 Genotype–Phenotype Mapping & 15-max (10%) 
Marks awarded for: 

•  Both binary encodings implemented 
•  Correct 15-max fitness function 
•  Proper testing 

4.5  Task 3 Parameter Tuning & Experiments with 15-max and soft-15-

max (15%) 
Marks awarded for: 

•  Systematic parameter optimisation or non-systematic but good reasoned choices 
•  10 independent runs per condition 
•  Correct implementation of soft-15-max 
•  Experiments repeated properly 
•  Appropriate recording, presentation and understating of results 
•  Clear comparison and explanation 

4.6  Task 4 Deceptive problem and 15-max Comparison (15%) 
Marks awarded for: 

•  Correct trap-style function 
•  Demonstrated slowdown/local optima 
•  Clear explanation 

4.7  Task 5 GP Representation & Operators (10%) 
Marks awarded for: 

•  Correct reuse of GA framework 
•  Correct primitive encoding 
•  Working operators 

 
 
 
4.8  Task 6 Interpreter & Fitness Functions (20%) 
Marks awarded for: 

•  Correct use of provided interpreter 
•  Fitness functions correctly defined 
•  Proper aggregation across fitness cases 
•  Clear explanation of objectives 

4.9  Task 7 Experimental Protocol & Statistics (10%) 
Marks awarded for: 

•  10 runs per experiment 
•  50 generations per run (no early stopping) 
•  Per-generation statistics 
•  Aggregated statistics across runs 
Ideal-solution reporting 
• 
•  Clear interpretation of results 
•  Link to EC theory 
•  Discussion of parameter effects 
•  Discussion of variability 

4.10  Task 8 Evolution of Primitives (10%) 
Marks awarded for: 

•  Primitive frequency tracking 
•  Clear explanation of trends

```

---

## B. Lecture 01（PDF可提取全文）

```text

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

1. Introduction, motivation, 
metaheuristics, module structure and 
some evolution in nature

Outline

• Hands-on experience: hints for knapsack problem 
• Why do we need evolutionary computation and genetic 

programming?

• What is in the module and how will it be run?
• How does natural evolution work?

2

Outline

• Who is your module supervisor?
• Why do we need evolutionary computation and genetic 

programming?

• How will the model be run? (Introduction to CE310)
• Evolution in nature

3

Module supervisor

Riccardo Poli
• Professor in Computer Science
• Expert in Evolutionary 

Computation and Genetic 
Programming

• Co-founder and former co-director 

Essex BCI-NE lab

Email: rpoli@essex.ac.uk
Office: 1NW.5.3B

4

Three decades of experience in EAs and GP

• First publication on EAs/GP 1993
• Involved in many EA/GP conferences and 

journals in the past

• ISGEC Fellow (2003), EvoStar award (2007) and 

ACM SigEvo award (2023).

• Fourth (out of 19,000+) most prolific author in 
GP worldwide (253 articles, 113 first author)
• 2002 first book on the theory of GP (with B. 

Langdon)

• 2008 field guide to GP book (with B. Langdon, N. 
McPhee and J. Koza,one of the most cited books 
in GP). Free!!

• Recently evolving better learning rules for neural 
networks using GP and completing the book 
“Taming the Complexity of Evolutionary 
Dynamics” (with C. Stephens)

5

Outline

• Who is your module supervisor?
• Why do we need evolutionary computation and genetic 

programming?

• How will the module be run? (Introduction to CE310)
• How does natural evolution work?

6

Let’s start with an example: Relocation

• Problem 1: Which of your things go 
in which box so that you have as 
few boxes as possible?

• Boxes are expensive, so with fewer 

boxes you save money

• Also, if you need to send the boxes 
via currier, fewer boxes → cheaper 
delivery

Picture from https://www.apartmentshere.com/top-10-moving-tips/

7

Problem 1: Bin Packing Problem (idealized, 1-D)

• Given are N items of different sizes si with i=1...N and B bins 

(boxes) each of capacity c. 

• Goal is to assign each item to a bin such that the total number 

bins is minimised. Let’s assume that all items have sizes si <= c.

• Why relevant? Applications include loading goods in shipping 
containers, warehouse storage, placing files on multiple disks, 
timetabling, …

8

Example Problem 1

Which items go in which bin (box)?

9

Example Problem 1: Intuitive solution (1)

10

Example Problem 1: Intuitive solution (2)

D

E

G

C

A

B

F

E F

A B D

C G

11

Example Problem 1: Intuitive solution (3)

E F

A B D

C G

A B D E FC G

• So, if we put the items ABCDEFG in bins one at a time in the order ABDEFCG

we end up using only 3 bins out of 4

12

Example Problem 1: Intuitive solution (4)

• ABDEFCG is called a permutation of ABCDEFG

(permutation=reshuffling)

• Had we chosen the original order ABCDEFG, we would have used all 4 bins

ABC DE F G

D E

G

A B C

F

• But how do we know the optimal order/permutation?
• A  ”brute-force” approach to solve the problem: Test all permutations!

13

How many permutations are there? (1)
• Suppose we have 3 items to place in boxes: A, B and C

• There are three ways of placing A: 

A can be first (A _ _), second (_ A _), or third (_ _ A). 

• For every placement of A, we only have two ways available for placing B. 

E.g., (A B _) and (A _ B).

• Once both A and B are placed, there is only one slot left for C, 

irrespective of where I placed A and B. 

• So, in total there are 3 x 2 x 1 = 6 = 3! ways of permuting A, B and C: 

ABC, ACB, BAC, BCA, CAB and CBA

14

How many permutations are there? (2)

• In general, the number of permutations of n elements is

𝑃𝑛 = 𝑛!

• In our example bin packing problem, we have n=7

𝑃7 = 7! = 1 ∙ 2 ∙ 3 ∙ 4 ∙ 5 ∙ 6 ∙ 7 = 5,040

15

Combinatorial Optimization

• Problem 1 is a combinatorial optimisation problem. 
• Combinatorial Optimization is concerned with finding an optimal

or close to optimal solution among a finite collection of 
possibilities

• Applications: Logistics, Travel route, Timetabling, Disk 
partitioning, Hyper-parameter selection for AI/ML, …

16

Another combinatorial optimisation 
problem: relocation example 2
• Problem 2: Your things have 

different values, and you cannot fit 
them all in your car. Which items
should you take with you in the first 
trip to your new home?

• You want to load the car with as many 
of the most valuable items as possible 

Picture from https://d2y7gcw37cyxhu.cloudfront.net/images/layout/cat_home/cat_umzugstransporter.jpg

17

Problem 2: Knapsack (Rucksack) problem

• Problem you face if you are constrained by a fixed-size knapsack 

and must fill it with the most valuable items. 

• Given a set of items (i=1...N), each with a size (si) and a value (vi), 
determine which items to include in the knapsack so that the total 
size is less than or equal to a given limit (Smax) and the total 
value is as large as possible (maximize vtot). 

For more info see https://en.wikipedia.org/wiki/Knapsack_problem

18

Computational complexity theory

• What is the computational complexity (amount of time needed to run) 

of the developed solution?

• Testing all permutations leads to the optimal solution, but the time 

required may be too high! 

• The number of operations required grows at least exponentially O(en) 

with size of input n (e= 2.718..)

n! = 1 ∙ 2 ∙ 3 ∙ 4 ∙ 5 ∙ 6 ∙ 7 … > 1 ∙ 2 ∙ 𝑒 ∙ 𝑒 ∙ 𝑒 ∙ 𝑒 ∙ 𝑒 ∙… 

n! = 1 ∙ 2 ∙ 3 ∙ 4 ∙ 5 ∙ 6 ∙ 7 ∙ 8 ∙ 9 ∙ 10 ∙ 11 ∙ 12 … > 1 ∙ 2 ∙ 3 ∙ 4 ∙ 5 ∙ 6 ∙ 7 ∙ 8 ∙ 9 ∙ 10 ∙ 10 ∙ 10 ∙ 10 ∙ 10 ∙… 
• This is the NP (Nondeterministic Polynomial) time complexity class. 

Most combinatorial optimisation problems are NP!

• The exponential growth in possible solutions = combinatorial explosion
• So, what can we do? 

19

Meta-heuristic stochastic optimization 
• Heuristic (from Greek heuriskein = to search): 

Approximate strategies (rules of thumb) or partial search 
algorithm which are problem specific.

• Metaheuristic (metá = beyond): Higher-level, more 

general procedure designed to find, generate, or select a 
heuristic that may provide a sufficiently good solution to 
an optimization problem, with an acceptable 
computation load

• Stochastic: Randomly determined process
• EAs and GP are highly successful meta-heuristics 

suitable for combinatorial optimization.

20

Questions?

21

What have we learnt so far today?

• We have learned about combinatorial optimisation 
problems (Bin Packing problem & Knapsack problem) 
• We have seen that exact/complete algorithms can be 

computationally complex (especially intuitive 
solutions). 

• Consequently, such algorithms may not be a viable 

solution to real-world problems, and we need alternatives 
(meta-heuristics). 

22

Outline

• Hands-on experience: hints for knapsack problem
• Why do we need evolutionary computation and genetic 

programming?

• What is in the module and how will it be run?
• How does natural evolution work?

23

What is in the module and how will it be run?

• The module is all about optimisation and problem solving, so we 

are in the AI domain

• Elements in this section:

• What is Evolutionary Computation?
• What is Genetic Programming?
• Course description, outcomes, assessment
• Sources of information (including online)

24

Evolutionary Computation

• Evolutionary Computation is a branch of Computer 
Science that studies and applies evolutionary 
algorithms (EAs)
• EAs are optimization and search procedures inspired 
by natural evolution. 
• Depending on the structures undergoing optimization, 
the reproduction strategies and the genetic
operations EAs can be grouped into: Genetic 
Algorithms (GAs), Evolution Strategies (ESs), 
Genetic Programming (GP), ....

25

Evolutionary Algorithms

• EAs are systematic methods inspired by Darwinian evolution for 
getting computers to automatically solve problems starting 
from a high-level statement of what needs to be done

• EAs are often domain-independent methods (i.e., they can be 

applied to a variety of domains with relatively little effort) → Need 
to only slightly adjust code

• GAs and ESs are different flavours of EA which act on linear 

representations (arrays) (e.g. problems 1 & 2)

26

Genetic Programming

• Genetic Programming (GP) is a class of EAs for solving problems 

which require solutions in the form of computer programs.

• GP genetically breeds a population of computer programs to solve 

a problem.

• EAs and GP iteratively transform a population of random solutions 

into new generations of better and better solutions.

27

Genetic Programming

• EAs and GP apply analogues of genetic operations like survival of 

the fittest, sexual recombination, mutation, etc.

28

Course Description
• The course starts with a primer on natural evolution 
(today!) and introducing the basics of evolutionary 
algorithms (ESs and GAs, in the next 2-3 weeks).

• Then we move onto the basics of Genetic Programming 

(GP) later studying some of GP's more advanced variants.

• We touch upon other nature-inspired metaheuristics, 

such as Particle Swarm Optimisers (PSOs)

• Part of the course is also devoted to presenting real-world 

applications of EAs and GP.

…all accompanied by hands-on experience in the classes.

29

Learning Outcomes (1)

After completing this module, you can:
• Discuss Evolutionary Algorithms and their relationships.
• Describe Genetic Programming and its relationship with other 

Evolutionary Algorithms.

30

Learning Outcomes (2)

After completing this module, you can:
• Compare application domains for GP and associate these with 

good GP techniques.

• Identify GP parameters and modify existing GP operators, 

representations and fitness functions for specific applications.

31

Syllabus (1)

• Evolution in Nature
• Genetic Algorithms
• Evolution Strategies
• The basics of GP
• Fitness functions in GP
• Advanced Representations
• Code growth and methods to control it

32

Syllabus (2)

• Applications of GP
• Koza's criteria for human-competitive machine intelligence and 

review of GP's human-competitive results

• Advanced GP techniques and tricks of the trade
• Some other nature-inspired metaheuristics.

33

Delivery

• Normally, two hours of lectures per week to cover main body of 
the course and one hour class per week for formative exercises, 
problem solving, interactive coding, etc.

• Learning by doing: To gain insight into the functioning of the 

methods you are expected to code core components yourself
and experiment with the methods outside of the lecture/class 
(spend 8 hours per week on the Module)

34

Assessment

• 60% Examination
• 40% Assignments (out around week 18 with deadline in week 23, see FASER) 
Components:

1. Code and/or run EAs in Python to solve optimisation problems → 50%
2. Code and or run simulations to investigate the impact of GP parameters on performance → 50%
Possibly post-submission elements to verify understanding of code and experimental results
3.

35

Academic integrity, authorship and 
plagiarism
• Plagiarism: “the act of using another person's words or 

ideas without giving credit to that person”

[https://www.merriam-webster.com/dictionary/plagiarism]

• Intentional, reckless, or unintentional? Note that intentional or 

reckless plagiarism is a disciplinary offence

• Please discuss the solutions to tasks among 

yourselves. But have the ambition to implement the 
solution yourself.

• Questions? Please check 

https://www.essex.ac.uk/student/academic-skills/academic-
integrity

36

Coursework help from AIs [work in progress]
• If you use AIs to help you with the coursework, you must make sure you can 

answer any questions I may have on the code or analysis.

• AIs tend to produce the same or similar answers over and over again and, so,       
AI-generated code tends to be flagged up by our plagiarism detection system for 
code.

• Protocol (v1) if you want to get help from AIs in producing the coursework:

1. Keep a log of the steps below and submit it with the coursework
2. Ask the AI to first produce the smallest possible fragment of code that gets you started, 
3. Make sure this does not only run but you fully understand it, e.g., you would be able to 

modify it by hand if required.
2.1 if it is correct proceed to step 4, 
2.2 else fix any issues yourself (preferred) or ask the AI to fix (ok but make sure you fully understand the fix). 
2.3 If you cannot fully understand the code, you  asked the AI to do too big a job. Ask for less.

4. Ask the AI to do a minimal extension of the code that will take you closer to where it needs 

to be and repeat step 3 until you are satisfied.

37

Sources of Information: Main source

• Lectures and classes. Slides, videos, code and handouts 

available on Moodle

• R. Poli, W.B. Langdon, N.F. McPhee. A field guide to Genetic 

Programming, 2008. 

• Free PDF http://www.gp-field-guide.org.uk/

38

Sources of Information: Background

• S. Luke, Essentials of Metaheuristics, Lulu, Second edition, 

2013. 

• Freely available as a PDF from here

• W.B. Langdon, R. Poli, Foundations of Genetic Programming, 

Springer, 2002.

Start with 
this book

39

Other On-line Resources (1)

• The Wikipedia (Evolutionary Algorithms) is a good starting 

point for online reading

• http://en.wikipedia.org/wiki/Evolutionary_algorithms

• A complete bibliography on genetic programming 

maintained by Bill Langdon at 
• https://gpbib.cs.ucl.ac.uk/

40

Other On-line Resources (2)

• Use AIs to ask questions on genetic programming and  

evolutionary algorithms

• Google Scholar http://scholar.google.com

365k hits for “genetic programming”, 613k hits for 
“evolutionary algorithms” and 2.1M hits for “genetic 
algorithm”

41

Questions on the module?

42

Outline

• Hands-on experience: hints for knapsack problem
• Why do we need evolutionary computation and genetic 

programming?

• What is in the module and how will it be run?
• How does natural evolution work?

43

Darwin's Theory of Evolution

• Charles Robert Darwin (1809-1882)
• 1859: On the origin of species …

• Variations (mutations) are present in all species
• Evolution is due to a “force” called natural selection which 
“selects” the individuals best adapted to the environment

• In a constant environment no changes occur as variants will tend 
to lose in the struggle for life. So, species preserve their identity.
• In a varying environment, however, some variants will be better 
than the originals and will be preserved. Species evolve in this 
way.

44

Mendel's independent discoveries

• Gregor Johann Mendel (1822-1884)

• 1865: Versuche über Pflanzenhybriden [Experiments on Plant 

Hybridization]

• Factors, what we now call genes/alleles, determine visible traits

in predictable ways

• Dominant and recessive characters

45

Example: pea colour

YY                                            yy

Yy

YY            Yy

?

?

Yy

Yy

yy

https://www.futurelearn.com/info/courses/genomics-for-educators/0/steps/305264

46

How natural selection works

• Individuals of a population that are fitter tend to survive 

for longer and reproduce

• Their characteristics, encoded in their genes, are 

transmitted to their offspring and, thus, tend to propagate 
into future generations

• In sexual reproduction, the genes of the offspring are a 

mix of those of their parents.

• Offspring's characteristics are partially inherited from 
their parents, and partially the result of new genes 
created during the process of reproduction.

47

Natural selection does not quite mean ”the 
survival of the fittest”
• “Fittest” means “best adapted”, not “in the best condition”
• “Best adapted” means “best adapted with respect to a niche” (a 

relevant sub-set of the environment)
• “Length of life” does not mean “fertility”
• “Fertility” does not mean “successful reproduction” (i.e., 
production of offspring who live long enough to reproduce 
themselves)

48

The cell

Membrane

• Cells are surrounded by a thin oily 

membrane

• The membrane has a voltage of about 
100mV across caused by different  
concentrations of ions inside and outside

• Cells include a nucleus
• The nucleus includes several 

chromosomes (“coloured bodies”)

• In diploid cells, chromosomes are paired 
(homologous chromosomes), the two 
elements of a pair carrying similar 
information

• Chromosomes are made up of DNA

(deoxyribonucleic acid)

49

DNA (1) 

• DNA is made up of bases and 

other molecules
• DNA bases are: 
• A (adenine)
• T (thymine)
• C (cytosine) and 
• G (guanine)

• These molecules are 

organised to form a double 
helix (spiral-shaped ladder)

https://siteman.wustl.edu/wp-content/uploads/ncipdq-media/CDR0000761781.jpg
50

DNA (2)
• DNA is a long description (a book) whose “characters” are T, G, C, A 

(about 3 billion bases in humans)

• The “words” of the DNA include three bases (triplets or codons) 

and represent amino-acids (building blocks of proteins)

e.g., TCT=Serine, CAA=Glutamine, TAA=Stop

• A gene is represented by a “sentence”  (a meaningful sequence of 

triplets) in the DNA

• Some triplets represent stop symbols (the end of a sentence)

51

Genetic code (1)

Also start symbol

52

Genetic code (2)
• Most genes (sentences in the DNA) code for proteins (structural

genes, i.e., trait determining factors)

E.g., haemoglobin→

• Some segments of the DNA have regulatory purposes, i.e., they 

bind to specific sequences in the DNA and control which genes to 
turn on or off under any particular conditions.

• Other genes have no function (introns, ”junk DNA”) or we do not 

understand their function yet.

53

Genetic code (3)

• A gene can be represented by a number of slightly different 

sequences called alleles.

• Gene is a portion of the DNA that determines a trait
• Allele express the characteristics (e.g., hair colour)

• Each homologous chromosome may have a different allele for each 

gene (remember the peas example)

• Approximately speaking, alleles are dominant if they produce

much more (and sufficient) protein than their recessive 
counterparts.

54

Genetic code (4)

• Central dogma of molecular biology (DNA as blueprint):
• DNA replicates to produce more DNA (DNA→DNA)
• DNA is transcribed into ribonucleic acid (RNA) which is 
translated into proteins (DNA→RNA→Protein)
• During these processes DNA can undergo mutations

• Copy error (10-10 nucleotides)
• Induced due to exposure to chemicals, UV, X-rays, … 
(external influences)
• Spontaneous due to reactions within organism

55

Type of mutations
• Substitution: Exchange one base for another

• Condon (triplet) encodes a different amino acid, the 

same amino acid or STOP (incomplete proteins)

• Insertion: Extra base pair inserted
• Deletion: Section of DNA lost or deleted
• Frameshift: Insertions/deletions can alter a gene so that 

message is no longer correctly parsed.

Example: The fat cat sat → hef atc ats at

• … 
• Mutation can be beneficial, neutral, or harmful!

56

Summary of main properties of DNA

• It stores and transmits information
• It copies itself (mainly) to generate proteins but 
also to transmit information
• It can mutate

57

Meiosis – Reproduction (1)

In meiosis (preparation of egg and sperm cells) homologous
chromosomes duplicate (46→92) (cyan=maternal, red=paternal)

Shyamala Iyer. (2014, February 03). Cell Division. ASU - Ask A Biologist. Retrieved January 8, 
2020 from https://askabiologist.asu.edu/cell-division
58

Meiosis – Reproduction (2)

Because of close proximity, they can become entangled, resulting 
in chromosomes that are a mixture of maternal and paternal genes 
(“crossover" or "genetic recombination”)

Shyamala Iyer. (2014, February 03). Cell Division. ASU - Ask A Biologist. Retrieved January 8, 
2020 from https://askabiologist.asu.edu/cell-division
59

Meiosis – Reproduction (3)

• The cell then divides twice so that only one of the 

homologous chromosomes of a pair is present in the 
resulting cells (sperm or eggs).

Shyamala Iyer. (2014, February 03). Cell Division. ASU - Ask A Biologist. Retrieved January 8, 
2020 from https://askabiologist.asu.edu/cell-division
60

Mating and Growth

• Mating produces (diploid) cells that start duplicating (mitosis)
• Duplication involves chromosome copying and cell division (no
crossover). Mutations can occur during the copying phase.
• The process of growth transforms the information in the genes 

(genotype) into an adult individual (phenotype).

• Growth is controlled mainly by the environment (but also by genetic 

factors)

• During the development of an individual cells specialise

(differentiation) and migrate

61

Cell differentiation
• Wait: all cells have exactly the same DNA! So, how do we get 

skin cells, neurons, muscle cells, …?

• Cell differentiation happens thanks to the regulation of gene
expression determined by environment surrounding the cell

• Regulation is performed by tracts of DNA that function as 

switches for groups of genes.

By Haileyfournier - Own work, CC BY-SA 4.0, 
https://commons.wikimedia.org/w/index.php?curid=79600426

62

Questions?

63

What did we learn today? (1)

• We have learned that combinatorial optimisation 

problems (Knapsack problem & Bin Packing problem) can 
be solved with meta-heuristic stochastic optimisation 
methods such as Evolutionary Algorithms. 

• In this module we will learn about EAs and work with 

them as tools to solve different types of (continuous and 
combinatorial) optimisation problems.

• EAs can also be used a form of machine learning: 

program induction (Genetic Programming)

• We also learned what is required in terms of assessment.

64

What did we learn today? (2)
• Natural selection means individuals in a population that 
are fitter with respect to their environment produce more 
offspring. The trait that made those individuals succeed 
becomes common in the population.

• Genes encode the various traits of an individual. All traits 

of an individual are combined in a long linear 
representation (1-D array) (DNA).

• Genetic recombination (crossover), i.e., the exchange of 

genetic material to create offspring's that are different 
than the parents, and random mutations drive evolution.

65

Don’t forget to …
…catch-up with Python coding if necessary in preparation for the 
lab this Friday.

Resources:

• Python (https://www.python.org/)
• Jupyter Lab (https://jupyter.org/)
• Anaconda (https://www.anaconda.com/)
• Google Colab (https://colab.research.google.com)
• VirtualLab (https://csee-horizon.essex.ac.uk/)

66

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Thanks for your participation!
Next time: 
Translating natural 
evolution into algorithms

```

---

## B. Lecture 02（PDF可提取全文）

```text

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Introduction to Genetic Algorithms

What did we learn last week? (1)

• We have learned about combinatorial optimisation problems 

(Knapsack problem & Bin Packing problem) and that exact 
algorithms can be computationally complex (especially intuitive 
solutions). Consequently, exact algorithms may not be a viable 
solution to real-world problems, and we need alternatives. 
• Meta-heuristic stochastic optimisation methods such as 

Evolutionary Algorithms are such an alternative. 

• In this module we will learn about EAs and work with them as 

tools to solve different types of problems.

2

What did we learn last week? (2)

• Natural selection means individuals in a population that are fitter 

with respect to their environment produce more offspring. The 
trait that made those individuals succeed becomes common in 
the population.

• Genes encode the various traits of an individual. All traits of an 
individual are combined in a linear representation (1-D array) 
(DNA).

• Genetic recombination (crossover, XO), i.e., the exchange of 
genetic material to create offspring's that are different from the 
parents, and random mutation drive evolution.

3

Today’s learning objectives (Part 1)

• Understand the nature-to-computer mapping 
• See how all Evolutionary Algorithms (EAs) conform to a General 

Evolutionary (GEA)

• Become familiar with a binary generational Genetic Algorithm 

(GA)

4

Evolutionary Algorithms (EAs)
• EAs are algorithms inspired to natural evolution, i.e., EAs 

simulate the key ingredients of evolution.

• Applications:

• Combinatorial optimisation (e.g., which packages go in a lorry to 

maximise load value? What is the shortest route to deliver packages?)

• Function optimisation (e.g., minimum or maximum of a function)
• Automatic programming (GP) 
• Machine learning
• Problem solving
• Automatic design, etc.

5

Nature-to-Computer mapping

• Individual: Solution to a problem
• Population: Set of solutions
• Fitness: Quality of a solution
• Chromosome: Representation for a solution
• Gene:Part of the representation of a solution
• Growth: Decoding of solutions (from “genes” to “creatures” :-)
• Crossover and mutation: Search operators
• Natural selection: Reuse of good (sub-)solutions

6

Example: Knapsack (Rucksack) problem

• Problem you face if you are constrained by a fixed-size knapsack 

and must fill it with the most valuable items. 

• Given a set of items (i=1...N), each with a weight/size (wi) and a 

value (vi), determine which items to include in a collection so that 
the total weight is less than or equal to a given limit/capacity 
(wmax) and the total value is as large as possible (maximize vtot). 

7

chosen items

8

Flashback: Evolution in Nature

https://www.genome.gov/sites/default/files/tg/en/illustration/dna_deoxyribonucleic_acid_adv.jpg

9

Knapsack: Representation of the solution?

10

Knapsack: Fitness of the solution?

11

Individual vs. Population

15

General Evolutionary Algorithm (1)

Initialise and evaluate fitness of population

1.
Repeat until quality of solution “sufficiently good” (or max 
generations exceeded):

2. Select sub-population for reproduction (Selection)
3. Recombine the “genes” of selected parents (Recombination or 

Crossover, XO)

4. Mutate new individuals randomly (Mutation)
5. Evaluate the fitness of the new population
6. Select the survivors from the actual fitness

16

Example

17

General Evolutionary Algorithm (2)

• Not all these steps are present in all EAs.
• There are as many EAs as researchers in EC!
• We will look at 3 main types:
• Genetic algorithms
• Evolution strategies
• Genetic programming

18

Genetic Algorithms (GAs)

• In GAs there is a strong distinction between phenotype (i.e., 

adult individual, solution) and genotype (i.e., chromosome, 
representation)

• GAs (like nature) act on genotypes only and a genotype-to-
phenotype decoding process is required (i.e., artificial 
growth)

• Chromosomes are strings/arrays of symbols (originally 0s & 

1s)

• Adult individuals can be anything as long as there is a way of 
representing them using a string of symbols (chromosome).

19

Generational GA (1)

1. Randomly generate a population of 

chromosomes/individuals

2. Evaluate the fitness of each individual (may require 

growing/decoding it first)

3. Generate a new population partly by cloning (copying), 

partly by recombining (crossover) and partly by mutating 
the chromosomes of the fittest individuals
4. Repeat 2 & 3 until a stop condition is true.
Note: There is no overlap between generations (hence generational GA). 
Cloning is used to simulate the survival of parents for more than one 
generation.

20

Generational GA (2)

21

A different example: Problem definition

• Problem: 

Find the number in the range {0,1,...,255}  with the 
maximum number of 2’s in it.

• Obvious solution: 

222

22

A different example: Getting ready

Decisions to be made before starting the GA:
• Chromosomes: strings of 8 binary digits (bit strings)
• Fitness evaluation: counting the number of 2’s in decimal 

representation of chromosome.

• Population: 10 individuals.
• Selection: use only the best 5 individuals for mating.
• Cloning: each of the selected individuals is copied.
• Recombination/Crossover: cutting two bit strings at a random 

position and swapping the left hand sides.

• Mutation: none.

23

A different example: Initialisation

#  
#  
#  
#  

Genotype
Genotype
Genotype
Genotype

Phenotype
Phenotype
Phenotype
Phenotype

Fitness
Fitness
Fitness
Fitness

a
a
a
a

b
b
b
b

c
c
c
c

d
d
d
d

e
e
e
e

f
f
f
f

g
g
g
g

h
h
h
h

i
i
i
i

j
j
j
j

10010111
10010111
10010111
10010111

01010010
01010010
01010010
01010010

11101010
11101010
11101010
11101010

00101001
00101001
00101001
00101001

11001010
11001010
11001010
11001010

10111110
10111110
10111110
10111110

01001110
01001110
01001110
01001110

10010010
10010010
10010010
10010010

00100000
00100000
00100000
00100000

11111110
11111110
11111110
11111110

151
151
151

82

234

41

202

190

78

146

32

254

0
0

1

1

0

2

0

0

0

1

1

24

A different example: Selection

#  

Genotype

Phenotype

Fitness

e

b

c

i

j

d

a

f

g

h

11001010

01010010

11101010

00100000

11111110

00101001

10010111

10111110

01001110

10010010

202

82

234

32

254

41

151

190

78

146

2

1

1

1

1

0

0

0

0

0

25

A different example: Selection

#  

Genotype

Phenotype

Fitness

e

b

c

i

j

11001010

01010010

11101010

00100000

11111110

202

82

234

32

254

2

1

1

1

1

26

A different example: Crossover

#  

Genotype

Phenotype

Fitness

Parent

Parent

e

b

1100 1010

0101 0010

Offspring

eb

1100 0010

202

82

194

2

1

0

27

A different example: Crossover
#  

Genotype

Phenotype

Parent

Parent

e

c

11 001010

11 101010

Offspring

ec

11 101010

202

234

234

Fitness

2

1

1

28

A different example: Crossover
#  

Genotype

Phenotype

Parent

Parent

Offspring

i

j

ij

00100 000

11111 110

00100 110

32

254

38

Fitness

1

1

0

29

A different example: Crossover

#  

Genotype

Phenotype

Fitness

Parent

Parent

Offspring

c

i

ci

11101 010

00100 000

11101 000

234

32

232

1

1

2

30

A different example: Crossover

#  

Genotype

Phenotype

Fitness

Parent

Parent

Offspring

e

j

ej

110 01010

111 11110

110 11110

202

254

222

2

1

3

31

A different example: New population

#  

Genotype

Phenotype

Fitness

e

b

c

i

j

eb

ec

ij

ci

ej

11001010

01010010

11101010

00100000

11111110

11000010

11101010

00100110

11101000

11011110

202

82

234

32

254

194

234

38

232

222

2

1

1

1

1

0

1

0

2

3

32

A different example: New pop. sorted by fitness

#  

ej

ci

e

b

c

i

j

ec

eb

ij

Genotype

Phenotype

Fitness

11011110

11101000

11001010

01010010

11101010

00100000

11111110

11101010

11000010

00100110

222

232

202

82

234

32

254

234

194

38

3

2

2

1

1

1

1

1

0

0

33

A different example: Observations

• The solution, 222, has been obtained after one generation. 
Usually, many generations are needed to find solutions.
• The average fitness of the population tends to increase 

generation after generation.

• Good solutions tend to have similar binary strings (e.g., all 
solutions end with 0 and the first 3 solutions start with 11…)

34

Any questions?

35

Today’s learning objectives (Part 2)

• Learn how to represent solutions (integer and real-valued 

parameters) for binary Genetic Algorithms (GAs)

• Become familiar with different ways to select individuals for 

reproduction and designate a solution

• Get a clear idea of the difference between generational and 

steady-state GAs

• Learn different ways to implement crossover and mutation 

operators in binary GA
• Design a non-binary GA

36

Solution Encoding in binary GAs

Note: least significant bit first!
(“Little Indian” bit order)

• Integer parameters: We can encode integer parameters p by 

using N consecutive bits bi of a chromosome. 

• For instance, 𝑏1 … 𝑏𝑁 can be interpreted/decoded as the integer 
𝐩 = 𝐛𝟏 ∙ 𝟐𝟎+𝐛𝟐 ∙ 𝟐𝟏+𝐛𝟑 ∙ 𝟐𝟐+ … +𝐛𝐍 ∙ 𝟐𝐍−𝟏
E.g., if   b1b2b3b4b5b6b7b8 = 11110000, then
p = b1∙1 + b2∙2 + b3∙4 + b4∙8+ b5∙16 + b6∙32 + b7∙64 + b8∙128
   = 1∙1 + 1∙2 + 1∙4 + 1∙8+ 0∙16 + 0∙32 + 0∙64 + 0∙128 = 1+2+4+8 = 15 

In Python?

def decode(chromosome):

return int(''.join(map(str, chromosome[::-1])),2)

37

 
Solution Encoding in binary GAs

• Integer parameters: We can encode integer parameters p by 

using N consecutive bits bi of a chromosome. 

• For instance, 𝑏1 … 𝑏𝑁 can be interpreted/decoded as the integer 
𝐩 = 𝐛𝟏 ∙ 𝟐𝟎+𝐛𝟐 ∙ 𝟐𝟏+𝐛𝟑 ∙ 𝟐𝟐+ … +𝐛𝐍 ∙ 𝟐𝐍−𝟏
E.g., if   b1b2b3b4b5b6b7b8 = 11110000, then
p = b1∙1 + b2∙2 + b3∙4 + b4∙8+ b5∙16 + b6∙32 + b7∙64 + b8∙128
   = 1∙1 + 1∙2 + 1∙4 + 1∙8+ 0∙16 + 0∙32 + 0∙64 + 0∙128 = 1+2+4+8 = 15 

• This works well if p varies in the range [0, 1,… 2N-1]
• What if the smallest p must be a number >0, say M?

38

Integers (1)

• More generally, if we need to represent only certain integer 

values [𝑰𝟏, 𝑰𝟐, … , 𝑰𝑵] we can use a lookup table

For example, if the only 
valid values of p are 4, 
22, 79, and 311, we can 
use N=2 and the table

Genotype Phenotype

Genotype

Phenotype

00

01

10

11

4

22

79

311

00......000

00......001

00......011

…

11......111

I1
I2
I3
…
IN

Problem: What happens if we have a number of values which isn't a 
power of 2? Why is this a problem?

39

Integers (2)

Suppose we have L distinct 
integers [I1, I2, … , IL] and 
𝐿 ≠ 2𝑁. 
For example, p can be 4, 22, 
79, 88, 131 and 311, only. 
We can use N=3                     ➔
Solutions:

• Clipping
• Wrapping
• Scaling

Genotype
000
001
010
011
100
101
110
111

Wrapping 
around
Phenotype
4
22
79
88
131
311

Phenotype
4
22
79
88
131
311

Phenotype
4

22

79
88
131
311

40

Real-valued parameters (1)

• Real-valued parameters can, in 

principle, be represented similarly to 
integer using a look up table

• However, if the values are equally 

spaced, the table can be 
represented more concisely.

Genotype
00......000
00......001
00......010
00......011
00......100
…

Phenotype
0.1
0.2
0.3
0.4
0.5
…

41

Real-valued parameters (2)
Fixed-point representation 

• If the parameter p must be in some range, [ pmin , pmax ], and we 

want to use N bits to encode it, then we can use:

𝒑 = 𝒑𝒎𝒊𝒏 +

𝒅𝒆𝒄𝒐𝒅𝒆 𝒃𝟏, … , 𝒃𝑵
𝟐𝑵 − 𝟏

∙ 𝒑𝒎𝒂𝒙 − 𝒑𝒎𝒊𝒏

𝒅𝒆𝒄𝒐𝒅𝒆 𝒃𝟏, … , 𝒃𝑵 = 𝒃𝟏 ∙ 𝟐𝟎 +   … + 𝒃𝑵 ∙ 𝟐𝑵−𝟏

• Example: if N=2, pmin = -1.0, pmax = +1.0 then
∙ +1.0 − (−1.0) = −1.0 +
    𝑝 = −1.0 +

𝑏1∙20+ 𝑏2∙21
22−1
So, b1b2=10 becomes 𝑝 = −1.0 +

𝑏1∙1+ 𝑏2∙2
3

∙ 2

1∙1+0∙2

3

∙ 2.0 = −1.0 +

1

3

∙ 2.0 = −

1

3

42

Real-valued parameters (3)

• Note: the resolution, i.e., the difference between two consecutive 

reals, is

𝐫𝐞𝐬𝐨𝐥𝐮𝐭𝐢𝒐𝒏  =

𝒑𝒎𝒂𝒙 − 𝒑𝒎𝒊𝒏
𝟐𝑵 − 𝟏

For instance, for N=2 and (pmax - pmin)=2 we have 
resolution=2/3=0.6666...
So, for real-valued parameters there is a conflict between the 
desire to keep the genes short for good convergence and the need 
to know the result with a certain precision.

43

Solution Encoding in binary Gas (1)

• Multiple of parameters (whether binary, integers, reals or a 

combination of them) are encoded combining (e.g., 
concatenating) their representations

44

Solution Encoding in binary Gas (2)
• Concatenation is not the only method
• When the same number of bits is used to encode each parameter, 

interleaving them can also be good under 1-point crossover

• If bi 

p = bit i of parameter p

• Traditional: b1

1 b2

1 b3

1 …b1

2 b2

2 b3

2 ….b1

N b2

N b3

N …

• Interleaved: b1

1 b1

2 b1

3 …b2

1 b2

2 b2

3 ….bN

1 bN

2 bN

3 …

45

 
Selection basics (1)
• Selection is the operation by which individuals (chromosomes) 
are randomly selected for mating or other genetic operations 
(mutation and cloning).

• Obviously for crossover, pairs of individuals are needed to 

produce an offspring

• For cloning, only single individuals are picked by each selection 

invocation.

• To emulate natural selection individuals with a higher fitness 

should be selected with a higher probability

• There are many different models of selection: some that are 

biologically plausible and some that are not.

46

Selection basics (2)

• Assumptions (for now):

• A quality measure Q (objective function) for the solutions of the problem 

is known.

• Q has to be maximised.
• Q is (almost) always positive.
• We take the (raw) fitness f of an individual to be its quality measure Q, i.e.,
f = Q

• For instance, if Q=total value of knapsack we can use f = Q

47

Fitness Proportionate Selection (FPS)

• FPS is often used in GAs.

• Let 𝒇𝒊 be the fitness of individual i, 𝒇𝒂𝒗𝒈 =

𝑓1+𝑓2+⋯+𝑓𝑀
𝑀

be the average fitness and M be the size of the population

• In FPS, individual i is selected for reproduction with a probability

𝒑𝒊 =

𝑓𝑖
𝑓1 + 𝑓2 + ⋯ + 𝑓𝑀

=

𝑓𝑖
𝑓𝑎𝑣𝑔 ∙ 𝑀

=

𝑓𝑖
𝑓𝑎𝑣𝑔

∙

1
𝑀

48

Roulette-wheel algorithm (1)

• For example, if M = 4, f1 = f2 = 10,  

f3 = 15 and f4 = 25

• Implementation: a random 
number r in [0, f1+ f2 +… fM) 
is chosen and individual i is 
selected if
f1+ f2 + … + fi-1  ≤  r  <  f1 + f2 + … + fi

49

Roulette-wheel algorithm (1)

• In the example, f1+ f2 + f3 + f4 = 60, so r is a random number in 

[0,60)

• Suppose the random
   number generator
   produces r = 23.5, 
   then                           ➔

  So, i=3.

i

1

2

3

4

Test

0 <= 23.5 < 10

10 <= 23.5 < 20

20 <= 23.5 < 35

35 <= 23.5 < 60

Result

False

False

True

False 
(but unnecessary)

50

Properties of FPS (1)
• Imagine that only cloning is taking place (no XO, no Mut) to 

produce a new generation of M individuals.

• Because we use cloning, M individuals have to be selected. 
• So, the expected number of copies of each individual in the new 
𝑓𝑖
𝑓𝑎𝑣𝑔

generation is:  𝑁𝑖 = 𝑝𝑖 ∙ 𝑀 =

• 𝑁𝑖 is usually a real number. The actual number of copies (an 

integer) will vary around Ni. 

51

Properties of FPS (2)
• Since 
𝑁𝑖 =

𝑓𝑖
𝑓𝑎𝑣𝑔

 ,    individuals with 𝒇𝒊 > 𝒇𝒂𝒗𝒈 tend to have 

more than one copy in the next generation

• For the same reason, below average individuals tend not to be 

copied.

• In a GA using recombination (crossover) and mutation, the 

principle is the same:

Above average individuals have a higher-than-average probability of being 
chosen as parents and vice versa.

52

Problems with FPS: Premature Convergence

• Suppose an individual with 𝑓𝑖  much bigger than 𝑓𝑎𝑣𝑔 but 𝑓𝑖 much 

smaller than 𝑓𝑚𝑎𝑥 is produced in an early generation.

• Such an individual will be selected very often for crossover and 

cloning.

• So, unavoidably the genes of such individual quickly spread all 

over the population, rendering it too uniform.

• At that point recombination cannot generate any new solutions 

(only mutation can) and 𝑓𝑎𝑣𝑔 is likely to remain much smaller than 
𝑓𝑚𝑎𝑥 forever.

53

Problems with FPS: Stagnation

• Towards the end of a run all individuals tend to have relatively high 
and similar values of fitness, i.e., 𝑓𝑖 is approximately equal to 𝑓𝑚𝑎𝑥 
for all i

• At that point 𝑁1 … 𝑁𝑀 are all approximately 1, so there is a very 
small selective pressure, i.e., the best solutions are favoured 
only slightly with respect to the worst ones.

Both problems can be solved with fitness scaling techniques, but 
other selection methods avoid the problems more naturally.

54

Tournament selection

• A group of N ≥ 2 random individuals is created
• The individual with the highest fitness in the group is selected, the 

others are discarded (tournament)

•  Advantages:

• No premature convergence
• No stagnation
• No global reordering required
• Explicit fitness not needed
• Naturally inspired

55

Solution designation

Which solution (individual) among the candidate solutions to 
chose?
• Fittest individual in the last generation
• Alternatively: save the fittest solution ever discovered, 

designate such structure as the solution

56

Steady State GAs

• In steady state GAs, the offspring are inserted in the current 
population, usually replacing the worst individual in the 
population.

• Sometimes an inverse tournament selection is used and the 

worst in the tournament is replaced.

• Steady state GAs require less memory and may be more efficient 

as they exploit the genetic material of a good solution 
immediately.

57

Properties of Crossover Operators

• Evolutionary algorithms work well only if their genetic operators 
allow an efficient and effective search of the solution space.

• Typical properties of good genetic operators:

• When parents share a common feature their offspring should always 

inherit such a feature.

• When parents have two different features it should be possible for the 

offspring to inherit both such features.

• These properties are often partially incompatible and operators 
with such properties can be more computationally demanding.

58

Crossover in binary GAs (1)

• One-point crossover involves cutting the chromosomes of the 

parents at a randomly chosen common point and exchanging the 
right-hand-side sub-chromosomes

Parent a
Parent b
Offspring

11 111111
00 000000
11 000000

59

Crossover in binary GAs (2)

• Two-point crossover involves cutting the chromosomes of the 

parents at two randomly chosen common points and exchanging 
the middle sections

Parent a
Parent b
Offspring

11 111 111
00 000 000
11 000 111

• N-point crossover is similarly defined.

60

Crossover in binary GAs (3)

• In uniform crossover each gene of the offspring is selected 
randomly from the corresponding genes of the parents, e.g.

Parent a
Parent b
Offspring

11111111
00000000
11010110

• Crossover is applied to the individuals of a population with a 
constant probability/rate pc (typically pc is within [0.5, 0.8])
• Cloning is applied with a probability 1- pc to keep the size of the 

population constant

61

Mutation in binary GAs (1)

• Mutation consists of making (usually small) alterations to the 

values of one or more genes in a chromosome

• In GAs, traditionally mutation is applied to the individuals 

produced by crossover and cloning before they are added to the 
population.

62

Mutation in binary GAs (2)

• In binary chromosomes mutation consists of inverting random 

bits (bit flip) of the genotypes, e.g.

11111111
Parent
Offspring 11101101

• Traditionally, in GAs, mutation is considered a method to recover 
lost genetic material (rather than to search for better solutions)
• In GAs, mutation is applied with a very low probability/rate pm 

(per bit). Generally pm is within [0.001, 0.01].
• A good rule of thumb is pm =1/Number of bits

63

Non-binary GAs (1)

• Non-binary chromosomes can be used to encode parameters that 

can take only a small number of values.

• Examples:

• If a parameter p is in the set {0, 1, 2}  we can simply use a ternary 

alphabet instead of a binary one

• If p is in the set {Rome, Milan, Birmingham, London, New York, Paris}, we 

can encode it using letters {R,M,B,L,N,P} or numbers {0,...,5}

64

Non-binary GAs (2)
• Genes may be treated as atomic (discrete) or not based on the 

application domain.

• If a gene is 3.2 and another is 3.4, does it make sense to talk about a 

gene half-way between them (3.3)? What about 36 and 42 vs 39?

• If 3.2 and 3.4 represent continuous quantities, e.g., temperatures, 
then 3.3 make senses. If they represented version numbers of a 
public API, maybe 3.3 was never released!

• If 36 and 42 represent number of apples, then 39 is a valid 

outcome, but if 36=Colchester and 42=Johannesburg, what is 39?
• Different forms of crossover and mutation are needed depending 

on whether it makes sense to interpolate genes or not.

65

Any questions?

66

What did we learn today? (1)

• We have learned how basic concepts of evolution in nature can be 

applied to solve real world problems. 

• We learned about the General Evolutionary Algorithm (GEA), 
which iteratively applies operators such as selection, cloning, 
recombination, and mutation to evolve solutions that are “fitter” 
and provide a more satisfactory solution to the problem.

• If we can find a linear representation for the solution of a problem, 

then we can use the GEA approach to solve that problem.

67

What did we learn today? (2)

68

What did we learn today? (2)

• We have learned how to encode integer and real-valued 

parameters for binary GA and that for real-values there is a 
trade-off between bitstring length and precision.

• We have learned about the concepts of fitness proportionate 

selection (FPS) and tournament selection. 

• We have learned that steady-state GAs insert offspring into the 

current population and exploit the genetic material of good 
solutions immediately.

69

What did we learn today? (3)

• We learned about one-point, two-point and uniform crossover 
(XO) and that these methods are applied to individuals with a 
certain probability pc with cloning being applied with a 
probability of 1- pc.

• We have learned that mutation is applied after crossover or 

cloning with a very low probability per bit.

• We have learned that GAs can be used with non-binary 

alphabets. 

70

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Thank you for your 
participation

Next time: 
GA applications and advanced 
techniques!

```

---

## B. Lecture 03（PDF可提取全文）

```text

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Genetic Algorithms
 Applications and  more 
Advanced Techniques

Today’s learning objective
• Describe how Genetic Algorithms can be used to solve 

unconstrained function optimisation and unconstrained 
combinatorial optimisation problems.

• Develop appropriate fitness functions for various problems.
• Describe crossover and mutation operators for real-valued 
Genetic Algorithms (GAs) and discuss possible ways to  
implement them.

• Describe rank selection
• Summarize different cases of mapping objective functions into 

fitness functions. 

• Discuss fitness functions in terms of constrained optimization 

problems

2

Constrained vs Unconstrained Optimisation

• Unconstrained optimisation means that we are looking for 

optimal solutions in a search space where every point we can visit 
is a valid solution.

• Constrained optimisation means that we are looking for optimal 
solutions in a search space where there are places that represent 
invalid or unacceptable solutions  (constraints). So, we must avoid 
such places. 

3

GA for Unconstrained Optimisation

• GAs can be easily used for:

• Unconstrained function optimisation, i.e., to find the values for the 
parameters that minimise or maximise a given objective function 𝑈(𝑥)

• Unconstrained combinatorial optimisation, i.e., to find the best 

combination of choices (for example integers) that optimise the function 
𝑈(𝑥)

The difference is only in the nature of the variables x: continuous vs. 
discrete.

4

Example: unconstrained function optimisation

• Find the minimum* of this parabola:

𝑦 = 0.4 𝑥2  −  2.76 𝑥  −  5.864

*Meaning: find the x
  value where the y 
  value is lowest

NOTE: x is continuous 
(real/float)

5

Example: unconstrained combinatorial 
optimisation
• The bin packing problem!
• It is combinatorial because solutions are represented by discrete 

quantities (permutations/lists of integers) 

• It is unconstrained because we have as many bins as needed, so 

any permutation is a valid assignment of items to bins. 

• Note, it would be constrained optimisation if:

• We have a limited number of bins. So, permutations that run out of bins 

are invalid

• If we used as a representation any list of integers (not guaranteed to be a 

permutation), lists where some items are binned twice or are never 
binned are invalid

6

Example 1: Neuron Evolution

• We are given this artificial neuron:
• First it computes its net input:  

 𝑛𝑒𝑡 = 𝑤1 ∙ 𝐼1 + 𝑤2 ∙ 𝐼2 + 𝑏
• Then it computes its output:

O(net) = 1  if net > 0
O(net) = 0  otherwise

def output(I1,I2,w1,w2,b):
    net = w1*I1 + w2*I2 + b
    if net > 0:
        return 1
    else:
        return 0

7

  
Example 1: Problem

• Find weights (w1 and w2) and bias (b) so that the neuron implements 

the Boolean OR function

T (I1 OR I2)

I1
0

0

1

1

I2
0

1

0

1

• Our objective function is to minimise the error:
  𝑈 𝑤1, 𝑤2, 𝑏 = abs 𝑂1 − 𝑇1 + abs 𝑂2 − 𝑇2 +

         abs 𝑂3 − 𝑇3 + abs 𝑂4 − 𝑇4

where:
• each term represents a fitness case (e.g., a row of the truth table),
• T1, T2, ... is the desired output of the neuron for a fitness case
• O1, O2,... is the corresponding actual output on the neuron

def output(I1,I2,w1,w2,b):
    net = w1*I1 + w2*I2 + b
    if net > 0:
        return 1
    else:
        return 0

8

     
 
Example 1: Solution approach
• Let us use a binary GA to solve the problem
• Parameters of the GA:

• One-point crossover with pc = 0.7
• No mutation
• Tournament selection (N = 2)
• Chromosomes = strings e1e2e3 with ei in the set {-1, 0,1}
• Search space size = 33 = 27 (# different networks)  
• Fitness: 𝑈 𝑤1, 𝑤2, 𝑏 = number of errors (worst=4, best=0), so…

𝒇  =  𝑒𝑟𝑟𝑜𝑟𝑚𝑎𝑥 –  𝑒𝑟𝑟𝑜𝑟  =  𝟒  −  𝑼(𝒘𝟏, 𝒘𝟐, 𝒃) 

• Number of individuals = 4
• Number of Generations = 3

9

 
 
Example 1: A few generations by hand (1)

Pop 0

Fitness

Pop 1

Fitness

-1-1 0

-1 0 1

0 0 1

1 1-1

1

1

3

2

1.75

average

10

Example 1: A few generations by hand (2)

Pop 0

Fitness

Pop 1

Fitness

001

3

-1-1 0

-1 0 1

0 0 1

1 1-1

1

1

3

2

1.75

11

Example 1: A few generations by hand (3)

Pop 0

Fitness

Pop 1

Fitness

001

111

3

3

-1-1 0

-1 0 1

0 0 1

1 1-1

1

1

3

2

1.75

12

Example 1: A few generations by hand (4)

Pop 0

Fitness

Pop 1

Fitness

001

111

000

3

3

1

-1-1 0

-1 0 1

0 0 1

1 1-1

1

1

3

2

1.75

13

Example 1: A few generations by hand (5)

Pop 0
Pop 0

Fitness
Fitness

Pop 1
Pop 1

Fitness
Fitness

Pop 2

Fitness

-1-1 0
-1-1 0
-1 0 1
-1 0 1
0 0 1
0 0 1
1 1-1
1 1-1

1
1
1
1
3
3
2
2
1.75
1.75

0 0 1
001
1 1 1
111
0 0 0
000
1 1 0
110

3
3
3
3
1
1
4
4
2.75
2.75

1 1 0

1 0 1

1 1 0

1 0 1

4

3

4

3

3.5

average

average

14

Example 1: A few generations by hand (6)

• The best string is 110 which corresponds to a neuron that 

implements exactly the OR function:

• Solutions sampled: 4 (individuals) x 3 (generations) = 12
• Fraction of search space explored: 12 / 27 = 44%

15

Example 2: Sphere Model

• We want to minimise the function
     𝑈 𝑥1, 𝑥2, 𝑥3 = 𝑥1 ∗ 𝑥1+ 𝑥2 ∗ 𝑥2+ 𝑥3 ∗ 𝑥3

with xi  real values in the range [-10, 10].

• The known minimum is (0,0,0)

• This function can be visualised only the equivalent of a heatmap 

or by reducing its dimensionality (e.g., by “slicing” or projecting its 
“3-D shadow”).

16

Example 2: Sphere Model
• Here it is as a 3-D heat map

17

Example 2: Sphere Model

• Here a plot of is its “slice” for x3 = 0
  𝑈𝑠𝑙𝑖𝑐𝑒 𝑥1, 𝑥2 = 𝑈 𝑥1, 𝑥2, 0

x1

x2

18

  
Example 2: Solution approach

• Let us use a binary GA to solve the problem
• Parameters of the GA:

• One-point crossover with pc = 0.7
• Mutation with pm = 0.01
• Tournament selection (N=2)
• Chromosomes with 3 × 10 = 30 bits 

  (Resolution = interval / #possible values = 20 / 210  = 20 / 1024 = 0.0196)

• Size of search space: 230=1,073,741,824
• Fitness function: 𝑓  =   −𝑼(𝒙𝟏, 𝒙𝟐, 𝒙𝟑)
• Number of individuals = 200
• Number of Generations = 50

19

 
 
 
Example 2: Fitness vs. generation plot

20

Example 2: Solution
• Best solution after 50 generations:

0000000001 1111111110 0000000001 
(LSB to MSB), that is x1 = x3 = 0.009777 and x2 = -0.009777, which 
corresponds to U = 0.000287.

• Why don't we get x1 = x2 = x3 = 0.0 (and U=0.0)?
   Hint: 0.009777 = Resolution / 2
• Solutions sampled: 200 x 50 = 10,000
• Fraction of search space explored: 0.00093%

21

Example 3: π (3.1415...)

• Find the best rational approximation of π using integers between 0 

and 1023

  i.e., find 𝒙𝟏 and 𝒙𝟐 such that 𝒙𝟏 /𝒙𝟐 is as close as possible to π
• This can be recast as: 

  minimise the function

 𝑈 𝑥1, 𝑥2 = 𝑎𝑏𝑠

𝑥1
𝑥2

− 𝜋

with x1 and x2 in the set {0,1,…,1023}
• A good solution is 22/7, but we want the best!

22

 
Example 3: Plot of  𝑈 𝑥1, 𝑥2  

• Brute force search (test all possible pairs) finds 355/113 (U<0.00001).

23

Example 3: Solution approach

• Let us solve the problem using a binary GA
• Parameters of the GA:

• One-point crossover with pc = 0.7
• Mutation with pm = 0.01
• Tournament selection (N=3)
• Chromosomes with 2 × 10 = 20 bits
• Search space size: 220 = 1,048,576
• Fitness function = −U(x1, x2)
• Number of individuals = 100
• Number of generations = 50

24

Example 3: fitness vs. generations plot

25

Example 3: Solution

• Best solution after 50 generations:

1110000011 0110111100 
(LSB to MSB), that is
x1 = 776 and x2 = 247
which corresponds to U = 0.000108. 

• Solutions sampled: 5,000
• Fraction of search space explored: 0.48%

26

Real-valued GAs

• In real-valued GAs each gene is represented by a floating-point 

number.

• These GAs are particularly suited for problems where the problem 
variables are naturally represented as real numbers within pre-
specified intervals.

• They have no problems zooming in onto solutions without the 

resolution barriers of binary GAs. 

27

Real-valued GAs

• It is possible to use standard crossovers on vectors of real-valued 

parameters, e.g.,

Parent a

Parent b

0.3 0.2  0.5 0.7 1.0
0.5 0.3  0.7 0.1 0.1

Offspring ab

0.3 0.2  0.7 0.1 0.1

• but this may lead to a poor search of the parameter space 

because crossover cannot create any new values.

28

Crossover

• In real-valued GAs crossover is often seen as an interpolation 

process in a multi-dimensional space.

29

Crossover

• Alternatively, crossover can be seen as the exploration of a multi-

dimensional (hyper-) box defined by the parents.

30

Implementation

Offspring[1] = Parent1[1] ∗ R1 + Parent2[1] ∗ (1 − R1)
…
 Offspring[N] = Parent1[N] ∗ RN + Parent2[N] ∗ (1 − RN)

where R1, ..., RN are random numbers between 0 and 1
If R1 = ... = RN = same random number → Interpolation Crossover

If R1, R2, ...RN = different random numbers → Box Crossover

31

Mutation

• Mutation is often seen as the addition of a small random 

variation to a point in a multi-dimensional space.

32

Implementation

Offspring[1] = Parent[1] + sigma ∙ R1
…
Offspring[𝑁] = Parent[N] + sigma ∙ R𝑁

where:
• sigma is a suitable positive constant and 
• R1, ..., RN are (different) random numbers either between -1.0 and 1.0 or 

normal/gaussian deviates

• In python: 

import random
R = random.uniform(-1, 1) 
R = random.gauss(0, 1)

33

Rank selection

• Individuals are sorted (ranked) on the basis of their fitness, so 𝑓1 ≥

𝑓2 ≥   … ≥ 𝑓𝑀

• Then each individual is assigned a probability of being selected pi 

taken from a given distribution, with the constraint

p1 + p2 + … + pM = 1

34

Typical distribution: Exponential
𝑝𝑖 = 𝑝 ∙ 𝑒−𝑝∙(𝑖−1)
• Exponential: 
𝑒−𝑝 ≅ (1 − 𝑝)   →  𝑝𝑖 = 𝑝 ∙ 𝑒−𝑝 (𝑖−1) ≅ 𝑝 ∙ (1 − 𝑝)(𝑖−1)
• For small p: 

• In Python:
selected = 1
while True:
  if random number < p:
    return selected
  else:
    selected += 1

35

Rank Selection

• Advantages:

• No premature convergence: no individual has 𝑁𝑖 much bigger than 1
• No stagnation: even at the end 𝑁1, 𝑁2, … are different. Explicit fitness not 

needed: only the ability to compare pairs of solutions is necessary.

• Disadvantages:

• Reordering overhead
• Little biological plausibility

36

Elitist selection

• At least a copy of the best 𝑵 individuals of the population is 

always passed to the new generation (often 𝑁 = 1)

• Advantage: 

• Convergence is guaranteed, i.e., if the global maximum is discovered, 

the GA converges to such maximum

• Disadvantage: 

• Risk of being trapped by local maxima

37

38

Mapping Objective Functions into Fitness 
Functions (1)
• Case 1: 

• In many problems a quality measure 𝑸(𝒔) is known such that for 
all solutions 𝑸(𝒔)   ≥  𝟎 and the objective is to find 𝒔∗ for which 
𝑸(𝒔∗)   =  𝒎𝒂𝒙𝒔 𝑸(𝒔).

• Solution: 

• We can use as a fitness measure
   𝒇(𝒔)   =  𝑸(𝒔)

39

Mapping Objective Functions into Fitness 
Functions (2)
• Case 2: 

In some problems 𝑸(𝒔)   <  𝟎 for some solutions 𝒔. So, FPS 
cannot be used (𝑓  <  0 gives negative selection probability!).

• Solution: 

Use an offset and a threshold:
  𝑓(𝑠)   =  𝑄(𝑠)   −  𝐶 
  𝑓(𝑠)   =  0 
where
• 𝐶  = minimum value 𝑄(𝑠) can take (when known) or
• 𝐶  = minimum 𝑄(𝑠) in the current generation (or last few gens)

if 𝑄(𝑠)   −  𝐶  >  0
otherwise

40

 
 
Mapping Objective Functions into Fitness 
Functions (3)
• Case 3: 

• In some problems the natural measure of quality is actually a cost or an 

error 𝑬(𝒔) and the problem is: 

find 𝒔∗ such that 𝑬(𝒔∗)   =  𝒎𝒊𝒏𝒔 𝑬(𝒔).

• Solution: 

• Take a quality measure to be maximised
• 𝑸(𝒔)   =   −𝑬(𝒔) and go back to Case 1.
• If 𝑸(𝒔)   <  𝟎 for some s go to Case 2, instead.

41

 
 
 
Mapping Objective Functions into Fitness 
Functions (4)
• Case 4: 

• If, for all s, Q(s) is in the range  [𝑸𝒎𝒊𝒏, 𝑸𝒎𝒂𝒙] with 

• 𝑸𝒎𝒊𝒏 much bigger than 0, but 
• 𝑸𝒎𝒂𝒙  −  𝑸𝒎𝒊𝒏 much smaller than 𝑸𝒎𝒊𝒏.
E.g. , [1000,1010] 

• FPS can lead to stagnation even at a beginning of a run!

• Solution: 

• Go back to Case 2 and use 𝑪  =  𝑸𝒎𝒊𝒏 so f(s) is in the range [𝟎, 𝑸𝒎𝒂𝒙  −  𝑸𝒎𝒊𝒏]

42

GAs for Constrained Optimisation
• Constrained optimisation means “find the minimum of 𝑼 in a 

predefined region of the space of possible solutions”.

• Usually this is formulated as:

Minimise 𝑼(𝒙) subject to the constraints:

𝒈𝒊(𝒙)   ≥  𝟎  for 𝑖  =  1, … , 𝑚 (type 1, inequality constraints)
𝒉𝒋(𝒙)   =  𝟎  for 𝑗  =  1, … , 𝑛 (type 2, equality constraints).
(where x is a set of variables)

• Does it remind you of the Knapsack problem?  (combinatorial 

constrained optimisation)

43

Example (1)

• Two variables (x = (x1, x2)), no equality constraints (𝑛  =  0) and one 

inequality constraint (𝑚  =  1):

“Minimise 𝑼(𝒙𝟏, 𝒙𝟐)   =  𝒙𝟏

𝟐  +  𝒙𝟐
with 𝒈(𝒙𝟏, 𝒙𝟐)   =  𝒙𝟏  ∗  𝒙𝟐  ≥  𝟎"

𝟐 

• Note that different kinds of constraints can be transformed into 
type 1 or type 2. For example, 𝑥1  +  𝑥2  −  3  ≤  0 is equivalent to 
3  −  𝑥1  −  𝑥2  ≥  0.

44

Penalty Method (1)

• Constrained optimisation problems can be transformed into 

unconstrained optimisation problems using the penalty method.

• Instead of minimising U(x), minimize

𝑈′ 𝑥 = 𝑈 𝑥 + 𝒓 ∙ 𝑭𝑷𝒆𝒏𝒂𝒍𝒕𝒚 𝒈𝟏 𝒙  

+ 𝒓 ∙ 𝑭𝑷𝒆𝒏𝒂𝒍𝒕𝒚 𝒈𝟐 𝒙
+ ⋯

  where r is a penalty coefficient and 𝑭𝑷𝒆𝒏𝒂𝒍𝒕𝒚 is a penalty  function.

45

 
 
Penalty Method (2)

• A typical penalty function is 

𝑭𝑷𝒆𝒏𝒂𝒍𝒕𝒚 𝑔𝑖 𝑥 =   𝑔𝑖
𝑭𝑷𝒆𝒏𝒂𝒍𝒕𝒚 𝑔𝑖 𝑥 = 0 

2(𝑥) 

if 𝑔𝑖 𝑥 < 0
otherwise

• For equality constraints we can use the same approach with 

penalty functions like 𝑭𝑷𝒆𝒏𝒂𝒍𝒕𝒚 ℎ𝑖 𝑥 =   ℎ𝑖

2(𝑥) 

46

 
Penalty Method in Python
r = 10        # penalty coefficient

def U(x1, x2):

return x1**2 + x2**2

def g(x1, x2):

return 3 - x1 - x2

def penalty( constraint ):

return constraint**2 if constraint < 0 else 0

def U_prime(x1, x2):

return U(x1,x2) + r * penalty( g(x1, x2) ) 

47

 
 
 
 
Example (2)

• Assume 𝑈(𝑥1, 𝑥2)   =  𝑥1
• Before the penalty has been added, the objective function is

2 and 𝑔(𝑥1, 𝑥2)   =  3  −   𝑥1  −  𝑥2  ≥  0

2  +  𝑥2

48

Example (3)

• After the penalty has been added (𝑟 = 10), the objective function is

49

Penalty Method (3)

• Advantage: no hard constraints on the values of x
• Disadvantage: some constraints can be “slightly” violated (e.g., 

by a good solution close to the border of the space of valid 
solutions).

• For most problems of combinatorial optimisation this is not 

acceptable, as the constraints enforce the syntactic correctness 
of the solutions

• Alternatives:

• special representations and operators
• repair slightly invalid solutions

50

What did we learn today? (1)

• We have learned that unconstrained function optimisation 
(UFO) is about finding the values for the parameters x that 
minimise or maximise a given objective function U(x), and that the 
difference between UFO and  unconstrained combinatorial 
optimisation is only in the nature of the variables: continuous vs. 
discrete.

• We have learned how to develop fitness functions for various 
problems and saw that solving new problems “just” requires 
definition of representation and fitness function. 

51

What did we learn today? (2)
• We have seen how real-valued GAs operate on arrays of real 

numbers better than binary GAs but require new crossover and 
mutation operators.

• We have introduced rank selection and found that it can 

implemented easily

• We have seen the benefits and risks of elitism
• We have understood how to transform objective functions (U) 

into fitness functions (f)

• We have seen how constrained optimisation can be transformed 

into unconstrained optimisation using penalties

52

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Next time:
Evolution strategies

```

---

## B. Lecture 04（PDF可提取全文）

```text

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Evolution strategies

Post Lab Addendum

Binary Steady State GA on OneMax function

Binary Steady State GA on deceptive/trap function

Binary Steady State GA on deceptive/trap function

Binary Steady State GA on deceptive/trap function

Today’s learning objective

• Describe evolution strategies (ESs) algorithm and possible ways 

to implement them.

• Discuss and contrast evolution strategies (EAs) and genetic 

algorithms (GAs)

7

Evolution Strategies

• An Evolution Strategy (ES) is EAs which uses arrays of real 

numbers as a representation, like real-valued GAs.

• Mutation is the key variation operator (unlike GAs, where 

recombination is usually deemed to play that role)

• Mutation = addition of Gaussian random numbers to the floats 

that represent the individuals being optimised.

• The amplitude of deviates is varied dynamically to maximise 
performance (but often ESs are also used with fixed mutation).

8

Gaussian Mutation

• Same implementation as mutation in real-valued GAs:

Offspring𝑃𝑎𝑟𝑎𝑚1 = Parent𝑃𝑎𝑟𝑎𝑚1 + sigma ∙ 𝑅1
…
Offspring𝑃𝑎𝑟𝑎𝑚𝑁 = Parent𝑃𝑎𝑟𝑎𝑚𝑁 + sigma ∙ 𝑅𝑁

but
R1, ..., RN = random numbers drawn from a  standardised 
Gaussian distribution

9

Gaussian Mutation

Same implementation as 
mutation in real-valued GAs but 
the Ri are NOT uniformly 
distributed

Offspring[1] = Parent[1] + sigma ∙ R1
…
Offspring[𝑁] = Parent[N] + sigma ∙ R𝑁

where:
• sigma is a suitable positive constant and 
• R1, ..., RN are (different) random numbers drawn from a 

normal/gaussian distribution

• In python: 

import random
Ri = random.gauss(0, sigma)

10

Standardised Gaussian Deviates

Probability of 
Deviate

Modified from https://en.wikipedia.org/wiki/Normal_distribution

Ri
Deviate

11

(1+1) ES

• The (1+1) ES uses a population consisting of only one individual 

(the first “1” in “(1+1)”).

• The parent generates one offspring (the second “1” in “(1+1)”) per 

generation by applying Gaussian mutations.

• If offspring performs no worse than its parent, it replaces it.

12

Sample 2-D Fitness Landscape

High

Fitness function 𝑓 𝑥, 𝑦  seen as a topographic map 
(contour lines connect points of equal elevation)

Low

13

(1+1)-ES Behaviour

6

3

5

8

7

2

4

1

14

(1+lambda), (mu+lambda) and (mu,lambda) 
ES
• (1+lambda) ES is like the (1+1) ES except it generates lambda 

offspring and it chooses the best as a candidate for replacing the 
parent.

• (mu+lambda) ES produces lambda offspring at each generation 
via crossover and mutation. The best mu individuals out of the 
lambda + mu available ones are retained.

• (mu, lambda) ES is like (mu+lambda) ES but it the replaces the 
parents with the best mu offspring out of lambda generated 
(naturally, lambda > mu for this to work).

15

(1,2) ES

4

4

3

2

3

2

1

Numbers 
represent 
generations

16

(1,4) ES

4

3

4

4

4

3

3

2

3

2

1

2

2

17

(2,4) ES

4

3

4

4

3

4

2

1

2

3

3

1

2

2

18

Which ES is best?

• It might seem that (1,4) and (2,4) ES are best.
• However, more offspring means more fitness evaluations, i.e., 

longer runtimes

Our example ES

Fitness 
evaluations

1+1

1,2

1,4

2,4

8

7

13

14

• So, fair comparison should be done on approximately same 

number of fitness evaluations

19

(1,2) ES run extended to 13 fitness 
evaluations

5

7

6

7

5

4

4

6

3

2

3

2

1

• This is the best this time, but the 
fitness function is unimodal (only 
one peak/max).

• For multi-modal fitness functions 

one needs more individuals 
(mu>1) in the parent pool and 
more offspring (lambda>2)

20

Which value of sigma to use? (1)

• Big sigma means children 

will be further away from the 
parents.

• Initially this may lead to 
bigger improvements in 
fitness

• However, the closer the 
population gets to the 
optimum the harder it gets 
to home on it.

21

Which value of sigma to use? (2)

• Small sigma means children 
will be closer to the parents.

• Initially this may lead to 

smaller improvements in 
fitness

• However, the closer the 
population gets to the 
optimum it is easier to home 
on it.

22

Sigma Adaptation and 1/5 Rule
• This issue is addressed by the 1/5 rule, where sigma is changed 

according to the frequency of successful mutations

• We define 

smut = fraction of times children are fitter than parents

• If smut > 1/5 ➔ increase sigma

# we’re exploring too little, e.g., on a gentle slope

• If smut < 1/5 ➔ decrease sigma

# we’re exploring too widely, e.g., near the optimum

• If smut = 1/5 ➔ do nothing           # we’re exploring just right! 

23

 
   
 
   
 
[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Next week: 
Genetic Programming

```

---

## B. Lecture 05（PDF可提取全文）

```text

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Genetic Programming

What did we learn last week? (1)

• We learned how to deal with real-valued parameters in GAs and 
how to implement the associated crossover (interpolation and 
box) and mutation operators.

• Rank selection scales the fitness function and assigns each 

individual a rapidly decreasing selection probability. 

• Elitist selection keeps copies of the N fittest individuals, which 

are passed on to the next generation.

3

What did we learn last week? (2)

• We have learned about several cases how objective functions Q(s) can be 

mapped into fitness functions f(s)

• Constrained optimisation means minimising 𝑼(𝒙) subject to the 
constraints 𝒈𝒊(𝒙) ≥ 𝟎 (inequality constraints) and 𝒉𝒋(𝒙) = 𝟎
(equality constraints).

• The penalty method allows us to transform constrained in 

unconstrained optimisation problems by adding penalty terms 
𝑈′ 𝑥 = 𝑈 𝑥 + 𝐫𝒊 ∙ 𝑭𝑷𝒆𝒏𝒂𝒍𝒕𝒚 𝒈𝒊 𝒙 + ⋯ .

4

What did we learn last week? (3)

• Evolution strategies (ESs) typically use arrays of real numbers as 
representation and mutation (equal addition of Gaussian random 
numbers)to explore the search space.

• (Parent + Offspring) vs. (Parents, Offspring) variants
• Sigma (step size) Adaptation: 1/5 rule

• 1/5 offspring better than parents: increase Sigma
• 1/5 offspring worse than parents: decrease Sigma

5

Today’s learning objective

• Describe program representation, crossover and mutation

operators in Genetic Programming (GP)

• Discuss terminal and function sets
• Discuss differences between GAs and GP (especially the genetic 

operators).

• Understand the range of problems that GP can solve and how to 

guide it with fitness functions.

6

Genetic Programming (GP)

• GP is a systematic, domain-independent method for getting 

computers to automatically solve a problem starting from a high-
level statement of what needs to be done.

• GP is a special GA where the individuals in the population are 

computer programs.

• So, GP iteratively transforms a population of programs into a new 
generation of programs under the guidance of a fitness function.

• To do so, GP applies  genetic operations like recombination, 

mutation, etc. which are specialised to handle computer programs

• Fitness functions are also specialised in many respects.

7

Executional Steps of GP

1. Randomly create an initial population of programs from an 

2.

available set of instructions (primitives).
Iterate the following sub-steps until the termination criterion is 
satisfied:
• Execute each program and ascertain its fitness.
• Select one or two program(s) from the population based on 

fitness to participate in genetic operations.

• Create new individual program(s) by applying genetic

operations with specified probabilities.

3. Return the best-so-far individual

8

Genetic Operations (1)

• Cloning: copy the selected individual program to the new 

population (generational GP only!).

• Crossover: create new offspring program(s) by recombining 

randomly chosen parts from two selected programs.

• Mutation: create one new offspring program by randomly mutating a 

randomly chosen part of one selected program.

• Architecture-altering operations: choose one such operation (e.g., 
subroutine creation/deletion, dummy argument addition/deletion, 
…) and create one new offspring using it.

9

Genetic Operations (2)

• In GAs:

Generational: cloning and crossover are mutually exclusive (either you 
create the offspring with one or the other). Mutation can be performed on 
the offspring after such operations or as an independent way of producing 
offspring.
Steady state: same but no cloning. 

• In GP:

• Generational: all genetic operations are mutually exclusive. So, either 
an offspring is created by cloning or by crossover or by mutation or by an 
architecture altering operation (irrespective of whether GP is generational 
or steady state).

• Steady state: same but no cloning.

10

Operator Rates (Probabilities) in GAs

• As a result, in generational GAs:

𝒑𝑿𝑶 + 𝒑𝒄𝒍𝒐𝒏𝒆 = 𝟏

where 𝒑𝑿𝑶 is the crossover rate and 𝒑𝒄𝒍𝒐𝒏𝒆 is the cloning rate.
Also, when we talk about mutation rate 𝒑𝒎𝒖𝒕 (or 𝒑𝒎) we normally mean the 
probability of hitting any particular bit or gene with a mutation

11

Operator Rates (Probabilities) in GP

• Instead, in generational GP:

𝒑𝒄𝒓𝒐𝒔𝒔 + 𝒑𝒄𝒍𝒐𝒏𝒆 + 𝒑𝒎𝒖𝒕 + 𝒑𝒂𝒓𝒄𝒉 = 𝟏

In GP when we talk about mutation rate 𝒑𝒎𝒖𝒕 we normally mean the 
probability of hitting any particular program with a mutation that can 
change many instructions at once

12

In Python…

13

Program Representation

• Programs are expressed in GP as syntax trees rather than as lines 

of code.
For example,

max(x*x,x+3*y) =

Terminals

Functions

14

Random Program Generation

• The programs in the initial population are typically built by 

recursively generating a tree composed of random choices of 
functions and terminals.

• The initial individuals are usually generated subject to a pre-

established maximum size.

15

Fitness (1)

• Normally, fitness evaluation requires executing the programs in 

the population multiple times within the GP system.

• Nearly always to decide whether a program is good or bad we 

need to execute it.

• In some problems we are interested in the output produced by a 

program. Normally, the value returned by the root node is the 
output of the program while the values of the variables are the 
inputs.

16

Fitness (2)

• In other problems we are interested in the actions performed by 
a program. In this case the primitive set will include functions 
with side effects (e.g. changing global data structures or 
controlling the motors of a robot).

• So, quite often the fitness of a program depends on the results 

produced by its execution in many different conditions (fitness 
cases).

17

Selection

• Genetic operators are applied to individual(s) that are 

probabilistically selected based on fitness.

• Fitter individuals are favoured over less fit individuals.
• The most commonly employed methods for selecting individuals 
are tournament selection and fitness-proportionate selection.

18

Sub-tree Crossover (1)

• Given two parents, 

crossover randomly selects 
a crossover point in each 
parent tree and replaces
the sub-tree rooted at one 
XO point with the sub-tree 
rooted at the other XO point.

19

Sub-tree Crossover (2)

• Seen as acting on expressions, the same crossover operation 

corresponds to

Parent 1: (x + y) + 3
Parent 2: (y + 1) * (x / 2)
Expression excised from parent 1 for deletion: (x+y)
Parent 1 thus donates the structure: ? + 3
Expression excised from parent 2 for insertion (replaces ?): (x / 2)
Resulting offspring: (x / 2) + 3

20

Sub-tree Crossover (3)

• Note the root node/edge can also be selected as a crossover point!
• Some time crossover points are not selected with uniform 

probability.

• Koza used a method where functions are chosen 90% of the times, while 

leaves are selected 10% of the times.

• This was done to avoid excessive exchange of very small trees (GP trees 

tend to have many leaves).

21

Sub-tree Mutation (1)

• Mutation randomly selects a mutation point in a tree and 

substitutes the sub-tree rooted there with a randomly generated
sub-tree.

22

Sub-tree Mutation (2)

• Seen as acting on expressions, the same mutation operation 

corresponds to
Parent: (x + y) + 3
Expression excised from parent 1 for deletion: 3
Parent 1 thus donates the structure: (x + y) + ?
Randomly generated expression to be inserted in the parent (replaces ?): y * (x / 2)
Resulting offspring: (x + y) + (y * (x / 2))

23

Sub-tree Mutation (3)

• One mutation can modify many nodes/primitives/instructions at 

once.

• The root node/edge can also be selected as a mutation point!

24

Point Mutation
• Point mutation is the equivalent for GP of GA mutation.
• Each node is visited, a (biased) coin is flipped, if heads the node is 
replaced with a different random primitive of the same number 
of arguments (arity) taken from the primitive set.

mutated

visited but 
not mutated

25

Point Mutation
• The coin is biased, and nodes are mutated with a given per-node

mutation rate.

• In addition, there is a per-individual mutation rate, as explained 

previously. 

• So, we need to specify two mutation rates: 

• per-node
• per-individual

26

Preparatory Steps of GP

• Users need to specify:

1. The terminal set (“leaves”),
2. The function set (internal nodes),
3. The fitness measure,
4. Certain parameters for controlling the run,
5. The termination criterion and method for designating the result of the 

run.

27

Terminal Set (Step 1)

• Steps 1 and 2 specify the ingredients that are available to create 

the computer programs (primitive set).

• The terminal set may consist of

• The program’s external inputs (e.g. x, y, sensor data, …),
• 0-arity functions (e.g. rand(), go_left()),
• Constants, typically numerical (e.g., 0.1, 3, or random) but not only 

numerical.

28

Function Set (Step 2) (1)

• For some problems, the function set may consist of merely the 
arithmetic functions (+, -, *, /) and a conditional operator.

• But all sort of functions

are allowed, e.g.

Kind of Primitive

Example(s)

Arithmetic

Mathematical

Boolean

Conditional

Looping
....

+, *, /

sin, cos, exp

AND, OR, NOT

IF-THEN-ELSE

FOR, REPEAT
....

29

Function Set (Step 2) (2)

• For many other problems, the primitive set includes specialized 

functions and terminals.
For example, if the goal is to program a robot to mop the floor

Function set = {moving, turning, swishing_the_mop}

30

Programs may be solutions or recipes to build solutions (1)

• The programs evolved by GP may or may not be used as solutions, 
i.e., we may not be interested in transforming inputs into outputs
or a program’s side effects.

• Sometimes programs are interpreted as a set of instructions on 

how to build a solution to a problem.

31

Programs may be solutions or recipes to build solutions (2)

• For example, imagine you wanted to evolve a shape. 
• This could be done by creating an artificial canvas and providing GP 

with drawing primitives and a sequencing primitives

• For instance

Sequence

MovePenUpOneStep

Sequence

MovePenLeftOneStep

Sequence

MovePenDownOneStep

MovePenRightOneStep

• When executed, this program would produce a square on the canvas.
• That is: by evolving programs one would indirectly evolve shapes.

32

Programs may be solutions or recipes to build solutions(3)

• So, GP's function sets may include functions that place elements 

of a solution, draw it, or grow it.

• If the goal is the automatic creation of a controller

Function set = {integrators, differentiators, leads, lags, gains}
Terminal set = {reference signal, plant output}

• If the goal is the synthesis of analogue electrical circuits

Function set = {transistors, capacitors, resistors}

33

Fitness Measure (Step 3) (1)

• The fitness measure is the mechanism for giving a high-level 
statement of the problem’s requirements to the GP system.
• The first two preparatory steps define the search space whereas 
the fitness measure implicitly specifies the search’s desired 
goal.

34

Fitness Measure (Step 3) (2)

• Fitness can be measured in terms of

• The amount of error between its output and the desired output,
• The amount of time (fuel, money, etc.) required to bring a system to a 

desired target state,

• The accuracy of the program in recognizing patterns or classifying objects 

into classes,

• The payoff that a game-playing program produces,
• The compliance of a structure with user-specified design criteria, ...

35

Fitness Measure (Step 3) (3)

• The fitness measure is, for many practical problems, multi-

objective, i.e. it combines two or more different elements that are 
often in competition with one another.

• For many problems, each program in the population is executed

over a representative sample of different fitness cases.

• Fitness cases may represent different values of the program’s 

inputs, different initial conditions of a system, different 
environments, …

36

Control Parameters (Step 4)

• An important control parameter is the population size.
• Other control parameters include:

• The probabilities of performing the genetic operations
• The maximum size for programs
• Other details of the run.

37

Termination Criterion (Step 5)

• We need to specify the termination criterion and the method of 

designating the result of the run.

• The termination criterion may include a maximum number of
generations to be run as well as a problem-specific success
predicate.

• The best-so-far individual is then harvested and designated as 

the result of the run.

38

Example (1)

• Goal: to automatically create a computer program whose output 
is equal to the values of the quadratic polynomial x2+x+1 in the 
range from –1 to +1.

39

Example (2)

• Step 1 – Definition of the Terminal Set:

• The problem is to find a mathematical function of one independent 

variable, so the terminal set must include x.

• In order to evolve any necessary coefficients, the terminal set also 

includes numerical constants.

• That is: T = {X, R}, where R denotes random numerical terminals in some 

range (e.g. [–5.0,+5.0]).

40

Example (3)

• Step 2 – Definition of the Function Set:

• One possible choice consists of the four ordinary arithmetic functions of 

addition, subtraction, multiplication, and division:

F = {+, -, *, /}.
• To avoid run-time errors, the division function / is protected: it returns a 

value of 1 when division by 0 is attempted, otherwise it returns the 
quotient of its two arguments.

41

Example (4)

• Step 3 – Definition of the Fitness Function:

• The fitness of a particular individual in the population must reflect 
how closely the output of an individual program comes to x2+x+1.

• The fitness measure could be defined as the area between the 

plot of x2+x+1 and the plot of an individual's mathematical 
expression.

• It is rarely possible to analytically compute the value of the area. 
So, this is numerically approximated using dozens or hundreds 
of different values of the independent/input variable, e.g.,

𝑥 ∈ −1.0, −0.9, … , 0.9, 1.0 .

42

Example (5)

• Step 4 – Fixing GP Parameters:

• Population size: 4 (typically thousands or millions of individuals)
• Crossover probability: 50% (traditionally high, e.g., 90%)
• Cloning probability: 25% (traditionally low, e.g., 8%)
• Mutation probability: 25% (traditionally very low, e.g., 1%)
• Architecture-altering operation probability: 0% (if used, very low, e.g., 1%)

43

Example (6)

• Step 5 – Termination Criterion:

• A reasonable termination criterion for this problem is that the run will 

continue from generation to generation until the fitness (error) of some 
individual gets below 0.01.

• Often a maximum number of generations is also used as an additional 

stopping criterion.

44

Example Run (1)

• Initial population

• Program (a) is  (x + 1) – 0 = x + 1
• Program (b) is  1 + (x * x) = x2 + 1
• Program (c) is  2 + 0 = 2
• Program (d) is  x * (-1 - -2) = x

45

Example Run (2)

• The fitness of each of the four 
randomly created individuals 
of generation 0 is equal to the 
area between two curves.

• Fitness of program 

(a): 0.67 
(b): 1.00 
(c): 1.67
(d): 2.67

46

Example Run (3)

• Suppose cloning is chosen first, and individual a, that is (x + 1) – 0, is 

selected and copied unchanged into the new generation.

Cloning

47

Example Run (4)

• Suppose mutation is picked next, individual c, that is, 2 + 0, is selected, and 
2 is chosen as the mutation point; the tree (x % x) is randomly generated; it 
replaces 2 to produce the offspring (x % x) + 0, which is equivalent to the 
constant 1.

Mutation

48

Example Run (5)
• Now crossover is chosen, individuals a, i.e., (x + 1) – 0, and b, i.e., 1 + (x * x), 
are selected; the subtree (x + 1) is excised from a; the leaf x is selected as 
crossover point in b and it is thus inserted in place of (x + 1) to produce the 
offspring x – 0, which is equivalent to x.

Crossov
er

49

Example Run (6)
• Finally crossover is chosen again; individuals a, i.e., 1 + (x * x), and b, i.e., (x + 
1) – 0, are selected (again); the first x in b is excised; the expression (x + 1) in  a
is selected as the subtree to be swapped; this is inserted in place of x to 
produce the offspring 1 + ((x + 1) * x) which is equivalent to x2 + x + 1

Crossov
er

50

New Generation

• Includes the programs:

(x + 1) – 0 = x + 1

(x % x) + 0 = 1

x – 0 = x

1 + ((x + 1)*x) = x2 + x + 1

51

Fitness of the new Programs

(x + 1) – 0 has fitness 0.67 (> 0.01, don't stop)
(x % x) + 0 has fitness 1.00 (> 0.01, don't stop)
x – 0 has fitness 2.67 (> 0.01, don't stop)
1 + ((x + 1)*x) has fitness 0.00 (< 0.01, → problem solved)

52

More on Fitness Functions and 
Symbolic Regression

53

Fitness functions in GP (1)

• The possible applications of GP are as many as the applications 

for programs (virtually infinite), but one needs to define an 
appropriate fitness function.

• In problems where only the side effects of the program are of 

interest, the fitness function usually compares the effects of the 
execution of a program in some suitable environments with a 
desired behaviour.

• These kinds of fitness functions are very much application 

dependent.

54

Fitness functions in GP (2)

• On the contrary it is possible to define general forms of fitness 

functions for all the problems in which the output of a program is 
of interest.
→ All of them can be seen as symbolic regression problems.

55

Symbolic Regression

• Regression is a technique used to interpret experimental data. It 

consists in finding the coefficients of a prefixed function 
(model) such that the resulting function best fits the data.

• If the must good, then the experimenter has to try with a 

different function until a good model for the data is found.
• The problem of symbolic regression consists in finding a 

function (with its coefficients) that fits well the data points.

56

57

58

59

Steps to Solve Symbolic Regression Problems

1. Collect a set of data points, where each point represents the (measured) 

values taken by some variables at a certain time or in a certain repetition of an 
experiment

2. Select which variable to consider as dependent.

3. Define a fitness function that measures the ability of each program to predict 
the value of the dependent variable given the values of the independent ones 
(for each data-point).

4. Select an appropriate set of functions and terminals. 

• Terminals often include all the independent variables plus maybe others, 
• Functions are selected on the basis of knowledge on the domain.

5. Choose the remaining GP parameters and run GP.

60

Real Symbolic Regression Run

Problem: find the symbolic expression that best fits the data:

{(xi ,yi)} = {(-1.0,0.0), (-0.9,-0.1629), (-0.8,-0.2624), … ,(1.0,4.0)}

GP parameters:

Parameter

Population size

Function set

Terminal set

Initial max depth

Initialisation method

Number of generations

Crossover probability

Mutation probability

Value

1000

{+ - * plog pexp sin cos pdiv}

{x}

4

Full

50

0.7

0

Fitness

- Sum of absolute errors

61

Best Program of Generation 1

(+ (- (plog (pexp x)) (+ (sin x) 
(- x x)))(+ (pexp (plog x)) 
(sin (plog x))))

Prefix representation of expressions:

x + y ➔ (+ x y)
x * (y + 1) ➔ (* x (+ y 1))

Traverse tree in depth first order:

+                     *
x    y               x     +
y    1

62

Best Program of Generation 3

(* (plog (- (sin x) (pexp x))) (+ (cos (* x x))
(+ (+ x x) (cos x))))

63

Best Program of Generation 6

(* (+ (+ (+ x (pexp (plog x))) 
(pdiv x x)) x) (plog (pexp x)))

64

Best Program of Generation 26

(* (+ (+ (+ (* (+ (pexp (plog x)) (sin (plog (+ x x)))) x)

c(pexp (plog x))) (pdiv x x)) x) (plog (pexp (+ (plog

(- (sinc(+ (plog (pexp (plog (- (sin (+ (+ (+ x x) (pdiv

(* (+ (+ (+ x (pexp (plog x))) (pdiv x x)) x) x) x)) x)) 

(pexp x))))) x)) (pexp (plog (- (sin (+ (+ (+ x x) (pdiv

(* (+ (+ (+ x (pexp (plog x))) (pdiv x x)) x) x) x)) x)) 

(pexp x)))))) (plog (- x x))))))

65

Evolution of Fitness and Size

Best-of-generation
Fitness vs. Generation

Best-of-generation
Size vs. Generation

Fitness increases rapidly initially, but the 
growth slows down after the first 15 
generations or so

Size is more or less constant for the first 15 
generations after which it starts growing very 
rapidly (bloat)

66

Another Example

• Using the symbolic regression approach GP can solve problems in 

completely different domains.

• Problem: Find a logic circuit that implements the XOR Boolean 
function using AND, OR, and NOT gates, i.e. find the Boolean 
function that best fits the data points
{(x1i , x2i , yi)} = {(0,0,0), (0,1,1), 
(1,0,1), (1,1,0)}.

67

GP parameters

Value
200
{AND OR NOT}
{x1 x2}
3

Parameter
Population size
Function set
Terminal set
Initial max depth
Initialisation method Grow
Number of 
50
generations
Crossover probability 0.9
Mutation probability
Fitness

0
1 / Sum of absolute errors

68

GP Run

• After 9 generations, GP found the following solution which 

includes 10 nodes:
(AND (NOT (AND x2 x1)) 
(OR (OR x1 x1) x2))

which can be interpreted as

NOT(x1 AND x2) AND (X1 OR X2)

69

Function set: NAND

Using only NAND gates GP found the solution:
(NAND (NAND (NAND x2 x1) x2)
(NAND x1 (NAND x1 x2)))

70

And yet another example… Classification

71

What did we learn today? (1)

• We have learned that GA, ES and GP use the same principles  and 

concepts. One difference is that genetic operators in GP are 
mutually exclusive. 

• We have learned that programs can be represented as syntax 
trees, and how to implement sub-tree crossover, sub-tree 
mutation and  point mutation.

• We have learned the preparatory steps of GP. Define terminal and 
function set (define the search space), fitness measure (goal, 
expressed as program output or action generated), hyper-
parameters and termination criterion.

72

What did we learn today? (2)

• Programs that the GP evolve may not be solutions, but recipes to 

build solutions

• For many problems, we need to run programs over a 
representative sample of different fitness cases

• Termination criterion may include maximum number of 
generations and problem-specific success predicate

• Symbolic regression can be seen as a general form of fitness

functions for problems where we are interested in the output of a 
program (vs. side effects)

73

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Next time: 
Implementing GP

```

---

## B. Lecture 06（PDF可提取全文）

```text

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Tree based Genetic 
Programming

Learning objective

• Discuss different ways to represent programs in tree-based GP
• Describe closure and sufficiency in the context of primitive sets
• Describe different way to initialize programs
• Discuss issues with program execution including macros and 

interpreters

• Describe crossover with tree-like representation.
• Describe and discuss multi-tree representations and 

automatically defined functions.

2

Before we start…

Any questions about coursework assignment?

Prefix Notation (1)

• GP trees and the corresponding expressions can be represented 

in prefix notation.

• In this notation, functions always precede their arguments. For 

example

corresponds to  

max(x*x,x+3*y)

(max (* x x)(+ x (* 3 y)))

• In Python: ['max', ['*', 'x', 'x'], ['+', 'x', ['*', '3', 'y']]]

4

Prefix Notation (2)

• With prefix notation it is easier to see the correspondence 

between expressions and syntax trees.

• Let us see it step by step

['max', ['*', 'x', 'x'], ['+', 'x', ['*', '3', 'y']]]

Legend:
•
•

terminal
function

5

Prefix Notation (3)
• Let us indent the expression:  ['max', ['*', 'x', 'x'], ['+', 'x', ['*', '3', 'y']]]

['max’, 

['*', 'x', 'x’], 
['+', 'x', ['*', '3', 'y']]]

• Let us indent more:

['max’, 

['*’, 

['+’, 

'x’, 
'x’], 

'x’, 
['*', '3', 'y']]]

6

Prefix Notation (4)

…and even more:

['max’, 

['*’, 

['+’, 

'x’, 
'x’], 

'x’, 
['*', '3', 'y']]]

['max’, 

['*’, 

['+’, 

A tree structure emerges

'x’, 
'x’], 

'x’, 
['*’, 

'3’, 
'y']]]

7

Prefix Notation (5)

…and finally…

['max’, 

['*’, 

['+’, 

'x’, 
'x’], 

'x’, 
['*’, 

Turn 
upside 
down

'3’, 
'y']]]

Rotate 90 
degrees

8

Prefix Notation (6)

9

Prefix Notation (7)
• With prefix notation it is easier to see the correspondence between 

expressions and syntax trees.

['max', ['*', 'x', 'x'], ['+', 'x', ['*', '3', 'y']]]

• Recursive functions can convert prefix into infix and vice versa.

10

Implementation Note

• In Lisp, Python  and many other languages lists are fundamental 
data types and expressions are represented internally as trees. 
So, GP can directly be performed using lists.

• However:

• Tree/list-based representations of programs are memory-inefficient

(for each node we need to store content and pointers as its 
arguments/children and there may be other sources of memory waste).

• Program size is hard to work out (requires recursion).

11

Prefix Notation (8)

• If all functions have a fixed arity (#arguments), the brackets 

become redundant in prefix-notation expressions.

• For example,

(max (* x x)(+ x (* 3 y)))

is equivalent to

max * x x + x * 3 y

• In Python: ['max', '*', 'x', 'x', '+', 'x', '*', '3', 'y']
• So, often GP trees are stored internally as linear sequences of 

instructions.

12

Syntax Errors Are Impossible

• IF all programs in the initial population of a run of GP are 

syntactically valid, executable programs,

• AND the genetic operations performed during the run are 
designed to produce offspring that are syntactically valid, 
executable programs,

• THEN every individual created during a run of GP is a 

syntactically valid, executable program.

13

Run-time Errors Can Be Avoided

• IF all functions in the primitive set can take as input the results 

produced by any other function or terminal (closure),

• THEN run-time errors are avoided.

14

Examples of closed primitive sets

• {AND,OR,NOT, x, y, true} where x and y are Boolean 

variables, and true is a Boolean constant.

• {PROG2, IF_FOOD_AHEAD, TURN_LEFT, TURN_RIGHT, 

MOVE_FORWARD} if world is toroidal.

15

Examples of closed primitive sets

• {+, -, *, x, y, 1, 0} where x and y are integer

variables: in theory there is no way of generating a non-valid 
expression but integer overflow may occur.

• {+, -, sin, cos, exp, x, y} where x and y are 

floating-point variables: in theory no problem because all 
functions accept arguments in (-∞,+ ∞) but floating-point
overflow is very likely.

16

Examples of non-closed primitive sets

• {+, -, *, /, x, y, 1, 0} where x and y are floating-

point variables: possible division by 0, e.g. x/0 or (x+y)/(x-x)
• {+, -, sin, cos, log, x, y, 0, 1} where x and y are 
floating-point variables: possible negative argument for log, 
e.g. log(0-x)

• {+, *, sqrt, x} can be non-closed depending on the range 

for x

17

Protected Functions

• Achieving closure requires modifying the primitive set 

appropriately, e.g. using protected versions of division, 
logarithm, square root, etc.

Function
x/y

Protected version
1    if y = 0
x/y  otherwise
log(x) 0       if x = 0

log(|x|)otherwise

sqrt(x) sqrt(|x|)

18

Exceptions

• An alternative to protected functions is to trap FP exceptions and 
strongly reduce the fitness of non-valid expressions when they 
cause math errors.

• However, with this method, if the likelihood of generating invalid 

expressions is very high, all individuals might get the same fitness 
and evolution might not start.

19

Primitive Set Sufficiency

• Sufficiency requires that the primitives in the primitive set are 

capable of expressing the solutions to the problem, i.e. that the 
set of all the possible recursive compositions of such primitives 
includes at least a solution.

• Sufficiency is guaranteed only for some problems, when theory 
(or experience with other methods) tells us that a solution can be 
obtained by combining the elements of the primitive set.

20

A Sufficient Primitive Set

• The primitive set {AND,OR,NOT,x1,x2,....,xN}

is always sufficient for Boolean function induction problems, 
since it can produce all Boolean functions of the variables x1, 
x2, ...., xN.

21

Proof

• Any Boolean function f can
be expressed with a truth 
table, which is also equivalent 
to the (disjunctive normal 
form, DNF) formula:

x1
0
1
...

1

x2
0
0
...

1

...

...

...

...

...

xN
0
0
...

1

f
a00...0
a10...0

...

a11...1

OR(AND(a00...0,NOT(x1),NOT(x2),...,NOT(xN)),

AND(a10...0,x1,NOT(x2),...,NOT(xN)),
…
AND(a11...1,x1,x2,...,xN)))

22

An Insufficient Primitive Set (PS) (1)

• If PS is not sufficient for a particular application, GP can only 

develop programs that approximate the desired one.
• Let us consider the problem of finding a program that that 

implements exp(x) using the primitives in 

C = {+, -, *, /, x, 0, 1, 2}

• exp cannot be expressed in closed form using the elements of C

• Why? It is a transcendental function

Cannot be written down using algebra

23

An Insufficient Primitive Set (2)

• The typical behaviour of GP is to produce finite algebraic 

approximations of exp(x), such as 1 + x or  
1 + x + x2/2

24

Search Space

• The theoretical search space of GP is the set of all the possible 
(recursive) compositions of the elements of the primitive set C. 
This is infinite.

• The real search space of GP is finite. It includes “only” all the 
(recursive) compositions of the functions in C whose size (e.g. 
depth or number of nodes) does not exceed a prefixed maximum 
value (e.g. the memory available on the computer).

• Nonetheless, the search space is huge.

25

Size of GP Search Space (1)

• Let us compute the number, N(d), of different trees of maximum 

depth d present in the search space explored by GP when

C  = {AND,OR,NOR,NAND,x1,x2,x3}

26

Size of GP Search Space (2)

• T = terminals: 3 choices x1,x2,x3
• F = functions: 4 choices AND,OR,NOR,NAND
• If max depth 𝑑 = 0
• Only 1 possible tree shape ➔
• Labelling with number of replacements ➔
• So, 𝑁(0) = 3

27

Size of GP Search Space (3)

• If max depth 𝑑 = 1
• Two possible tree shapes ➔

with replacements ➔

𝑁 0

• So, 𝑁 1 = 𝑁 0 + 4×3×3 = 3 + 36 = 39

28

Size of GP Search Space (4)
• If max depth 𝑑 = 2
• Five possible tree shapes ➔

with replacements ➔

𝑁 1

• So, 𝑁 2 = 𝑁 1 + 4×4×3×3×3 + 4×4×3×3×3 + 4×4×4×3×3×3×3            

= 39 + 432 + 432 + 5184 = 6087

29

Bigger depth?

𝑁(0) = 3

𝑁(1) = 39

𝑁(2) = 6087

𝑁(6) = 3.8×1069

𝑁 17 = 1.1×10143735

30

General Answer

• Assuming 𝑎𝑟𝑖𝑡𝑦(𝑝) returns the number of arguments of primitive 𝑝 and 

that 𝑎𝑟𝑖𝑡𝑦 𝑇 = 0 (note 𝑛0 = 1 for any 𝑛)

• Recursion:

𝑁(𝑑)= 𝑁(𝑑 − 1)arity(p
1

)+𝑁(𝑑 − 1)arity(p
2

)+…+𝑁(𝑑 − 1)arity(p

)

n

where 𝑁(0) = number of terminals

31

“Full” Initialisation Method

• Nodes are taken from the function set until a maximum tree 
depth is reached. Beyond that depth only terminals can be 
chosen.

32

Example “Full”

• Assume max depth d = 2.
• At time t=1 a “+” node is selected as the root 

of the tree.

• At t=2 the 1st child of the root (“+”) is 

chosen. It is a product, “*”.

• At t=3 the 1st child of the “*” is chosen. We 
have reached max depth, so we pick a leaf, 
“x”.

• At t=4 the 2nd child of the “*” is chosen. 

Again it is a leaf, “y”.

• At t=5 the 2nd child of the root (“+”) is 

chosen. It is a division, “/”.

• At t=6 and t=7 we complete the tree with two 

more leaves.

33

“Grow” Initialisation Method

• It behaves like “full” except it allows the selection of nodes from 

the whole primitive set until the depth limit is reached.

34

Example “Grow”

• Again, assume max depth d = 2.
• At time t=1 a “+” node is selected as the root of the 

tree.

• At t=2 the 1st child of the root (“+”) is chosen. It 
can be either a function or a terminal. It is the 
terminal, “x”.

• At t=3 the 2nd child of the root is chosen similarly. 

It is a subtraction, “-”.

• At t=4 the 1st child of the “-” is chosen. We have 
reached max depth, so we must pick a terminal. 
“2” is chosen.

• At t=5 the 2nd child of the “-” is chosen. Again it 

must be a leaf, “y”.

35

Implementation (1)

• If trees are represented in prefix notation, initialisation with the 
“full” and the “grow” methods can be performed using recursive 
procedures.

• Set up:

36

Implementation (2)
• “Full” method:

37

Implementation (3)
• “Grow” method:

ONLY DIFFERENCE!

38

Ramped “half-and-half” Initialisation

• This method combines the previous two methods to get a higher 

diversity in the initial population.

• Fore example: If P = 1000, dmin= 1 and dmax= 5, for each possible 
depth (i.e. d =1, 2, 3, 4 and 5), 100 individuals will be produced 
with the “grow” method and 100 with the “full” method.

39

Simplest (approx.) implementation

40

Execution Strategies

• Full off-line compilation and linking of the individuals produced 

in each generation.

• Full on-line compilation and dynamic linking of each individual 

generated.

• Special-purpose on-line compilation of the primitive set into 

machine code

• Virtual-machine code compilation
• Interpretation

41

Compilation vs. interpretation

• Compiling programs before executing them takes time.
• Executing compiled programs is quicker.
• Compilation is convenient when:

𝜏𝑐 + 𝑁 × 𝑡𝑐< 𝑁 × 𝑡𝑖

compilation time

𝜏𝑐
𝑁 number of executions (fitness cases)
𝑡𝑖
execution time when interpreted
𝑡c
execution time when compiled

42

Interpretation (1)

• Some languages like Lisp and Python have built-in interpreters. 

In such languages interpreting/executing programs is trivial.
• For other languages it is necessary to build an interpreter.
• A full interpreter is seldom needed, since

• Programs are not represented as lines of text, so a lexical analysis is 

unnecessary.

• Not all the primitives of the language are used.

43

Program Interpretation

• Interpreting a program tree means recursively traversing the tree 
(in “depth-first” order) and executing its nodes only when their 
arguments are known.
E.g.

44

Recursive Interpreter for GP

45

Problems with “non-functional” instructions (1)

• Some instructions like conditionals or loops cannot be 

implemented properly as normal functions.

• For example, when interpreting

IF(<condition>, <do_this>, <do_that>) 
execute first evaluates all the arguments and then it invokes IF, 
which returns the value of <do_this> or  <do_that> 
depending on the value of <condition>.

46

Problems with “non-functional” instructions (2)
• When there are no functions or terminals with side effects this is only 

a waste of computation.

• However, the interpretation of an expressions like 

IF FOOD_ON_THE_LEFT, TURN_LEFT, TURN_RIGHT

would produce the wrong behaviour. Same with:
IF <cond>, mem_set(val), mem_get()
where mem_set(val) and mem_get() are memory ops

• Another example: REPEAT <times>, <something>

have no way of executing <something> in different contexts.

47

Macros in GP (1)

• The solution to this problem is to use special functions, called 

macros in the GP literature, which receive as input their 
arguments unevaluated (i.e. as sub-expressions).

• Macros are free to decide if, when and how many times to 

evaluate their arguments by explicitly calling the interpreter.

48

Macros in GP (2)

• For example, a macro implementation for IF is:

Compare with:

49

Handling Macros in eval

• In order to handle macros properly, the interpreter has to be able 

to distinguish between macros and normal functions.

50

New interpreter for GP

51

Running the interpreter

Mutation Implementation (1)

• The implementation of mutation is representation dependent.
• For GP trees represented as list of lists one needs to recursively
identify a random sub-list in the parent and replace it with a 
randomly generate small program. 

• The operations are performed on a copy of the parent so as not to 
destroy the original (as it could be used to produce more than 
one offspring and/or be cloned)

53

Mutation Implementation (2)

54

Crossover Implementation (1)

• The implementation of crossover is representation dependent.
• For GP trees represented as list of lists one needs to recursively
identify a random sub-list in the first parent and replace it with a 
recursively randomly selected sub-list from the second parent. 

• The operations are also performed on copies.

55

Crossover Implementation (2)

• Identification of a random sub-list/sub-tree in a program

56

Crossover Implementation (3)

57

Crossover Implementation (4)

• Testing the code

58

Multi-tree Representation
• GP programs can be composed of multiple trees representing 

different components of the program

• We can represent a multi-tree program as an array/list of trees.
• But multi-tree programs are often represented as trees with a 

special root node with as many children as there are components in 
the program.

• The root node acts as glue for the multiple trees, it is not meant to be 

executed.

• The components are also called branches.
• Specialised initialization, operators and interpreters are required.

59

Example

• Here, a special node called “Root”, has 

N children.

• Each child is a tree which represent a 
different component of a program.

• Each component may play a different 

role in the program.

• For example, if we want to evolve 

programs to control a robotic football 
team, Component 1 might represent 
the program controling the goalkeeper, 
Component 2 may control a defender, 
etc.

60

Divide and Conquer (1)

• In the presence of a complex problem, every good engineer will try 

and use the following ”divide-and-conquer'' strategy:

1. Decompose the problem into sub-problems which are simpler to solve
2. Solve the sub-problems
3. Combine the solutions of the sub-problems to build the solution for the 

original problem.
Iterate 1, 2 and 3 for the sub-problems if they are still too difficult.

4.

61

Divide and Conquer (2)

• This strategy applies also to programming. In this case the 
solutions of the sub-problems are usually subroutines.
• Good programmers try to build parameterised subroutines

which solve entire classes of sub-problems instead of a single 
one.

• Parameterised reuse improves the quality (e.g. generality) of 

programs and reduces their complexity.

62

Automatically Defined Function (ADF)

• It is possible to generalise GP to exploit the ``divide-and-

conquer'' strategy, i.e. to discover and use automatically good 
reusable subroutines.

• This can be easily obtained by:

• Using a multi-tree program representation with a fixed number of 

branches (components)

• Interpreting some of the branches as Automatically Defined Functions

(ADFs), i.e. subroutines

• Interpreting one of the branches as the main program.

63

ADF Example

Here, the node called “Root” has 2 children.
The first child is the function-defining branch,
which represents the program (omitting quotes):
[+, [-, arg1, arg2], arg3]

where arg1, arg2 and arg3 are the dummy
arguments of the function defined by this branch.
The second child is the value-returning branch,
i.e., the main for the program
This can (and does) use the automatically
defined function (ADF) described by the first
branch.
The main program is
[ADF, [ADF, -1, x, y], x, [-, 2, x]]

Note:
primitive sets.

the two branches have different

64

Changes required by ADFs (1)

• Different branches have different function and terminals sets:
• The main program cannot have dummy arguments but can use ADFs
• ADFs should not use global variables, i.e. variables not passed as 

arguments (better reusability, no side-effects,...)

• To prevent infinite recursion, ADFs should not call themselves nor other 

ADFs that in turn can call them.

• ADFs can use safely the ADFs defined “on their left”.

65

Changes required by ADFs (2)

• The random initialisation procedure must generate trees with the 
root special node as root node and must use different terminals 
and functions for the different children of the root node.

• Crossover has to be slightly modified to ensure it swaps sub-trees 

taken from the same branches of the parents.

• Mutation requires generating random trees using of the same

primitive set as the subtree to be excised. 

66

Example: even-4 parity function

• The even-4 parity function is a Boolean function of 4 variables 
which returns 1 (or true) if an even number of its arguments has 
value 1. It returns 0 (or false) otherwise.

• Problem: find a program that implements such a function using 

AND, OR, NAND and NOR functions.

• Again this can be seen as a symbolic regression problem with 

the following dataset:
{(x1i, x2i, x3i, x4i, yi)} = 

{(0,0,0,0,1)(0,0,0,1,0)(0,0,1,0,0)(0,0,1,1,1) .... }

67

Without ADFs

• GP parameters:
• Population size = 4000
• Function set = {AND OR NAND NOR}
• Terminal set = {x1 x2 x3 x4}
• Initial max depth = 4
• Initialisation method = Full
• Number of generations = 50
• Crossover probability = 0.7
• Mutation probability = 0
• Fitness =  - Sum over i of abs(yi - eval(prog,x1i,x2i,x3i,x4i))

68

Solution

• After 31 generations, GP found the following error-free solution 

with 71 nodes:

[AND [OR [NOR [NOR x4 x1] [AND x4 x1]]
[NAND [NAND x2 x3] [OR x3 x2]]]

[OR [AND [AND [OR x4 [OR x3 x2]]

[OR x2 x3]]

[NAND [NOR [NOR x4 x1]

[AND x4 [AND x4 x1]]]

[OR x2 x3]]]

[NAND [OR [NOR [NOR x4 x1]

[AND x4 [AND x4 x1]]]

[NOR [NOR x4 x1]
[AND x4

[NAND [OR x1 x2]

[NOR x3 x4]]]]]
[NAND [NAND x2 x3] [OR x3 x2]]]]]

69

Its tree-based representation

• There is no particular regularity in this representation.
• The tree looks rather bushy.
• Its maximum depth is 9, but most leaves are at depths 5, 6, and 7.

70

With 2 ADFs – GP Parameters

General:
• Population size = 4000
• Number of generations = 50
• Crossover probability = 0.7
• Mutation probability = 0
• Fitness = same as before

ADF1:
• function set = {AND OR NAND NOR }
• terminal set = {arg1 arg2}
• initial max depth = 3
• initialisation method = Full

ADF2:
• function set = {AND OR NAND NOR 

ADF1}

• terminal set = {arg1 arg2}
• initial max depth = 3
• initialisation method = Full

Value-returning branch:
• function set = {AND OR NAND NOR 

ADF1 ADF2}

• terminal set = {x1 x2 x3 x4}
• initial max depth = 4
• initialisation method = Full

71

With 2 ADFs Solution

• After 13 generations, GP found the following error-free solution 

with 64 nodes:

[root [NOR [NOR [NAND arg1 arg1] [NAND arg1 arg1]]

[AND [NOR arg1 arg2] [OR arg2 arg2]]]

[NAND [NAND [AND arg1 arg2] [AND arg1 arg1]]

[NAND [ADF1 arg2 arg2] [NAND arg1 arg1]]]

[ADF1 [NAND [ADF1 [AND [NOR x1 x3] x1]

[OR x3 x2]]

[ADF2 [ADF2 x4 x3] [ADF2 x1 x2]]]

[OR [ADF2 [ADF1 x3 x2] [ADF2 x1 x2]]

[ADF1 [ADF2 x3 x4] [NOR x1 x3]]]]]

72

ADF1

ADF1 is the program:

[NOR [NOR [NAND arg1 arg1]

[NAND arg1 arg1]]

[AND [NOR arg1 arg2]

[OR arg2 arg2]]]

Graphically, it is a tree with 4 levels, all the leaves being at the same 
level (full tree).

73

ADF2

ADF2 is the program:

[NAND [NAND [AND arg1 arg2]

[AND arg1 arg1]]
[NAND [ADF1 arg2 arg2]

[NAND arg1 arg1]]]

• Graphically, it is also a tree with 4 levels, with all the leaves at the 

same level (full tree).

• NOTE: ADF2 makes use of ADF1 once.         

74

Main Program

[ADF1 [NAND [ADF1 [AND [NOR x1 x3]

x1]

[OR x3 x2]]

[ADF2 [ADF2 x4 x3]

[ADF2 x1 x2]]]

[OR [ADF2 [ADF1 x3 x2]

[ADF2 x1 x2]]

[ADF1 [ADF2 x3 x4]

[NOR x1 x3]]]]]

• Graphically, it is a tree with 5 levels, with most of its leaves at level 4. It uses 

ADF1 four times and ADF2 six times.

75

Advantages and Disadvantages (1)

• For this problem the structural complexity with ADFs is only 
slightly smaller than without ADFs. However, in some more 
complex problems the saving may be much bigger.

• Reduction in complexity may be accompanied by a reduction in 

computation load.

• Programs with ADFs may be easier to understand.

76

Advantages and Disadvantages (2)
• For example, by building the truth tables of ADF1 and ADF2 we discover that

ADF1(arg1,arg2) = NOT arg1
ADF2(arg1,arg2) = NOT ( arg1 XOR arg2 )

= EVEN2(arg1,arg2)

• So, we can rewrite the main program as

[NOT [NAND [NOT [AND [NOR x1 x3] x1]]

[EVEN2 [EVEN2 x4 x3]

[EVEN2 x1 x2]]]]

• Further analysis shows that this is equivalent to

[EVEN2 [EVEN2 x4 x3]

[EVEN2 x1 x2]]]]

77

Advantages and Disadvantages (3)

Graphically

=

• In problems which present either minor internal regularities or 
regularities that cannot be easily captured by ADFs, ADFs can 
slow down GP rather than help it.

78

What did we learn? (1)

• We have learned that GP trees can be represented as expressions 

in prefix notation

• We have learned that we can create syntactically correct 

programs, and we can avoid run-time errors when using closed
primitive sets

• Sufficient primitive sets allow the GP to create programs that are 

capable of expressing the solution. Insufficient primitive sets only 
find approximations.

79

What did we learn? (2)

• We have seen how huge the search space is, even with small 

trees.

• The Full initialisation method takes nodes from the function set

until the maximum tree depth is reached. The Grow initialisation 
method selects nodes from the whole primitive set. In practice, a 
ramped half-and-half initialisation is usually used.

80

What did we learn? (3)

• We have learned that different program execution strategies exist 
and that the decision “compilation vs. interpretation” in terms of 
computational complexity depends on the specific problem.

• We focused on interpretation and have seen that interpreting a 

program tree means recursively traversing the tree and 
executing nodes when their arguments are known. We have 
learned that there are problems with non-functional instructions 
and that we need macros, which have unevaluated arguments as 
their input.

81

What did we learn? (4)

• XO with tree-like programs requires swapping of sub-trees.

• Mutation requires replacing a randomly chosen subtree with a 

newly generated random program.

• Programs can also be composed of multiple trees, each 

representing a different component of the program. This allows 
the GP to reduce the complexity of solutions and to discover and 
automatically use “good” reusable subroutines. Of course, such 
structural changes require adaptation of genetic operators and 
initialisation routines.

82

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Next time: 
Bloat in GP

```

---

## B. Lecture 07（PDF可提取全文）

```text

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

Bloat in GP

What did we learn last time? (1)

• We learned that different program execution strategies exist 

focusing on interpretation.

• We have seen that interpreting a program tree means recursively

traversing the tree and executing nodes when their arguments are 
known. 

• We have learned that there are problems with non-functional

instructions and that we need macros, which have unevaluated 
arguments as their input.

2

What did we learn today? (2)

• XO with tree-like programs requires swapping of sub-trees, 

mutation requires replacing a sub-tree with a new random one.

• Programs can also be composed of multiple trees, each 

representing a different component of the program. 

• This can be used to define subroutines (ADFs) that may reduce

the complexity and increase generality and understandability of 
solutions.

3

This week’s learning objectives

• Describe bloat
• Describe different theories that explain “why bloat happens?”

and discuss them.

• Explain approaches to control bloat

4

What’s bloat?

Bloat = Growth in program size (variable length representation) 
without significant return in terms of fitness.

Size

Fitness

t

McPhee & Miller (1995), McPhee & Poli (2001) 

5

Does it continue forever?

Average behaviour

Single run

6

Artificial ant problem (Santa Fe trail)

7

Artificial ant problem (Santa Fe trail)

Santa Fe trail problem: https://www.youtube.com/watch?v=BKF7pGw8qbY

Langdon & Poli (1998)   

8

Ant Problem: Mean Fitness vs Generations

Fitnes
s

90

45

10

20
Generations

30

40

50

9

Ant Problem: Mean Program Size vs Gen.

Fitnes
s
90

45

Size limit

Size
500

250

10

20
Generations

30

40

50

10

Bloat - Why does it happen?

• Bloat has been thoroughly investigated for decades  
• (Too) many theories propose to explain it.
• So,  for some people bloat is still a mystery.

11

GP Search Space

Double logarithmic scale

Exponentials

12

Limiting distribution

• Empirically and theoretically, it has been shown that as program 
length grows the distribution of functionality reaches a limit

13

{d0,d1,NAND} search space

Proportion of 2-input logic functions 
implemented using NAND primitives

14

Search spaces

• Proportion of Ant programs 

with each score

• Error Distribution Sextic

Polynomial Problem (x6+…)

15

Nature of program search spaces theory

• Above a certain size,  the distribution of fitness does not vary 

with size.

• Since there are more long programs, the number of long  

programs of a given fitness is greater than the number of short  
programs of the same fitness.

• Thus, over time GP samples longer  and longer programs simply 

because there are more of them.

16

Active vs Inactive Code
• Most code in bloated programs is inactive, e.g.

• a * 0 = 0 however big the expression for a is
• IF( 0, b, c ) = c whatever b is

• When a fit program is changed, it produces unfit offspring most

of the time.

• Active code is like “icing on the cake”

17

Replication accuracy theory

• The success of a GP individual  depends on its ability to have 

offspring that are functionally similar to the parent.

• So, GP evolves towards (bloated)  representations that 

increase replication accuracy.

18

Removal bias theory

• Inactive code in a GP tree is low in the tree, forming smaller-

than-average-size subtrees.

• Crossover events excising inactive subtrees produce offspring 

with the same fitness as their parents.

• On average the inserted subtree is bigger than the excised one, 

so such offspring are bigger than average.

19

More evidence: No Fitness = No Bloat

Fitnes
s
90

45

Size
500

250

10

20
Generations

30

40

50

20

Crossover Bias

Proportion 
of programs

Just XO, no fitness!

Generation

Size

21

Can fitness override the XO bias?

Proportion 
of programs

fitness

size

Generation

Size

22

Crossover Bias Theory of Bloat

• Crossover does not change the mean program size, on average, 

but…

• It creates a population with a large proportion of small 

programs.

• In most problems, very small programs are unfit, so they are 

ignored by selection. Thus…

• Only larger programs will be picked as parents, hence …
• Mean program size increases.

23

Size Evolution (1)

• The mean size of the programs in the current generation is 

𝜇𝑔 =

1
𝑁

𝑁

෍

𝑖=1

𝑠𝑖

with N number of programs

• However, if we group programs by size:

𝝁𝒈 = 𝟏 × 𝚽 𝟏 + 𝟐 × 𝚽 𝟐 + ⋯ = σ 𝐬 × 𝚽 𝒔

with 𝚽 𝒔 = proportion of programs of size s in the population

24

Size Evolution (2)
• Instead of creating a new generation g+1 by selection and crossover, 

we split this into two steps: 

1. we create a new generation just by selection and duplication, and
2. create a further generation by applying crossover (randomly selecting 

parents from the first). 

• After (1), the mean program size will be 

𝝁𝒔𝒆𝒍 = 𝟏 × 𝐩 𝟏 + 𝟐 × 𝐩 𝟐 + ⋯

where p(s) = probability of selecting a program of size s from the population

• On average, crossover on its own takes away as much as it puts in.
• So going from (1) to (2) we should not see any changes in mean 

program size. That is 

𝝁𝐠+𝟏 = 𝝁𝒔𝒆𝒍 = 𝟏 × 𝐩 𝟏 + 𝟐 × 𝐩 𝟐 + ⋯

25

Conditions for Growth

• Growth/bloat can happen only if

𝐄 𝝁𝐠+𝟏 − 𝝁𝒈 = 1 ∙ 𝑝 1 − Φ 1 + 2 ∙ 𝑝 2 − Φ 2 + ⋯ + N ∙ 𝑝 N − Φ N > 𝟎

• So, there must be:

• some short programs for which 𝒑 𝒔 < 𝜱 𝒔 or
• some longer ones for which 𝒑 𝒔 > 𝜱 𝒔 (or both, at least on average).
• For years, the focus was on why are longer programs were preferred?

(𝒑 𝒔 > 𝜱 𝒔 for big 𝒔)
• The crossover bias theory (and my experiments with Nic McPhee) showed that the 

culprit was the short/bad programs!

(𝒑 𝒔 < 𝜱 𝒔 for small 𝒔) 

26

Main techniques for limiting code bloat: Size 
limits
• Fixed size or depth limit: Programs exceeding the limit are 

discarded and a parent is kept instead.

• This is very dangerous as it gives a fitness advantage to programs 

that tend to violate the constraint.

• Trying crossover again or giving 0 fitness to programs above the 

threshold is a better way to do it

27

Main techniques for limiting code bloat: 
Modifying operators
• Modification of operators: variation of the selection probability of 
crossover points by using explicitly defined introns, rejection of 
destructive crossover events, size-fair operators, multi-objective 
optimization (MOO) techniques, etc.

• For example, point mutation (applied with a fixed probability per 

node) has an anti bloat effect.

28

Main techniques for limiting code bloat: 
Acting on Selection
• Size evolution equation shows that to prevent growth one needs

• To decrease the selection probability  for  bigger than average programs
• To increase the selection probability  for below-average-size programs
• Or both

29

Bloat Control with Fitness Holes

• If one can create artificial fitness holes in areas of the search 

space which we want to avoid, then evolution will try to stay away 
from those areas.

30

Parsimony Pressure Method

• A term is added to the fitness function that penalises larger 

programs.  Typically:

fparsimony(prog) = fraw(prog)–c*size(prog)

where c is a constant (parsimony coefficient)

• An alternative

fparsimony(prog) = fraw(prog)+c/size(prog)

31

Tarpeian bloat control

• The basic Tarpeian method decreases the selection probability of  
longer-than-average programs, but it does it for some random 
individuals in the set and for some of the time

• Tarpeian fitness-wrapper

IF (size(program) > average_pop_size) AND (rand_num < ptarp) THEN

return( very_low_fitness );

ELSE

return( fitness(program) );

• The Tarpeian method  creates fitness holes  dynamically and 
non-deterministically (only for larger-than-average programs).

32

Why “Tarpeian”?

33

Features of the Tarpeian Method (1)

• The wrapper does not evaluate the individuals killed, so  

computation is saved not wasted.

• If enough better-than-average longer-than-average individuals are 
produced, the average program size  grows. That is, the algorithm  
allows growth as long as it is associated to fitness 
improvements.

34

Features of the Tarpeian Method (2)

• If the average program size increases, the fitness hole moves so 

as to discourage further growth.

• The parameter ptarp determines the intensity of the repulsive  force 

exerted by the fitness hole.

• The pressure to shrink does not change with program size.

35

Hot Air Balloon Metaphor

36

Covariant parsimony pressure

• Parsimony pressure method 

𝑓𝑝 = 𝑓 − 𝑐 ∙ s

• Size evolution equation can be rewritten as:

𝐸 ∆𝜇 =

𝐶𝑜𝑣 𝑓, 𝑠 − 𝑐 ∙ 𝑉𝑎𝑟(𝑠)
ҧ𝑓 − 𝑐 ∙ 𝜇

• If we want no growth, then we can set the right-hand side to 0. 

Solving for c gives

c =

𝐶𝑜𝑣(𝑓,𝑠)

𝑉𝑎𝑟(𝑠)

37

What did we learn? (1)

• We have learned that bloat is the growth in program size

(variable length representation) without significant return in 
terms of fitness.

• Replication accuracy theory: GPs evolve bloated 

representations that are functionally like the parents.

• Removal bias theory: crossover inserts subtrees that on average 

are bigger than excised ones

• Crossover bias theory: Crossover creates many small and unfit 

programs.

38

What did we learn? (2)

• Growth can only occur when the selection probability of short
programs is lower than average and of long programs is higher
than average.

• Limit bloat by using a fixed size or depth limit or modifying the 

genetic operators

• Prevent bloat by adding a penalty term to the fitness (parsimony
pressure) or by dynamically and non-deterministically creating 
fitness holes (Tarpeian)

39

[CE310]
Evolutionary Computation 
and Genetic Programming

Riccardo Poli

….

```

---
