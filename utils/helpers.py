import allure
import base64
from allure_commons.types import AttachmentType


_REPORT_CONTEXT = None
_FAILURE_MARKERS = ("fail", "failed", "error", "exception", "abort")


def set_report_context(context):
    """Store the active Behave context so report embedding works without passing context everywhere."""
    global _REPORT_CONTEXT
    _REPORT_CONTEXT = context

def _embedding_payload(formatter, screenshot_bytes):
    """Return the screenshot payload in the form a given formatter expects.

    The data contract differs by formatter and the two we run together disagree:

    * ``behave_html_formatter`` drops the value straight into a
      ``data:image/png;base64,{data}`` URI, so it needs a base64 *string*.
    * behave's built-in JSON formatter base64-encodes the value itself
      (``base64.b64encode(data)``), so it needs raw *bytes*.

    Passing the wrong type makes one formatter raise (JSON) or render a broken
    image (HTML), which is exactly why screenshots never reached the report.
    """
    module = (type(formatter).__module__ or "")
    if "html_formatter" in module:
        return base64.b64encode(screenshot_bytes).decode("utf-8")
    return screenshot_bytes


def attach_screenshot(page, name="Screenshot", context=None, force=False):
    """Attach screenshot to reports.

    Captures only for failure-like names so reports include failure evidence only.
    The force flag is intentionally ignored for non-failure names to avoid
    pass-step screenshot noise from step definitions.
    """
    lowered = str(name).lower()
    is_failure_name = any(marker in lowered for marker in _FAILURE_MARKERS)
    if not is_failure_name:
        return
    try:
        screenshot_bytes = page.screenshot(full_page=True)
    except Exception as exc:
        print(f"Screenshot capture failed: {exc}")
        return

    # Allure attachment
    try:
        allure.attach(screenshot_bytes, name=name, attachment_type=AttachmentType.PNG)
    except Exception:
        pass  # No active Allure context — safe to skip.

    # Embed into behave formatters directly instead of via context.attach().
    #
    # context.attach() loops every formatter that exposes embedding() and stops
    # at the first one that raises.  Because the JSON formatter (which wants raw
    # bytes) is registered before the HTML formatter (which wants a base64
    # string), a wrong-typed payload made JSON throw and the HTML formatter was
    # never reached — so no screenshots appeared in the report.  Embedding each
    # formatter independently, with the payload type it expects, fixes that.
    active_context = context if context is not None else _REPORT_CONTEXT
    runner = getattr(active_context, "_runner", None)
    formatters = getattr(runner, "formatters", None) or []
    for formatter in formatters:
        if not hasattr(formatter, "embedding"):
            continue
        try:
            data = _embedding_payload(formatter, screenshot_bytes)
            try:
                # behave_html_formatter accepts an optional caption.
                formatter.embedding("image/png", data, caption=name)
            except TypeError:
                # behave's JSON/built-in formatters take (mime_type, data) only.
                formatter.embedding("image/png", data)
        except Exception as exc:
            print(f"Screenshot embed into {type(formatter).__name__} failed: {exc}")

def highlight_element(page, locator, duration: int = 1500):
    """Highlight an element by adding a red border temporarily.
    
    Args:
        page: Playwright page object
        locator: Element locator (can be string or locator object)
        duration: How long to highlight in milliseconds (default 1500ms)
    """
    try:
        # Convert string locator to locator object if needed
        if isinstance(locator, str):
            element = page.locator(locator)
        else:
            element = locator
        
        # Check if locator resolves to multiple elements
        try:
            count = element.count()
            if count > 1:
                capped_count = min(count, 20)
                # Highlight all matching elements
                for i in range(capped_count):
                    single_element = element.nth(i)
                    try:
                        single_element.scroll_into_view_if_needed(timeout=1000)
                        page.evaluate("""
                            (el) => {
                                if (el) {
                                    el.style.border = '5px solid red';
                                    el.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';
                                    el.style.outline = '3px solid yellow';
                                }
                            }
                        """, single_element.element_handle())
                    except:
                        pass
                
                page.wait_for_timeout(100)
                
                # Remove highlights
                for i in range(capped_count):
                    single_element = element.nth(i)
                    try:
                        page.evaluate("""
                            (el) => {
                                if (el) {
                                    el.style.border = '';
                                    el.style.backgroundColor = '';
                                    el.style.outline = '';
                                }
                            }
                        """, single_element.element_handle())
                    except:
                        pass
                return
        except:
            pass
        
        # Single element highlighting
        element.scroll_into_view_if_needed(timeout=1000)
        
        # Scroll up a bit to ensure title/heading is fully visible (not cut off at top)
        page.evaluate("window.scrollBy(0, -150)")
        
        # Add red border with JavaScript
        page.evaluate("""
            (element) => {
                if (element) {
                    element.style.border = '5px solid red';
                    element.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';
                    element.style.outline = '3px solid yellow';
                }
            }
        """, element.element_handle())
        
        # Wait briefly for visualization
        page.wait_for_timeout(200)
        
        # Remove the highlight
        page.evaluate("""
            (element) => {
                if (element) {
                    element.style.border = '';
                    element.style.backgroundColor = '';
                    element.style.outline = '';
                }
            }
        """, element.element_handle())
    except Exception as e:
        print(f"Could not highlight element: {e}")


