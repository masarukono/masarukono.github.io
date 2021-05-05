const displayedImage = document.querySelector('.displayed-img');
const thumbBar = document.querySelector('.thumb-bar');

const btn = document.querySelector('button');
const overlay = document.querySelector('.overlay');

/* Looping through images */

function imgNo(i) {
    return 'images/pic' + i.string() + '.jpg';
}

for (let i = 1; i < 6; i++) {
    const newImage = document.createElement('img');
    newImage.setAttribute('src', imgNo(i));
    thumbBar.appendChild(newImage);
}

thumbBar.onclick = function() {
    const src = getAttribute('src').split('.');
    const i = Number(src[0][src[0].length-1]);
    displayedImage.setAttribute('src', imgNo(i));
}

/* Wiring up the Darken/Lighten button */
