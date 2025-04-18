if (document.getElementById('vid')) {
  document.getElementById('vid').currentTime = 57;
}

function beforeSend() {
  $("#staticBackdrop .modal-content").html("");
  $("#staticBackdrop").modal("show");
}

document.addEventListener("click", function (e) {
  if (e.target.id == "remove") {
    let formdata = new FormData();
    let comment_id = e.target.getAttribute('data-id');
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    formdata.append('comment_id', comment_id);
    formdata.append('csrfmiddlewaretoken', csrf);
    fetch('/videos/remove/', {
      method: 'POST',
      mode: 'same-origin',
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf,
      },
      body: formdata
    }).then(response => {
        return response.json()
      }).then(data => {
        let commentcontainer = document.getElementById('commentcontainer');
        commentcontainer.innerHTML = data.partial_video_comments
        document.getElementById("commentcount").textContent = data.comment_count;
      })
  }
});

document.addEventListener("keydown", function (e) {
  if (e.target.id == "usercomment") {
    if (e.keyCode == 13) {
      let form = document.querySelector('#comment');
      let data = new FormData(form);
      let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      data.append('csrfmiddlewaretoken', csrf);
      fetch('/videos/comment/', {
        method: 'POST',
        mode: 'same-origin',
        headers: {
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': csrf,
        },
        body: data
      }).then(response => {
          return response.json()
        }).then(data => {
          if (Object.entries(data).length != 0) {
            let commentcontainer = document.getElementById('commentcontainer');
            commentcontainer.innerHTML = data.partial_video_comments
            document.getElementById("commentcount").textContent = data.comment_count;
            document.getElementById('usercomment').value = ''
          }
        })
    }
  }
});
document.addEventListener("click", function (e) {
  if (e.target.id == "upload") {
    beforeSend();
    fetch('/videos/add_video/', {
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
    }).then(response => {
        return response.json()
      }).then(data => {
        document.getElementById("modal-content").innerHTML = data.video_form;
      })
  }
});

document.addEventListener("click", function (e) {
  if (e.target.id == "video_submit") {
    let formdata = new FormData();
    let video_file = document.getElementById('id_video_file').files[0];
    formdata.append('video_file', video_file);
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    formdata.append('csrfmiddlewaretoken', csrf);
    let post = document.querySelector('input[name="post"]').value;
    formdata.append('post', post)
    fetch('/videos/add_video/', {
      method: 'POST',
      mode: 'same-origin',
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf,
      },
      body: formdata
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
        if (!data.form_is_valid) {
          document.getElementById("modal-content").innerHTML = " ";
          document.getElementById("modal-content").innerHTML = data.video_form;
        } else if (data.form_is_valid) {
          $("#staticBackdrop").modal("hide");
          location.reload();
        }
      })
  }
});

document.addEventListener("click", function (e) {
  if (e.target.id == "edit") {
    let video_id = e.target.getAttribute('data-id');
    beforeSend();

    fetch('/videos/edit_video/' + video_id + "/", {
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
        document.getElementById("modal-content").innerHTML = data.edit_video;
      })
  }
});

document.addEventListener("click", function (e) {
  if (e.target.id == "submit_edited_video") {
    let formdata = new FormData();
    let video_file = document.getElementById('id_video_file').files[0];
    formdata.append('video_file', video_file);
    let csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    formdata.append('csrfmiddlewaretoken', csrf);
    let post = document.getElementById('id_post').value;
    formdata.append('post', post)
    let video_id = e.target.getAttribute('data-id');
    fetch('/videos/edit_video/' + video_id + "/", {
      method: 'POST',
      mode: 'same-origin',
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
        'X-CSRFToken': csrf,
      },
      body: formdata
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
        if (!data.form_is_valid) {
          document.getElementById("modal-content").innerHTML = " ";
          document.getElementById("modal-content").innerHTML = data.edited_video;
        } else if (data.form_is_valid) {
          $("#staticBackdrop").modal("hide");
          location.reload();
        }
      })
  }
});

document.addEventListener("click", function (e) {
  if (e.target.id == "deleteVideo") {
    let video_id = e.target.getAttribute('data-id');
    beforeSend();

    fetch('/videos/delete_video/' + video_id + "/", {
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
        // return data;
        document.getElementById("modal-content").innerHTML =  data.data;
      })
  }
});

document.addEventListener("click", function (e) {
  if (e.target.id == "delete_Video") {
    let video_id = e.target.getAttribute('data-id');
    beforeSend();

    fetch('/videos/delete_video_confirmation/'+ video_id +'/', {
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
    })
      .then(response => {
        return response.json()
      })
      .then(data => {
        document.getElementById("modal-content").innerHTML =  data.data;
      })
  }
});

document.getElementById("like-button").addEventListener("click", function () {
  let videoId = this.getAttribute("data-video-id");

  fetch(`/videos/like/${videoId}/`, {
      method: "GET",
      headers: { "X-Requested-With": "XMLHttpRequest" }
  })
  .then(response => response.json())
  .then(data => {
      document.getElementById("like-count").innerText = data.total_likes;
      let icon = document.getElementById("like-icon");
      if (data.liked) {
        icon.classList.remove("bi-hand-thumbs-up");
        icon.classList.add("bi-hand-thumbs-up-fill");
    } else {
        icon.classList.remove("bi-hand-thumbs-up-fill");
        icon.classList.add("bi-hand-thumbs-up");
    }
    })
  .catch(error => console.error("Error:", error));
});


document.getElementById("subscribe-button").addEventListener("click", function () {
  let userId = this.getAttribute("data-user-id");

  fetch(`/videos/subscribe/${userId}/`, {
      method: "GET",
      headers: { "X-Requested-With": "XMLHttpRequest" }
  })
  .then(response => response.json())
  .then(data => {
      if (data.is_subscribed) {
          document.getElementById("subscribe-button").innerText = "Unsubscribe";
      } else {
          document.getElementById("subscribe-button").innerText = "Subscribe";
      }
      document.getElementById("subscriber-count").innerText = data.total_subscribers;
  })
});