# spice-tutorials

Hands-on tutorials for NASA/NAIF's SPICE toolkit in Python (SpiceyPy): slides,
background primers and runnable Jupyter notebooks, using MAVEN as a worked example.
Developed at LASP for the SPICE Book Club, a seven-session biweekly reading group.

## Contents

| Path | What |
|---|---|
| `course-plan.qmd` | Session-by-session syllabus, hosting and logistics |
| `slides/` | One Quarto (reveal.js) deck per session |
| `primers/` | Background reading the NAIF tutorials skip *(coming)* |
| `notebooks/` | Homework notebooks, runnable in Colab or Binder |
| `spiceclub/` | Small helper package: downloads and caches NAIF kernels |
| `kernels/` | Meta-kernels; kernel files are downloaded, not committed |

## Build the site

```bash
pip install quarto-cli -r requirements.txt
python -c "from spiceclub import kernels; kernels.generic()"   # LSK, PCK, de440s into kernels/
quarto preview            # live preview
quarto render             # full site into _site/
```

## License

MIT. See [LICENSE](LICENSE).
