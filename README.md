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
| `notebooks/` | Homework notebooks, runnable in Colab or Binder *(coming)* |
| `kernels/` | Meta-kernels; kernel files are downloaded, not committed |

## Build the site

```bash
pip install quarto-cli spiceypy numpy matplotlib jupyter
curl -o kernels/naif0012.tls \
  https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls
quarto preview            # live preview
quarto render             # full site into _site/
```

## License

MIT. See [LICENSE](LICENSE).
