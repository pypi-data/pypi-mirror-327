from deFIBrillator import FIBG2, plot_stream_file

# Initialize the G2 FIB
fib = FIBG2()

# Set the Ion beam. Beams are found under fib.Beams (default beam is 48 pA at 30kV).
fib.set_beam(fib.Beams.Acceleration30kV.pA48)

# Set the magnification of the fib. This can be done by setting it directly, or settings the field of view.
fib.set_fov(5, "um")
# or ie. fib.set_magnification(5000)

# You can print the fib instance to see all specific and derived parameters
print(fib)

# Create a new pattern and specify dwell time and depth
pat = fib.new_pattern()
pat.set_dwell_time(1, "us")
pat.set_depth(100, "nm")

# Create a circle shape
circle = pat.add.circle(radius=100, millable=True)

# Create a 3x3 square lattice with periodicity 300 nm in x and y. Add the circle so it's placed at each lattice point.
# Alpha is the lattice vector in x, and beta in y. Gamma is the angle between them.
lat = pat.add.lattice(rows=3, cols=3, alpha=300, beta=300, gamma=90, shape=circle)

# Plot the pattern
pat.plot_pattern()

# Plot the beam path
pat.plot_beam_path()

# Show animation of the beam path
pat.animate_beam_path()

# Create stream file of the pattern
pat.write_stream("circle_array")

# Optionally you can plot the stream file you created to verify that it's correct. For very low FIB magnifications,
# converting physical coordinates to pixel values can really mess up the beam path, so it's good to check.
plot_stream_file("circle_array.str")
