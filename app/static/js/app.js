document.addEventListener('DOMContentLoaded', () => {
    const revealItems = document.querySelectorAll('.reveal-on-load');

    revealItems.forEach((item, index) => {
        window.setTimeout(() => {
            item.classList.add('is-visible');
        }, 70 * index);
    });
});
