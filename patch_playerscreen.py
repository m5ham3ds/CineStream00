import re

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'r') as f:
    content = f.read()

old_code = """                    onVideoUrlFound = { extractedUrl ->
                        viewModel.setExtractedUrl(extractedUrl)
                    },
                    onServersFound = { servers ->"""

new_code = """                    onVideoUrlFound = { extractedUrl ->
                        viewModel.setFinalVideoUrl(extractedUrl)
                    },
                    onIframeUrlFound = { iframeUrl ->
                        viewModel.setIframeUrl(iframeUrl)
                    },
                    onServersFound = { servers ->"""

content = content.replace(old_code, new_code)

with open('app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt', 'w') as f:
    f.write(content)

