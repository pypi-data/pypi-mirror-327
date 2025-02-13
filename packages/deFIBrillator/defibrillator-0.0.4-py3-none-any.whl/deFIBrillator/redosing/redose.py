#
# # Build spatial index
#     tree = STRtree(points)
#
#     # Calculate dwell times
#     for spot in points:
#         # Find all spots within the Euclidian overlap distance
#         neighbors: NDArray = tree.query(buffer(spot, beam_radius), predicate="dwithin", distance=beam_radius)
#         print(neighbors)
#         if neighbors.shape[0] != 0:
#             n = [tree.geometries[int(neighbor)] for neighbor in neighbors]
#             distances = [spot.distance(ne) for ne in n]
#             dose_pr_area_goal = beam.get_dose(mill.get_dwell_time("us") / beam.get_area("nm"))
#             dose_pr_area_actual = beam.get_dose(float(point_dict[spot][0]) / beam.get_area("nm"))
#         else:
#             continue
#
#         dose_goal = dose_pr_area_goal * beam.get_area("nm")  # The dose this spot should ideally have.
#         total_dose = dose_pr_area_actual * beam.get_area("nm")  # Dose contribution from the spot itself.
#
#         this_spot = Point().buffer(beam_radius)
#         for neighbor, distance in zip(neighbors, distances):
#             print(distance)
#             n_spot = Point((distance, 0)).buffer(beam_radius)
#             intersection = this_spot.intersection(n_spot)
#             plt.figure()
#             plt.plot(*intersection.exterior.xy)
#             plt.show()
#             dose = (intersection.area
#                     * beam.get_dose(float(point_dict[tree.geometries[neighbor]][0] * 100))
#                     / beam.get_area("nm")
#                     )
#             total_dose += dose
#
#         print(dose_goal, total_dose, dose_goal/total_dose)
#
#         point_dict[spot][0] *= dose_goal/total_dose
#
#     plt.figure(figsize=(15, 15))
#     for c in streamlines:
#         xx = []
#         yy = []
#         for _, x, y, _ in c:
#             xx.append(x)
#             yy.append(y)
#         plt.plot(xx, yy, "o-")
#     plt.show()
#
#     from scipy.interpolate import griddata
#
#     # Extract x, y, and dose values
#     x = np.array([p.x for p in point_dict.keys()])
#     y = np.array([p.y for p in point_dict.keys()])
#     dose = np.array([v[0] for _, v in point_dict.items()])
#
#     # Define grid resolution
#     grid_x, grid_y = np.mgrid[min(x):max(x):1000j, min(y):max(y):1000j]
#
#     # Interpolate dose values onto the grid
#     grid_z = griddata((x, y), dose, (grid_x, grid_y), method='cubic')
#
#     # Plot the heatmap
#     plt.figure(figsize=(6, 5))
#     plt.imshow(grid_z, extent=(min(x), max(x), min(y), max(y)), origin='lower', cmap='hot')
#     plt.colorbar(label="Dose Value")
#     plt.scatter(x, y, c='blue', marker='o', label="Data Points")  # Original points
#     plt.legend()
#     plt.title("Dose Heatmap")
#     plt.xlabel("X Coordinate")
#     plt.ylabel("Y Coordinate")
#     plt.show()
#
#     return streamlines