var navPoint = document.getElementsByClassName('navPoint')
for (var i = 0; i < navPoint.length; i++) {
    navPoint[i].addEventListener("click", function() {
        var current = document.getElementsByClassName("active");
        console.log(current)
        current[0].className = current[0].className.replace(" active", "");
        this.className += " active";
    });
}