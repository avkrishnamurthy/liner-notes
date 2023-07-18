const openModals = document.querySelectorAll('[data-modal-target]')
const closeModals = document.querySelectorAll("[data-modal-close]");

openModals.forEach(button => {
    button.addEventListener('click', () => {
      const modal = document.querySelector(button.dataset.modalTarget)
      modal.showModal()
    })
  })

closeModals.forEach(button => {
button.addEventListener('click', () => {
    const modal = document.querySelector(button.dataset.modalClose)
    modal.close()
})
})


function submitReview(event, albumImgUrl, albumName, albumId) {
    event.preventDefault();

    let rating = document.getElementById("rating-"+albumName).value;
    let review = document.getElementById("review-"+albumName).value;
    let modal = document.getElementById("modal-"+albumId)
    let favoriteButton = document.getElementById("favorite-button-"+albumId)

    if (favoriteButton.style.color === "red") {
      fetch("/add-favorite", {
        method: "POST",
        body: JSON.stringify({ albumImgUrl: albumImgUrl, albumName:albumName }),
        }).then((_res) => {
          console.log("success favoriting")
            });
    }
    const reviewData = {
      albumImgUrl: albumImgUrl,
      albumName: albumName,
      rating: rating,
      review: review
    };

    fetch("/add-album", {
      method: "POST",
      body: JSON.stringify(reviewData),
    })
    .then((_res) => {
    // Clear the rating and review fields
    document.getElementById("rating-"+albumName).value = "";
    document.getElementById("review-"+albumName).value = "";

    // Hide the review form for the submitted album
    // const reviewForm = document.getElementById(`reviewForm-${albumName}`);
    // reviewForm.style.display = 'none';

    // Show the success message
    const successMessage = document.getElementById('success-message');
    successMessage.style.display = 'block';
    
    console.log(modal)
    modal.close()
    // Optional: You can also display a notification or perform any other action here

    // Delay the success message for 5 seconds
    setTimeout(() => {
      successMessage.style.display = 'none';
    }, 5000);
  });
  }

function toggleFavorite(albumId) {
  let favoriteButton = document.getElementById('favorite-button-'+albumId)
  if (favoriteButton.style.color === "red") {
    favoriteButton.style.color = "grey"
  }
  else {
    favoriteButton.style.color = "red"
  }
}