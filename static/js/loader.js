let progress = 0;
const progressBar = document.getElementById("progress-bar");
const loader = document.getElementById("loader");
const content = document.getElementById("content");

const mouth = document.querySelector('.mouth');

function updateFace(percentage) {
    if(percentage < 25) {
        mouth.setAttribute("d", "M22,42 Q32,36 42,42"); // triste
    } else if(percentage < 50) {
        mouth.setAttribute("d", "M22,42 Q32,42 42,42"); // neutre
    } else if(percentage < 75) {
        mouth.setAttribute("d", "M22,42 Q32,46 42,42"); // sourire léger
    } else {
        mouth.setAttribute("d", "M22,42 Q32,50 42,42"); // grand sourire
    }
}

let interval = setInterval(() => {
    progress += 1;
    progressBar.style.width = progress + "%";
    updateFace(progress);
    if(progress >= 100){
        clearInterval(interval);
        loader.style.transition = "opacity 0.8s ease";
        loader.style.opacity = 0;
        setTimeout(() => {
            loader.style.display = "none";
            content.style.display = "block";
        }, 800);
    }
}, 30);