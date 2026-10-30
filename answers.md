# CMPS 6610 Problem Set 04

## Answers

**Name:** Kailee Segarra

### 1d. Fixed-length vs. Huffman encoding

The costs below are in bits. The ratio is Huffman cost divided by fixed-length cost.

| File | Fixed-Length Coding (bits) | Huffman Coding (bits) | Ratio |
|---|---:|---:|---:|
| f1.txt | 1,340 | 826 | 0.616 |
| alice29.txt | 1,039,367 | 676,374 | 0.651 |
| asyoulik.txt | 876,253 | 606,448 | 0.692 |
| grammar.lsp | 26,047 | 17,356 | 0.666 |
| fields.c | 78,050 | 56,206 | 0.720 |

**Trend:** Huffman encoding is less costly than or equal to fixed-length encoding. By giving shorter bit strings to frequent characters and longer ones to rare characters, Huffman coding takes advantage of unequal character frequencies. A lower ratio means greater compression.

### 1e. Equal character frequencies

Let $m = |\Sigma|$ be the number of distinct characters and $N$ the total number of characters in the document. If every character occurs equally often, Huffman produces a nearly balanced tree: codewords have lengths $\lfloor\log_2 m\rfloor$ or $\lceil\log_2 m\rceil$. When $m$ is a power of two, every character uses exactly $\log_2 m$ bits, giving a total cost of $N\log_2 m$ bits. Otherwise, some codes are one bit longer than others. More precisely, for $m\ge 2$, letting $L=\lfloor\log_2 m\rfloor$, the average length is $L+2-2^{L+1}/m$ bits per character, so the total cost is $N(L+2-2^{L+1}/m)$ bits.

The total cost is **not** the same across all documents: it depends on $N$ and $m$. For a fixed alphabet size with equally frequent characters, however, the average number of bits per character is consistent, regardless of which specific characters appear.

### 2a. Constructing a binary min-heap in $O(n)$ work

Store the $n$ elements in an array as an almost-complete binary tree. The leaves already satisfy the min-heap property. Starting at the last internal node, index $\lfloor n/2\rfloor-1$, move backward to the root. At each node, **sift down**: compare the node with its children and swap it with the smaller child until it is no larger than either child.

This builds a min-heap because each node is fixed after its two child subtrees are already heaps. Although an individual sift-down may take $O(\log n)$ work, most nodes are close to the leaves. There are at most $n/2^{h+1}$ nodes at height $h$, so the total work is bounded by

$$O\left(\sum_{h=0}^{\lfloor\log_2 n\rfloor}\frac{n}{2^{h+1}}h\right)=O(n).$$

### 2b. Span

In the sequential bottom-up algorithm described above, the sift-down operations run one after another, so the span is $O(n)$. If nodes at the same depth are processed in parallel (working from the lowest internal level upward), their subtrees do not overlap. Each level then takes at most $O(\log n)$ span, giving $O(\log^2 n)$ span with the same $O(n)$ total work.

### 3a. Greedy algorithm for powers-of-two coins

Process the coin denominations from largest to smallest, starting with $2^k$. For each denomination $2^i$, take $q=\lfloor N/2^i\rfloor$ coins, then replace $N$ by $N-q2^i$. Continue until the remaining amount is zero. This uses the largest available denomination as often as possible before moving to the next one.

### 3b. Proof of optimality

**Greedy-choice property:** In an optimal solution, there cannot be two coins of value $2^i$ when $i<k$, because replacing those two coins with one $2^{i+1}$ coin gives the same value with fewer coins. Therefore, all coins smaller than $2^k$ together can contribute at most $2^k-1$. The optimal solution must use exactly $\lfloor N/2^k\rfloor$ coins of the largest denomination; otherwise it cannot make up the remaining value optimally. This is exactly the greedy choice.

**Optimal substructure:** After taking those coins, the remaining amount is less than $2^k$. The same argument applies to the remaining denominations: any optimal solution for the full amount must use an optimal solution for the remainder, or we could replace it with a better one. Repeating this process gives the binary representation of the remainder and uses the minimum number of coins.

### 3c. Work and span

