document.addEventListener('DOMContentLoaded', () => {

    /* --- Mobil menyu (hamburger morph) --- */
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

    /* --- Nav shrink on scroll --- */
    const nav = document.getElementById('main-nav');
    let navTicking = false;
    const updateNav = () => {
        nav.style.transform = window.scrollY > 40
            ? 'translateY(-2px) scale(0.985)'
            : '';
        nav.style.boxShadow = window.scrollY > 40
            ? '0 12px 40px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.06)'
            : '';
        navTicking = false;
    };
    if (nav) {
        window.addEventListener('scroll', () => {
            if (!navTicking) {
                navTicking = true;
                requestAnimationFrame(updateNav);
            }
        }, { passive: true });
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

    /* --- Live particle background canvas --- */
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const canvas = document.getElementById('bg-canvas');
    if (canvas && !reduced) {
        const ctx = canvas.getContext('2d');
        let w, h, dpr, particles = [], mouse = { x: -9999, y: -9999 };
        const count = () => Math.min(90, Math.floor(window.innerWidth / 16));

        const rand = (min, max) => min + Math.random() * (max - min);

        const makeParticle = () => ({
            x: Math.random() * w,
            y: Math.random() * h,
            r: rand(0.8, 2.6),
            vy: rand(0.12, 0.5),
            vx: rand(-0.12, 0.12),
            alpha: rand(0.08, 0.5),
            pulse: rand(0.4, 1.6),
        });

        const resize = () => {
            dpr = Math.min(window.devicePixelRatio || 1, 2);
            w = window.innerWidth;
            h = window.innerHeight;
            canvas.width = w * dpr;
            canvas.height = h * dpr;
            canvas.style.width = w + 'px';
            canvas.style.height = h + 'px';
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            particles = Array.from({ length: count() }, makeParticle);
        };

        let frame;
        const loop = (t) => {
            const dt = (t - (frame || t)) / 1000;
            frame = t;
            ctx.clearRect(0, 0, w, h);
            for (const p of particles) {
                p.y -= p.vy * dt * 60;
                p.x += (p.vx + (mouse.x - p.x) * 0.00002) * dt * 60;
                if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
                if (p.x < -10) p.x = w + 10;
                if (p.x > w + 10) p.x = -10;
                const twinkle = 0.6 + 0.4 * Math.sin((t / 1000) * p.pulse + p.r * 7);
                ctx.beginPath();
                ctx.fillStyle = `rgba(52, 211, 153, ${(p.alpha * twinkle).toFixed(3)})`;
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fill();
            }
            requestAnimationFrame(loop);
        };

        resize();
        window.addEventListener('resize', resize, { passive: true });
        window.addEventListener('mousemove', (e) => {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        }, { passive: true });
        requestAnimationFrame(loop);
    }

    /* --- Cursor glow (lerp follow, fine pointers only) --- */
    const glow = document.getElementById('cursor-glow');
    if (glow && window.matchMedia('(pointer: fine)').matches && !reduced) {
        let tx = window.innerWidth / 2, ty = window.innerHeight / 2, x = tx, y = ty;
        window.addEventListener('mousemove', (e) => {
            tx = e.clientX;
            ty = e.clientY;
        }, { passive: true });
        const glowLoop = () => {
            x += (tx - x) * 0.08;
            y += (ty - y) * 0.08;
            glow.style.transform = `translate(${x - 240}px, ${y - 240}px)`;
            requestAnimationFrame(glowLoop);
        };
        glowLoop();
    }
});