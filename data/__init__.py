from os import path

__FILE__ = str(path.abspath(__file__))
ROOT = path.dirname(__FILE__)


def _calculate_container_base_weight():
    import json
    gsm = 350
    file = path.join(ROOT, 'containers.json')

    with open(file, 'r') as f:
        container_data = json.loads(f.read())
        for container in container_data:
            # dimensions in cm
            l, w, h = (
                container['dimensions']['length'],
                container['dimensions']['width'],
                container['dimensions']['height'],
            )
            surface_area = 2 * (l * w + l * h + w * h)
            weight = surface_area * gsm / 10000
            container['base_weight'] = weight

    with open(file, 'w') as f:
        f.write(json.dumps(container_data, indent=2))


if __name__ == '__main__':
    _calculate_container_base_weight()