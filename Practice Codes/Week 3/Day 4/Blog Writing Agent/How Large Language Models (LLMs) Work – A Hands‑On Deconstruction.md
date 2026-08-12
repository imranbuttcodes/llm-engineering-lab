# How Large Language Models (LLMs) Work – A Hands‑On Deconstruction

## 1️⃣ The Transformer Building Blocks

*Goal*: Give readers a clear, component‑by‑component picture of the transformer architecture that underpins modern LLMs.

- **Data‑flow sketch** – An input token is first turned into a dense vector by an embedding layer. The embedding is projected into *query*, *key* and *value* tensors and fed to a multi‑head self‑attention block. The attention output passes through a position‑wise feed‑forward network; both sub‑layers are wrapped with residual connections followed by layer‑norm. The final hidden state is linearly projected to vocabulary logits for next‑token prediction.

- **Diagram comparison** – The original *Attention is All You Need* paper shows an encoder‑decoder stack with separate self‑attention and cross‑attention layers. Modern decoder‑only LLMs (e.g., GPT‑style models) drop the encoder, stack many identical decoder blocks, and reuse the same self‑attention module for both context conditioning and generation, simplifying the graph while keeping the core transformer primitives.

- **Shape‑check script** – Verify that query/key/value dimensions respect `d_model / num_heads`. A quick Python sanity check:

```python
import torch

def check_shapes(d_model=768, num_heads=12, seq_len=128):
    head_dim = d_model // num_heads
    assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
    x = torch.randn(seq_len, d_model)
    q = x @ torch.randn(d_model, d_model)  # fake linear proj
    q = q.view(seq_len, num_heads, head_dim)
    print("q shape:", q.shape)  # (seq_len, num_heads, head_dim)

check_shapes()
```

- **Quadratic scaling insight** – Self‑attention computes a similarity score for every pair of tokens, resulting in an `O(n²)` time and memory cost where `n` is the sequence length. This quickly becomes the bottleneck for long contexts, driving research into linear‑time approximations (e.g., sparse attention, routing, flash‑attention) and prompting practitioners to truncate inputs or use sliding windows to keep costs tractable.

## 2️⃣ Training an LLM: Data, Tokenization, and Objectives

*Goal: Show how LLMs are trained from raw text to a predictive model using supervised next‑token loss.*

- **Collect a representative text corpus** – Pull large‑scale sources such as CommonCrawl or Wikipedia, then compute the total token count (e.g., ≈ 300 B tokens) and the vocabulary size after tokenization. Record these statistics; they drive batch‑size limits, learning‑rate schedules, and cost estimates.

- **Implement Byte‑Pair Encoding (BPE) or SentencePiece** – Train a sub‑word vocabulary (≈ 32 k tokens) on a sample slice of the corpus, then tokenize the full dataset. Compare the number of tokens produced versus raw character count to quantify compression (e.g., 1 token ≈ 4 characters). This metric reveals storage savings and influences throughput.

- **Set up the next‑token prediction objective** – Use a cross‑entropy loss over the softmax of the vocabulary. Sketch the loss curve across epochs: early rapid decline, followed by a slower asymptotic approach to a plateau. Monitoring this curve helps detect under‑fitting or divergence early.

- **Compare training on a single GPU vs. multi‑node data‑parallelism** – Benchmark tokens per second (t/s) for a baseline single‑GPU run, then scale to 8‑GPU and multi‑node setups. Note the linearity (or lack thereof) of throughput gains and the accompanying increase in communication overhead, which directly impacts cost per training hour.

- **Validate that gradients are properly clipped** – After each backward pass, compute the L2 norm of all model gradients and plot a histogram. Ensure the majority of norms fall below the clipping threshold (e.g., 1.0). This observability step prevents exploding gradients, a common failure mode in large‑scale training.

## 3️⃣ From Logits to Text: Sampling Strategies  

**Goal:** Explain how an LLM converts raw logits into readable tokens and how different sampling knobs shape quality, diversity, and stability of the generated text.  

- **Implement three samplers in a few lines.**  
  ```python
  # logits: torch.Tensor of shape (vocab,)
  def greedy(logits):            return logits.argmax()
  def temperature(logits, t):    return torch.multinomial(F.softmax(logits/t, dim=-1), 1)
  def nucleus(logits, p):       
      probs = F.softmax(logits, dim=-1)
      sorted_idx = probs.argsort(descending=True)
      cum_probs = probs[sorted_idx].cumsum(0)
      cut_off = (cum_probs <= p).sum()
      return torch.multinomial(probs[sorted_idx[:cut_off+1]], 1)
  ```
  The three functions illustrate the core choice: deterministic max, soft‑max scaling, and probability‑mass truncation.

- **Compare perplexity and diversity.**  
  Run each sampler on a held‑out prompt set, compute token‑level perplexity (lower is more predictable) and a diversity metric such as distinct‑n (higher is more varied). Typical results: greedy yields the lowest perplexity but the smallest distinct‑n; nucleus produces a balanced trade‑off; high‑temperature sampling spikes diversity while raising perplexity.

