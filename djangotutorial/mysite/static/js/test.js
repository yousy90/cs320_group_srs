alert(5);

fetch('/polls/apitest')
    .then(res => res.json())
    .then(data => console.log(data));



function clack(event) {
    console.log(`you clicked! ${event.offsetX}, ${event.offsetY}`);
}


function mmove(event) {
    console.log(`coordinates: (${event.offsetX}, ${event.offsetY}`);
}

window.addEventListener("click", clack);
window.addEventListener('mousemove', mmove);
