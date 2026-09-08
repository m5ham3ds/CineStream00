var str = "Spider-Man: Brand New Day";
var words = str.toLowerCase().replace(/[^a-z0-9]/gi, ' ').replace(/\s+/g, ' ').trim().split(' ');
console.log(words);
