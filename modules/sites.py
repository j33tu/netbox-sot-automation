import pulumi
from modules.netbox_provider import NetBoxResource

class SiteComponent(pulumi.ComponentResource):
    def __init__(self, name: str, site_name: str, site_slug: str, status: str, region_id: pulumi.Output, opts=None):
        super().__init__('custom:netbox:SiteComponent', name, None, opts)

        self.site = NetBoxResource(
            f"{name}-site",
            endpoint="dcim/sites",
            props={
                "name": site_name,
                "slug": site_slug,
                "status": status,
                "region": region_id.apply(lambda id_: int(id_))
            },
            opts=pulumi.ResourceOptions(parent=self)
        )

        self.register_outputs({"site_id": self.site.id})