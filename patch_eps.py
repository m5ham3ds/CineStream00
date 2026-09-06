import re

with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'r') as f:
    content = f.read()

old_sel = "var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a, ul#episodes-list-container li.episode-list-item a, .tabcontent ul a');"

new_sel = "var epLinks = document.querySelectorAll('.episodes__list li a, .EpsList li a, .episodes-list li a, .all-episodes-list li a, .SeasonsEpisodes a, .episodelist a, .episodes a, .ListEp a, ul.episodes li a, .ep-card a, .episode-card a, .List-Episodes a, .list-episodes a, .EpisodesList a, .eplist a, .episode-list a, ul#episodes-list-container li.episode-list-item a, .tabcontent ul a, div.anime-grid#episodesList a, .episodes-list-content a, ul.episodes-lists a, ul.episodes-links a, div.epnum a, div.hover a');"

if old_sel in content:
    content = content.replace(old_sel, new_sel)
    with open('app/src/main/java/com/example/ui/screens/player/SiteScripts.kt', 'w') as f:
        f.write(content)
    print("Patched epLinks successfully.")
else:
    print("Could not find old_sel")

