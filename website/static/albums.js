function deleteAlbum(albumId) {
    fetch("/delete-album", {
    method: "POST",
    body: JSON.stringify({ albumId: albumId }),
    }).then((_res) => {
        window.location.href = "/all-albums";
        });
}