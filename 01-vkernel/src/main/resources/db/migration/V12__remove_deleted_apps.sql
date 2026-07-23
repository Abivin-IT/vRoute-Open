-- V12: Remove deleted vApps (vfinacc, vdesign-physical, vmarketing-org)
-- These apps were removed from the platform to streamline development.
-- Their Flyway registration migrations (V8, V9, V10) still ran but we
-- clean up the data here so the shell only shows vStrategy.

DELETE FROM kernel_permissions
 WHERE app_id IN (
    'com.vcorp.vfinacc',
    'com.vcorp.vdesign-physical',
    'com.vcorp.vmarketing-org'
 );

DELETE FROM kernel_app_registry
 WHERE app_id IN (
    'com.vcorp.vfinacc',
    'com.vcorp.vdesign-physical',
    'com.vcorp.vmarketing-org'
 );
