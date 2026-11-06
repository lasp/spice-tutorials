# Kernels

SPICE kernels are downloaded from NAIF at build or run time and are not
committed. Meta-kernels (`*.tm`) for each session will live here.

Until the download helper exists, fetch the leapseconds kernel manually:

```bash
curl -o kernels/naif0012.tls \
  https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/naif0012.tls
```
