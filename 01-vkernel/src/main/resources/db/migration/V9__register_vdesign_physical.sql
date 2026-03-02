-- V9: Register vDesign Physical in App Registry (so it appears in GET /api/v1/apps)
INSERT INTO kernel_app_registry (app_id, name, version, icon, status, manifest_json, installed_by)
VALUES (
    'com.vcorp.vdesign-physical', 'vDesign Physical', '0.5.0', '🔬', 'ACTIVE',
    '{"app":{"id":"com.vcorp.vdesign-physical","name":"vDesign Physical","version":"0.5.0","min_kernel_version":"0.4.0"},"dependencies":[{"app_id":"com.vcorp.kernel.settings","version_range":"^1.0.0","reason":"Core platform settings required"}],"permissions":[{"code":"design.sample.view","name":"View Samples","description":"View golden samples and prototypes","category":"design","default_roles":["CEO","DESIGN_MGR"]},{"code":"design.sample.manage","name":"Manage Samples","description":"Create, seal, compromise golden samples and manage prototypes","category":"design","default_roles":["DESIGN_MGR","DESIGN_LEAD"]},{"code":"design.lab.execute","name":"Execute Lab Tests","description":"Create and complete lab test runs","category":"design","default_roles":["DESIGN_MGR","LAB_TECH"]}],"events":{"published":["GOLDEN_SAMPLE_SEALED","LAB_TEST_COMPLETED","HANDOVER_KIT_DISPATCHED","PROTOTYPE_RETIRED"],"subscribed":["kernel.app.installed","kernel.config.changed","strategy.kpi.updated"]}}',
    'system'
);

-- vDesign Physical permissions
INSERT INTO kernel_permissions (app_id, permission_code, name, description, category) VALUES
('com.vcorp.vdesign-physical', 'design.sample.view', 'View Samples', 'View golden samples and prototypes', 'design'),
('com.vcorp.vdesign-physical', 'design.sample.manage', 'Manage Samples', 'Create, seal, compromise golden samples and manage prototypes', 'design'),
('com.vcorp.vdesign-physical', 'design.lab.execute', 'Execute Lab Tests', 'Create and complete lab test runs', 'design');
