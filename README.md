# CW2

# 泰裤辣

## Deadline

 **16:00 May 12, 2023**

## Poster

**Poster Presentation: 1 pm-5 pm May 17, 2023**

Tentative plan：

- Time: 1 pm - 5 pm, Wednesday, May 17th

- Venue: Entrance of MB Building

- Each group should prepare a poster

- Printing options:

  - We print it for you (send the file to our TA XueqiYao20@student.xitlu.edu.cn by May 14th)

  - Print it out yourself and bring it to the poster presentation

## Requirements

Each group (not each person) should submit a report:

- Hard copy (A4 size) to the mailbox (Min's or Ruonan's) on the 5th floor MB building
- 1000-1500 words (including tables & figures,excluding references and appdendix).
- Include a cover page, specifying your team name and which topic you choose

## TOPIC 3

Search or designed by yourself to investigate a real-life MIP problem. Formulate the general model for the problem and solve it using existing solvers, such as Excel, LINGO, CPLEX, etc.

CPLEX download: <https://www.ibm.com/products/ilog-cplex-optimization-studio>

LINGO download: <https://lindo.com/>

**Report outline sample for Topic 3:**

- Introduction(the background of your problem, the story)

- Problem description(what are the inputs, the assumptions, the objective, and the constraints; a toy example, figure illustrations if possible; etc.)

- MIP Model(Notations for sets, parameters, variables; explain how to model each constraint, present the entire model)

- Computational Results(data, software/solver used to solve the MIP model, sensitivity analysis and other interesting results, etc)

- Conclusion

- References

- Appendix (snapshot of models and results in the solver, etc)

## MARKING Criteria

**Report**

(15%) Structure

(10%) Creativity

(30%) Methodology

(20%) Coherent account in own words

(15%) Ease of reading and grammar

(10%) Word count

**Poster presentation**

(40%) Preparation of poster

(20%) Clarity of voice and spoken language

(40%) Logic and structure of the contents

Lecturer’s marks will be given to the entire team (same for all the members) considering report and presentation, each with 50%

## Inspiration

### Objective function规范写法

如果你想遍历两个图结构中的所有节点一次, 可以将这个问题建模为一个“广义旅行商问题” (Generalized Traveling Salesman Problem, GTSP)， 因为你需要找到一个能够遍历所有节点的最短路径, 同时考虑两个图中的连通性。

假设两个图分别是 $\mathrm{G} 1(\mathrm{~V} 1, \mathrm{E} 1)$ 和 G2(V2, E2)，其中 $V 1$ 和 $\mathrm{V} 2$ 是节点集合, E1 和 E2 是边集 合。我们需要找到一个路径 $P$, 使得 $P$ 能够遍历所有节点, 并尽可能地优化某个目标（例如 最短路径）。

首先, 我们需要将两个图进行合并。可以定义一个新的图 $G(V, E)$, 其中 $V=V 1 \cup V 2$, 然后 定义 $E$ 的集合，使得如果两个节点在 G1 或 G2 中是连通的，那么它们在 G 中也是连通的。
具体来说, $E=\{(u, v) \mid(u, v) \in E 1$ 或 $(u, v) \in E 2\}$ 。
然后, 在新图 G 上应用广义旅行商问题的公式：
Minimize:
$$\sum_{(u, v) \in E} c(u, v) \cdot x(u, v)$$

Subject to:
$$\sum_{(u, v) \in \delta(S)} x(u, v) \geq 1 \quad \forall S \subseteq V, S \neq \emptyset, V$$
$$\sum_{v \in V} x(u, v) = 1 \quad \forall u \in V$$
$$\sum_{u \in V} x(u, v) = 1 \quad \forall v \in V$$

In this formulation:

- 'c(u, v) ' is the cost (e.g., distance) between nodes 'u’ and 'v'.
- ' $x(u, v)$ ' is a binary variable, equal to 1 if the edge ' $(u, v)$ ' is included in the solution, and $O$ otherwise.
- ' $\delta(\mathbf{S})$ ' is the set of edges with one endpoint in the subset ' $\mathbf{S}$ ' and the other endpoint outside of ' $\mathbf{S}$ '.
- The first constraint ensures that at least one edge enters and leaves every subset ' $\mathbf{S}^{\text {' }}$ of nodes.
- The second and third constraints ensure that exactly one edge enters and leaves each node.

### 假设

1. 来回cost和time都一样
