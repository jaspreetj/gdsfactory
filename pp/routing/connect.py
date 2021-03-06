from pp.routing.manhattan import route_manhattan
from pp.routing.manhattan import generate_manhattan_waypoints
from pp.routing.manhattan import round_corners
from pp.components.bend_circular import bend_circular
from pp.components import waveguide
from pp.components import taper as taper_factory
from pp.components.electrical import wire, corner

from pp.config import WG_EXPANDED_WIDTH, TAPER_LENGTH
from pp.layers import LAYER


def get_waypoints_connect_strip(*args, **kwargs):
    return connect_strip(*args, **kwargs, route_factory=generate_manhattan_waypoints)


def connect_strip(
    input_port,
    output_port,
    bend_factory=bend_circular,
    straight_factory=waveguide,
    taper_factory=taper_factory,
    start_straight=0.01,
    end_straight=0.01,
    min_straight=0.01,
    bend_radius=10.0,
    route_factory=route_manhattan,
):

    bend90 = bend_factory(radius=bend_radius, width=input_port.width)

    if taper_factory:
        if callable(taper_factory):
            taper = taper_factory(
                length=TAPER_LENGTH,
                width1=input_port.width,
                width2=WG_EXPANDED_WIDTH,
                layer=input_port.layer,
            )
        else:
            # In this case the taper is a fixed cell
            taper = taper_factory
    else:
        taper = None

    connector = route_factory(
        input_port,
        output_port,
        bend90,
        straight_factory=straight_factory,
        taper=taper,
        start_straight=start_straight,
        end_straight=end_straight,
        min_straight=min_straight,
    )
    return connector


def connect_strip_way_points(
    way_points=[],
    bend_factory=bend_circular,
    straight_factory=waveguide,
    taper_factory=taper_factory,
    bend_radius=10.0,
    wg_width=0.5,
    layer=LAYER.WG,
    **kwargs
):
    """
    Returns a deep-etched route formed by the given way_points with
    bends instead of corners and optionally tapers in straight sections.
    
    taper_factory: can be either a taper component or a factory
    """

    bend90 = bend_factory(radius=bend_radius, width=wg_width)

    if taper_factory:
        if callable(taper_factory):
            taper = taper_factory(
                length=TAPER_LENGTH,
                width1=wg_width,
                width2=WG_EXPANDED_WIDTH,
                layer=layer,
            )
        else:
            # In this case the taper is a fixed cell
            taper = taper_factory
    else:
        taper = None

    connector = round_corners(way_points, bend90, straight_factory, taper)
    return connector


def connect_strip_way_points_no_taper(*args, **kwargs):
    return connect_strip_way_points(*args, taper_factory=None, **kwargs)


def connect_elec_waypoints(
    way_points=[],
    bend_factory=bend_circular,
    straight_factory=waveguide,
    taper_factory=taper_factory,
    bend_radius=10.0,
    wg_width=0.5,
    layer=LAYER.WG,
    **kwargs
):

    bend90 = bend_factory(width=wg_width, radius=bend_radius, layer=layer)

    def _straight_factory(length=10.0, width=wg_width):
        return straight_factory(length=length, width=width, layer=layer)

    if "bend_radius" in kwargs:
        bend_radius = kwargs.pop("bend_radius")
    else:
        bend_radius = 10

    connector = round_corners(way_points, bend90, _straight_factory, taper=None)
    return connector


def connect_elec(
    input_port,
    output_port,
    straight_factory=wire,
    bend_factory=corner,
    layer=None,
    **kwargs
):
    width = input_port.width

    # If no layer is specified, the component factories should use the layer
    # given in port.type
    if layer is None:
        layer = input_port.layer

    def _bend_factory(width=width, radius=0):
        return bend_factory(width=width, radius=radius, layer=layer)

    def _straight_factory(length=10.0, width=width):
        return straight_factory(length=length, width=width, layer=layer)

    if "bend_radius" in kwargs:
        bend_radius = kwargs.pop("bend_radius")
    else:
        bend_radius = 10

    return connect_strip(
        input_port,
        output_port,
        bend_radius=bend_radius,
        bend_factory=_bend_factory,
        straight_factory=_straight_factory,
        taper_factory=None,
        **kwargs
    )


if __name__ == "__main__":
    import pp

    c = pp.c.waveguide()
    cc = connect_strip(c.ports["E0"], c.ports["W0"])
    pp.show(cc)
