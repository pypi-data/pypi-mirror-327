import matplotlib.pyplot as plt


def plot_stream_file(file_path: str, title: str = None) -> None:

    if not file_path.endswith(".str"):
        file_path += ".str"

    segments = []  # List to store segments (each segment is a list of (x, y) tuples)
    current_segment = []  # List to store the current segment

    # Open the file and read all lines.
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Skip the first three header lines.
    for line in lines[3:]:
        line = line.strip()
        if not line:  # Skip empty lines, if any.
            continue

        # Split the line into parts.
        parts = line.split()

        # We expect at least three numbers per line.
        if len(parts) < 3:
            continue

        # The second and third elements are x and y pixel coordinates.
        # (Remember: list indices start at 0, so parts[1] is the second element.)
        x = float(parts[1])
        y = float(parts[2])

        # Check if there is a fourth element.
        if len(parts) >= 4:
            if int(parts[3]) == 0:
                current_segment.append((x, y))
                segments.append(current_segment.copy())
                current_segment = []
            elif int(parts[3]) == 1:
                current_segment.append((x, y))
        else:
            current_segment.append((x, y))

    # Now, plot each segment.
    for seg in segments:
        # Unzip the list of (x,y) tuples into separate x and y lists.
        xs, ys = zip(*seg)
        plt.plot(xs, ys, marker='o')  # You can remove or adjust marker style if desired.

    plt.xlabel("X Pixels")
    plt.ylabel("Y Pixels")
    plt.title("Streamlines")
    plt.gca().set_aspect("equal")
    plt.show()
