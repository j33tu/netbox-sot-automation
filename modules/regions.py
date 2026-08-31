import pulumi
from modules.netbox_provider import NetBoxResource

class RegionHierarchy(pulumi.ComponentResource):
    def __init__(self, name: str, parent_name: str, parent_slug: str, sub_name: str, sub_slug: str, opts=None):
        super().__init__('custom:netbox:RegionHierarchy', name, None, opts)

        self.parent_region = NetBoxResource(
            f"{name}-parent",
            endpoint="dcim/regions",
            props={"name": parent_name, "slug": parent_slug},
            opts=pulumi.ResourceOptions(parent=self)
        )

        self.sub_region = NetBoxResource(
            f"{name}-sub",
            endpoint="dcim/regions",
            props={
                "name": sub_name, 
                "slug": sub_slug, 
                "parent": self.parent_region.id.apply(lambda id_: int(id_))
            },
            opts=pulumi.ResourceOptions(parent=self)
        )

        self.register_outputs({"sub_region_id": self.sub_region.id})