import xml.etree.ElementTree as ET

def create_xml(model_name: str, static_obj: str, mesh_uri: str, collision_scale: str = None):
    if collision_scale == None:
        collision_scale = '0.0 0.0 0.0'
    # Create the root element
    sdf = ET.Element("sdf", version="1.6")

    # Create the model element
    model = ET.SubElement(sdf, "model", name=model_name.split('/')[-1])

    # Create the static element under model
    static = ET.SubElement(model, "static")
    static.text = static_obj.lower()

    # Create the link element
    link = ET.SubElement(model, "link", name="link")

    # Create the collision element under link
    collision = ET.SubElement(link, "collision", name="collision")
    geometry_collision = ET.SubElement(collision, "geometry")
    mesh_collision = ET.SubElement(geometry_collision, "mesh")
    scale_collision = ET.SubElement(mesh_collision, "scale")
    scale_collision.text = str(collision_scale)
    uri_collision = ET.SubElement(mesh_collision, "uri")
    uri_collision.text = mesh_uri

    # Create the visual element under links
    visual = ET.SubElement(link, "visual", name="visual")
    geometry_visual = ET.SubElement(visual, "geometry")
    mesh_visual = ET.SubElement(geometry_visual, "mesh")
    scale_visual = ET.SubElement(mesh_visual, "scale")
    scale_visual.text = str(collision_scale)
    uri_visual = ET.SubElement(mesh_visual, "uri")
    uri_visual.text = mesh_uri
    # Create the XML tree
    tree = ET.ElementTree(sdf)
    ET.indent(tree, space="  ", level=0)
    tree.write(model_name + ".sdf", xml_declaration=True)

if __name__ == "__main__":
    create_xml()
