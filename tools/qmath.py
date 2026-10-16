"""Helpers for quantum-math computations (finite-dimensional Hilbert spaces).

Exact work uses SymPy matrices; randomized numeric checks use NumPy.
Import from a scratch script with:

    import os, sys  # from a script in scratch/; never hardcode absolute paths
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
    from qmath import *

Conventions: kets are column vectors, |0> = (1,0)^T, tensor order is left-to-right
(kron(A, B) acts as A on the first subsystem), partial_trace keeps the listed subsystems.
"""
from __future__ import annotations

import numpy as np
import sympy as sp

# ---------------------------------------------------------------- exact (SymPy)

I2 = sp.eye(2)
X = sp.Matrix([[0, 1], [1, 0]])
Y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
Z = sp.Matrix([[1, 0], [0, -1]])
H = sp.Matrix([[1, 1], [1, -1]]) / sp.sqrt(2)
S = sp.Matrix([[1, 0], [0, sp.I]])
T = sp.Matrix([[1, 0], [0, sp.exp(sp.I * sp.pi / 4)]])
CNOT = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]])
PAULIS = {"I": I2, "X": X, "Y": Y, "Z": Z}


def ket(bits: str, d: int = 2) -> sp.Matrix:
    """Computational-basis ket, e.g. ket('01') = |0>|1>; digits must be < d."""
    v = sp.Matrix([1])
    for b in bits:
        e = sp.zeros(d, 1)
        e[int(b)] = 1
        v = kron(v, e)
    return v


def bra(bits: str, d: int = 2) -> sp.Matrix:
    return dag(ket(bits, d))


def dag(A: sp.Matrix) -> sp.Matrix:
    return A.conjugate().T


def kron(*ms: sp.Matrix) -> sp.Matrix:
    out = ms[0]
    for m in ms[1:]:
        out = sp.kronecker_product(out, m)
    return out


def comm(A, B):
    return A * B - B * A


def acomm(A, B):
    return A * B + B * A


def proj(v: sp.Matrix) -> sp.Matrix:
    """|v><v| (v need not be normalized; not normalized here)."""
    return v * dag(v)


def is_zero(M: sp.Matrix) -> bool:
    """Exact check that every entry simplifies to 0."""
    return all(sp.simplify(e) == 0 for e in M)


def is_hermitian(A) -> bool:
    return is_zero(A - dag(A))


def is_unitary(U) -> bool:
    return is_zero(dag(U) * U - sp.eye(U.shape[0]))


def partial_trace(rho: sp.Matrix, dims: list[int], keep: list[int]) -> sp.Matrix:
    """Trace out every subsystem not in `keep` (0-indexed). Exact."""
    n = len(dims)
    keep = sorted(keep)
    traced = [i for i in range(n) if i not in keep]
    dk = int(np.prod([dims[i] for i in keep])) if keep else 1
    out = sp.zeros(dk, dk)
    for r in range(rho.shape[0]):
        ri = np.unravel_index(r, dims)
        for c in range(rho.shape[1]):
            ci = np.unravel_index(c, dims)
            if any(ri[t] != ci[t] for t in traced):
                continue
            rk = np.ravel_multi_index([ri[k] for k in keep], [dims[k] for k in keep]) if keep else 0
            ck = np.ravel_multi_index([ci[k] for k in keep], [dims[k] for k in keep]) if keep else 0
            out[int(rk), int(ck)] += rho[r, c]
    return out


def is_density(rho, numeric_tol: float = 1e-10) -> bool:
    """Hermitian, trace 1, positive semidefinite (PSD tested on numeric eigenvalues)."""
    if not is_hermitian(rho) or sp.simplify(rho.trace() - 1) != 0:
        return False
    ev = np.linalg.eigvalsh(np.array(rho.evalf(), dtype=complex))
    return bool(ev.min() >= -numeric_tol)


def kraus_complete(kraus: list[sp.Matrix]) -> bool:
    """Trace preservation: sum_k K_k^dagger K_k = I."""
    d = kraus[0].shape[1]
    return is_zero(sum((dag(K) * K for K in kraus), sp.zeros(d, d)) - sp.eye(d))


def apply_channel(kraus, rho):
    return sum((K * rho * dag(K) for K in kraus), sp.zeros(kraus[0].shape[0], kraus[0].shape[0]))


def choi(kraus: list[sp.Matrix]) -> sp.Matrix:
    """Choi matrix J = sum_ij |i><j| (x) Phi(|i><j|) (unnormalized). CP iff J >= 0."""
    d = kraus[0].shape[1]
    J = None
    for i in range(d):
        for j in range(d):
            Eij = sp.zeros(d, d)
            Eij[i, j] = 1
            term = kron(Eij, apply_channel(kraus, Eij))
            J = term if J is None else J + term
    return J


