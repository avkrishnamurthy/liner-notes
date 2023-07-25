function deleteAlbum(albumId) {
    const delAlbum = confirm("Are you sure you want to delete this review from your profile?")
    if (delAlbum) {
    fetch("/delete-album", {
    method: "POST",
    body: JSON.stringify({ albumId: albumId }),
    }).then((_res) => {
        window.location.href = "/my-reviews";
        });
    }
}