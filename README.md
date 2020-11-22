# HackNet
Utilities for the game HackNet

## password.py
Recover passwords for DEC-encrypted files

If you haven't gotten far enough in the game to encounter DEC-encryption, stop reading now,
because there will be spoilers. (Also, what are you doing here?)

With that out of the way: You probably already know that DEC-encryption is __super__ weak,
and it's very easy to write code to decrypt them, even if you don't know the password.
However, I prefer to stick to in-game tools as much as possible, and the in-game _Decrypt.exe_
utility requires a password. This script brute-forces the password space (its size is only 65536)
to find potentially valid passwords, which you can then use in-game. If you're clever and
lucky, you might be able to reverse-engineer some of the _actual_ passwords as well, assuming
they're short and all-lowercase.

### How to use

Here's a sample header from an encoded file:

#DEC_ENC::162549 182591 193523 158905 177125 164371 96957 164371 180769 160727 188057 200811 184413 191701 171659 182591 180769::127931 126109 127931 122465 126109 122465 140685 142507 122465 127931 135219 133397::201493 217891 197849 219713 199671 201493 199671::211743 177125 157083 200811 164371 188057 129753 122465 220853 222675 219031

The number you want is the one right before the last "::". In this case, that is 199671.
Some headers only have three sets of "::", in which case you just want the last number.
You can double-check because it will be the same as the number two before it.

Then, pass that number on the commandline:

```txt
./password.py 199671

"u_k_h_b_" is valid
"a_c_n_l_" is valid
"z_f_e_u_" is valid
"d_e_t_o_" is valid
"y_o_v_x_" is valid
"b_q_s_t_" is valid
"r_h_n_z_" is valid
```

There will almost always be multiple valid passwords, typically 8 characters long.
The underscores represent any character - C# has a weak hashing function, which means that
the even characters do not contribute to the result in this context. So you can replace them
with anything, or leave them as underscores. You can also trim the last one (dropping down
to 7 characters) if you like, and that extends to valid solutions of any length.
