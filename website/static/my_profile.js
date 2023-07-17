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

function openModal(modal) {
  if (modal == null) return
  modal.classList.add('active')
  overlay.classList.add('active')
}

function closeModal(modal) {
  if (modal == null) return
  modal.classList.remove('active')
  overlay.classList.remove('active')
}

// Function to hide the arrows
function hideArrows() {
    leftArrow.classList.add('hidden');
    rightArrow.classList.add('hidden');
  }
  
  // Function to show the arrows
  function showArrows() {
    leftArrow.classList.remove('hidden');
    rightArrow.classList.remove('hidden');
  }