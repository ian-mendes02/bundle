import pyvista as pv
import src.domain.objects as app
from src.domain.geometry import Box

def _Label(
    text: str,
    bounds: Box,
    offset_x: float,
):
    center = (
        bounds.x + offset_x + bounds.length / 2,
        bounds.y + bounds.width / 2,
        bounds.z + bounds.height + 0.5,
    )
    return {
        "mesh": pv.Text3D(
            text,
            depth=0,
            width=bounds.width * 0.25,
            center=center,
        ),
        "color": "black",
    }


def _Package(package: app.Package, offset_x: float):
    return (
        _Label(package.sku_list[0], package, offset_x),
        {
            "mesh": pv.Box(
                bounds=(
                    package.x + offset_x,
                    package.x + offset_x + package.length,
                    package.y,
                    package.y + package.width,
                    package.z,
                    package.z + package.height,
                ),
            ),
            "color": "red" if package.is_fragile else "blue",
            "opacity": 0.5,
            "show_edges": True,
            "edge_color": "black",
            "edge_opacity": 1.0,
        },
    )


def _Container(
    container_id: str,
    container: app.Container,
    offset_x: float,
):
    return (
        _Label(container_id, container, offset_x),
        {
            "mesh": pv.Box(
                bounds=(
                    offset_x,
                    offset_x + container.length,
                    0,
                    container.width,
                    0,
                    container.height,
                ),
            ),
            "color": "gray",
            "opacity": 0.15,
            "show_edges": True,
            "edge_color": "black",
            "edge_opacity": 1.0,
        },
    )


class Scene(pv.Plotter):
    def __init__(self):
        super().__init__()
        self.__offset_x = 0.0
        self.__box_spacing = 15.0
        self.__index = 1

    def setup(
        self,
        bundles: list[app.Bundle],
        loose_packages: list[app.Package],
    ) -> None:
        for bundle in bundles:
            label, container = _Container(
                f"#{self.__index} - {bundle.container.id}",
                bundle.container,
                self.__offset_x,
            )
            self.add_mesh(**container)
            self.add_mesh(**label)
            self.__index += 1

            for package in bundle.packages:
                self.add_package(package)

            self.__offset_x += bundle.container.length + self.__box_spacing

        if loose_packages:
            for package in loose_packages:
                label, pkg = _Package(package, self.__offset_x)
                pkg["color"] = "pink"
                self.add_mesh(**pkg)
                self.add_mesh(**label)

    def add_package(self, package: app.Package) -> None:
        label, pkg = _Package(package, self.__offset_x)
        self.add_mesh(**pkg)
        self.add_mesh(**label)


def show_result_3d(
    bundles: list[app.Bundle],
    loose_packages: list[app.Package] | None = None,
) -> None:
    sc = Scene()
    sc.setup(bundles, loose_packages or [])
    sc.add_axes()
    sc.camera.azimuth = -120
    sc.camera.elevation = 20
    sc.show()
