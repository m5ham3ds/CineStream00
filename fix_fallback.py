import re

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "r") as f:
    content = f.read()

old_fallback = """var oldResults = document.querySelectorAll('a.boxItem, .boxItem a, a.postBlockCol, .postBlockCol, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0, .GridItem a');"""
new_fallback = """var oldResults = document.querySelectorAll('a.boxItem, .boxItem a, a.postBlockCol, .postBlockCol, section.main-section ul.posts-list li.movieItem a, .movieItem a, .postBlock a, ul.pm-ul-browse-videos li a, ul.movie__blocks__ul li a.movie__block, ul.series__ul li a, div.media-block a.image, div.owl-animes a.overlay, div.embla__slide a, .movie-card a, .anime-card a, .item-list a, article a, .post a, .thumb a, .Blocks-Area a.Block-Item, .ep-card a, .episode-card a, .box-item a, .hover-content a, .anime-list-content a, .half-post a, .Block-Item, a.header-featured-item, a.movie-item__link, .pm-video-thumb a, .lucodeia-slider-slide-item, a.overlay, a.absolute.inset-0, .GridItem a, div.movieBlock a, .movieBlock a, div.postItem a, .postItem a, a.movie, a.series, .item a');"""

content = content.replace(old_fallback, new_fallback)

with open("app/src/main/java/com/example/ui/screens/player/SiteScripts.kt", "w") as f:
    f.write(content)
