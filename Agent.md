# awesome-peptide maintainer agent (`awe-agent`)

This is the **private maintainer agent** used by the `awesome-peptide` project to add one paper at a time from **PDF / DOI / URL**, then update:
- `data/paper.csv`
- `README.md` (generated)

If you are reading this inside the main repo, the full step-by-step protocol is also available at:
- `AGENT.md`

---

## Install (one-time)

From the repo root:

```bash
pip install -e '.[agent]'
```

Verify:

```bash
awe-agent --help
awe-agent add --help
```

---

## Configure LLM (no key in git)

Recommended: create `awepep-agent.toml` (gitignored) in repo root:

```bash
cp awepep-agent.example.toml awepep-agent.toml
```

Edit `awepep-agent.toml`:

```toml
[llm]
base_url = "https://api.openai.com/v1"
api_key = "YOUR_KEY"
model = "gpt-4o-mini"
```

Defaults:
- If you don’t set `AWEPEP_LLM_MODEL`, it defaults to `gpt-4o-mini`.

---

## Quick usage

Safe preview (no repo changes):

```bash
awe-agent add 'https://arxiv.org/abs/2508.14765' --dry-run
```

Apply changes (writes `data/paper.csv` + regenerates `README.md` after confirmation):

```bash
awe-agent add 'https://arxiv.org/abs/2508.14765'
```

Using a PDF (best for extracting code links), with URL as DOI fallback:

```bash
awe-agent add \
  --pdf '/absolute/path/to/paper.pdf' \
  --url 'https://arxiv.org/abs/2508.14765' \
  --dry-run
```

