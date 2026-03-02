-- V5: Register vStrategy in App Registry (so it appears in GET /api/v1/apps)
INSERT INTO kernel_app_registry (app_id, name, version, icon, status, manifest_json, installed_by)
VALUES (
    'com.vcorp.vstrategy', 'vStrategy', '1.0.0', '♟️', 'ACTIVE',
    '{"app":{"id":"com.vcorp.vstrategy","name":"vStrategy","version":"1.0.0","min_kernel_version":"0.4.0"},"dependencies":[{"app_id":"com.vcorp.kernel.settings","version_range":"^1.0.0","reason":"Core platform settings"}],"permissions":[{"code":"strategy.vision.edit","name":"Edit Vision","description":"Create/edit vision","category":"strategy","default_roles":["CEO"]},{"code":"strategy.plan.manage","name":"Manage Plans","description":"Create/edit plans","category":"strategy","default_roles":["CEO","CAO"]},{"code":"strategy.alignment.edit","name":"Edit Alignment","description":"Edit OKR assignments","category":"strategy","default_roles":["CEO","CAO","CMO","CPO"]},{"code":"strategy.scorecard.view","name":"View Scorecard","description":"View scorecard","category":"strategy","default_roles":["CEO","CAO","CMO","CPO"]}],"events":{"published":["OKR_STATUS_CHANGED","PIVOT_SIGNAL_RAISED","SOP_PLAN_APPROVED"],"subscribed":["MONTHLY_CLOSE_COMPLETED"]}}',
    'system'
);

-- vStrategy permissions
INSERT INTO kernel_permissions (app_id, permission_code, name, description, category) VALUES
('com.vcorp.vstrategy', 'strategy.vision.edit', 'Edit Vision', 'Create/edit company vision and objectives', 'strategy'),
('com.vcorp.vstrategy', 'strategy.plan.manage', 'Manage Plans', 'Create/edit strategic plans', 'strategy'),
('com.vcorp.vstrategy', 'strategy.alignment.edit', 'Edit Alignment', 'Edit OKR and initiative assignments', 'strategy'),
('com.vcorp.vstrategy', 'strategy.scorecard.view', 'View Scorecard', 'View balanced scorecard and analytics', 'strategy');
