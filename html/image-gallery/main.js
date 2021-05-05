const displayedImage = document.querySelector('.displayed-img');
const thumbBar = document.querySelector('.thumb-bar');

const btn = document.querySelector('button');
const overlay = document.querySelector('.overlay');

/* Looping through images */

function imgPick(i) {
    return 'images/pic' + i.string() + '.jpg';
}

for (let i = 1; i < 6; i++) {
    const newImage = document.createElement('img');
    newImage.setAttribute('src', imgPick(i));
    thumbBar.appendChild(newImage);
}

/* Wiring up the Darken/Lighten button */
