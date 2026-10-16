# Complete positivity range of the qubit depolarizing map

**Claim.** For real $p$ let $\Phi_p:M_2(\mathbb C)\to M_2(\mathbb C)$, $\Phi_p(X)=(1-p)X+p\,\operatorname{Tr}(X)\,I/2$.

- (a) $\operatorname{Tr}\Phi_p(X)=\operatorname{Tr}X$ for all $X\in M_2$ and all real $p$.
- (b) $\Phi_p$ is completely positive iff $0\le p\le 4/3$.

**Sources.** The proof below is self-contained. The only result from the user's papers is Choi's criterion, and it appears only in the optional cross-check: [bu-gu-jaffe-magic, unnumbered statement before Lemma 67, p. 25 (PDF page)]. Other standard facts are named where they are used.

## Hypotheses
- H1. $\mathcal H=\mathbb C^2$ (finite-dimensional). $p\in\mathbb R$.
- H2. $\Phi_p$ is defined by the formula above on all of $M_2(\mathbb C)$. It is linear.
- H3. Completely positive (CP) means: for every $n\ge1$, $\Phi_p\otimes\mathrm{id}_{M_n}$ maps positive semidefinite (PSD) elements of $M_2\otimes M_n$ to PSD elements.

## Conventions
- Physics inner product (linear in the second slot). $\{|0\rangle,|1\rangle\}$ is the computational basis and $E_{ij}=|i\rangle\langle j|$.
- Choi matrix (unnormalized, with $\Phi$ on the **second** factor): $J(\Phi)=\sum_{i,j}E_{ij}\otimes\Phi(E_{ij})$. This is what `tools/qmath.py: choi` computes.
- $|\Omega\rangle=(|00\rangle+|11\rangle)/\sqrt2$, so $\sum_{i,j}E_{ij}\otimes E_{ij}=2|\Omega\rangle\langle\Omega|$.
- Paulis: $\sigma_0=I$, $\sigma_1=X$, $\sigma_2=Y$, $\sigma_3=Z$.

## Strategy
Part (a) is a one-line computation. For (b), the proof is self-contained and does not need Choi's theorem.
- **Necessity:** apply $\Phi_p\otimes\mathrm{id}_2$ to the PSD matrix $2|\Omega\rangle\langle\Omega|$. The result is $2(1-p)|\Omega\rangle\langle\Omega|+\tfrac p2 I_4$, with eigenvalues $2-\tfrac{3p}{2}$ (once) and $\tfrac p2$ (three times). It fails to be PSD exactly when $p<0$ or $p>4/3$.
- **Sufficiency:** for $0\le p\le4/3$, write $\Phi_p$ in Kraus form, $\Phi_p(X)=\sum_\mu K_\mu XK_\mu^\dagger$ with $K_0=\sqrt{1-3p/4}\,I$ and $K_k=\sqrt{p/4}\,\sigma_k$. Any such map is CP.

Choi's theorem gives the same result from the spectrum of $J(\Phi_p)$; it is noted as a cross-check.

## Proof

**Step 1 (part (a)).** For any $X\in M_2$:
$$\operatorname{Tr}\Phi_p(X)=(1-p)\operatorname{Tr}X+p\operatorname{Tr}X\cdot\frac{\operatorname{Tr} I_2}{2}=(1-p)\operatorname{Tr}X+p\operatorname{Tr}X=\operatorname{Tr}X.$$
This uses linearity of the trace and $\operatorname{Tr}I_2=2$. It holds for every real $p$, and indeed for every complex $p$. **[Own reasoning]**, **[Computed]** (C3).

**Step 2 (Choi matrix).** By linearity, $\Phi_p(E_{ij})=(1-p)E_{ij}+\tfrac p2\delta_{ij}I$, because $\operatorname{Tr}E_{ij}=\delta_{ij}$. So
$$J(\Phi_p)=(1-p)\sum_{i,j}E_{ij}\otimes E_{ij}+\frac p2\sum_i E_{ii}\otimes I=2(1-p)|\Omega\rangle\langle\Omega|+\frac p2 I_4,$$
using $\sum_iE_{ii}=I_2$. **[Own reasoning]**, **[Computed]** (C1).

