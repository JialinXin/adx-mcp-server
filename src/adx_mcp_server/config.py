#!/usr/bin/env python
import os
from dataclasses import dataclass

@dataclass
class ADXConfig:
    cluster_url: str
    database: str

config = ADXConfig(
    cluster_url=os.environ.get("ADX_CLUSTER_URL", ""),
    database=os.environ.get("ADX_DATABASE", ""),
)