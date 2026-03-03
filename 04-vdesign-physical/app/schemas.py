# vDesign Physical — DTO Re-exports (backward-compat shim)
from app.golden_sample.models.schema import (  # noqa: F401
    GoldenSampleCreate,
    GoldenSampleUpdate,
    GoldenSampleOut,
)
from app.material.models.schema import (  # noqa: F401
    MaterialInboxCreate,
    MaterialInboxOut,
)
from app.prototype.models.schema import (  # noqa: F401
    PrototypeCreate,
    PrototypeOut,
)
from app.lab_test.models.schema import (  # noqa: F401
    LabTestCreate,
    LabTestOut,
)
from app.handover_kit.models.schema import (  # noqa: F401
    HandoverKitCreate,
    HandoverKitOut,
)

__all__ = [
    "GoldenSampleCreate", "GoldenSampleUpdate", "GoldenSampleOut",
    "MaterialInboxCreate", "MaterialInboxOut",
    "PrototypeCreate", "PrototypeOut",
    "LabTestCreate", "LabTestOut",
    "HandoverKitCreate", "HandoverKitOut",
]
