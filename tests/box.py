from src.domain.geometry import Box, Orientation, Point3D
from pytest import fixture


@fixture(scope="module")
def positions():
    return [
        Point3D(0.0, 0.0, 0.0),
        Point3D(1.0, 2.0, 3.0),
        Point3D(-1.0, -2.0, -3.0),
        Point3D(10.5, 20.5, 30.5),
    ]


@fixture(scope="module")
def orientations():
    return [
        (Orientation.LWH, ("length", "width", "height")),
        (Orientation.LHW, ("length", "height", "width")),
        (Orientation.WLH, ("width", "length", "height")),
        (Orientation.WHL, ("height", "length", "width")),
        (Orientation.HLW, ("width", "height", "length")),
        (Orientation.HWL, ("height", "width", "length")),
    ]


@fixture(scope="module")
def bounding_boxes():
    return [
        Box((1.0, 2.0, 3.0)),
        Box((10.0, 5.0, 7.5)),
        Box((22.0, 5.5, 20.3)),
    ]

def test_placed_at(positions):
    box = Box((1.0, 2.0, 3.0))

    for new_position in positions:
        new_box = box.placed_at(new_position)

        assert new_box.position == new_position
        assert new_box.length == box.length
        assert new_box.width == box.width
        assert new_box.height == box.height


def test_oriented_to(bounding_boxes, orientations):
    for box in bounding_boxes:
        for orientation, (l_attr, w_attr, h_attr) in orientations:
            new_box = box.oriented_to(orientation)

            assert getattr(new_box, l_attr) == box.length
            assert getattr(new_box, w_attr) == box.width
            assert getattr(new_box, h_attr) == box.height


def test_fits_inside():
    outer_box = Box((5.0, 5.0, 5.0))
    inner_box = Box((3.0, 3.0, 3.0))

    assert inner_box.fits_inside(outer_box) is True
    assert outer_box.fits_inside(inner_box) is False

    # Test with equal dimensions
    equal_box = Box((5.0, 5.0, 5.0))
    assert equal_box.fits_inside(outer_box) is True


def test_collides_with():
    box1 = Box((1.0, 1.0, 1.0))
    box2 = box1.placed_at(Point3D(0.5, 0.5, 0.5))
    box3 = box1.placed_at(Point3D(2.0, 2.0, 2.0))

    assert box1.collides_with(box2) is True
    assert box1.collides_with(box3) is False


def test_collides_with_neighbors():
    box1 = Box((1.0, 1.0, 1.0))
    box2 = box1.placed_at(Point3D(0.5, 0.5, 0.5))
    box3 = box1.placed_at(Point3D(2.0, 2.0, 2.0))

    assert box1.collides_with_neighbors([box2, box3]) is True
    assert box1.collides_with_neighbors([box3]) is False


def test_in_bounds():
    boundaries = Box((5.0, 5.0, 5.0))
    box_inside = Box((1.0, 1.0, 1.0), Point3D(1.0, 1.0, 1.0))
    box_outside = Box((1.0, 1.0, 1.0), Point3D(6.0, 6.0, 6.0))

    assert box_inside.is_in_bounds(boundaries) is True
    assert box_outside.is_in_bounds(boundaries) is False


def test_out_of_bounds():
    boundaries = Box((5.0, 5.0, 5.0))
    box_inside = Box((1.0, 1.0, 1.0), Point3D(1.0, 1.0, 1.0))
    box_outside = Box((1.0, 1.0, 1.0), Point3D(6.0, 6.0, 6.0))

    assert box_inside.is_out_of_bounds(boundaries) is False
    assert box_outside.is_out_of_bounds(boundaries) is True
