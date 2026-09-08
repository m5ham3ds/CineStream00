fetch("https://tv10.egydead.live/?s=Spider-Man%3A+Brand+New+Day")
  .then(res => res.text())
  .then(text => console.log(text.substring(0, 500)))
  .catch(err => console.error(err));
