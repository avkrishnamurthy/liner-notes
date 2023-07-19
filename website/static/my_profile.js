var indexValue = 1;
showImg(indexValue);
function side_slide(e) {
    const overlay = document.getElementById('overlay');
  if (overlay.classList.contains('active')) {
    return; // Return early if overlay is active
  }
    showImg(indexValue+=e);
}

function showImg(e) {
    var i;
    const img = document.querySelectorAll('.my-album-things');
    if (e > img.length){
        indexValue = 1
    }

    if (e < 1) {
        indexValue = img.length;
    }

    for (i=0; i<img.length; i++) {
        img[i].style.display = "none";
    }

    img[indexValue - 1].style.display = "block";
}

const openModalButtons = document.querySelectorAll('[data-modal-target]')
const closeModalButtons = document.querySelectorAll('[data-close-button]')
const overlay = document.getElementById('overlay')
const leftArrow = document.getElementById('left');
const rightArrow = document.getElementById('right');

openModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = document.querySelector(button.dataset.modalTarget)
    console.log(modal)
    openModal(modal)
    hideArrows();
  })
})

overlay.addEventListener('click', () => {
  const modals = document.querySelectorAll('.modal.active')
  modals.forEach(modal => {
    closeModal(modal)
    showArrows(); // Show the arrows when the overlay is closed
  })
})

closeModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = button.closest('.modal')
    closeModal(modal)
    showArrows(); // Show the arrows when the overlay is closed
  })
})



//Favorites Modal 
var favIndexValue = 1;
fav_showImg(favIndexValue);
function fav_side_slide(e) {
    const overlay = document.getElementById('overlay');
  if (overlay.classList.contains('active')) {
    return; // Return early if overlay is active
  }
    fav_showImg(favIndexValue+=e);
}

function fav_showImg(e) {
    var i;
    const img = document.querySelectorAll('.my-fav-album-things');
    if (e > img.length){
        favIndexValue = 1
    }

    if (e < 1) {
        favIndexValue = img.length;
    }

    for (i=0; i<img.length; i++) {
        img[i].style.display = "none";
    }

    img[favIndexValue - 1].style.display = "block";
}

const favOpenModalButtons = document.querySelectorAll('[data-fav-modal-target]')
const favCloseModalButtons = document.querySelectorAll('[data-fav-close-button]')
const favLeftArrow = document.getElementById('fav-left');
const favRightArrow = document.getElementById('fav-right');

favOpenModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = document.querySelector(button.dataset.favModalTarget)
    console.log(modal)
    openModal(modal)
    hideArrows();
  })
})

overlay.addEventListener('click', () => {
  const modals = document.querySelectorAll('.fav-modal.active')
  modals.forEach(modal => {
    closeModal(modal)
    showArrows(); // Show the arrows when the overlay is closed
  })
})

favCloseModalButtons.forEach(button => {
  button.addEventListener('click', () => {
    const modal = button.closest('.fav-modal')
    closeModal(modal)
    showArrows(); // Show the arrows when the overlay is closed
  })
})

function openModal(modal) {
  if (modal == null) return
  modal.classList.add('active')
  overlay.classList.add('active')
  console.log(overlay)
}

function closeModal(modal) {
  if (modal == null) return
  modal.classList.remove('active')
  overlay.classList.remove('active')
}

// Function to hide the arrows
function hideArrows() {
    favLeftArrow.classList.add('hidden')
    favRightArrow.classList.add('hidden')
    leftArrow.classList.add('hidden');
    rightArrow.classList.add('hidden');
  }
  
// Function to show the arrows
function showArrows() {
  favLeftArrow.classList.remove('hidden')
  favRightArrow.classList.remove('hidden')
  leftArrow.classList.remove('hidden');
  rightArrow.classList.remove('hidden');
}


function deleteFavorite(favoriteId) {
  const removeFromFavorites = confirm("Are you sure you want to remove this album from your favorites?")
  if (removeFromFavorites) {
    let modal = document.getElementById("modal-"+favoriteId)
    fetch("/delete-favorite", {
    method: "POST",
    body: JSON.stringify({ favoriteId: favoriteId }),
    }).then((_res) => {
        window.location.href = "/my-profile";
        });
  }
}