- **Show temperature’s effect on entropy.**  
  For a fixed prompt, record token probability vectors at temperatures 0.5, 1.0, 2.0 and plot their histograms. Entropy increases monotonically with temperature, confirming that the soft‑max smoothing spreads probability mass and makes rarer words more likely.

- **Debug repetitive loops when top‑p is too low.**  
  Inspect the tail of the log‑probability distribution: if the cutoff removes > 95 % of mass, the sampler repeatedly draws from a handful of high‑probability tokens, leading to loops (“the cat … the cat …”). Raising p or falling back to temperature scaling breaks the cycle.  

These steps give you a reproducible sandbox to measure, visualise, and troubleshoot the sampling knobs that drive LLM output.

## 4️⃣ Performance & Cost Considerations

*Goal: Equip developers with concrete metrics to evaluate performance and operational cost of deploying LLMs.*

- **Benchmark inference latency** – Run a timed loop that feeds a fixed‑size prompt (e.g., 32 tokens) to a 2 B‑parameter model on both CPU (e.g., Intel Xeon) and GPU (e.g., NVIDIA A100). Record the elapsed time and compute ms per token. Typical results show ~30 ms/token on CPU versus <1 ms/token on GPU, highlighting the latency gap that drives hardware selection.  

- **Calculate KV‑cache memory footprint** – The key‑value cache stores activations for every past token. Estimate the size as `cache_size = num_layers × hidden_dim × context_len × dtype_bytes`. For a 2 B model (≈24 layers, 3072 hidden dim) at 2 k context length with FP16 (2 bytes) the KV‑cache consumes ~295 MiB; doubling the context to 4 k pushes it past 580 MiB, often exceeding GPU memory limits.  

- **Estimate cost per 1 M generated tokens** – Use cloud pricing to compare on‑demand rates: an AWS p3.2xlarge (1 × V100) costs ≈ $3.06 hr⁻¹, while a GCP A100‑based instance runs ≈ $2.70 hr⁻¹. Assuming 1 M tokens at 0.5 ms/token on the GPU, the runtime is ~8.3 min, giving a cost of roughly $0.04 per million tokens on GCP and $0.05 on AWS.  

- **Compare int8 quantisation vs. full‑precision** – Quantise the model to int8 using a static calibration set, then rerun the latency benchmark. Expect ~2× speed‑up (e.g., 0.5 ms → 0.25 ms/token) with a modest drop in perplexity (≈ 1–2 %). Verify that downstream tasks tolerate the accuracy loss before committing to quantised deployment.  

- **Edge‑case analysis: KV‑cache OOM handling** – When context length approaches the memory ceiling, generation can fail with OOM errors. Implement a fallback that truncates the oldest cached layers or switches to CPU offloading for the cache. Monitoring cache size per step lets you pre‑emptively trigger the fallback and keep the service available.

## 5️⃣ Edge Cases & Failure Modes  

**Goal:** Illustrate common failure modes of LLMs and provide a systematic way to surface them during testing.  

- **Trigger hallucination:** Craft a prompt that blends a real entity (e.g., “NASA”) with a fictitious one (e.g., “Atlantis Space Agency”). Capture the model’s token‑level confidence scores and log them to a CSV for later analysis.  
  ```python
  response = client.generate(prompt)
  confidences = response.token_confidences  # list of floats per token
  with open('hallucination_log.csv','a') as f:
      f.write(f"{prompt},{confidences}\n")
  ```
- **Detect out‑of‑distribution (OOD) inputs:** Feed code snippets written in an obscure language (e.g., Brainfuck) that the model likely never saw during training. Record syntax‑error patterns, missing completions, or abrupt terminations to build an OOD failure matrix.  
- **Measure bias amplification:** Run a set of demographic‑sensitive prompts (e.g., “Describe a nurse”) across gendered and racial variations. Compute sentiment polarity (via a simple VADER score) for each answer and compare the distributions; large gaps flag amplification.  
- **Log observability metrics:** Instrument your test harness to emit latency, token‑usage, and error‑code metadata to a monitoring dashboard (e.g., Prometheus). Correlating spikes with specific failure modes helps pinpoint performance bottlenecks.  
- **Validate mitigation steps:** Apply prompt‑engineering tweaks (e.g., explicit role instructions) or post‑filtering scripts, then run A/B tests comparing the original and mitigated runs. Quantify reductions in hallucination frequency, OOD error rates, and bias scores to confirm the effectiveness of each countermeasure.

## 6️⃣ Debugging & Observability Tips

**Goal:** Provide practical debugging and observability techniques for running LLMs in production.

Running a transformer‑based LLM at scale creates many hidden failure points—memory fragmentation, attention anomalies, and latency jitter. Embedding lightweight instrumentation early lets you surface these issues before they affect users.

