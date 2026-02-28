import logging
import time
from contextlib import suppress
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.selectors import (
    BUILD_ARTIFACT_DOWNLOAD_LINK,
    BUILD_ARTIFACTS_LIST,
    BUILD_ARTIFACTS_TAB,
    BUILD_LOG_CONTAINER,
    BUILD_LOG_LINE,
    BUILD_LOG_TAB,
    BUILD_LOG_TIMESTAMP,
    BUILD_RESULTS_STATUS_TEXT,
    BUILD_STOP_BUTTON,
    BUILD_STOP_CONFIRM_BUTTON,
)
from src.main.ui.pages.ui_element import UIElement

logger = logging.getLogger(__name__)


class BuildResultsPage(BasePage):
    def __init__(self, page, build_id: int):
        super().__init__(page)
        self.build_id = build_id
        self.last_download_path: Path | None = None

    def url(self) -> str:
        return f"/viewLog.html?buildId={self.build_id}"

    @property
    def build_log_tab(self) -> UIElement:
        return UIElement(self.page.locator(BUILD_LOG_TAB).first, name="Build Log tab")

    @property
    def artifacts_tab(self) -> UIElement:
        return UIElement(self.page.locator(BUILD_ARTIFACTS_TAB).first, name="Artifacts tab")

    @property
    def status_text(self) -> UIElement:
        return UIElement(self.page.locator(BUILD_RESULTS_STATUS_TEXT).first, name="Build status text")

    def _click_first_visible(self, selectors: list[str]):
        for selector in selectors:
            locator = self.page.locator(selector)
            count = locator.count()
            for idx in range(count):
                candidate = locator.nth(idx)
                with suppress(Exception):
                    if candidate.is_visible(timeout=1_000):
                        candidate.click()
                        return True
        return False

    def open_build_log_tab(self):
        def _action():
            start = time.time()
            while int((time.time() - start) * 1000) < 10_000:
                clicked = self._click_first_visible(
                    [
                        BUILD_LOG_TAB,
                        '#mainContent span.ring-tabs-visible:has-text("Build Log")',
                        '#mainContent span:has-text("Build Log")',
                    ]
                )
                if clicked:
                    self.page.wait_for_load_state("domcontentloaded", timeout=10_000)
                    return self
                self.page.wait_for_timeout(500)

            # Fallback: open log tab via URL parameter.
            parsed = urlparse(self.page.url)
            query = parse_qs(parsed.query)
            query["buildTab"] = ["log"]
            query["logView"] = ["linear"]
            query["focusLine"] = ["1"]
            log_url = urlunparse(parsed._replace(query=urlencode(query, doseq=True)))
            self.page.goto(log_url, wait_until="domcontentloaded")
            return self

        return self._step(
            title=f"Open Build Log tab for build {self.build_id}",
            action=_action,
        )

    def open_artifacts_tab(self):
        def _action():
            start = time.time()
            while int((time.time() - start) * 1000) < 10_000:
                clicked = self._click_first_visible(
                    [
                        BUILD_ARTIFACTS_TAB,
                        '#mainContent span.ring-tabs-visible:has-text("Artifacts")',
                        '#mainContent span:has-text("Artifacts")',
                    ]
                )
                if clicked:
                    self.page.wait_for_load_state("domcontentloaded", timeout=10_000)
                    return self
                self.page.wait_for_timeout(500)

            parsed = urlparse(self.page.url)
            query = parse_qs(parsed.query)
            query["buildTab"] = ["artifacts"]
            artifacts_url = urlunparse(parsed._replace(query=urlencode(query, doseq=True)))
            self.page.goto(artifacts_url, wait_until="domcontentloaded")
            return self

        return self._step(
            title=f"Open Artifacts tab for build {self.build_id}",
            action=_action,
        )

    def should_have_realtime_log_updates(
        self,
        timeout: int = 15_000,
        poll_interval_ms: int = 1_000,
    ):
        def _action():
            container = self.page.locator(BUILD_LOG_CONTAINER).first
            with suppress(Exception):
                container.wait_for(state="visible", timeout=5_000)

            lines = self.page.locator(BUILD_LOG_LINE)
            start = time.time()
            initial_count = lines.count()

            # Allow small warm-up for first lines to appear.
            while initial_count == 0 and int((time.time() - start) * 1000) < timeout // 3:
                self.page.wait_for_timeout(300)
                initial_count = lines.count()

            current_max = initial_count
            while int((time.time() - start) * 1000) < timeout:
                self.page.wait_for_timeout(poll_interval_ms)
                current_count = lines.count()
                if current_count > current_max:
                    return self
                current_max = max(current_max, current_count)

            raise AssertionError(
                f"Build log did not update in realtime: initial={initial_count}, final={current_max}"
            )

        return self._step(
            title=f"Check realtime log updates for build {self.build_id}",
            action=_action,
        )

    def should_have_timestamps_for_log_lines(self, min_timestamped_lines: int = 1):
        def _action():
            timestamps = self.page.locator(BUILD_LOG_TIMESTAMP)
            count = timestamps.count()
            assert count >= min_timestamped_lines, (
                f"Expected at least {min_timestamped_lines} log timestamps, got {count}"
            )
            return self

        return self._step(
            title=f"Check log timestamps for build {self.build_id}",
            action=_action,
        )

    def stop_running_build(self):
        def _action():
            start = time.time()
            clicked = False
            while int((time.time() - start) * 1000) < 10_000 and not clicked:
                clicked = self._click_first_visible(
                    [
                        BUILD_STOP_BUTTON,
                        '#mainContent button:has-text("Stop")',
                        '#mainContent [class*="BuildOverviewProgress-module__stop"]',
                        '#mainContent [class*="StopBuild-module__stopBuild"]',
                    ]
                )
                if not clicked:
                    self.page.wait_for_timeout(500)

            if not clicked:
                # In some layouts stop control is only visible on Build Log tab.
                self.open_build_log_tab()
                clicked = self._click_first_visible(
                    [
                        BUILD_STOP_BUTTON,
                        '#mainContent button:has-text("Stop")',
                        '#mainContent [class*="BuildOverviewProgress-module__stop"]',
                        '#mainContent [class*="StopBuild-module__stopBuild"]',
                    ]
                )

            if not clicked:
                raise AssertionError("Stop action is not visible/clickable on build page")

            # Some TeamCity skins use an in-page confirm control.
            self.page.wait_for_timeout(500)
            self._click_first_visible(
                [
                    BUILD_STOP_CONFIRM_BUTTON,
                    '#stopBuildFormDialog input[value="Stop"]',
                    '#stopBuildFormDialog .submitButton',
                ]
            )

            return self

        return self._step(
            title=f"Stop running build {self.build_id}",
            action=_action,
        )

    def should_show_any_status(self, allowed_statuses: Iterable[str], timeout: int = 20_000):
        allowed = [status.lower() for status in allowed_statuses]

        def _action():
            start = time.time()
            while int((time.time() - start) * 1000) < timeout:
                page_text = (self.page.locator("#mainContent").inner_text() or "").lower()
                if any(status in page_text for status in allowed):
                    return self
                self.page.wait_for_timeout(500)

            raise AssertionError(
                f"Expected one of statuses {list(allowed_statuses)} in UI"
            )

        return self._step(
            title=f"Check build status is one of {list(allowed_statuses)}",
            action=_action,
        )

    def should_have_artifacts(self):
        def _action():
            with suppress(Exception):
                self.page.get_by_text("Show hidden artifacts").first.click(timeout=2_000)

            artifacts_list = self.page.locator(BUILD_ARTIFACTS_LIST)
            if artifacts_list.count() > 0:
                with suppress(Exception):
                    artifacts_list.first.wait_for(state="visible", timeout=10_000)

            links = self.page.locator(BUILD_ARTIFACT_DOWNLOAD_LINK)
            assert links.count() > 0, (
                "Expected at least one artifact download link. "
                f"Current artifacts tab text: {(self.page.locator('#mainContent').inner_text() or '')[:500]}"
            )
            return self

        return self._step(
            title=f"Check artifacts exist for build {self.build_id}",
            action=_action,
        )

    def download_first_artifact(self, download_dir: Path) -> Path:
        """Download first artifact using either browser download or direct API."""
        with suppress(Exception):
            self.page.get_by_text("Show hidden artifacts").first.click(timeout=2_000)

        # Look specifically for repository download links
        links = self.page.locator('a[href*="/repository/download/"]')
        if links.count() == 0:
            # Fallback to general artifact links
            links = self.page.locator(BUILD_ARTIFACT_DOWNLOAD_LINK)

        if links.count() == 0:
            raise AssertionError("No artifact download links found on page")

        links.first.wait_for(state="visible", timeout=10_000)

        # First try: use Playwright's download event
        try:
            with self.page.expect_download(timeout=10_000) as download_info:
                links.first.click()
            download = download_info.value
            target_path = Path(download_dir) / download.suggested_filename
            download.save_as(str(target_path))
            logger.info("Artifact downloaded via browser to %s", target_path)
            return target_path
        except Exception as e:
            logger.warning(f"Browser download failed: {e}, trying direct URL download")

        # Fallback: get the href and download via requests
        href = links.first.get_attribute("href")
        if not href:
            raise AssertionError("Could not get artifact URL from link")

        # Build full URL from href
        from urllib.parse import urljoin, urlparse, unquote
        from src.main.api.configs.config import Config

        server = Config.get('server').rstrip('/')
        if href.startswith("/"):
            full_url = urljoin(server, href)
        elif href.startswith("http"):
            full_url = href
        else:
            # Relative URL - build from current page
            base = self.page.url.split('?')[0]
            full_url = urljoin(base, href)

        import requests

        # Use admin credentials for download
        headers = {
            "Authorization": f"Bearer {Config.get('admin.bearerToken')}",
            "Accept": "*/*"
        }

        response = requests.get(full_url, headers=headers, timeout=30)
        response.raise_for_status()

        # Extract filename from URL or Content-Disposition
        import re
        disposition = response.headers.get("Content-Disposition", "")
        filename_match = re.search(r'filename[*]?=["\']?([^"\';\s]+)', disposition)
        if filename_match:
            filename = unquote(filename_match.group(1))
        else:
            # Extract from URL path
            path = urlparse(full_url).path
            filename = unquote(path.split("/")[-1])
            if not filename or '.' not in filename:
                filename = "artifact.txt"

        # Sanitize filename
        filename = re.sub(r'[<>:"|?*]', '_', filename)
        # Remove query string if present
        filename = filename.split('?')[0].split('#')[0]

        target_path = Path(download_dir) / filename
        target_path.write_bytes(response.content)
        self.last_download_path = target_path
        logger.info("Artifact downloaded via API to %s", target_path)
        return target_path
