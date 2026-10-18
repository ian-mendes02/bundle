from os import path
from data import ROOT

def _export_containers_table_html():
    file = path.join(ROOT, 'containers.json')
    template_file = path.join(ROOT, 'templates', 'containers.html')
    export = path.join(ROOT, 'export', 'containers.html')
    with open(file, 'r') as j:
        with open(template_file, 'r') as t:
            template = str(t.read())
            with open(export, 'w') as e:
                e.write(template.replace("%DATA%", j.read()))


def _export_products_table_html():
    file = path.join(ROOT, 'products.json')
    template_file = path.join(ROOT, 'templates', 'products.html')
    export = path.join(ROOT, 'export', 'products.html')
    with open(file, 'r') as j:
        with open(template_file, 'r') as t:
            template = str(t.read())
            with open(export, 'w') as e:
                e.write(template.replace("%DATA%", j.read()))

def export_tables():
    _export_containers_table_html()
    _export_products_table_html()