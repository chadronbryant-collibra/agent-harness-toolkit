'use strict';

const selection = document.querySelector('.selection');
const buttons = [...selection.querySelectorAll('button')];
const stories = [...document.querySelectorAll('[data-story]')];

function show(name, animate) {
  for (const button of buttons) {
    button.setAttribute('aria-pressed', String(button.dataset.example === name));
  }
  for (const story of stories) {
    const active = story.dataset.story === name;
    story.hidden = !active;
    story.classList.toggle('reveal', active && animate);
  }
}

for (const button of buttons) {
  button.addEventListener('click', () => show(button.dataset.example, true));
}
show('context', false);
selection.hidden = false;