**Step 3 (spectrum).** $2|\Omega\rangle\langle\Omega|$ is $2\times$ a rank-one projector. So $J(\Phi_p)$ has:
- eigenvalue $2(1-p)+\tfrac p2=2-\tfrac{3p}{2}$ on $|\Omega\rangle$;
- eigenvalue $\tfrac p2$ on the 3-dimensional subspace $|\Omega\rangle^\perp$ (for example $|01\rangle$, $|10\rangle$, $(|00\rangle-|11\rangle)/\sqrt2$).

Hence $J(\Phi_p)\ge0 \iff p\ge0$ and $p\le 4/3$. **[Own reasoning]** (spectral theorem for a Hermitian matrix that is a combination of $I$ and a projector), **[Computed]** (C2).

**Step 4 (the test matrix under $\Phi_p\otimes\mathrm{id}$).** Let $P=\sum_{i,j}E_{ij}\otimes E_{ij}=2|\Omega\rangle\langle\Omega|\in M_2\otimes M_2$. It is PSD because it is $2\times$ a projector. Then
$$(\Phi_p\otimes\mathrm{id}_2)(P)=\sum_{i,j}\Phi_p(E_{ij})\otimes E_{ij}=2(1-p)|\Omega\rangle\langle\Omega|+\frac p2 I_4=J(\Phi_p).$$
The middle expression is the same computation as in Step 2 with the tensor factors swapped. The swap leaves both $|\Omega\rangle\langle\Omega|$ and $I_4$ unchanged. So the hypothesis H3 convention ($\Phi$ on the first factor) and the Choi convention ($\Phi$ on the second factor) give the identical matrix here. **[Own reasoning]**, **[Computed]** (C8).

**Step 5 (necessity).** Suppose $\Phi_p$ is CP. Apply H3 with $n=2$ to the PSD matrix $P$ from Step 4: then $(\Phi_p\otimes\mathrm{id}_2)(P)=J(\Phi_p)\ge0$. By Step 3, $0\le p\le 4/3$.

The contrapositive gives explicit witnesses:
- If $p<0$: $\langle01|J(\Phi_p)|01\rangle=p/2<0$.
- If $p>4/3$: $\langle\Omega|J(\Phi_p)|\Omega\rangle=2-3p/2<0$.

In both cases $\Phi_p\otimes\mathrm{id}_2$ is not even positive. **[Own reasoning]**, **[Computed]** (C10, C11).

**Step 6 (Pauli twirl identity).** For every $X\in M_2$:
$$\sum_{\mu=0}^3\sigma_\mu X\sigma_\mu=2\operatorname{Tr}(X)\,I.$$
*Proof.* Both sides are linear in $X$, and $\{\sigma_\nu\}$ is a basis of $M_2$, so it suffices to check $X=\sigma_\nu$.
- For $\nu=0$: the left side is $4I$, and $2\operatorname{Tr}(I)I=4I$.
- For $\nu=k\in\{1,2,3\}$: $\sigma_\mu\sigma_k\sigma_\mu=\sigma_k$ if $\sigma_\mu$ commutes with $\sigma_k$ ($\mu\in\{0,k\}$). It equals $-\sigma_k$ if they anticommute (the other two $\mu$). This uses $\sigma_\mu^2=I$ and the fact that distinct non-identity Paulis anticommute. So the sum is $(1+1-1-1)\sigma_k=0=2\operatorname{Tr}(\sigma_k)I$. $\square$

This is a standard result, not from your papers (e.g. Nielsen–Chuang, the depolarizing-channel section). **[Own reasoning]**, **[Computed]** (C4).

