0.0.2a0
-------

- Add radius attribute (cf015d92de06)
- Add lats, lons and LATS, LONS attributes (3098c638f9c0)
- More attributes and methods copied: some needs attention deltay, dealiasing (07065375be36)
- Bug divrotsh_from_vec v, u order in vsh_from_vec call (1e9f96300d52)
- Bring back fluidpythran.boost, more operator attributes for FluidSim (0b8680eb0da1)
- Use radians to represent lat, lon attributes; default normalization=orthonormal, no cs_phase, args and kwargs for create_sht_object (35b18163a12a)
- Allow passing u, v buffers to vec_from{div,rot}sh methods (360ef5e62e66)
- Laplacian, invlaplacian implementation; fix a bug with inv_K2_r, vsh_from_divrotsh (53da4f5d5da2, 214a338cf1bb, b33d3d1f18bc, 73fd1b0479e6)


Minor changes
~~~~~~~~~~~~~

- Try to setup continuous deploy, improved setup. (1a59618982e1, e62cf2545a1e, 155aee95a4c9)
- Apply black, version 18.9b0 (323291f150f7)
- Use hg versions of fluiddyn, fluidpythran (762695f32a14)
- Tox, be more verbose (ec7136dbddcc)
- Tox FLUIDPYTHRAN_NO_REPLACE to improve coverage (76e217792235)

