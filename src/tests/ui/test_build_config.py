import pytest
from playwright.sync_api import Page

from src.main.ui.pages.edit_build_runners_page import EditBuildRunnersPage
from src.main.api.models.create_buildtype_request import CreateBuildTypeRequest
from src.main.ui.pages.create_build_config_page import CreateBuildConfigurationPage
from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.generate_data import GenerateData
from src.main.api.models.create_project_request import CreateProjectRequest
from src.main.ui.pages.projects_page import ProjectsPage
from src.tests.ui.base_test import BaseUITest


@pytest.mark.ui
class TestCreateBuildConfiguration(BaseUITest):
    def test_admin_can_create_build_configuration(
        self, page: Page, api_manager: ApiManager):
        
        # pre steps: create a project via API
        create_project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name()
        )
        created_project = api_manager.admin_steps.create_project(create_project_request)     
           
        self.auth_as_admin(page)

        # ui steps
        build_config_name = GenerateData.get_build_configuration_name()
        projects_page = ProjectsPage(page).open()
        
        create_build_config_page: CreateBuildConfigurationPage = projects_page.click_new_build_configuration(created_project.name)
        projects_page: ProjectsPage = create_build_config_page.create_build_configuration(build_config_name)
        
        projects_page.should_have_build_configuration(build_config_name)


    def test_add_build_step(self, page: Page, api_manager: ApiManager):
        self.auth_as_admin(page)
        
        # Create project
        created_project = api_manager.admin_steps.create_project(
            CreateProjectRequest(
                id=GenerateData.get_project_id(), 
                name=GenerateData.get_project_name()
            )
        )
        
        build_config = api_manager.admin_steps.create_buildtype(
            CreateBuildTypeRequest(
                id=created_project.id,
                name=GenerateData.get_project_name(),
                project={"id": created_project.id}
            )
        )
        
        step_name = GenerateData.get_step_name()
        step_script = GenerateData.get_step_script()
        
        edit_runners_page = EditBuildRunnersPage(page).open(build_config.id)
        edit_runners_page.add_command_line_step(step_name, step_script)
        edit_runners_page.should_have_build_step(step_name)
        
        
    def test_cancel_build_configuration_creation(self, page: Page, api_manager: ApiManager):
        self.auth_as_admin(page)

        # pre steps: create a project via API
        create_project_request = CreateProjectRequest(
            id=GenerateData.get_project_id(),
            name=GenerateData.get_project_name()
        )
        created_project = api_manager.admin_steps.create_project(create_project_request)     
           
        # ui steps
        build_config_name = GenerateData.get_build_configuration_name()
        projects_page = ProjectsPage(page).open()
        
        create_build_config_page: CreateBuildConfigurationPage = projects_page.click_new_build_configuration(created_project.name)
        create_build_config_page.cancel_button.click()
        
        projects_page.should_not_have_build_configuration(build_config_name)