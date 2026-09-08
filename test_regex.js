var title = "Spider-Man: Brand New Day";
var searchTarget = title;
var normTarget = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\s+/g, ' ').trim();
console.log("normTarget:", normTarget);

var searchTargetOld = searchTarget.toLowerCase().replace(/[^a-z0-9 ]/g, '');
console.log("searchTargetOld:", searchTargetOld);
