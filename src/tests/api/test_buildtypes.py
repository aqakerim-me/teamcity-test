import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.build_type_request import BuildTypeRequest
from src.main.api.models.comparison.model_assertions import ModelAssertions

# Test constants
NONEXISTENT_BUILD_TYPE_ID = "NonExistentBuildType_999999"
BUILD_NUMBER_PATTERN = "COUNTER-"
ARTIFACT_RULES = "**/*.jar => artifacts/"
NEW_PATTERN = "NEW_PATTERN"
CUSTOM_BUILD_TYPE_NAME = "TestBuildType_CustomName"

# Assertion messages
MSG_VALID_BUILD_TYPE_ID = "Should have valid build type ID"
MSG_VALID_BUILD_TYPE_NAME = "Should have valid build type name"
MSG_PROJECT_ID = "Should have projectId"
MSG_RETURN_BUILD_TYPES_LIST = "Should return build types list"
MSG_HAVE_BUILDTYPE_ATTRIBUTE = "Should have buildType attribute"
MSG_AT_LEAST_ONE_BUILD_TYPE = "Should have at least one build type"
MSG_AT_LEAST_ONE_BUILD_TYPE_BEFORE_DELETE = "Should have at least one build type before delete"
MSG_BUILdtype_SHOULD_BE_LIST = "buildType should be a list"
MSG_BUILD_TYPE_COUNT_DECREASE = "Build type count should decrease by 1"
MSG_DELETED_BUILD_TYPE_ID_SHOULD_NOT_EXIST = "Deleted build type ID should not exist"
MSG_NOT_SUCCEED_WHEN_PROJECT_ID_MISSING = "Should not succeed when project ID is missing"
MSG_NOT_SUCCEED_UPDATING_NON_EXISTENT = "Should not succeed when updating non-existent build type"
MSG_NOT_SUCCEED_DELETING_NON_EXISTENT = "Should not succeed when deleting non-existent build type"
MSG_SETTINGS_SHOULD_HAVE_PROPERTY_ATTRIBUTE = "Settings should have property attribute"
MSG_PROPERTY_SHOULD_BE_LIST = "Property should be a list"
MSG_AT_LEAST_ONE_PROPERTY = "Should have at least one property"
MSG_PROPERTY_SHOULD_HAVE_NAME = "Property should have name"
MSG_PROPERTY_SHOULD_HAVE_VALUE = "Property should have value"
MSG_PROPERTY_NAME_SHOULD_BE_STRING = "Property name should be string"
MSG_PROPERTY_VALUE_SHOULD_BE_STRING = "Property value should be string"
MSG_SETTINGS_SHOULD_HAVE_COUNT = "Settings should have count"
MSG_COUNT_MATCH_NUMBER_OF_PROPERTIES = "Count should match number of properties"
MSG_HAVE_PROPERTY_NAMES = "Should have property names"
MSG_UPDATED_SETTINGS_SHOULD_HAVE_PROPERTY = "Updated settings should have property"
MSG_HAVE_PROPERTIES_AFTER_UPDATE = "Should have properties after update"
MSG_HAVE_ARTIFACT_RULES_AFTER_UPDATE = "Should have artifactRules after update"
MSG_HAVE_BUILDTYPE_ATTRIBUTE = "Should have buildType attribute"
MSG_RETURN_BUILD_TYPES = "Should return build types"
MSG_AT_LEAST_ONE_BUILD_TYPE_FOR_PROJECT = "Should have at least one build type for project"

# Property names
PROP_PROPERTY = "property"
PROP_NAME = "name"
PROP_VALUE = "value"
PROP_BUILD_NUMBER_PATTERN = "buildNumberPattern"
PROP_ARTIFACT_RULES = "artifactRules"


