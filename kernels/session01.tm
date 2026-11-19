KPL/MK

Meta-kernel for SPICE Book Club Session 1.

Paths are relative to the directory SPICE is called from, NOT to this file.
'../kernels' works when your working directory is notebooks/ or slides/ in
the spice-tutorials repo. From anywhere else, edit PATH_VALUES (or let
spiceclub.kernels.write_metakernel() write one with absolute paths).

Fetch the files first:

   from spiceclub import kernels
   kernels.generic()

   File               Type   Contents
   -----------------  -----  ------------------------------------------
   naif0012.tls       LSK    leap seconds, UTC <-> ET
   pck00011.tpc       PCK    body radii and IAU rotation models
   de440s.bsp         SPK    planet, Sun and Moon ephemerides 1849-2150

\begindata

   PATH_VALUES  = ( '../kernels' )
   PATH_SYMBOLS = ( 'KERNELS' )

   KERNELS_TO_LOAD = (
      '$KERNELS/naif0012.tls'
      '$KERNELS/pck00011.tpc'
      '$KERNELS/de440s.bsp'
   )

\begintext
