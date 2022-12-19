# Brief Writeup

## Description
> Author: @Gary#4657

`Recursion is all fun and games until...
Hint - Matrix Diagonalization could be useful `

## Writeup
I'm not going to explain the math too much, because it's a lot of Linear Algebra that you can find better resources for online. Here are two links that helped me remember how to do this stuff.

- [Carnegie Mellon](https://mathcourses.nfshost.com/archived-courses/mat-335-2017-summer/sage/sagecell-diagonalization.html)
- [JustinMath](https://www.justinmath.com/recursive-sequence-formulas-via-diagonalization/)
- [nsfhost.com](https://mathcourses.nfshost.com/archived-courses/mat-335-2017-summer/sage/sagecell-diagonalization.html) - Explains how to do the math in SageMath

Basically, the challenge is less crypto, and attempting to evaluate the result of the following recursive function:

```python
def f(i):
    if i < 5:
        return i+1
    
    return 1905846624*f(i-5) - 133141548*f(i-4) + 3715204*f(i-3) - 51759*f(i-2) + 360*f(i-1)
```

Python cannot do everything, and here's why we can't do `f(13371337)` very quickly like this:
- Recursion can make things look nice, but it's a lot more demanding compared to iterative solutions since it needs to store and break down all of the function calls
- Even if we wrote an iterative solution, I'm not sure it would be that much faster, as the numbers we're crunching are pretty large, even for Python

If you've taken any kind of algebra course, you're probably familiar with sequences, and this function is just a recursive definition of a sequence.

$$
\begin{align*}
f_i &= 1905846624f_{i-5} - 133141548f_{i-4} + 3715204f{i-3} - 51759f{i-2} + 360f{i-1}
\end{align*}
$$

From here, the process to solve is fairly simple:
- Construct a matrix from the equation
- Diagonalize the matrix to create a computationally feasible situation
- $v_{n+1} = A^{n-1}v_4$ will take the diagonalized matrix $A$ times a vector of initial values $v_4$ to calculate whatever number we want
- The decryption code is written for us.