The algorithm examines each of the $k+1$ denominations once, using division and subtraction to decide how many coins to take. Therefore, the work is $O(k)$ and, for this sequential algorithm, the span is also $O(k)$. This counts coin quantities rather than outputting each coin separately.

### 4a. Counterexample to greedy change-making

Suppose the denominations are $\{1,3,4\}$ and we want to make $N=6$. Greedy chooses $4+1+1$, using **3 coins**. But $3+3$ uses only **2 coins**, so choosing the largest denomination first is not always optimal.

### 4b. Optimal substructure

Let $OPT(x)$ be the minimum number of coins needed to make amount $x$, with $OPT(0)=0$ and $OPT(x)=\infty$ if $x$ is impossible. If an optimal solution for $x$ contains a coin of denomination $d$, the remaining coins must form an optimal solution for $x-d$. Otherwise, replacing them with a solution using fewer coins would improve the original solution, contradicting optimality.

Thus,

$$OPT(x)=1+\min_{d\in D,\ d\le x}OPT(x-d),$$

where the result is infinite if no valid choice can make the amount. This proves optimal substructure.

### 4c. Dynamic programming algorithm

Use bottom-up dynamic programming. Set $dp[0]=0$ and initialize $dp[1],\ldots,dp[N]$ to infinity. For every amount $x$ from $1$ through $N$, examine each denomination $d\le x$ and update

$$dp[x]=\min(dp[x],1+dp[x-d]).$$

Since the smaller amounts have already been computed, $dp[x]$ is optimal by the recurrence in 4b. If $dp[N]$ is still infinity, making change is impossible. Otherwise, $dp[N]$ is the fewest coins; storing the selected last coin at each amount lets us reconstruct the solution.

There are $N$ amounts and at most $k$ denominations to check for each, so **work is $O(Nk)$** and **span is $O(Nk)$** for the sequential bottom-up implementation. If the comparisons for each amount run in parallel, the minimum can be reduced in $O(\log k)$ span per amount, giving $O(N\log k)$ span.

### 5a. Optimal substructure for weighted task selection

**Yes.** Sort tasks by finish time. Suppose an optimal schedule includes task $a_i$. The tasks scheduled before $a_i$ must finish by its start time $s_i$. Those earlier tasks must themselves be the maximum-value compatible schedule among the tasks finishing by $s_i$. If a higher-value compatible subset existed, we could replace the earlier tasks with that subset, keep $a_i$, and improve the total value. That would contradict optimality.

Thus, an optimal solution can be built from optimal solutions to smaller sets of compatible tasks.

### 5b. Greedy-choice property

The usual greedy rules do **not** guarantee an optimal solution when task values differ. Two counterexamples are:

- **Earliest finish time:** Task A is $(s=0,f=2,v=1)$ and task B is $(s=0,f=3,v=100)$. Choosing A because it finishes earlier yields value $1$, while choosing B yields value $100$.
- **Highest individual value:** Task A is $(0,4,10)$, task B is $(0,2,6)$, and task C is $(2,4,6)$. Choosing A first yields value $10$. Choosing the compatible tasks B and C yields $6+6=12$.

So neither earliest finish time nor highest individual value has the greedy-choice property for this problem. Dynamic programming is needed to account for how a choice affects the remaining schedule.

### 5c. Dynamic programming for weighted task selection

First, sort tasks by finish time and number them $1,\ldots,n$. For each task $i$, calculate $p(i)$, the index of the last task that finishes at or before $s_i$ (or $0$ if none exists). Let $OPT(i)$ be the maximum value obtainable from the first $i$ tasks.

$$OPT(0)=0,$$

$$OPT(i)=\max\big(OPT(i-1),\ v_i+OPT(p(i))\big).$$

The first option skips task $i$; the second takes it and adds the best compatible earlier schedule. By the optimal substructure property in 5a, the larger choice is optimal. Compute the table from $i=1$ through $n$ and return $OPT(n)$. We can reconstruct the chosen tasks by following the decisions made in the table.

Sorting takes $O(n\log n)$ work. Finding all predecessor indices with binary search takes $O(n\log n)$ work, and filling the table takes $O(n)$. Thus, the **total work is $O(n\log n)$**, the **span is $O(n\log n)$ for this sequential implementation**, and the table uses $O(n)$ additional space.
