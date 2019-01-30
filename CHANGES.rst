0.0.3a0 (2018-01-31)
--------------------

- Bye bye fluidpythran, hello transonic (:rev:`238efcbcb574`)
- Rewrite setup using transonic>=0.1.9.post0 (:rev:`8840f876c728`, :rev:`ef77ce858634`)

Minor changes
~~~~~~~~~~~~~

- Clarify readme, add authors (:rev:`62021bfda8e1`, :rev:`8de7f39a56a5`)

0.0.2a0
-------

- Add radius attribute (:rev:`cf015d92de06`)
- Add lats, lons and LATS, LONS attributes (:rev:`3098c638f9c0`)
- More attributes and methods copied: some needs attention deltay, dealiasing (:rev:`07065375be36`)
- Bug divrotsh_from_vec v, u order in vsh_from_vec call (:rev:`1e9f96300d52`)
- Bring back fluidpythran.boost, more operator attributes for FluidSim (:rev:`0b8680eb0da1`)
- Use radians to represent lat, lon attributes; default normalization=orthonormal, no cs_phase, args and kwargs for create_sht_object (:rev:`35b18163a12a`)
- Allow passing u, v buffers to vec_from{div,rot}sh methods (:rev:`360ef5e62e66`)
- Laplacian, invlaplacian implementation; fix a bug with inv_K2_r, vsh_from_divrotsh (:rev:`53da4f5d5da2`, :rev:`214a338cf1bb`, :rev:`b33d3d1f18bc`, :rev:`73fd1b0479e6`)


Minor changes
~~~~~~~~~~~~~

- Try to setup continuous deploy, improved setup. (:rev:`1a59618982e1`, :rev:`e62cf2545a1e`, :rev:`155aee95a4c9`)
- Apply black, version 18.9b0 (:rev:`323291f150f7`)
- Use hg versions of fluiddyn, fluidpythran (:rev:`762695f32a14`)
- Tox, be more verbose (:rev:`ec7136dbddcc`)
- Tox TRANSONIC_NO_REPLACE to improve coverage (:rev:`76e217792235`)
