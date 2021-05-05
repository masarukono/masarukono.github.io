const displayedImage = document.querySelector('.displayed-img');
const thumbBar = document.querySelector('.thumb-bar');

const btn = document.querySelector('button');
const overlay = document.querySelector('.overlay');

/* Looping through images */

function imgNo(i) {
    return 'images/pic' + i + '.jpg';
}

for (let i = 1; i < 6; i++) {
    const newImage = document.createElement('img');
    //newImage.setAttribute('src', imgNo(i));
    newImage.setAttribute('src', 'images/pic' + i + '.jpg');
    thumbBar.appendChild(newImage);
}

thumbBar.onclick = function() {
    const src = getAttribute('src');
    displayedImage.setAttribute('src', src);
}

/* Wiring up the Darken/Lighten button */
