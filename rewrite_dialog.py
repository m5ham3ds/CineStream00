import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# We want to replace everything from `if (isLoading && !isFailed) {` to `} // End if (!isCloudflare)`
# This requires a very careful regex or manual finding.

start_str = "if (isLoading && !isFailed) {"
end_str = "} // End if (!isCloudflare)"

start_idx = content.find(start_str)
end_idx = content.find(end_str) + len(end_str)

if start_idx != -1 and end_idx != -1:
    original_block = content[start_idx:end_idx]
    
    # We want to change the structure.
    # From:
    # if (isLoading && !isFailed) {
    #     key(retryTrigger) {
    #         Box(...) { AndroidView(...) }
    #     }
    #     if (isNetworkError) { ... }
    #     else if (!isCloudflare) { ... Loading UI ... }
    # }
    
    # To:
    # if (isLoading && !isFailed) {
    #     Box(modifier = Modifier.fillMaxWidth().animateContentSize(), contentAlignment = Alignment.Center) {
    #         key(retryTrigger) {
    #             Box(modifier = Modifier.fillMaxWidth().height(450.dp).clip(androidx.compose.foundation.shape.RoundedCornerShape(12.dp))) {
    #                 AndroidView(modifier = Modifier.fillMaxSize().alpha(if (bypassStatus == "NORMAL" || bypassStatus == "VERIFIED") 0.01f else 1f), ...)
    #             }
    #         }
    #         if (isNetworkError) {
    #             Box(modifier = Modifier.fillMaxWidth().height(450.dp).background(Color(0xFF16161A)), contentAlignment = Alignment.Center) {
    #                 // Network Error UI
    #             }
    #         } else if (!isCloudflare) {
    #             Box(modifier = Modifier.fillMaxWidth().height(450.dp).background(Color(0xFF16161A)), contentAlignment = Alignment.Center) {
    #                 Column(horizontalAlignment = Alignment.CenterHorizontally, verticalArrangement = Arrangement.Center, modifier = Modifier.fillMaxSize()) {
    #                     // Loading UI
    #                 }
    #             }
    #         }
    #     }
    # }

    print("Found block, proceeding with regex replacement")
else:
    print("Block not found!")

