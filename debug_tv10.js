var title = "Spider-Man: Brand New Day";
var originalTitle = title.toLowerCase().replace("'", "").replace("\"", "");
var baseTitle = originalTitle;
var searchTarget = baseTitle;
var normTarget = searchTarget.toLowerCase().replace(/[^a-z0-9]/gi, ' ').replace(/\s+/g, ' ').trim();
console.log("normTarget:", normTarget);