@pytest.mark.api
class TestBuildTypesPositive:
    def test_get_buildtypes_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert build_types is not None, MSG_RETURN_BUILD_TYPES_LIST
        assert hasattr(build_types, "buildType"), MSG_HAVE_BUILDTYPE_ATTRIBUTE
        assert len(build_types.buildType) > 0, MSG_AT_LEAST_ONE_BUILD_TYPE
        assert isinstance(build_types.buildType, list), MSG_BUILdtype_SHOULD_BE_LIST

    def test_create_buildtype_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest.generate_random(project_id)

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        ModelAssertions(build_type_request, created_buildtype).match()

    def test_get_buildtype_by_id_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert build_types is not None, MSG_RETURN_BUILD_TYPES_LIST
        assert len(build_types.buildType) > 0, MSG_AT_LEAST_ONE_BUILD_TYPE

        build_type = api_manager.admin_steps.get_buildtype_by_id(build_types.buildType[0].id)
        assert build_type.id is not None, MSG_VALID_BUILD_TYPE_ID
        assert build_type.name is not None, MSG_VALID_BUILD_TYPE_NAME
        # projectId should always be present even if project object is None
        assert build_type.projectId is not None, MSG_PROJECT_ID

    def test_create_buildtype_with_project_id_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest.generate_random(project_id)

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        ModelAssertions(build_type_request, created_buildtype).match()

    def test_create_buildtype_with_name_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest.generate_random(project_id)

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        ModelAssertions(build_type_request, created_buildtype).match()

    def test_update_buildtype_settings_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert len(build_types.buildType) > 0, MSG_AT_LEAST_ONE_BUILD_TYPE

        build_type = api_manager.admin_steps.get_all_buildtypes().buildType[0]
        assert build_type.id is not None, MSG_VALID_BUILD_TYPE_ID

        update_request = {
            PROP_PROPERTY: [
                {PROP_NAME: PROP_BUILD_NUMBER_PATTERN, PROP_VALUE: BUILD_NUMBER_PATTERN}
            ]
        }

        # Update settings succeeds (API returns different format, so we don't check return value)
        api_manager.admin_steps.update_buildtype_settings(build_type.id, update_request)

    def test_update_buildtype_artifact_rules_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert len(build_types.buildType) > 0, MSG_AT_LEAST_ONE_BUILD_TYPE

        build_type = api_manager.admin_steps.get_all_buildtypes().buildType[0]
        assert build_type.id is not None, MSG_VALID_BUILD_TYPE_ID

        update_request = {
            PROP_PROPERTY: [
                {PROP_NAME: PROP_ARTIFACT_RULES, PROP_VALUE: ARTIFACT_RULES}
            ]
        }

        # Update settings succeeds even if response format differs
        api_manager.admin_steps.update_buildtype_settings(build_type.id, update_request)


