# Std lib
from typing import List

# 3rd party lib
import numpy as np
from numpy import array
from numpy.typing import NDArray
from shapely import buffer, Polygon, MultiPolygon, LineString

# Local lib
from ..beams import BeamType
from ..mill import Mill


def contour(shape: Polygon | MultiPolygon, mill: Mill, beam: BeamType, rasterize: bool = True) -> List[NDArray]:
    """Generates a scan path consisting of shrinkingcontours from edges to center."""

    beam_radius = beam.get_radius(units="nm")
    overlap = mill.get_overlap()
    step = 2 * beam_radius * (1 - overlap)

    contours = []

    def add_linestrings(geometry):
        if isinstance(geometry, Polygon):
            if not geometry.exterior.is_empty:
                contours.append(geometry.exterior)
            for interior in geometry.interiors:
                contours.append(interior)
        elif isinstance(geometry, MultiPolygon):
            for polygon in geometry.geoms:
                if not polygon.exterior.is_empty:
                    contours.append(polygon.exterior)
                for interior in polygon.interiors:
                    contours.append(interior)

    k = 0
    buffered = buffer(shape, -beam_radius, join_style="mitre")

    while True:

        if k != 0:
            buffered: Polygon = buffer(buffered, -step, join_style="round", quad_segs=100)

            if buffered.is_empty:
                break

        add_linestrings(buffered)
        k += 1

    # Extract all spots from contours
    streamlines = []
    if rasterize:

        for line in contours:
            line: LineString
            first_spot = True
            cont = []
            nr_steps = max(2, round(line.length / step))
            if nr_steps == 2:
                points: List[Polygon] = [line.centroid]
            else:
                points: List[Polygon] = []
                for distance in np.linspace(0, line.length, nr_steps):
                    points.append(line.interpolate(distance))

            if len(points) > 1:
                _idx = slice(None, -1, None)
            else:
                _idx = slice(None, None, None)

            for point in points[_idx]:
                if first_spot:
                    spot_line = array([int(mill.get_dwell_time("ns") / 100), point.centroid.x, point.centroid.y, 1])
                    cont.append(spot_line)
                    first_spot = False
                else:
                    spot_line = array([int(mill.get_dwell_time("ns") / 100), point.centroid.x, point.centroid.y, 2])
                    cont.append(spot_line)

            if line.is_closed:
                cont.append(array([1, cont[0][1], cont[0][2], 0]))
            else:
                cont.append(array([1, cont[-1][1], cont[-1][2], 0]))
            streamlines.append(array(cont))

    else:
        for line in contours:
            c = []
            for coordinate in line.coords:
                c.append(array([0, coordinate[0], coordinate[1], 0]))
            streamlines.append(array(c))

    return streamlines
