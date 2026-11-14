# 3-round AES integral evidence and 4-round attack

## What I will implement and why

1) A small, self-contained AES-128 implementation in Python (S-box, key schedule, and round functions). This is needed to generate concrete outputs for 3 and 4 rounds without external libraries.

2) A computational check of the monomial property for 3 full rounds. We vary the 8 input bits of the first S-box (the first byte of the plaintext) through all 256 values, keep the other 120 input bits fixed, and XOR all 128 output bits. If the coefficient of the monomial $x_0 x_1 \dots x_7$ is zero for every output bit, this XOR must be the all-zero vector.

3) A 4-round integral key recovery (square) attack. We use the 3-round balance property and partially invert the last round to recover all 16 bytes of the last-round key. This is the classic way to turn an integral distinguisher into a key recovery.

## Mathematical reasoning

### Monomial coefficient and the integral sum

Let $f(x_0,\dots,x_7, y)$ be any output bit of 3-round AES, where $x_0,\dots,x_7$ are the 8 bits of the first S-box input (the first plaintext byte), and $y$ denotes all other input bits (fixed during the experiment).

Over $\mathbb{F}_2$, the ANF coefficient of the monomial $x_0 x_1 \dots x_7$ equals the XOR of $f$ over the full 8-bit cube:

$$
\text{coef}(x_0\dots x_7) = \bigoplus_{x\in\{0,1\}^8} f(x, y).
$$

Therefore, to show that the monomial $x_0\dots x_7$ does not appear in any output bit, it is enough to show that the XOR of each output bit over all 256 choices of the first plaintext byte is zero (for any fixed values of the other 120 bits). This is exactly the integral (balanced) property.

### Why the property is key-independent

Round keys only add (XOR) into the state. Since XOR is linear, it cannot create a new monomial term that depends on $x_0,\dots,x_7$. Thus, if the coefficient of $x_0\dots x_7$ is zero for one key, it is zero for all keys. The computational evidence tests several random keys and several random fixed inputs.

### Degree question

The absence of the specific monomial $x_0\dots x_7$ does NOT imply that the algebraic degree of 3-round AES is at most 8. It only tells us that one particular monomial coefficient is zero. The degree can still be much higher because it can involve other variables.

For AES, one round has degree 7 (the S-box has degree 7 and the rest is linear). After 3 full rounds, the algebraic degree is upper-bounded by $\min(7^3, 128)=128$, which is much larger than 8. So the degree bound 8 is not implied by the property.

## How the 4-round integral attack works

1) Build a set of 256 plaintexts where only the first byte varies (0..255) and the other 15 bytes are fixed.
2) Encrypt these plaintexts with 4-round AES (3 full rounds, then a final round without MixColumns, as in standard AES).
3) For each byte position $i$, guess the last-round key byte $k_i$.
4) For each ciphertext, compute $\text{InvSBox}(c_i \oplus k_i)$ and XOR the results over all 256 ciphertexts.
5) For the correct $k_i$, this XOR equals 0 because it equals the XOR of the corresponding state byte after 3 full rounds, which is balanced.
6) Wrong guesses behave like random and (with overwhelming probability) do not give zero. If multiple candidates appear for any byte, repeat with another plaintext set and intersect candidate sets.

## How to run

Run the script:

```
python aes_integral.py
```

It prints:
- Whether the 3-round XOR over the 256-byte cube is all zero across multiple random keys and fixed inputs.
- The recovered last-round key (all 16 bytes) for a 4-round AES instance, and the true last-round key for verification.
