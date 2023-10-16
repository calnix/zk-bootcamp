'''
Let’s create a simple plot of an elliptic curve

y² = x³ + 3 (mod 11)

# Use Visual Studio Code in Interactive mode
- similar to a notebook in many ways, as it splits your code into cells that can be run individually.
- but file remains .py
- split code by adding " # %% " at the top. 
- Running code this way, Visual Studio Code opens an Interactive pane that displays the plots inline.

'''
# %%
import libnum
import matplotlib.pyplot as plt

def generate_points(mod):
    xs = []
    ys = []

    def y_squared(x):
        return (x**3 + 3) % mod

    for x in range(0, mod):
        if libnum.has_sqrtmod_prime_power(y_squared(x), mod, 1):
            square_roots = libnum.sqrtmod_prime_power(y_squared(x), mod, 1)

            # we might have two solutions 
            for sr in square_roots:
                ys.append(sr)
                xs.append(x)
    return xs, ys


xs, ys = generate_points(11)
fig, (ax1) = plt.subplots(1, 1);
fig.suptitle('y^2 = x^3 + 3 (mod 11)');
fig.set_size_inches(6, 6);
ax1.set_xticks(range(0,11));
ax1.set_yticks(range(0,11));
plt.grid()
plt.scatter(xs, ys)


# %%
# diplay plot
plt.show()

'''
Some observations:
- There won’t be any x values larger than the modulus we use
- Just like the real-valued plot, the modular one “appears symmetric”, about some horizontal line.
'''