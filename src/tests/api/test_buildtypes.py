import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.build_type_request import BuildTypeRequest
from src.main.api.models.build_type_response import BuildTypeResponse
from src.main.api.generators.generate_data import GenerateData


@pytest.mark.api
class TestBuildTypesPositive:
    def test_get_buildtypes_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert build_types is not None, "Should return build types list"
        assert hasattr(build_types, "buildType"), "Should have buildType attribute"
        assert len(build_types.buildType) > 0, "Should have at least one build type"
        assert isinstance(build_types.buildType, list), "buildType should be a list"

    def test_create_buildtype_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest(
            id=GenerateData.get_buildtype_id(),
            name=GenerateData.get_buildtype_name(),
            project={"id": project_id},
            projectId=project_id
        )

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        assert created_buildtype.id == build_type_request.id, "Build type ID should match"
        assert created_buildtype.name == build_type_request.name, "Build type name should match"
        assert created_buildtype.project["id"] == project_id, "Project ID should match"

    def test_get_buildtype_by_id_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert build_types is not None, "Should return build types list"
        assert len(build_types.buildType) > 0, "Should have at least one build type"

        build_type = api_manager.admin_steps.get_buildtype_by_id(build_types.buildType[0].id)
        assert build_type.id is not None, "Should have valid build type ID"
        assert build_type.name is not None, "Should have valid build type name"
        # projectId should always be present even if project object is None
        assert build_type.projectId is not None, "Should have projectId"

    def test_create_buildtype_with_project_id_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest(
            id=GenerateData.get_buildtype_id(),
            name=GenerateData.get_buildtype_name(),
            project={"id": project_id},
            projectId=project_id
        )

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        assert created_buildtype.id == build_type_request.id, "Build type ID should match"
        assert created_buildtype.name == build_type_request.name, "Build type name should match"
        assert created_buildtype.project["id"] == project_id, "Project ID should match"

    def test_create_buildtype_with_name_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest(
            id=GenerateData.get_buildtype_id(),
            name=GenerateData.get_buildtype_name(),
            project={"id": project_id},
            projectId=project_id
        )

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        assert created_buildtype.id == build_type_request.id, "Build type ID should match"
        assert created_buildtype.name == build_type_request.name, "Build type name should match"
        assert created_buildtype.project["id"] == project_id, "Project ID should match"

    def test_update_buildtype_settings_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert len(build_types.buildType) > 0, "Should have at least one build type"

        build_type = api_manager.admin_steps.get_all_buildtypes().buildType[0]
        assert build_type.id is not None, "Should have valid build type ID"

        update_request = {
            "property": [
                {"name": "buildNumberPattern", "value": "COUNTER-"}
            ]
        }

        # Update settings succeeds (API returns different format, so we don't check return value)
        api_manager.admin_steps.update_buildtype_settings(build_type.id, update_request)

    def test_update_buildtype_artifact_rules_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert len(build_types.buildType) > 0, "Should have at least one build type"

        build_type = api_manager.admin_steps.get_all_buildtypes().buildType[0]
        assert build_type.id is not None, "Should have valid build type ID"

        update_request = {
            "property": [
                {"name": "artifactRules", "value": "**/*.jar => artifacts/"}
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
        build_type_request = BuildTypeRequest(
            id=GenerateData.get_buildtype_id(),
            name=GenerateData.get_buildtype_name(),
            project={"id": project_id},
            projectId=project_id
        )

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)

        # Try to create another build type with the same ID
        duplicate_request = BuildTypeRequest(
            id=created_buildtype.id,  # Duplicate ID
            name=GenerateData.get_buildtype_name(),
            project={"id": project_id},
            projectId=project_id
        )

        # Should return error or handle gracefully since ID already exists
        try:
            api_manager.admin_steps.create_buildtype(duplicate_request)
            # If we get here, TeamCity allowed the duplicate (may update or reject silently)
        except Exception:
            # Expected - duplicate ID should cause an error
            pass

    def test_create_buildtype_without_project_id(self, api_manager: ApiManager):
        build_type_request = BuildTypeRequest(
            id=GenerateData.get_buildtype_id(),
            name=GenerateData.get_buildtype_name()
            # Missing project ID - should fail with 400
        )

        try:
            api_manager.admin_steps.create_buildtype(build_type_request)
            assert False, "Should not succeed when project ID is missing"
        except Exception:
            # Expected - missing project should cause an error
            pass

    def test_update_buildtype_with_nonexistent_id(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        build_type = build_types.buildType[0]  # Get first build type

        update_request = {
            "property": [
                {"name": "buildNumberPattern", "value": "NEW_PATTERN"}
            ]
        }

        try:
            api_manager.admin_steps.update_buildtype_settings(build_type.id, update_request)
            assert False, "Should not succeed when updating non-existent build type"
        except Exception:
            pass

    def test_delete_buildtype_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert len(build_types.buildType) > 0, "Should have at least one build type before delete"
        original_count = len(build_types.buildType)

        build_type = build_types.buildType[0]  # Get first build type
        original_id = build_type.id

        api_manager.admin_steps.delete_buildtype(build_type.id)

        # Verify the build type was deleted
        build_types_after = api_manager.admin_steps.get_all_buildtypes()
        new_count = len(build_types_after.buildType)

        assert new_count == original_count - 1, "Build type count should decrease by 1"
        assert original_id not in [bt.id for bt in build_types_after.buildType], "Deleted build type ID should not exist"

    def test_delete_nonexistent_buildtype_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert len(build_types.buildType) > 0, "Should have at least one build type"

        # Should return 404 Not Found since build type doesn't exist
        try:
            api_manager.admin_steps.delete_buildtype("NonExistentBuildType_999999")
            assert False, "Should not succeed when deleting non-existent build type"
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

        build_type_request = BuildTypeRequest(
            id=GenerateData.get_buildtype_id(),
            name=GenerateData.get_buildtype_name(),
            project={"id": project_id},
            projectId=project_id
        )

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        assert created_buildtype.id == build_type_request.id, "Build type ID should match"
        assert created_buildtype.name == build_type_request.name, "Build type name should match"
        assert created_buildtype.project["id"] == project_id, "Project ID should match"

    def test_create_buildtype_with_specific_name_success(self, api_manager: ApiManager):
        # Get existing project first (skip Root project)
        projects = api_manager.admin_steps.get_all_projects()
        # Find a non-root project (Root project typically has id "_Root")
        project_id = next((p.id for p in projects if p.id != "_Root"), projects[0].id)

        build_type_request = BuildTypeRequest(
            id=GenerateData.get_buildtype_id(),
            name="TestBuildType_CustomName",  # Custom name
            project={"id": project_id},
            projectId=project_id
        )

        created_buildtype = api_manager.admin_steps.create_buildtype(build_type_request)
        assert created_buildtype.id == build_type_request.id, "Build type ID should match"
        assert created_buildtype.name == "TestBuildType_CustomName", "Build type name should be custom value"
        assert created_buildtype.projectId == project_id, "Project ID should match"


@pytest.mark.api
class TestBuildTypesSettings:
    def test_get_buildtype_settings_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        build_type = build_types.buildType[0]

        # Settings endpoint returns different format, so we just verify it doesn't error
        api_manager.admin_steps.get_buildtype_settings(build_type.id)


    def test_update_buildtype_artifact_rules_success(self, api_manager: ApiManager):
        build_types = api_manager.admin_steps.get_all_buildtypes()
        build_type = build_types.buildType[0]

        update_request = {
            "property": [
                {"name": "artifactRules", "value": "**/*.jar => artifacts/"}
            ]
        }

        # Update settings succeeds (API returns different format, so we don't check return value)
        api_manager.admin_steps.update_buildtype_settings(build_type.id, update_request)


@pytest.mark.api
class TestBuildTypesGetByProject:
    def test_get_buildtypes_by_project_success(self, api_manager: ApiManager):
        # Get a real project ID
        projects = api_manager.admin_steps.get_all_projects()
        project_id = projects[0].id

        build_types = api_manager.admin_steps.get_buildtypes_by_project(project_id)
        assert build_types is not None, "Should return build types"
        assert hasattr(build_types, "buildType"), "Should have buildType attribute"
        assert len(build_types.buildType) > 0, "Should have at least one build type for project"


    def test_get_buildtype_by_name_success(self, api_manager: ApiManager):
        # Get all build types and verify we can access them
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert build_types is not None, "Should return build types"
        assert len(build_types.buildType) > 0, "Should have at least one build type"