import re

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'r') as f:
    content = f.read()

# We will just replace the autoPlayScript block to be robust for all cases (clicking play buttons, bypassing Cloudflare, getting iframes)
# It's identical to the advanced script, but focused on finding the video/iframe since the server is already chosen.

js_code = """
                                var intervalId = setInterval(function() {
                                    // Bypass Cloudflare Turnstile / Captcha
                                    var cf = document.querySelector('.cf-turnstile-wrapper, #challenge-stage, input[type="checkbox"], #challenge-form, .mark-as-human');
                                    if (cf) { cf.click(); return; }
                                    
                                    try {
                                        var iframesCF = document.querySelectorAll('iframe');
                                        for (var i = 0; i < iframesCF.length; i++) {
                                            var innerBtn = iframesCF[i].contentWindow.document.querySelector('input[type="checkbox"]');
                                            if (innerBtn) innerBtn.click();
                                        }
                                    } catch(e) {}

                                    var iframes = document.getElementsByTagName('iframe');
                                    for (var i = 0; i < iframes.length; i++) {
                                        try {
                                            var playBtn = iframes[i].contentWindow.document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .fp-play, .play-icon, #play-video, .btn-play');
                                            if (playBtn) playBtn.click();
                                        } catch(e) {}
                                    }
                                    var localPlay = document.querySelector('.play-button, .jw-icon-display, video, .vjs-big-play-button, .fp-play, .play-icon, #play-video, .btn-play');
                                    if (localPlay) localPlay.click();
                                    
                                    var watchBtnFirst = document.querySelector('.watch-btn, #watch-btn, a.watch, .btn-watch, .play-btn, .watchNow button, .watchNow form button');
                                    if(watchBtnFirst && !loc.includes('watch')) watchBtnFirst.click();

                                    var serverList = document.querySelectorAll('ul.servers li, .server-list li, .serversList li, .watch-servers li, .list-servers li, .servers-list li, .mob-servers ul li, #servers li, .server_list li, .watch-btn, .DownloadServers li, ul#episode-servers li, ul.NavTabs li, .server-list a, .watch-servers a, .servers-container li, .btn-server, .servers a, .item-server, .server-item, .server-btn, .server-link, a.server-link, ul.donwload-servers-list li, .servers-container button, ul.servers__list li, div.embeding ul li, ul#watch-servers-list li, button.watchButton, div.servers span.server a, div.watch--servers--list li.server--item, ul.WatchServers li, ul.list_servers li');

                                    if (targetServer !== "" && targetServer !== "السيرفر الرئيسي") {
                                        // Attempt to find and click the specific target server
                                        for(var i=0; i<serverList.length; i++) {
                                            var sName = serverList[i].innerText.trim().replace(/1080p|720p|480p|360p|240p|1080|720|480|360|240/gi, '').trim();
                                            if (sName === "" || sName.includes('جودة') || sName.includes('FHD') || sName.includes('HD') || sName.includes('SD')) {
                                                sName = "سيرفر " + (i+1);
                                            }
                                            if(sName === targetServer || serverList[i].innerText.trim() === targetServer || serverList[i].getAttribute('data-server') === targetServer) {
                                                serverList[i].click();
                                                break;
                                            }
                                        }
                                    } else if (serverList && serverList.length > 0) {
                                        if (document.getElementsByTagName('iframe').length === 0 && document.querySelectorAll('video').length === 0) {
                                            serverList[0].click();
                                        }
                                    }
                                    
                                    // Monitor iframe creation/changes and report them as video URLs to Kotlin
                                    var currentIframe = document.querySelector('iframe[src*="http"]');
                                    if (currentIframe && typeof AndroidBridge !== 'undefined') {
                                        var src = currentIframe.getAttribute('src');
                                        if (src && !src.includes('cloudflare') && !src.includes('facebook') && !src.includes('twitter')) {
                                            AndroidBridge.sendIframeUrl(src);
                                        }
                                    }

                                }, 1500);
"""

pattern = r"setInterval\(function\(\) \{.*?\}, 1500\);"
content = re.sub(pattern, js_code.strip(), content, flags=re.DOTALL)

with open('app/src/main/java/com/example/ui/screens/player/VideoExtractor.kt', 'w') as f:
    f.write(content)
