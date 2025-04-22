from webview import Webview
from urllib.parse import quote

html = """
<html>
  <head>
    <style>
      body {
        margin: 0;
        padding: 0;
      }
      .drag-bar {
        -webkit-app-region: drag;
        background: #f00;
        height: 40px;
        width: 100%;
      }
    </style>
  </head>
  <body>
    <div class="drag-bar">Drag me</div>
    <div style="padding: 20px;">Hello from WebView2!</div>
  </body>
</html>
"""

webview = Webview()
webview.navigate(f"data:text/html,{quote(html)}")
webview.run()
