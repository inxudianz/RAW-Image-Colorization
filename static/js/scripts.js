function loadFile(event) {
    var filename = event.target.value.toString();
    var file_ext = filename.split('.').pop();
    console.log(file_ext);

    document.getElementById('button').disabled = true;

    if(file_ext == 'jpg' || file_ext == "jpeg") {
        document.getElementById("button").disabled = false;
    }
    var output = document.getElementById('output');
    output.src = URL.createObjectURL(event.target.files[0]);
}

function showProgress() {
    var progress = document.getElementById("progress");
    progress.style.visibility = "visible";
    progress_value = document.getElementById("progress_value");
    progress_value.value = "0";
    moveProgress()
}

function moveProgress() {
    var progress = document.getElementById("progress_value");
    var value = 0;
    var id = setInterval(frame,30);

    function frame() {
        if (value >= 100) {
            clearInterval(id);
        }
        else {
            value += 1;
            progress.value = value;
        }
    }
}