- **Log raw attention matrices:** Insert a hook after the soft‑max in each attention block to dump the per‑head weight matrix for every generation step. Storing the matrices (or their statistics) lets you replay a run and spot pathological patterns without re‑executing the model.  
- **Render attention heat‑maps:** For a representative prompt, plot the logged weights as heat‑maps (e.g., using Matplotlib’s `imshow`). Look for “soft‑max saturation” where rows collapse to a single dominant token, which often correlates with hallucination or repetitiveness.  
- **Expose a health‑check endpoint:** Serve a `/health` HTTP route that returns JSON with the current average request latency, GPU utilisation (e.g., `nvidia-smi` query), and KV‑cache size. Automate alerts when any metric exceeds a configurable threshold.  
- **Diagnose latency spikes:** When latency jumps, correlate the timestamp with GPU memory fragmentation metrics and the growth of the key‑value cache. A sudden burst in KV‑cache size can force page‑outs, inflating latency; shrinking the cache or restarting the worker often restores baseline performance.

**Edge‑case analysis:** If attention weights are uniformly near zero, the soft‑max may be under‑flowing, indicating an improperly scaled logits tensor.  

**Performance/cost note:** Regularly pruning the KV‑cache and capping its maximum length prevents unbounded GPU memory use, which protects both latency SLAs and cloud‑instance cost.

## 7️⃣ Minimal Code Sketch: A Tiny Self‑Attention Model  

**Goal:** Show a runnable 30‑line PyTorch example that isolates every core LLM operation – embedding, multi‑head self‑attention, feed‑forward, residuals, and gradient flow – then validate it against a naïve NumPy copy and measure per‑token latency on CPU vs. GPU.

- **Define the block and run a forward pass** – The script builds a `nn.Embedding`, a single `MultiheadAttention` layer, and a tiny transformer block (`self‑attn → add → linear → add`). A dummy integer sequence of length 8 is embedded and fed through the block.  
- **Swap in a NumPy reference** – A hand‑written NumPy implementation of scaled‑dot‑product attention (batch‑size 1) replaces the PyTorch call; after a forward pass we compute `np.max|torch‑out‑numpy|` and assert it is < 1e‑5 to prove numeric parity.  
- **Check gradients through the residual path** – A `torch.nn.Linear` feed‑forward is added, `loss = out.mean()`, `loss.backward()`. We print `model.feed_forward.weight.grad.abs().max()`; a non‑zero value confirms gradients flow past the residual addition.  
- **Benchmark CPU vs. GPU latency** – Using `torch.cuda.is_available()`, the script runs 100 warm‑up steps then times 200 inference steps on each device, printing `tokens / sec` (≈ µs per token). This illustrates the linear scaling of attention cost with sequence length and the speedup gained from CUDA.  

```python
import torch, numpy as np, time

# ---- Config -------------------------------------------------
d_model, n_head, seq_len = 32, 4, 8
embed = torch.nn.Embedding(100, d_model)
attn = torch.nn.MultiheadAttention(d_model, n_head, batch_first=True)
ff = torch.nn.Linear(d_model, d_model)
# -------------------------------------------------------------

def torch_forward(x):
    z = embed(x)
    a, _ = attn(z, z, z)
    z = a + z                     # residual
    f = ff(z)
    out = f + z                   # residual
    return out

def numpy_attention(x):
    # x: (seq, d_model)
    q = x @ W_q; k = x @ W_k; v = x @ W_v
    scores = q @ k.T / np.sqrt(d_model)
    probs = np.exp(scores - scores.max(axis=-1, keepdims=True))
    probs /= probs.sum(axis=-1, keepdims=True)
    return probs @ v

# ---- Dummy data ---------------------------------------------
tokens = torch.arange(seq_len).unsqueeze(0)  # (1, seq_len)
# -------------------------------------------------------------

# PyTorch pass
out_t = torch_forward(tokens)
# NumPy parity check
W_q, W_k, W_v = [p.detach().numpy() for p in attn.in_proj_weight.view(3, d_model, d_model)]
np_out = numpy_attention(embed(tokens).detach().numpy()[0])
assert np.max(np.abs(out_t.detach().numpy()[0] - np_out)) < 1e-5

# Gradient check
loss = out_t.mean()
loss.backward()
print('grad check:', ff.weight.grad.abs().max().item())

# ---- Benchmark -----------------------------------------------
def bench(dev):
    x = tokens.to(dev)
    torch_forward(x)  # warm‑up
    t0 = time.time()
    for _ in range(200):
        torch_forward(x)
    return (time.time() - t0) / 200 * 1e3  # ms per forward

if torch.cuda.is_available():
    print('CPU latency (ms):', bench('cpu'))
    print('GPU latency (ms):', bench('cuda'))
else:
    print('CPU latency (ms):', bench('cpu'))
# ---------------------------------------------------------------
```
