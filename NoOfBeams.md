Let me clarify the calculation of $ M_2 $ step by step with more detail so it's easier to understand.

### **What is $ M_2 $?**
The matrix $ M_2 $ represents the scores when we expand the beams (sequences) from the first step into the next step by considering possible new tokens.

---

### **Input for Calculation of $ M_2 $**
1. **Initial Beam Scores** ($ M_1 $):
   This is the starting matrix of probabilities for the first set of beams:
   $$
   M_1 = \begin{pmatrix} 0.6 & 0.3 & 0.1 \\ 0.5 & 0.4 & 0.1 \\ 0.2 & 0.7 & 0.1 \end{pmatrix}
   $$
   Here:
   - Each **row** corresponds to one beam.
   - Each **column** represents a token's probability for that beam.

2. **Expansion with New Tokens**:
   At the next step, the model outputs probabilities for possible **next tokens** for each beam. Assume there are 3 possible tokens, with probabilities computed (or predicted) for each beam.

---

### **How $ M_2 $ Is Computed**
To compute $ M_2 $, you multiply or combine the scores of the current beam (from $ M_1 $) with the predicted probabilities for possible next tokens. This can be thought of as expanding each beam into multiple new beams.

---

#### Example:
Assume the model generates probabilities for the **next tokens** as:
$$
\text{Next Token Probabilities (example)} = \begin{pmatrix} 
0.3 & 0.4 & 0.3 \\
0.5 & 0.2 & 0.3 \\
0.2 & 0.3 & 0.5
\end{pmatrix}
$$
- Each row corresponds to probabilities for new tokens for a specific beam.

Now, multiply each score in $ M_1 $ with these probabilities to compute $ M_2 $. For each row in $ M_1 $, expand it into 3 rows by combining with the above probabilities.

---

#### Calculation:
For $ M_1 $, row-by-row:

**Row 1 (from $ M_1 $):**
$$ [0.6, 0.3, 0.1] \quad \text{(beam scores for tokens 1, 2, 3)} $$
Multiply each score with the new token probabilities row-wise:
- For token 1: $ 0.6 \times [0.3, 0.4, 0.3] $
- For token 2: $ 0.3 \times [0.5, 0.2, 0.3] $
- For token 3: $ 0.1 \times [0.2, 0.3, 0.5] $

Combine these into a new expanded matrix.

---

Repeat this for **Row 2** and **Row 3** of $ M_1 $. Once all calculations are done, the final $ M_2 $ matrix contains the expanded scores for all beams and possible next tokens.

---

### **Key Point**
The multiplication ensures that the scores from $ M_1 $ are "distributed" into probabilities for the next tokens, which is why the size of $ M_2 $ grows. Let me know if you'd like me to work through any specific numbers explicitly!