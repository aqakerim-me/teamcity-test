from src.main.ui.pages.base_page import BasePage
import time


class EditBuildRunnersPage(BasePage):
    def url(self, build_type_id: str) -> str:
        return f"/admin/editBuildRunners.html?id=buildType:{build_type_id}"
    
    @property
    def add_build_step_button(self):
        return self.page.locator("span:has-text('Add build step')").locator("xpath=ancestor::a")
    
    @property
    def command_line_step(self):
        return self.page.locator("div[data-test='build-step-selector-item runner']:has-text('Command Line')")
    
    @property
    def step_name_input(self):
        """Input field for the build step name"""
        return self.page.locator("input#buildStepName")
    
    @property
    def custom_script_input(self):
        return self.page.locator(".CodeMirror-lines")
    
    @property
    def save_button(self):
        return self.page.locator("div[id='saveButtons'] input[type='submit'][value='Save']")

    def add_command_line_step(self, step_name: str, script: str):
        """Add a Command Line build step"""
        # Wait for page to fully load
        self.page.wait_for_load_state("domcontentloaded")
        
        try:
            self.page.locator("text=Loading...").wait_for(state="hidden", timeout=30000)
        except:
            pass
        
        time.sleep(2)
        
        # Click "Add build step" button
        self.add_build_step_button.wait_for(state="visible", timeout=10000)
        self.add_build_step_button.click()
        self.page.wait_for_load_state("networkidle")
        
        # Click "Command Line" option
        self.command_line_step.wait_for(state="visible", timeout=10000)
        self.command_line_step.click()
        self.page.wait_for_load_state("networkidle")
        
        # Enter step name
        self.step_name_input.wait_for(state="visible", timeout=5000)
        self.step_name_input.fill(step_name)
        
        # Enter script in CodeMirror
        self.custom_script_input.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.type(script)
        
        # Save the step
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")
        
        return self

    def should_have_build_step(self, step_name: str):
        """Verify build step was created"""
        # Wait for page to fully load after save
        self.page.wait_for_load_state("domcontentloaded")
        time.sleep(2)
        
        # Try to find the step - it should be in a table row
        # Look for the step name in any element
        step = self.page.locator(f"text='{step_name}'").first
        
        # Wait for it to appear
        step.wait_for(state="visible", timeout=15000)
        
        return self