**Step 7 (Kraus form).** By Step 6, $p\operatorname{Tr}(X)I/2=\tfrac p4\left(X+\sum_{k=1}^3\sigma_kX\sigma_k\right)$. Therefore
$$\Phi_p(X)=\Bigl(1-\tfrac{3p}{4}\Bigr)X+\tfrac p4\sum_{k=1}^3\sigma_kX\sigma_k\qquad(\text{all real }p).$$
For $0\le p\le4/3$ both coefficients are $\ge0$, so we can set $K_0=\sqrt{1-3p/4}\,I$ and $K_k=\sqrt{p/4}\,\sigma_k$ ($k=1,2,3$). Then:
- $\Phi_p(X)=\sum_{\mu=0}^3K_\mu XK_\mu^\dagger$, since each $\sigma_k$ is Hermitian;
- $\sum_\mu K_\mu^\dagger K_\mu=(1-\tfrac{3p}{4}+\tfrac{3p}{4})I=I$. This is consistent with Step 1.

**[Own reasoning]**, **[Computed]** (C5, C6, C7).

**Step 8 (sufficiency).** Let $0\le p\le4/3$, $n\ge1$, and $Y\in M_2\otimes M_n$ with $Y\ge0$. By Step 7 and linearity:
$$(\Phi_p\otimes\mathrm{id}_n)(Y)=\sum_\mu (K_\mu\otimes I_n)\,Y\,(K_\mu\otimes I_n)^\dagger.$$
To check this identity: both sides are linear in $Y$, and product elements $A\otimes B$ span $M_2\otimes M_n$, so it suffices to check it on them. On $A\otimes B$ the right side is $\bigl(\sum_\mu K_\mu AK_\mu^\dagger\bigr)\otimes B=\Phi_p(A)\otimes B$ by Step 7, which is the left side. (Also checked exactly for a general symbolic $Y\in M_2\otimes M_2$ by the referee: **[Computed]**, `scratch/ref_depolarizing_cp_check.py`, test 3.) Each term $(K\otimes I)Y(K\otimes I)^\dagger$ is PSD: $\langle v|(K\otimes I)Y(K\otimes I)^\dagger|v\rangle=\langle w|Y|w\rangle\ge0$ with $|w\rangle=(K\otimes I)^\dagger|v\rangle$. A sum of PSD matrices is PSD. So $\Phi_p$ is CP. **[Own reasoning]**, **[Computed]** (C9, a random numerical spot check with $n=3$).

**Step 9 (conclusion).** Steps 5 and 8 together give: $\Phi_p$ is CP $\iff 0\le p\le4/3$. Together with Step 1, $\Phi_p$ is a CPTP map (a quantum channel) exactly for $p\in[0,4/3]$. $\blacksquare$

**Cross-check via Choi's theorem.** For $n$-qubit maps, [bu-gu-jaffe-magic, unnumbered statement before Lemma 67, p. 25 (PDF page)] states that the map $\rho\mapsto 2^n\operatorname{Tr}_A[J\,(\rho_A^T\otimes I_{A'})]$ is completely positive iff $J\ge0$. **[Paper]** That paper uses the normalized Choi state $J_\Lambda=(\mathrm{id}_A\otimes\Lambda)(|\Phi\rangle\langle\Phi|)$. For $n=1$ this equals $J(\Phi_p)/2$, and a positive rescaling does not affect $J\ge0$. **[Own reasoning]**, **[Computed]** (`scratch/ref_depolarizing_cp_check.py`, test 1). To apply the criterion we also need $\Phi_p(\rho)=2\operatorname{Tr}_A[J_{\Phi_p}(\rho^T\otimes I)]$. The paper states this reconstruction (its eq. (83)) only for quantum channels, so quoting it for $p\notin[0,4/3]$ would be circular. In fact it holds for every linear map: **[Own reasoning]**, **[Computed]** exactly for symbolic real $p$ and general $\rho$ (same script, test 2). The paper also phrases the criterion for maps on states; extending it to all of $M_2$ by linearity is implicit. The general statement (a linear map $M_d\to M_m$ is CP iff $J(\Phi)\ge0$) is Choi (1975); see also Watrous, *TQI*, Ch. 2. Its hypotheses hold here: finite dimension and a linear map (H1, H2). Combined with Step 3, it gives (b) at once. The argument above does not depend on it.

