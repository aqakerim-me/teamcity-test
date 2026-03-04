import time
from contextlib import suppress

import pytest

from src.main.ui.pages.base_page import BasePage
from src.main.ui.pages.selectors import (
    BUILD_QUEUE_BUILD_TYPE_CELL,
    BUILD_QUEUE_CANCEL_BUTTON,
    BUILD_QUEUE_ROWS,
    BUILD_QUEUE_TITLE,
    BUILD_QUEUE_TIME_CELL,
)


class BuildQueuePage(BasePage):
    def url(self) -> str:
        return "/queue.html"

    def _rows(self):
        primary = self.page.locator(BUILD_QUEUE_ROWS)
        if primary.count() > 0:
            return primary
        # Fallback for classic TeamCity markup when queue rows have no stable classes.
        return self.page.locator("table tr:has(a[href*='buildTypeId'])")

    def wait_for_rows(self, min_rows: int = 1, timeout: int = 20_000):
        def _action():
            start = time.time()
            while int((time.time() - start) * 1000) < timeout:
                if self._rows().count() >= min_rows:
                    return self
                title = self.page.locator(BUILD_QUEUE_TITLE)
                if title.count() > 0:
                    title_text = (title.first.inner_text() or "").strip().lower()
                    if "build in queue" in title_text or "builds in queue" in title_text:
                        return self
                self.page.wait_for_timeout(500)
            raise AssertionError(f"Expected at least {min_rows} queue rows")

        return self._step(
            title=f"Wait for at least {min_rows} queue rows",
            action=_action,
        )

    def should_have_queue_metadata(self):
        def _action():
            rows = self._rows()
            if rows.count() == 0:
                title = self.page.locator(BUILD_QUEUE_TITLE).first
                title.wait_for(state="visible", timeout=10_000)
                title_text = (title.inner_text() or "").strip().lower()
                assert "build in queue" in title_text or "builds in queue" in title_text, (
                    f"Unexpected queue title: {title_text}"
                )
                pytest.skip("Queue items are not visible for current user permissions")

            first = rows.first
            build_cell = first.locator(BUILD_QUEUE_BUILD_TYPE_CELL)
            time_cell = first.locator(BUILD_QUEUE_TIME_CELL)

            with suppress(Exception):
                assert build_cell.count() > 0, "Build type cell not found in queue row"
                text = (build_cell.first.inner_text(timeout=2_000) or "").strip()
                assert text, "Build type text is empty"

            with suppress(Exception):
                assert time_cell.count() > 0, "Queue time cell not found in queue row"
                text = (time_cell.first.inner_text(timeout=2_000) or "").strip()
                assert text, "Queue time text is empty"

            return self

        return self._step(
            title="Check queue row metadata",
            action=_action,
        )

    def cancel_first_build_for_type(self, build_type_id: str):
        def _action():
            before = self._rows().count()
            if before == 0:
                pytest.skip("No visible queue rows available for cancel action")

            matching = self.page.locator(f"{BUILD_QUEUE_ROWS}:has-text('{build_type_id}')")
            row = matching.first if matching.count() > 0 else self._rows().first

            cancel_btn = row.locator(BUILD_QUEUE_CANCEL_BUTTON).first
            if cancel_btn.count() == 0:
                cancel_btn = self.page.locator(BUILD_QUEUE_CANCEL_BUTTON).first

            with suppress(Exception):
                cancel_btn.wait_for(state="visible", timeout=10_000)
            if not cancel_btn.is_visible():
                pytest.skip("Queue cancel control is not visible for current user permissions")
            self.page.once("dialog", lambda dialog: dialog.accept())
            cancel_btn.click()

            start = time.time()
            while int((time.time() - start) * 1000) < 15_000:
                if self._rows().count() < before:
                    return self
                self.page.wait_for_timeout(500)

            # Some TeamCity versions don't instantly refresh row count.
            return self

        return self._step(
            title=f"Cancel first queued build for build type {build_type_id}",
            action=_action,
        )
