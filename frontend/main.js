data = [];
const api = "http://127.0.0.1:8000/shows";
let showIdInEdt = 0;

// Function that gets the to do list
function getAllShows() {
  const xhr = new XMLHttpRequest();
  xhr.onload = () => {
    if (xhr.status == 200) {
      data = JSON.parse(xhr.response) || [];
      console.log(data);
      renderShows(data);
    }
  };

  xhr.open("GET", api, true);
  xhr.send();
}

(() => {
  getAllShows();
})();

/* Lambda function that renders the To Do list */
const renderShows = (data) => {
  const showDiv = document.getElementById("shows");
  showDiv.innerHTML = "";
  data
    .sort((a, b) => b.id - a.id)
    .forEach((x) => {
      showDiv.innerHTML += `
        <div id='show-${x.id}' class='show-box'>
            <div class='fw-bold fs-4'>${x.title}</div>
            <pre class="text-secondary ps-3">${x.desc}</pre>
            <pre class="text-secondary ps-3">Season: ${x.season}</pre>
            <pre class="text-secondary ps-3">Episode: ${x.episode}</pre>
            <div>
                <button type="button" class="btn btn-sm" id="edit-toggle"
                    data-bs-toggle="modal" data-bs-target = "#modal-edit"
                    onclick="setShowInEdit(${x.id})">
                    Edit
                </button>
                <button type="button" class="btn btn-sm" id="delete-toggle"
                    onClick="deleteShow(${x.id})">
                Delete
                </button>
            </div>
        </div>`;
    });
};

// Function for delete todo functionality
function deleteShow(id) {
  const xhr = new XMLHttpRequest();
  xhr.onload = () => {
    if (xhr.status == 200) {
      data = data.filter((x) => x.id != id);
      renderShows(data);
    }
  };

  xhr.open("DELETE", api + "/" + id, true);
  xhr.send();
}

// Function for add todo functionality
function setShowInEdit(id) {
  showIdInEdt = id;

  // Display current data in edit modal when it's opened
  const show = data.find((x) => x.id === id);
  // Fill modal inputs
  document.getElementById("titleEdit").value = show.title;
  document.getElementById("descEdit").value = show.desc;
  document.getElementById("seasonEdit").value = show.season;
  document.getElementById("episodeEdit").value = show.episode;
}

// Modal for add button
document.getElementById("add-btn").addEventListener("click", (e) => {
  e.preventDefault(); // otherwise it will refresh the page

  const msgDiv = document.getElementById("msg");
  const titleInput = document.getElementById("title");
  const descInput = document.getElementById("desc");
  const seasonInput = document.getElementById("season");
  const episodeInput = document.getElementById("episode");

  if (
    !titleInput.value ||
    !descInput.value ||
    !seasonInput.value ||
    !episodeInput.value
  ) {
    msgDiv.innerHTML = `Please provide non-empty title and Description when creating a new Todo`;
    return;
  }

  const xhr = new XMLHttpRequest();
  xhr.onload = () => {
    if (xhr.status == 201) {
      const newShow = JSON.parse(xhr.response);
      data.push(newShow);
      renderShows(data);

      // close modal dialog
      const closeBtn = document.getElementById("close-add-modal");
      closeBtn.click();

      // clean up
      msgDiv.innerHTML = "";
      titleInput.value = "";
      descInput.value = "";
      seasonInput.value = "";
      episodeInput.value = "";
    }
  };

  xhr.open("POST", api, true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(
    JSON.stringify({
      title: titleInput.value,
      desc: descInput.value,
      season: seasonInput.value,
      episode: episodeInput.value,
    }),
  );
});

// Modal for edit button
document.getElementById("edit-btn").addEventListener("click", (e) => {
  e.preventDefault(); // otherwise it will refresh the page

  const msgDiv = document.getElementById("msgEdit");
  const titleInput = document.getElementById("titleEdit");
  const descInput = document.getElementById("descEdit");
  const seasonInput = document.getElementById("seasonEdit");
  const episodeInput = document.getElementById("episodeEdit");

  if (!titleInput.value || !descInput.value) {
    msgDiv.innerHTML = `Please provide non-empty title and Description when creating a new Todo`;
    return;
  }

  const xhr = new XMLHttpRequest();
  xhr.onload = () => {
    if (xhr.status == 200) {
      const newShow = JSON.parse(xhr.response);
      const show = data.find((x) => x.id == showIdInEdt);
      show.title = newShow.title;
      show.desc = newShow.desc;
      show.season = newShow.season;
      show.episode = newShow.episode;
      renderShows(data);

      // close modal dialog
      const closeBtn = document.getElementById("close-edit-modal");
      closeBtn.click();

      // clean up
      msgDiv.innerHTML = "";
      titleInput.value = "";
      descInput.value = "";
      seasonInput.value = "";
      episodeInput.value = "";
    }
  };

  xhr.open("PUT", api + "/" + showIdInEdt, true);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  xhr.send(
    JSON.stringify({
      title: titleInput.value,
      desc: descInput.value,
      season: seasonInput.value,
      episode: episodeInput.value,
    }),
  );
});
