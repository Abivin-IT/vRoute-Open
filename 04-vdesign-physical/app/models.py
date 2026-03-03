# vDesign Physical — ORM Model Re-exports (backward-compat shim)
from app.golden_sample.models._types import FlexibleJSON         # noqa: F401
from app.golden_sample.models.entity import GoldenSample          # noqa: F401
from app.material.models.entity import MaterialInbox              # noqa: F401
from app.prototype.models.entity import Prototype                 # noqa: F401
from app.lab_test.models.entity import LabTest                    # noqa: F401
from app.handover_kit.models.entity import HandoverKit            # noqa: F401

__all__ = ["FlexibleJSON", "GoldenSample", "MaterialInbox", "Prototype", "LabTest", "HandoverKit"]

