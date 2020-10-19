function clickRegrade(i) {
  if(document.getElementById("reason"+i).style.display == "none"||!document.getElementById("reason"+i).style.display){
     document.getElementById("reason"+i).style.display = "block";
  } else {
    document.getElementById("reason"+i).style.display = "none";
  }
}