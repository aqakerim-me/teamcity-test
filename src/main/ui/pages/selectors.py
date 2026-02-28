ALERT_SELECTOR = '[data-test="alert"], .errorMessage, .error'
LOGIN_USERNAME_INPUT = '[data-test="login-username"], input[name="username"], input[type="text"]'
LOGIN_PASSWORD_INPUT = '[data-test="login-password"], input[name="password"], input[type="password"]'
LOGIN_BUTTON = '[data-test="login-submit"], button:has-text("Log in")'
LOGIN_ERROR_MESSAGE = '#errorMessage:visible, [data-test="login-error"]:visible, .errorMessage:visible'
ADMIN_PANEL_TEXT = "h1"
ADMIN_CREATE_USER_BUTTON = '[data-test="create-user"]'
ADMIN_USERNAME_INPUT = '[data-test="username-input"], #input_teamcityUsername'
ADMIN_PASSWORD_INPUT = '[data-test="password-input"], #password1'
ADMIN_CONFIRM_PASSWORD_INPUT = '[data-test="confirm-password-input"], #retypedPassword'
ADMIN_SUBMIT_BUTTON = '[data-test="submit"], input[name="submitCreateUser"]'
ADMIN_USERS_LIST = '[data-test="users-list"], table'
PROJECTS_LIST = '[data-test="projects-list"], [data-test="sidebar"]'
CREATE_PROJECT_BUTTON = '[data-test="create-project"]'
PROJECT_ID_INPUT = '[data-test="project-id-input"], #projectId, input[name="projectId"], input[placeholder*="project id" i]'
PROJECT_NAME_INPUT = '[data-test="project-name-input"], #name, input[name="name"], input[placeholder*="project name" i]'
PROJECT_SUBMIT_BUTTON = '[data-test="submit"], input[type="submit"], button:has-text("Submit")'
PROJECT_WELCOME_TEXT = "main h1, h1"
PROJECT_NAVIGATION_MENU = '[data-test="sidebar"], nav'

# Build Configuration page selectors
BUILD_RUN_BUTTON = '[data-test="run-build"], button:has-text("Run")'
BUILD_STATUS_INDICATOR = '[data-test="status"], [class*="status"], .status'
BUILD_CONFIGURATION_PAGE = '.buildConfiguration, [data-test="build-configuration"]'
BUILD_STATE_TEXT = '[data-test="build-state"], .build-state, .statusText'

# Build Queue page selectors
BUILD_QUEUE_ROWS = 'table.queue tr, .queue-row, [data-test="queue-row"]'
BUILD_QUEUE_TITLE = 'h1, .pageHeader, [data-test="queue-title"]'
BUILD_QUEUE_BUILD_TYPE_CELL = 'td:first-child, .buildType, [data-test="build-type"]'
BUILD_QUEUE_TIME_CELL = 'td:last-child, .time, [data-test="queue-time"]'
BUILD_QUEUE_CANCEL_BUTTON = '[data-test="cancel"], button:has-text("Cancel"), .cancel'

# Build Results page selectors
BUILD_LOG_TAB = '[data-test="log-tab"], span:has-text("Build Log")'
BUILD_ARTIFACTS_TAB = '[data-test="artifacts-tab"], span:has-text("Artifacts")'
BUILD_LOG_CONTAINER = '[data-test="log-container"], .log-content, pre'
BUILD_LOG_LINE = '[data-test="log-line"], .log-line, div[class*="log"]'
BUILD_LOG_TIMESTAMP = '[data-test="log-timestamp"], .timestamp, [class*="time"]'
BUILD_ARTIFACTS_LIST = '[data-test="artifacts-list"], .artifacts-list, table.artifacts'
BUILD_ARTIFACT_DOWNLOAD_LINK = (
    'a[href*="/repository/download/"], '  # TeamCity artifact download URLs
    'a[href*="artifact"], '                # General artifact links
    '[data-test="artifact-download"], '    # Test attribute
    'table.artifacts tr:not(:has(td)) a, '# Artifact links in artifact table
    '.artifactList a'                      # Another common pattern
)
BUILD_RESULTS_STATUS_TEXT = (
    '#mainContent .StatusBadge-module__status--w9, '
    '#mainContent .Description-module__text--cQ, '
    '#mainContent [class*="status"]'
)
BUILD_STOP_BUTTON = (
    '#mainContent button:has-text("Stop"), '
    '#mainContent .StopBuild-module__stopBuild--KS, '
    '#mainContent button[class*="stop"], '
    '#mainContent input[value="Stop"]'
)
BUILD_STOP_CONFIRM_BUTTON = (
    '#stopBuildFormDialog input[value="Stop"], '
    '#stopBuildFormDialog .submitButton, '
    '#stopBuildFormDialog button:has-text("Stop"), '
    'button:has-text("Confirm"), input[value="Stop"]'
)
