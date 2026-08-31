import os
import yaml
import pulumi

from modules.regions import RegionHierarchy
from modules.sites import SiteComponent
from modules.locations import LocationAndRackComponent

# Load Site YAML Configuration
data_path = os.path.join("site_data", "site-syd01.yml")
with open(data_path, "r") as f:
    config = yaml.safe_load(f)

# 1. Instantiate Region Module
region_module = RegionHierarchy(
    name="anz-region-hierarchy",
    parent_name=config["region"],
    parent_slug=config["region_slug"],
    sub_name=config["sub_region"],
    sub_slug=config["sub_region_slug"]
)

# 2. Instantiate Site Module
site_module = SiteComponent(
    name="syd01-site-component",
    site_name=config["site_name"],
    site_slug=config["site_slug"],
    status=config["status"],
    region_id=region_module.sub_region.id
)

# 3. Instantiate Locations & Racks Module
infra_module = LocationAndRackComponent(
    name="syd01-infra-component",
    site_id=site_module.site.id,
    locations_data=config.get("locations", [])
)

# Stack Outputs
pulumi.export("site_id", site_module.site.id)
pulumi.export("racks_created", infra_module.created_racks)