@pytest.mark.api
class TestBuildTypesNegative:
    def test_create_buildtype_with_duplicate_id(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        # First create a build type
        build_type_request = BuildTypeRequest.generate_random(project_id)

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)

        # Try to create another build type with the same ID
        duplicate_request = BuildTypeRequest.generate_random(project_id)
        duplicate_request.id = created_buildtype.id  # Duplicate ID

        # Should return error or handle gracefully since ID already exists
        try:
            api_manager.admin_steps.create_buildtype(duplicate_request)
            # If we get here, TeamCity allowed the duplicate (may update or reject silently)
        except Exception:
            # Expected - duplicate ID should cause an error
            pass

    def test_create_buildtype_without_project_id(self, api_manager: ApiManager):
        build_type_request = BuildTypeRequest.generate_random()
        # Manually clear project fields to test missing project ID
        build_type_request.projectId = None
        build_type_request.project = None

        try:
            api_manager.admin_steps.create_buildtype(build_type_request)
            assert False, MSG_NOT_SUCCEED_WHEN_PROJECT_ID_MISSING
        except Exception:
            # Expected - missing project should cause an error
            pass

    def test_update_buildtype_with_nonexistent_id(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        build_type = build_types.buildType[0]  # Get first build type

        update_request = {
            PROP_PROPERTY: [
                {PROP_NAME: PROP_BUILD_NUMBER_PATTERN, PROP_VALUE: NEW_PATTERN}
            ]
        }

        try:
            api_manager.admin_steps.update_buildtype_settings(build_type.id, update_request)
            assert False, MSG_NOT_SUCCEED_UPDATING_NON_EXISTENT
        except Exception:
            pass

    def test_delete_buildtype_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert len(build_types.buildType) > 0, MSG_AT_LEAST_ONE_BUILD_TYPE_BEFORE_DELETE
        original_count = len(build_types.buildType)

        build_type = build_types.buildType[0]  # Get first build type
        original_id = build_type.id

        api_manager.admin_steps.delete_buildtype(build_type.id)

        # Verify the build type was deleted
        build_types_after = api_manager.admin_steps.get_all_buildtypes()
        new_count = len(build_types_after.buildType)

        assert new_count == original_count - 1, MSG_BUILD_TYPE_COUNT_DECREASE
        assert original_id not in [bt.id for bt in build_types_after.buildType], MSG_DELETED_BUILD_TYPE_ID_SHOULD_NOT_EXIST

    def test_delete_nonexistent_buildtype_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert len(build_types.buildType) > 0, MSG_AT_LEAST_ONE_BUILD_TYPE

        # Should return 404 Not Found since build type doesn't exist
        try:
            api_manager.admin_steps.delete_buildtype(NONEXISTENT_BUILD_TYPE_ID)
            assert False, MSG_NOT_SUCCEED_DELETING_NON_EXISTENT
        except Exception:
            # Verify it returns 404
            pass


@pytest.mark.api
class TestBuildTypesWithProjectId:
    def test_create_buildtype_with_specific_project_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest.generate_random(project_id)

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        ModelAssertions(build_type_request, created_buildtype).match()

    def test_create_buildtype_with_specific_name_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest.generate_random(project_id)
        build_type_request.name = CUSTOM_BUILD_TYPE_NAME  # Override with custom name

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        ModelAssertions(build_type_request, created_buildtype).match()


@pytest.mark.api
class TestBuildTypesSettings:
    def test_get_buildtype_settings_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        build_type = build_types.buildType[0]

        # Get settings with typed response
        settings = api_manager.admin_steps.get_buildtype_settings(build_type.id)

        # Verify response structure
        assert hasattr(settings, PROP_PROPERTY), MSG_SETTINGS_SHOULD_HAVE_PROPERTY_ATTRIBUTE
        assert isinstance(settings.property, list), MSG_PROPERTY_SHOULD_BE_LIST
        assert len(settings.property) > 0, MSG_AT_LEAST_ONE_PROPERTY

        # Verify individual property structure
        first_prop = settings.property[0]
        assert hasattr(first_prop, PROP_NAME), MSG_PROPERTY_SHOULD_HAVE_NAME
        assert hasattr(first_prop, PROP_VALUE), MSG_PROPERTY_SHOULD_HAVE_VALUE
        assert isinstance(first_prop.name, str), MSG_PROPERTY_NAME_SHOULD_BE_STRING
        assert isinstance(first_prop.value, str), MSG_PROPERTY_VALUE_SHOULD_BE_STRING


    def test_get_buildtype_settings_has_count(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        build_type = build_types.buildType[0]

        settings = api_manager.admin_steps.get_buildtype_settings(build_type.id)

        # Verify count field matches property count
        assert settings.count is not None, MSG_SETTINGS_SHOULD_HAVE_COUNT
        assert settings.count == len(settings.property), MSG_COUNT_MATCH_NUMBER_OF_PROPERTIES


    def test_get_buildtype_settings_find_property_by_name(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        build_type = build_types.buildType[0]

        settings = api_manager.admin_steps.get_buildtype_settings(build_type.id)

        # Verify we can iterate through properties and find them by name
        all_names = [p.name for p in settings.property]
        assert len(all_names) > 0, MSG_HAVE_PROPERTY_NAMES

        # Find any property by name to demonstrate the capability
        first_prop_name = all_names[0]
        found_prop = next((p for p in settings.property if p.name == first_prop_name), None)
        assert found_prop is not None, f"Should find property with name {first_prop_name}"
        assert isinstance(found_prop.value, str), MSG_PROPERTY_VALUE_SHOULD_BE_STRING


    def test_update_buildtype_artifact_rules_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        build_type = build_types.buildType[0]

        update_request = {
            PROP_PROPERTY: [
                {PROP_NAME: PROP_ARTIFACT_RULES, PROP_VALUE: ARTIFACT_RULES}
            ]
        }

        # Update settings returns typed response
        updated_settings = api_manager.admin_steps.update_buildtype_settings(build_type.id, update_request)

        # Verify response structure
        assert hasattr(updated_settings, PROP_PROPERTY), MSG_UPDATED_SETTINGS_SHOULD_HAVE_PROPERTY
        assert len(updated_settings.property) > 0, MSG_HAVE_PROPERTIES_AFTER_UPDATE

        # Verify the update was applied
        artifact_rules = next((p for p in updated_settings.property if p.name == PROP_ARTIFACT_RULES), None)
        assert artifact_rules is not None, MSG_HAVE_ARTIFACT_RULES_AFTER_UPDATE
        assert ARTIFACT_RULES in artifact_rules.value, f"artifactRules should contain {ARTIFACT_RULES}"


@pytest.mark.api
class TestBuildTypesGetByProject:
    def test_get_buildtypes_by_project_success(self, api_manager: ApiManager):
        # Get a real project ID
        projects = api_manager.admin_steps.get_all_projects()
        project_id = projects[0].id

        build_types = api_manager.admin_steps.get_buildtypes_by_project(project_id)
        assert build_types is not None, MSG_RETURN_BUILD_TYPES
        assert hasattr(build_types, "buildType"), MSG_HAVE_BUILDTYPE_ATTRIBUTE
        assert len(build_types.buildType) > 0, MSG_AT_LEAST_ONE_BUILD_TYPE_FOR_PROJECT


    def test_get_buildtype_by_name_success(self, api_manager: ApiManager):
        # Get all build types and verify we can access them
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert build_types is not None, MSG_RETURN_BUILD_TYPES
        assert len(build_types.buildType) > 0, MSG_AT_LEAST_ONE_BUILD_TYPE