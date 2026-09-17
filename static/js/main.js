document.addEventListener('DOMContentLoaded', () => {

    /* --- Mobillda menyu (hamburger morph) --- */
    const menuBtn = document.getElementById('menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const lines = document.querySelectorAll('.menu-line');

    const openMenu = () => {
        mobileMenu.classList.remove('hidden');
        mobileMenu.classList.add('flex');
        requestAnimationFrame(() => {
            lines[0].style.transform = 'translateY(0) rotate(45deg)';
            lines[1].style.transform = 'translateY(0) rotate(-45deg)';
            document.querySelectorAll('#mobile-menu .menu-link').forEach(link => {
                link.style.opacity = '1';
                link.style.transform = 'translateY(0)';
            });
        });
        menuBtn.dataset.open = 'true';
    };

    const closeMenu = () => {
        lines[0].style.transform = '';
        lines[1].style.transform = '';
        document.querySelectorAll('#mobile-menu .menu-link').forEach(link => {
            link.style.opacity = '0';
            link.style.transform = '';
        });
        setTimeout(() => {
            mobileMenu.classList.add('hidden');
            mobileMenu.classList.remove('flex');
        }, 400);
        menuBtn.dataset.open = 'false';
    };

    if (menuBtn) {
        menuBtn.addEventListener('click', () => {
            menuBtn.dataset.open === 'true' ? closeMenu() : openMenu();
        });
        mobileMenu.querySelectorAll('a, button').forEach(el => {
            el.addEventListener('click', closeMenu);
        });
    }

    /* --- Scroll entry animations (IntersectionObserver) --- */
    const revealEls = document.querySelectorAll('.reveal');
    if (revealEls.length && 'IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach((entry, i) => {
                if (entry.isIntersecting) {
                    setTimeout(() => entry.target.classList.add('reveal-visible'), (i % 4) * 80);
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });
        revealEls.forEach(el => io.observe(el));
    } else {
        revealEls.forEach(el => el.classList.add('reveal-visible'));
    }

    /* --- Toasts auto-dismiss + close --- */
    document.querySelectorAll('.toast').forEach(toast => {
        const dismiss = () => {
            toast.classList.add('toast-out');
            setTimeout(() => toast.remove(), 400);
        };
        const closeBtn = toast.querySelector('.toast-close');
        if (closeBtn) closeBtn.addEventListener('click', dismiss);
        setTimeout(dismiss, 4500);
    });

    /* --- Delete confirm --- */
    document.querySelectorAll('form[data-confirm]').forEach(form => {
        form.addEventListener('submit', (e) => {
            if (!confirm(form.dataset.confirm)) e.preventDefault();
        });
    });
});