import pulumi
from modules.netbox_provider import NetBoxResource

class LocationAndRackComponent(pulumi.ComponentResource):
    def __init__(self, name: str, site_id: pulumi.Output, locations_data: list, opts=None):
        super().__init__('custom:netbox:LocationAndRackComponent', name, None, opts)

        self.created_racks = []

        for loc in locations_data:
            loc_name = f"Floor-{loc['floor']}-{loc['type']}"
            loc_slug = f"f{loc['floor']}-{loc['type'].lower()}"

            location_res = NetBoxResource(
                f"{name}-{loc_slug}",
                endpoint="dcim/locations",
                props={
                    "name": loc_name,
                    "slug": loc_slug,
                    "site": site_id.apply(lambda id_: int(id_))
                },
                opts=pulumi.ResourceOptions(parent=self)
            )

            for rack_data in loc.get("racks", []):
                rack_res = NetBoxResource(
                    f"{name}-rack-{rack_data['name'].lower()}",
                    endpoint="dcim/racks",
                    props={
                        "name": rack_data["name"],
                        "site": site_id.apply(lambda id_: int(id_)),
                        "location": location_res.id.apply(lambda id_: int(id_)),
                        "width": rack_data["width"],
                        "u_height": rack_data["u_height"],
                        "status": "active"
                    },
                    opts=pulumi.ResourceOptions(parent=self)
                )
                self.created_racks.append(rack_res.id)

        self.register_outputs({"racks": self.created_racks})