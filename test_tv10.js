var title = "Spider-Man: Brand New Day";
var originalTitle = title.toLowerCase().replace("'", "").replace("\"", "");
var isSeries = originalTitle.includes(' - s') && originalTitle.includes('e');
var baseTitle = originalTitle;
var epNum = "";

var searchTarget = baseTitle;
var normTarget = searchTarget.toLowerCase().replace(/[^a-z0-9]/gi, ' ').replace(/\s+/g, ' ').trim();
var words = normTarget.split(' ').filter(function(w){ return w.length > 1; });

console.log("normTarget:", normTarget);
console.log("words:", words);
