import pytest
from playwright.sync_api import Page

from src.main.ui.pages.edit_build_runners_page import EditBuildRunnersPage
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.ui.pages.projects_page import ProjectsPage
from src.main.ui.pages.edit_build_page import EditBuildPage
from src.main.ui.pages.build_config_page import BuildConfigPage

@pytest.mark.test
class TestBuildConfiguration():
    @pytest.mark.admin_session
    def test_admin_can_create_build_configuration(
        self, page: Page, api_manager: ApiManager, created_project
    ):
        build_config_name = GenerateData.get_build_configuration_name()
        
        ProjectsPage(page)\
            .open()\
            .click_new_build_configuration(created_project.name, created_project.id)\
            .create_build_configuration(build_config_name)\
            .should_have_build_configuration(build_config_name)
            
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert any(
            build_config.name == build_config_name for build_config in build_types
        ), "Build configuration was not created successfully"
        

    @pytest.mark.admin_session
    def test_admin_can_delete_build_configuration(
        self, page: Page, api_manager: ApiManager, build_config
    ):
        EditBuildPage(page)\
            .open(build_config.id)\
            .delete_build_configuration()\
            .should_not_have_build_configuration(build_config.name)
            
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert not any(
            bt.name == build_config.name for bt in build_types
        ), f"Build configuration '{build_config.name}' was not deleted properly"
        

    @pytest.mark.admin_session
    def test_cancel_build_configuration_creation(
        self, page: Page, api_manager: ApiManager, created_project
    ):
        build_config_name = GenerateData.get_build_configuration_name()  
           
        ProjectsPage(page)\
            .open()\
            .click_new_build_configuration(created_project.name, created_project.id)\
            .click_cancel()\
            .should_not_have_build_configuration(build_config_name)
            
        build_types = api_manager.admin_steps.get_all_buildtypes()
        assert not any(
            build_config.name == build_config_name for build_config in build_types
        ), "Build configuration was created when it should have been cancelled"
        
        
    @pytest.mark.admin_session
    def test_pause_and_activate_build_configuration(self, page: Page, api_manager: ApiManager, build_config):
        build_config_page = BuildConfigPage(page).open(build_config.id)
        
        build_config_page\
            .pause_build_configuration()\
            .should_be_paused()

        assert api_manager.admin_steps.get_buildtype_paused_status(build_config.id), \
            f"Expected build config '{build_config.id}' to be paused via API"
            
        build_config_page\
            .activate_build_configuration()\
            .should_not_be_paused()
            
        assert not api_manager.admin_steps.get_buildtype_paused_status(build_config.id), \
            f"Expected build config '{build_config.id}' to be active via API"
            

    @pytest.mark.admin_session
    def test_add_build_step(self, page: Page, api_manager: ApiManager, build_config):
        step_name = GenerateData.get_step_name()
        step_script = GenerateData.get_step_script()
        
        EditBuildRunnersPage(page)\
            .open(build_config.id)\
            .add_command_line_step(step_name, step_script)\
            .should_have_build_step(step_name)

        build_steps = api_manager.admin_steps.get_build_steps(build_config.id)
        step = next((step for step in build_steps if step.name == step_name), None)
        assert step is not None, f"Step with name '{step_name}' not found in build steps list"
        
    