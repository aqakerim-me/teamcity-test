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
PROJECT_ID_INPUT = '[data-test="project-id-input"]'
PROJECT_NAME_INPUT = '[data-test="project-name-input"]'
PROJECT_SUBMIT_BUTTON = '[data-test="submit"]'
PROJECT_WELCOME_TEXT = "main h1, h1"
PROJECT_NAVIGATION_MENU = '[data-test="sidebar"], nav'

# Build Configuration page selectors
BUILD_RUN_BUTTON = 'button:has-text("Run"), .run-button, .runBtn, input[value="Run"], .btn_run, .run'
BUILD_RUN_BUTTON_DROPDOWN = 'a[title*="Run"], .runMenu, a.run-menu-trigger'
BUILD_STATUS_INDICATOR = '[data-test="build-status"], .build-status, .statusIcon'
BUILD_QUEUE_ITEM = '[data-test="build-queue-item"], .build-queue-item, .queuedBuild'
BUILD_HISTORY_LIST = '[data-test="build-history"], .build-history, .buildsList'
BUILD_CONFIGURATION_PAGE = 'buildConfiguration.html'
BUILD_TYPE_LINK = 'a[href*="buildTypeId"]'
BUILD_DETAILS_PAGE = 'viewLog.html'
BUILD_STATE_TEXT = '[data-test="build-state"], .build-state'
BUILD_PAGE_HEADER = '.pageHeader, .header, .toolbar'

# Build Results page selectors
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
BUILD_LOG_TAB = (
    '#mainContent span.ring-tabs-visible:has-text("Build Log"), '
    '#mainContent a:has-text("Build Log"), '
    '#mainContent span:has-text("Build Log")'
)
BUILD_LOG_CONTAINER = '#mainContent [data-log-row], #mainContent [data-log-message], #mainContent [class*="BuildLog"]'
BUILD_LOG_LINE = '#mainContent [data-log-row="true"], #mainContent [data-test-log-message="true"]'
BUILD_LOG_TIMESTAMP = '[data-test-log-message-time="true"], [data-log-message-time="true"]'
BUILD_ARTIFACTS_TAB = (
    '#mainContent span.ring-tabs-visible:has-text("Artifacts"), '
    '#mainContent a:has-text("Artifacts"), '
    '#mainContent span:has-text("Artifacts")'
)
BUILD_ARTIFACTS_LIST = '#mainContent [class*="artifacts"], #mainContent [class*="Artifacts"]'
BUILD_ARTIFACT_DOWNLOAD_LINK = (
    '#mainContent a[href*="/repository/download/"], '
    '#mainContent a[href*="guestAuth/repository/download"], '
    '#mainContent a[href*="download"]'
)

# Build Queue page selectors
BUILD_QUEUE_TITLE = '#mainContent h1'
BUILD_QUEUE_ROWS = '#mainContent [data-test*="queue-row"], #mainContent [class*="QueueBuild"], #mainContent tr'
BUILD_QUEUE_BUILD_TYPE_CELL = '#mainContent [class*="buildType"], #mainContent [class*="BuildType"], #mainContent a[href*="buildConfiguration"]'
BUILD_QUEUE_TIME_CELL = '#mainContent [class*="queuedDate"], #mainContent [class*="date"], #mainContent [class*="time"]'
BUILD_QUEUE_CANCEL_BUTTON = (
    '#mainContent button:has-text("Remove"), #mainContent button:has-text("Cancel"), #mainContent button:has-text("Stop"), '
    '#mainContent a:has-text("Remove"), #mainContent a:has-text("Cancel"), #mainContent a:has-text("Stop")'
)