**Remarks.**
- Boundary cases:
  - $p=0$ is the identity channel; $J$ has rank 1 (eigenvalues $2,0,0,0$).
  - $p=1$ is the completely depolarizing channel; $J=I_4/2$.
  - $p=4/3$ gives $\Phi(X)=\tfrac13\sum_k\sigma_kX\sigma_k$; $J$ has rank 3 (eigenvalues $0,\tfrac23,\tfrac23,\tfrac23$) and $K_0=0$.
- For $1<p\le4/3$ the channel is still CP, even though the "weight" $1-p$ on $X$ is negative.
- Positivity alone (not complete positivity) holds on the larger range $0\le p\le 2$: for a pure state $\Phi_p(|\psi\rangle\langle\psi|)$ has eigenvalues $1-p/2$ (on $|\psi\rangle$) and $p/2$ (on $|\psi\rangle^\perp$), and every PSD matrix is a nonnegative combination of pure states. So for $4/3<p\le2$ the map $\Phi_p$ is positive but not CP. **[Own reasoning, not needed for the claim]**, **[Computed]** (C12: the Bloch-vector scaling $r\mapsto(1-p)r$ checked exactly; exact counterexamples at $p=-1/100$ and $p=201/100$).

## Claims to compute
All matrices are $2\times2$ or $4\times4$ over $\mathbb C$, with the basis order $|00\rangle,|01\rangle,|10\rangle,|11\rangle$ (first factor most significant). Notation:
- $\Phi_p(X)=(1-p)X+p\operatorname{Tr}(X)I_2/2$;
- $J_p=\sum_{i,j}E_{ij}\otimes\Phi_p(E_{ij})$;
- $|\Omega\rangle=(|00\rangle+|11\rangle)/\sqrt2$.

The reference script is `scratch/depolarizing_cp.py` (SymPy, symbolic real $p$, plus a NumPy random test). All C1–C9 passed there.

- **C1.** For symbolic real $p$: $J_p=2(1-p)|\Omega\rangle\langle\Omega|+\tfrac p2I_4$ (exact matrix equality).
- **C2.** For symbolic $p$: the eigenvalues of $J_p$ are $2-3p/2$ (multiplicity 1, eigenvector $|\Omega\rangle$) and $p/2$ (multiplicity 3).
- **C3.** For arbitrary symbolic $X=\begin{pmatrix}x_0&x_1\\x_2&x_3\end{pmatrix}$ and symbolic $p$: $\operatorname{Tr}\Phi_p(X)-\operatorname{Tr}X=0$.
- **C4.** For arbitrary symbolic $X\in M_2$: $\sum_{\mu=0}^3\sigma_\mu X\sigma_\mu=2\operatorname{Tr}(X)I_2$.
- **C5.** With $K_0=\sqrt{1-3p/4}\,I$ and $K_k=\sqrt{p/4}\,\sigma_k$: $\sum_\mu K_\mu XK_\mu^\dagger=\Phi_p(X)$ for symbolic $X$, at $p\in\{0,1/7,1/2,1,4/3\}$ (or symbolic $p\in[0,4/3]$, taking care that the square roots are real).
- **C6.** Same $K_\mu$ and same $p$ values: $\sum_\mu K_\mu^\dagger K_\mu=I_2$.
- **C7.** `qmath.choi([K_0..K_3])` equals $J_p$, at $p=1/2$ (and at the other values in C5).
- **C8.** $\sum_{i,j}\Phi_p(E_{ij})\otimes E_{ij}=J_p$ for symbolic $p$ (the $\Phi\otimes\mathrm{id}$ convention gives the same matrix).
- **C9.** Numerical check: for $p\in\{0,0.3,1,4/3\}$ and 500 random density matrices $\rho$ on $\mathbb C^2\otimes\mathbb C^3$, $\lambda_{\min}\bigl((\Phi_p\otimes\mathrm{id}_3)(\rho)\bigr)\ge-10^{-12}$.
- **C10 (boundary, exact rationals).** The spectra of $J_p$:
  - $p=0$: $\{2,0,0,0\}$;
  - $p=4/3$: $\{0,2/3,2/3,2/3\}$;
  - $p=1$: $\{1/2\times4\}$;
  - $p=1/2$: $\{5/4,1/4,1/4,1/4\}$.
