// This Script will convert the tile name into "..." if it exceed 20 charaters.
document.addEventListener('DOMContentLoaded', function () {
    var truncateElements = document.querySelectorAll('.songname');

    truncateElements.forEach(function (element) {
    var originalText = element.textContent;

    if (originalText.length > 20) {
        element.textContent = originalText.substring(0, 20) + '...';
    }
    });
});
