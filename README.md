# CW2

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

CPLEX download: https://www.ibm.com/products/ilog-cplex-optimization-studio 

LINGO download: https://lindo.com/

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

Minimize:
$$\sum_{(u, v) \in E} c(u, v) \cdot x(u, v)$$

Subject to:
$$\sum_{(u, v) \in \delta(S)} x(u, v) \geq 1 \quad \forall S \subseteq V, S \neq \emptyset, V$$
$$\sum_{v \in V} x(u, v) = 1 \quad \forall u \in V$$
$$\sum_{u \in V} x(u, v) = 1 \quad \forall v \in V$$

In this formulation:

- 'c(u, v) ' is the cost (e.g., distance) between nodes 'u' and 'v'.
- ' $x(u, v)$ ' is a binary variable, equal to 1 if the edge ' $(u, v)$ ' is included in the solution, and $O$ otherwise.
- ' $\delta(\mathbf{S})$ ' is the set of edges with one endpoint in the subset ' $\mathbf{S}$ ' and the other endpoint outside of ' $\mathbf{S}$ '.
- The first constraint ensures that at least one edge enters and leaves every subset ' $\mathbf{S}^{\text {' }}$ of nodes.
- The second and third constraints ensure that exactly one edge enters and leaves each node.


