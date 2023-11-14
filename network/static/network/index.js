document.addEventListener('DOMContentLoaded', function () {
  document
    .querySelector('#follow-btn')
    .addEventListener('click', () => load_follow());
});

function load_follow() {
  const btnForm = document.querySelector('#following-status');

  const newBtn = document.createElement('button');
  newBtn.classList.add('btn', 'btn-outline-danger', 'unfollow-btn');
  newBtn.type = 'submit';
  newBtn.innerHTML = 'Unfollow';
  btnForm.appendChild(newBtn);
}
