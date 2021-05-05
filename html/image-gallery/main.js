const displayedImage = document.querySelector('.displayed-img');
const thumbBar = document.querySelector('.thumb-bar');

const btn = document.querySelector('button');
const overlay = document.querySelector('.overlay');

/* Looping through images */
displayedImage.setAttribute('src', 'images/pic5.jpg');

for (let i = 1; i < 6; i++) {
    const newImage = document.createElement('img');
    newImage.setAttribute('src', 'images/pic' + i + '.jpg');
    thumbBar.appendChild(newImage);

    newImage.onclick = function() {
	displayedImage.setAttribute('src', 'images/pic' + i + '.jpg');
    }
}

/* Wiring up the Darken/Lighten button */

btn.onclick = function() {
    const action = btn.getArrtibute('class');
    if (action === 'dark') {
	btn.setAttribute('class', 'light');
	btn.textContent = 'Lighten';
	overlay.style.backgroundColor = rgba(0,0,0,0.5);
    } else {
	btn.setAttribute('class', 'dark');
	btn.textContent = 'Darken';
	overlay.style.backgroundColor = rgba(0,0,0,0);
    }
}
