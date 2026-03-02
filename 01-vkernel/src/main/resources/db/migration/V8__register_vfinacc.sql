-- V8: Register vFinacc in App Registry (so it appears in GET /api/v1/apps)
INSERT INTO kernel_app_registry (app_id, name, version, icon, status, manifest_json, installed_by)
VALUES (
    'com.vcorp.vfinacc', 'vFinacc', '1.0.0', '💰', 'ACTIVE',
    '{"app":{"id":"com.vcorp.vfinacc","name":"vFinacc","version":"1.0.0","min_kernel_version":"0.4.0"},"dependencies":[{"app_id":"com.vcorp.kernel.settings","version_range":"^1.0.0","reason":"Core platform settings required"},{"app_id":"com.vcorp.vstrategy","version_range":"^1.0.0","reason":"Cost Center targets come from S&OP plan"}],"permissions":[{"code":"finance.ledger.view","name":"View Ledger","description":"View journal entries and financial reports","category":"finance","default_roles":["CEO","CFO"]},{"code":"finance.ledger.post","name":"Post Ledger Entries","description":"Create and post journal entries to the general ledger","category":"finance","default_roles":["CFO","ACC_MGR"]},{"code":"finance.transaction.approve","name":"Approve Transactions","description":"Approve and reconcile financial transactions","category":"finance","default_roles":["CFO","ACC_MGR"]},{"code":"finance.compliance.manage","name":"Manage Compliance","description":"Run tax and compliance checks, manage regulatory reports","category":"finance","default_roles":["CFO","TAX_MGR"]}],"events":{"published":["TRANSACTION_POSTED","BUDGET_OVERRUN_ALERT","RECON_COMPLETED","COMPLIANCE_VIOLATION"],"subscribed":["SALES_INVOICE_CREATED","PROCUREMENT_PO_APPROVED"]}}',
    'system'
);

-- vFinacc permissions
INSERT INTO kernel_permissions (app_id, permission_code, name, description, category) VALUES
('com.vcorp.vfinacc', 'finance.ledger.view', 'View Ledger', 'View journal entries and financial reports', 'finance'),
('com.vcorp.vfinacc', 'finance.ledger.post', 'Post Ledger Entries', 'Create and post journal entries to the general ledger', 'finance'),
('com.vcorp.vfinacc', 'finance.transaction.approve', 'Approve Transactions', 'Approve and reconcile financial transactions', 'finance'),
('com.vcorp.vfinacc', 'finance.compliance.manage', 'Manage Compliance', 'Run tax and compliance checks, manage regulatory reports', 'finance');
