document.addEventListener('DOMContentLoaded', function () {
  load_posts();

  // Submit new post
  document
    .querySelector('#compose-form')
    .addEventListener('click', compose_post);
});
