function resize() {
    var heights = window.innerHeight;
    document.getElementById("map").style.height = heights-40 + "px";
}
resize();
window.onresize = function() {
    resize();
};