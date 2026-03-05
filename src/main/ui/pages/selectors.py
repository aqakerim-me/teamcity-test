ALERT_SELECTOR = '[data-test="alert"], .errorMessage, .error'
LOGIN_USERNAME_INPUT = (
    '[data-test="login-username"], input[name="username"], input[type="text"]'
)
LOGIN_PASSWORD_INPUT = (
    '[data-test="login-password"], input[name="password"], input[type="password"]'
)
LOGIN_BUTTON = '[data-test="login-submit"], button:has-text("Log in")'
LOGIN_ERROR_MESSAGE = (
    '#errorMessage:visible, [data-test="login-error"]:visible, .errorMessage:visible'
)
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
BUILD_RUN_BUTTON = '[data-test="run-build"], button:has-text("Run"), .runButton'
BUILD_STATUS_INDICATOR = '[data-test="build-status"], .build-status, .statusIcon'
BUILD_STATE_TEXT = '[data-test="build-state"], .buildStateText, .status-text'
BUILD_RUN_BUTTON = '[data-test="run-build"], button:has-text("Run"), .runButton'
BUILD_STATUS_INDICATOR = '[data-test="build-status"], .build-status, .statusIcon'
BUILD_STATE_TEXT = '[data-test="build-state"], .buildStateText, .status-text'
BUILD_QUEUE_ROWS = '[data-test="queue-row"], .buildQueueRow, table tr:has(td)'
BUILD_QUEUE_TITLE = '[data-test="queue-title"], .queueTitle, h1'
BUILD_QUEUE_BUILD_TYPE_CELL = (
    '[data-test="build-type-cell"], td:first-child, .buildTypeName'
)
BUILD_QUEUE_TIME_CELL = '[data-test="queue-time-cell"], td:last-child, .queuedTime'
BUILD_QUEUE_CANCEL_BUTTON = (
    '[data-test="cancel-build"], button:has-text("Cancel"), .cancelBuild'
)
BUILD_ARTIFACT_DOWNLOAD_LINK = (
    '[data-test="artifact-download"], a[href*="artifacts"], .artifactLink'
)
BUILD_ARTIFACTS_LIST = '[data-test="artifacts-list"], .artifacts, #artifacts'
BUILD_ARTIFACTS_TAB = '[data-test="artifacts-tab"], a:has-text("Artifacts")'
BUILD_LOG_CONTAINER = '[data-test="build-log"], .buildLog, #buildLog'
BUILD_LOG_LINE = '[data-test="log-line"], .logLine, .line'
BUILD_LOG_TAB = '[data-test="log-tab"], a:has-text("Build Log")'
BUILD_LOG_TIMESTAMP = '[data-test="log-timestamp"], .timestamp'
BUILD_RESULTS_STATUS_TEXT = (
    '[data-test="build-results-status"], .buildResultsStatus, .statusText'
)
BUILD_STOP_BUTTON = '[data-test="stop-build"], button:has-text("Stop"), .stopBuild'
BUILD_STOP_CONFIRM_BUTTON = (
    '[data-test="stop-confirm"], button:has-text("Stop build"), .confirmStop'
)