def to_latex(expr) -> str:
    """SymPy -> LaTeX, using pmatrix for matrices."""
    return sp.latex(expr, mat_delim="(", mat_str="matrix")


# ---------------------------------------------------------------- numeric (NumPy)

rng = np.random.default_rng(0)


def N(M) -> np.ndarray:
    """SymPy matrix -> complex NumPy array."""
    return np.array(sp.Matrix(M).evalf(), dtype=complex)


def rand_unitary(d: int) -> np.ndarray:
    """Haar-random unitary (QR of a Ginibre matrix with phase fix)."""
    z = (rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    return q * (np.diag(r) / np.abs(np.diag(r)))


def rand_hermitian(d: int) -> np.ndarray:
    a = rng.standard_normal((d, d)) + 1j * rng.standard_normal((d, d))
    return (a + a.conj().T) / 2


def rand_state(d: int) -> np.ndarray:
    v = rng.standard_normal(d) + 1j * rng.standard_normal(d)
    return v / np.linalg.norm(v)


def rand_density(d: int, rank: int | None = None) -> np.ndarray:
    g = rng.standard_normal((d, rank or d)) + 1j * rng.standard_normal((d, rank or d))
    rho = g @ g.conj().T
    return rho / np.trace(rho)


def sqrtm_psd(A: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eigh((A + A.conj().T) / 2)
    return (v * np.sqrt(np.clip(w, 0, None))) @ v.conj().T


def fidelity(rho: np.ndarray, sigma: np.ndarray) -> float:
    """Uhlmann fidelity F = (tr sqrt(sqrt(rho) sigma sqrt(rho)))^2 (squared convention)."""
    s = sqrtm_psd(rho)
    return float(np.real(np.trace(sqrtm_psd(s @ sigma @ s))) ** 2)


def trace_distance(rho, sigma) -> float:
    return float(0.5 * np.abs(np.linalg.eigvalsh(rho - sigma)).sum())


def vn_entropy(rho: np.ndarray, base: float = 2) -> float:
    w = np.linalg.eigvalsh(rho)
    w = w[w > 1e-14]
    return float(-(w * np.log(w)).sum() / np.log(base))


def partial_trace_np(rho: np.ndarray, dims: list[int], keep: list[int]) -> np.ndarray:
    n = len(dims)
    t = rho.reshape(dims + dims)
    for i in sorted((i for i in range(n) if i not in keep), reverse=True):
        t = np.trace(t, axis1=i, axis2=i + t.ndim // 2)
    dk = int(np.prod([dims[k] for k in keep])) if keep else 1
    return t.reshape(dk, dk)


def random_test(check, samplers: dict, trials: int = 200, tol: float = 1e-9):
    """Run `check(**sample) -> float residual` on random inputs.

    Returns (passed: bool, worst_residual, worst_sample). Supports a claim; never a proof.
    Example: random_test(lambda A, B: np.linalg.norm(...), {"A": lambda: rand_hermitian(3), ...})
    """
    worst, worst_s = 0.0, None
    for _ in range(trials):
        s = {k: f() for k, f in samplers.items()}
        r = float(check(**s))
        if r > worst:
            worst, worst_s = r, s
    return worst <= tol, worst, worst_s


if __name__ == "__main__":
    # Self-test of the library against standard facts.
    assert is_zero(comm(X, Y) - 2 * sp.I * Z)
    assert is_zero(acomm(X, Y))
    assert all(is_unitary(U) for U in (H, S, T, CNOT))
    bell = (ket("00") + ket("11")) / sp.sqrt(2)
    rhoA = partial_trace(proj(bell), [2, 2], [0])
    assert is_zero(rhoA - I2 / 2) and is_density(proj(bell))
    p = sp.Rational(1, 3)
    dep = [sp.sqrt(1 - 3 * p / 4) * I2] + [sp.sqrt(p / 4) * P for P in (X, Y, Z)]
    assert kraus_complete(dep)
    assert min(np.linalg.eigvalsh(N(choi(dep)))) > -1e-12
    r1, r2 = rand_density(4), rand_density(4)
    assert np.allclose(partial_trace_np(r1, [2, 2], [0]), N(partial_trace(sp.Matrix(r1), [2, 2], [0])))
    assert abs(fidelity(r1, r1) - 1) < 1e-8 and 0 <= trace_distance(r1, r2) <= 1
    ok, worst, _ = random_test(
        lambda U, rho: abs(vn_entropy(U @ rho @ U.conj().T) - vn_entropy(rho)),
        {"U": lambda: rand_unitary(3), "rho": lambda: rand_density(3)},
    )
    assert ok, worst
    print("qmath self-test passed")
