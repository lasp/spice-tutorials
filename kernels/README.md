# Kernels

SPICE kernels are downloaded from NAIF at run time and are not committed.
Only meta-kernels (`*.tm`) live in git.

Fetch the generic kernels (LSK, PCK, `de440s.bsp`) into this folder from
the repo root, or from any subfolder of it:

```bash
python -c "from spiceclub import kernels; kernels.generic()"
```

`spiceclub.kernels` caches into this folder when run inside a checkout,
otherwise into `~/spiceclub_kernels` (Colab). Set `SPICECLUB_KERNELS` to use
another folder, or `SPICECLUB_NAIF_URL` to use a mirror of NAIF's `/pub/naif/`.

| Meta-kernel | Session | Contents |
|---|---|---|
| `session01.tm` | 1 | LSK, PCK, `de440s.bsp` |
