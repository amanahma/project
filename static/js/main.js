(function () {
    var trigger  = document.getElementById('btn-how-it-works');
    var modal    = document.getElementById('video-modal');
    var iframe   = document.getElementById('video-iframe');
    var closeBtn = document.getElementById('modal-close-btn');

    if (!trigger || !modal || !iframe || !closeBtn) return;

    var videoSrc = iframe.dataset.src;

    function openModal() {
        iframe.src = videoSrc;
        modal.classList.add('is-open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
    }

    function closeModal() {
        iframe.src = '';
        modal.classList.remove('is-open');
        modal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    trigger.addEventListener('click', function (e) {
        e.preventDefault();
        openModal();
    });

    closeBtn.addEventListener('click', closeModal);

    // Close on backdrop click (not on dialog click)
    modal.addEventListener('click', function (e) {
        if (e.target === modal) closeModal();
    });

    // Close on Escape key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && modal.classList.contains('is-open')) {
            closeModal();
        }
    });
}());