- **C11 (just outside the range).**
  - $p=4/3+1/1000$: $J_p$ has eigenvalue $-3/2000<0$ (on $|\Omega\rangle$); equivalently $\langle\Omega|J_p|\Omega\rangle<0$.
  - $p=-1/1000$: $J_p$ has eigenvalue $-1/2000<0$ (multiplicity 3); equivalently $\langle01|J_p|01\rangle=-1/2000$.

  So $(\Phi_p\otimes\mathrm{id}_2)(2|\Omega\rangle\langle\Omega|)$ is not PSD in either case.

## Computational checks
Independent scripts by the `quantum-computer` agent: `scratch/q_depolarizing-cp_*.py` (shared definitions in `scratch/q_depolarizing-cp_common.py`; the prover's own script `scratch/depolarizing_cp.py` was not reused).

| ID | Claim | Method | Verdict |
|---|---|---|---|
| C0 | PSD range of $J_p$ (i); main statement on a grid (ii) | (i) exact `solveset` on the eigenvalues of $J_p$, plus factored characteristic polynomial; (ii) 256 $p$ values: $[-0.5,2]$ in steps of $0.01$, plus probes at $4/3$, $4/3\pm10^{-3}$, $\pm10^{-3}$, applying $\Phi_p\otimes\mathrm{id}_n$ ($n=2,3$) directly | (i) Proved symbolically that $J_p\ge0\iff p\in[0,4/3]$; (ii) Supported: negative eigenvalues appear at exactly the grid points outside $[0,4/3]$ (innermost ones $-0.001$ and $1.33433$) |
| C1 | Closed form of $J_p$ | exact | Proved symbolically |
| C2 | Spectrum of $J_p$ | exact eigenvalues and eigenvectors | Proved symbolically |
| C3 | Trace preservation | exact, general $X$ | Proved symbolically |
| C4 | Pauli twirl identity | exact | Proved symbolically |
| C5, C6 | Kraus form and $\sum K^\dagger K=I$ | exact, two parametrizations covering $[0,4/3]$, plus 5 rational values | Proved symbolically (a third, $t$-parametrization in the script is inconclusive because SymPy can't use $t\le1$; not relied on) |
| C7 | `qmath.choi` $=J_p$ | exact at $p\in\{0,1/7,1/2,1,4/3\}$ | Exact at 5 rational points |
| C8 | Swapped-factor convention | exact | Proved symbolically |
| C9 | $\Phi_p\otimes\mathrm{id}_3$ preserves PSD | 500 random $\rho$ per $p$, ranks 1/2/3/6; worst $\lambda_{\min}\approx-4\times10^{-16}$ | Supported (numerical, not a proof) |
| C10 | Boundary spectra | exact rationals | Proved symbolically |
| C11 | Witnesses just outside the range | exact rationals | Proved symbolically |
| C12 | Positive iff $0\le p\le2$ | exact Bloch scaling, `solveset`, exact witnesses | Proved symbolically (the step from states to all PSD matrices is own reasoning) |

Scope: everything is for $M_2$. The CP check for general $n$ rests on the Kraus argument in Step 8, which is exact via C5/C6. C0(ii) and C9 are numerical evidence only.

## Open doubts
- None on the main mathematics: every step is elementary, every concrete identity except the numerical checks C0(ii) and C9 was proved symbolically, and the referee found no errors.
- The cross-check citation is to an unnumbered statement in [bu-gu-jaffe-magic, p. 25]. That paper states it for its own normalized Choi state; the $n=1$ rescaling is own reasoning.
- Referee (`proof-checker`): **Correct, with minor gaps**. All three gaps are now closed: the Step 8 spanning argument, the circularity of eq. (83) in the cross-check, and the table wording. The note states that C0(i) gives the PSD range of $J_p$; getting from there to CP uses Steps 5/8 (or Choi).
