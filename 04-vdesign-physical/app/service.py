# vDesign Physical — Service Re-exports (backward-compat shim)
from app.golden_sample.controllers.service import (  # noqa: F401
    list_golden_samples,
    get_golden_sample,
    create_golden_sample,
    update_golden_sample,
    seal_golden_sample,
    compromise_golden_sample,
)
from app.material.controllers.service import (  # noqa: F401
    list_materials,
    get_material,
    ingest_material,
    scrap_material,
)
from app.prototype.controllers.service import (  # noqa: F401
    list_prototypes,
    get_prototype,
    create_prototype,
    retire_prototype,
)
from app.lab_test.controllers.service import (  # noqa: F401
    list_lab_tests,
    get_lab_test,
    create_lab_test,
    complete_lab_test,
    get_lab_summary,
)
from app.handover_kit.controllers.service import (  # noqa: F401
    list_handover_kits,
    get_handover_kit,
    create_handover_kit,
    dispatch_handover_kit,
    receive_handover_kit,
)

__all__ = [
    "list_golden_samples", "get_golden_sample", "create_golden_sample",
    "update_golden_sample", "seal_golden_sample", "compromise_golden_sample",
    "list_materials", "get_material", "ingest_material", "scrap_material",
    "list_prototypes", "get_prototype", "create_prototype", "retire_prototype",
    "list_lab_tests", "get_lab_test", "create_lab_test", "complete_lab_test", "get_lab_summary",
    "list_handover_kits", "get_handover_kit", "create_handover_kit",
    "dispatch_handover_kit", "receive_handover_kit",
]
