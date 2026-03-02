-- V10: Register vMarketing Org in App Registry (so it appears in GET /api/v1/apps)
INSERT INTO kernel_app_registry (app_id, name, version, icon, status, manifest_json, installed_by)
VALUES (
    'com.vcorp.vmarketing-org', 'vMarketing Org', '0.5.0', '📢', 'ACTIVE',
    '{"app":{"id":"com.vcorp.vmarketing-org","name":"vMarketing Org","version":"0.5.0","min_kernel_version":"0.4.0"},"dependencies":[{"app_id":"com.vcorp.kernel.settings","version_range":"^1.0.0","reason":"Core platform settings required"}],"permissions":[{"code":"marketing.campaign.view","name":"View Campaigns","description":"View ABM campaigns and audience segments","category":"marketing","default_roles":["CEO","MARKETING_MGR"]},{"code":"marketing.campaign.manage","name":"Manage Campaigns","description":"Create, launch, pause, complete ABM campaigns","category":"marketing","default_roles":["MARKETING_MGR","MARKETING_LEAD"]},{"code":"marketing.lead.qualify","name":"Qualify Leads","description":"Score leads, qualify and hand off to sales","category":"marketing","default_roles":["MARKETING_MGR","SALES_MGR"]}],"events":{"published":["CAMPAIGN_LAUNCHED","CAMPAIGN_COMPLETED","LEAD_QUALIFIED","LEAD_HANDED_OFF"],"subscribed":["kernel.app.installed","kernel.config.changed","strategy.kpi.updated"]}}',
    'system'
);

-- vMarketing Org permissions
INSERT INTO kernel_permissions (app_id, permission_code, name, description, category) VALUES
('com.vcorp.vmarketing-org', 'marketing.campaign.view', 'View Campaigns', 'View ABM campaigns and audience segments', 'marketing'),
('com.vcorp.vmarketing-org', 'marketing.campaign.manage', 'Manage Campaigns', 'Create, launch, pause, complete ABM campaigns', 'marketing'),
('com.vcorp.vmarketing-org', 'marketing.lead.qualify', 'Qualify Leads', 'Score leads, qualify and hand off to sales', 'marketing');
