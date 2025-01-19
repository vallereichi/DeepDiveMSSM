# Differential Evolution

DE is an efficient algorithm for finding minima in a n-dimensional parameter space. Since it is a greedy algorithm it has to be initialised with many points in the parameter space to ensure sufficient exploration and to find the global minimum. This is a contrast to other optimization algorithms which handle exploration differently. One example for this would be the MCMC algorithm. The specific details of differential evolution are explained in the sections below.

## algorithmic details

The most simple and commonly used form of differential evolution is the _rand/1/bin_ algorithm. It is also very easy to understand and implement. The first step is to select _NP_ (number of points) from the parameter space. This is usually done by randomly sampling the parameter space. Here it is important to note that the space itself should be confined in order to avoid unsensible outputs and non converging runs. The initial population now consists of _NP_ n-dimensional points and will be denoted as the _target vectors_:

$$\textbf{X}^g = \set{X_1^g, ..., X_{NP}^g}$$

$$
X_i^g = \left(\begin{array}{c}
    X_{i_1} \\
    \vdots  \\
    X_{i_n}  \\
\end{array}\right)
$$

where the _g_ keeps track of the generation of the population. The subsequent transformation of the population will be performed on one of the target vectors and can differ from generation to generation. The selection of the target vector depends on the form of the algorithm in use. In the case of _rand/1/bin_ the target vector is chosen randomly for each generation. This is denoted by the "_rand_". Other options will be discussed in a later section of this readme file. Depending on the target vector choice one can achieve different behaviors of the algorithm, such as fast convergance or contour building.

### Mutation

The mutation process is the first step of the algorithm. The goal of muation is the creation of so called _donor vectors_, which are found by adding a scaled difference vector to a vector frmo the current pupulation. In the _rand/1/bin_ scheme the "_1_" suggests that only one difference vector will be applied in the following way. Three vectors are chosen randomly from the current population ($X_{r_1}^0, X_{r_2}^0, X_{r_3}^0$) such that none of them arethe same and none of them maches the current target vector $X_i$. Then the new donor vector $V_i$ will be:

$$V_i = X_{r_1} + F * (X_{r_2} - X_{r_3})$$

where _F_ is the mutation scale factor, which controls the exploration of the parameter space. Generally this strategy allows the algorithm to explore the objective function dynamically. Lower values for _F_ can lead to insufficient exploration and premature convergence, while the mutation scale factor is still required to be less than 1 in order to achieve convergence.

### Crossover
