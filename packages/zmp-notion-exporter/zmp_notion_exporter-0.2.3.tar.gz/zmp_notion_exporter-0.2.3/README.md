# zmp-notion-exporter

![Platform Badge](https://img.shields.io/badge/platform-zmp-red)
![Component Badge](https://img.shields.io/badge/component-exporter-red)
![CI Badge](https://img.shields.io/badge/ci-github_action-green)
![License Badge](https://img.shields.io/badge/license-MIT-green)
![PyPI - Version](https://img.shields.io/pypi/v/zmp-notion-exporter)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/zmp-notion-exporter)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zmp-notion-exporter)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/zmp-notion-exporter)

<!-- ![Language Badge](https://img.shields.io/badge/language-python-blue)
![Version Badge](https://img.shields.io/badge/version-^3.12-blue) -->

The zmp-notion-expoter is the utility library to export the Mardown, HTML and PDF files from the notion pages.

# Goals
This is the utility project for the Cloud Z MP manual system

# Examples
## Export to markdown
include all sub pages of the root notion page
```python
import os
import time

from dotenv import load_dotenv

from zmp_notion_exporter import NotionPageExporter, extract_notion_page_id

load_dotenv()

notion_token = os.environ.get("NOTION_TOKEN", "")

if not notion_token:
    raise ValueError("NOTION_TOKEN is not set")


root_page_url = "https://www.notion.so/cloudzcp/Cloud-Z-CP-193b7135d33b801a942fd1706edcb026?pvs=4"  # Cloud Z CP

output_dir = ".output"

exporter = NotionPageExporter(
    notion_token=notion_token,
    root_page_id=extract_notion_page_id(root_page_url),
    root_output_dir=output_dir,
)

start_time = time.time()

path = exporter.markdownx(include_subpages=True)

print(path)

end_time = time.time()

print("-" * 100)
print(f"Export took {end_time - start_time:.2f} seconds")
print("-" * 100)

# Output sample
.output
.output/
└── docs/
    └── Cloud_Z_CP/
        └── v2.0/
            └── Supported_Notion_Blocks_for_Manual
            └── Unsupported_Blocks_for_Manual
            └── Tutorials/
                └── 1_Gettting
                └── 2_Getting
            └── Installation
            └── FAQ
            └── Release_Notes
        └── v3.0
.output/
└── static/
    └── image/
        └── Cloud_Z_CP/
            └── v2.0/
                └── Tutorials/
----------------------------------------------------------------------------------------------------
Export took 24.26 seconds
----------------------------------------------------------------------------------------------------

# double check using the os command
$ tree .output
.output
├── docs
│   └── Cloud_Z_CP
│       ├── v2.0
│       │   ├── FAQ.mdx
│       │   ├── Installation.mdx
│       │   ├── Release_Notes.mdx
│       │   ├── Supported_Notion_Blocks_for_Manual.mdx
│       │   ├── Tutorials
│       │   │   ├── 1_Gettting.mdx
│       │   │   └── 2_Getting.mdx
│       │   └── Unsupported_Blocks_for_Manual.mdx
│       └── v3.0.mdx
└── static
    └── image
        └── Cloud_Z_CP
            └── v2.0
                ├── 193b7135-d33b-808b-87de-dc5707394d08_docling_processing.png
                ├── 193b7135-d33b-80b3-b2e8-fecf91125711.png
                ├── Tutorials
                └── wildcard-shinhan-cloudzcp-net-cert.yaml

9 directories, 11 files
```

## Export to markdown files of the specific page
```python
import os
import time

from dotenv import load_dotenv

from zmp_notion_exporter import NotionPageExporter, extract_notion_page_id

load_dotenv()

notion_token = os.environ.get("NOTION_TOKEN", "")

if not notion_token:
    raise ValueError("NOTION_TOKEN is not set")


root_page_url = "https://www.notion.so/cloudzcp/Cloud-Z-CP-193b7135d33b801a942fd1706edcb026?pvs=4"  # Cloud Z CP
target_page_urls = [
    "https://www.notion.so/cloudzcp/Getting-Started-Sample-Page-193b7135d33b80e0954fc9e52d94291a?pvs=4",  # Getting Started Sample Page
    "https://www.notion.so/v2-0-193b7135d33b803ba24bdccaaa8496f5?pvs=4",  # Release Notes
]

output_dir = ".output"

exporter = NotionPageExporter(
    notion_token=notion_token,
    root_page_id=extract_notion_page_id(root_page_url),
    root_output_dir=output_dir,
)

start_time = time.time()

path = exporter.markdownx(
    page_id=extract_notion_page_id(target_page_urls[2]), include_subpages=False
)

print(path)

docs_node, static_image_node = exporter.get_output_nodes()
docs_node.print_pretty(include_leaf_node=True)
static_image_node.print_pretty(include_leaf_node=False)

end_time = time.time()

print("-" * 100)
print(f"Export took {end_time - start_time:.2f} seconds")
print("-" * 100)

# Output sample
.output/docs/Cloud_Z_CP/v2.0/Release_Notes
.output/
└── docs/
    └── Cloud_Z_CP/
        └── v2.0/
            └── Supported_Notion_Blocks_for_Manual
            └── Unsupported_Blocks_for_Manual
            └── Tutorials/
                └── 1_Gettting
                └── 2_Getting
            └── Installation
            └── FAQ
            └── Release_Notes
        └── v3.0
.output/
└── static/
    └── image/
        └── Cloud_Z_CP/
            └── v2.0/
                └── Tutorials/
----------------------------------------------------------------------------------------------------
Export took 10.78 seconds
----------------------------------------------------------------------------------------------------

# doubule check using the os command
$ tree .output
.output
├── docs
│   └── Cloud_Z_CP
│       └── v2.0
│           ├── Release_Notes.mdx
│           └── Tutorials
└── static
    └── image
        └── Cloud_Z_CP
            └── v2.0
                └── Tutorials

9 directories, 1 file
```
