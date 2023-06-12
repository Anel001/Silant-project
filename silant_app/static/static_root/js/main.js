function myFunction1() {
    var mach = document.getElementById('machineInfo');
    var to = document.getElementById('toInfo');
    var rec = document.getElementById('reclamsInfo');
    console.log(mach)
    mach.style.display = "block";
    to.style.display = "none";
    rec.style.display = "none";

}

function myFunction2() {
    var mach = document.getElementById("machineInfo");
    var to = document.getElementById("toInfo");
    var rec = document.getElementById("reclamsInfo");
    mach.style.display = "none";
    to.style.display = "block";
    rec.style.display = "none";
}

function myFunction3() {
    var mach = document.getElementById("machineInfo");
    var to = document.getElementById("toInfo");
    var rec = document.getElementById("reclamsInfo");
    mach.style.display = "none";
    to.style.display = "none";
    rec.style.display = "block";
}