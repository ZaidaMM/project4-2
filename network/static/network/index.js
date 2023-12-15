function follow_unfollow(query) {
  const a = document.querySelector('#user_name').innerText;
  fetch(`../follow_unfollow/${query}/${a}`)
    .then((response) => response.json())
    .then((result) => {
      if (result['message'] == 'you unfollowed this user') {
        const a = parseInt(
          document.querySelector('#followed_count').innerText.split(':')[1]
        );
        const c = a - 1;
        document.querySelector(
          '#followed_count'
        ).innerHTML = `<strong>following</strong>: ${c} users`;
      }
      if (result['message'] == 'you are now following this user') {
        const a = parseInt(
          document.querySelector('#followed_count').innerText.split(':')[1]
        );
        const c = a + 1;
        document.querySelector(
          '#followed_count'
        ).innerHTML = `<strong>following</strong>: ${c} users`;
      }
      console.log(result['message']);
      document.querySelector(
        '#message'
      ).innerHTML = `<div class="alert alert-info alert-dismissible fade in">
        <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
        ${result['message']}
    </div>`;
    });
}
