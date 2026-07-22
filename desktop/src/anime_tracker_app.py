"""
Anime Tracker - desktop application.

Wraps the anime-tracker.html web app in a native window (via pywebview /
Edge WebView2), so it runs as a real standalone Windows app with no browser
chrome. Streaming/info links are opened in the system default browser.
"""
import os
import sys
import webbrowser

import webview


def resource_path(rel: str) -> str:
    """Path to a bundled resource, whether run from source or a PyInstaller exe."""
    # When frozen, PyInstaller's _MEIPASS root has the resource bundled at its
    # top (see --add-data below). When run from source, this file lives in
    # src/, but anime-tracker.html lives one directory up, at the project root.
    default = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base = getattr(sys, "_MEIPASS", default)
    return os.path.join(base, rel)


class Api:
    """Exposed to the page as window.pywebview.api."""

    def open_url(self, url: str):
        try:
            if url:
                webbrowser.open(url)
        except Exception:
            pass


# Route every external (http/https) link click to the system browser instead
# of navigating inside the app window. Capture phase + stopPropagation so it
# runs before the page's own link handler.
_INJECT_JS = r"""
(function () {
  if (window.__desktopLinkHook) return;
  window.__desktopLinkHook = true;
  document.addEventListener('click', function (e) {
    var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (/^https?:/i.test(href)) {
      e.preventDefault();
      e.stopPropagation();
      if (window.pywebview && window.pywebview.api && window.pywebview.api.open_url) {
        window.pywebview.api.open_url(href);
      }
    }
  }, true);
})();
"""


def main():
    html = resource_path("anime-tracker.html")
    api = Api()
    window = webview.create_window(
        "Anime Tracker",
        url=html,
        js_api=api,
        width=900,
        height=840,
        min_size=(420, 600),
    )

    def on_loaded():
        try:
            window.evaluate_js(_INJECT_JS)
        except Exception:
            pass

    window.events.loaded += on_loaded
    webview.start()


if __name__ == "__main__":
    main()
