from src.main.ui.pages.base_page import BasePage

class EditBuildPage(BasePage):
        
    def url(self, build_config_id: str) -> str:
        return f"/admin/editBuild.html?id=buildType:{build_config_id}"
    
    @property
    def delete_link(self):
        return self.page.get_by_role("link", name="Delete...", exact=True)
    
    @property
    def actions_button(self):
        return self.page.locator('[data-hint-container-id="build-configuration-admin-actions"] button').first
    
    def delete_build_configuration(self):
        self.actions_button.click()
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.delete_link.click()
        self.page.wait_for_load_state("domcontentloaded")
        from src.main.ui.pages.projects_page import ProjectsPage
        return self.get_page(ProjectsPage)
    
    def should_not_have_build_configuration(self, build_config_name):
        assert not self.page.get_by_role("link", name=build_config_name).is_visible(), \
            f"Build configuration '{build_config_name}' was found but should have been deleted"