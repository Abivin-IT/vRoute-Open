-- V11: Mark built-in kernel stub apps as INACTIVE so they no longer appear
-- in the Business Apps section of the shell. The "/dashboard/settings" and
-- "/dashboard/appstore" routes (System section) replace these entries.
-- Dependency checks still pass because deps are validated at install-time only.
UPDATE kernel_app_registry
   SET status = 'INACTIVE'
 WHERE app_id IN ('com.vcorp.kernel.settings', 'com.vcorp.kernel.appstore');
