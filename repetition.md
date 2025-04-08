The **repetition penalty** is a mechanism used in text generation models (like GPT) to discourage the model from repeating the same tokens, phrases, or patterns too often. It works by modifying the logits (scores) of tokens before applying the softmax function during decoding, penalizing tokens that have already been generated.

---

### **Mathematical Explanation**
The repetition penalty modifies the logits for each token $z_i $ as follows:
$$
z'_i = z_i / r
$$
Here:
- $z_i $: Original logit score for token $i $.
- $r $: Penalty factor applied to repeated tokens ($r > 1 $).

Tokens that have been repeated in the output receive a lower effective logit score ($z'_i $), reducing their probability when passed through softmax.

---

### **Example with Matrix**
Let’s break this down step by step:

#### **Step 1: Initial Logits**
Consider the following logits matrix where each row represents the scores for 4 tokens ($t_1, t_2, t_3, t_4 $) at different decoding steps.

$$
Z = \begin{pmatrix} 
2.0 & 1.0 & 0.5 & 0.1 \\ 
1.8 & 1.2 & 0.4 & 0.2 \\ 
1.5 & 1.0 & 0.3 & 0.1 \\ 
1.2 & 0.8 & 0.2 & 0.05 
\end{pmatrix}
$$

#### **Step 2: Penalize Repeated Tokens**
Suppose token $t_1 $ has already been generated. Apply a repetition penalty ($r = 2 $) to $t_1 $’s logits in subsequent rows.

Update the matrix $Z $ as follows:
$$
Z' = \begin{pmatrix} 
2.0 & 1.0 & 0.5 & 0.1 \\ 
0.9 & 1.2 & 0.4 & 0.2 \\ 
0.75 & 1.0 & 0.3 & 0.1 \\ 
0.6 & 0.8 & 0.2 & 0.05 
\end{pmatrix}
$$

- The logits for $t_1 $ are divided by $r = 2 $ after the first step.

#### **Step 3: Compute Softmax Probabilities**
Apply the softmax function to the updated logits $Z' $ row by row:
$$
P(y_i) = \frac{e^{z'_i}}{\sum_{j} e^{z'_j}}
$$

Example (second row):
Original logits: $[0.9, 1.2, 0.4, 0.2] $:
$$
P = \left[ \frac{e^{0.9}}{e^{0.9} + e^{1.2} + e^{0.4} + e^{0.2}}, \frac{e^{1.2}}{e^{0.9} + e^{1.2} + e^{0.4} + e^{0.2}}, \frac{e^{0.4}}{e^{0.9} + e^{1.2} + e^{0.4} + e^{0.2}}, \frac{e^{0.2}}{e^{0.9} + e^{1.2} + e^{0.4} + e^{0.2}} \right]
$$
This generates probabilities that discourage $t_1 $ due to the repetition penalty.

---

### **Key Takeaways**
1. **Penalty Factor**:
   - Higher $r $: Stronger discouragement of repeated tokens.
   - Lower $r $: Mild discouragement of repeated tokens.

2. **Applications**:
   - Reduces verbatim repetition (e.g., "I like pizza pizza pizza").
   - Encourages diverse and coherent text generation.

3. **Example Use in Code**:
The repetition penalty is implemented in frameworks like Hugging Face's `transformers` library, where token logits are adjusted dynamically during decoding.

Let me know if you'd like to explore code for this! 🚀