    // Hero portrait: the head turns toward the cursor. 64 pre-rendered frames,
    // one per 5.625deg around the face; nearest frame is drawn, never blended.
    // Fine pointers only, and not under reduced motion: everyone else keeps the still portrait.
    (function () {
      var canvas = document.getElementById('heroCanvas');
      var hero = canvas && canvas.closest('.hero');
      if (!canvas || !matchMedia('(pointer: fine) and (hover: hover)').matches || matchMedia('(prefers-reduced-motion: reduce)').matches) return;
      var N = 64, STEP = 360 / N, VW = 1280, VH = 720, FACE_X = 640, FACE_Y = 270;
      var RESPONSE = 0.26, DEADZONE = 0.12, ANCHOR_Y = 0.25;
      var ctx = canvas.getContext('2d', { alpha: false });
      var frames = new Array(N), center = null, pending = N + 1;
      var W = 0, H = 0, scale = 1, ox = 0, oy = 0, dpr = 1;
      var pointer = null, angle = null, drawn = null, last = 0, raf = 0, inView = true;
      function lerpAngle(a, b, t) { return a + ((((b - a) % 360) + 540) % 360 - 180) * t; }
      function resize() {
        dpr = Math.min(window.devicePixelRatio || 1, 2);
        W = hero.clientWidth; H = hero.clientHeight;
        canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
        scale = Math.max(W / VW, H / VH);
        ox = (W - VW * scale) / 2; oy = (H - VH * scale) * ANCHOR_Y;
        ctx.imageSmoothingQuality = 'high'; drawn = null;
      }
      function draw(img, key) {
        if (!img || key === drawn) return;
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        ctx.drawImage(img, ox, oy, VW * scale, VH * scale);
        drawn = key;
      }
      function tick(now) {
        raf = 0;
        if (!inView) return;
        var dt = Math.min(now - (last || now), 100); last = now;
        var fx = ox + FACE_X * scale, fy = oy + FACE_Y * scale;
        var dx = pointer ? pointer.x - fx : 0, dy = pointer ? pointer.y - fy : 0;
        if (!pointer || Math.sqrt(dx * dx + dy * dy) < DEADZONE * Math.max(W, H)) {
          angle = null; draw(center, 'c');
        } else {
          var target = Math.atan2(dy, dx) * 180 / Math.PI;
          angle = angle === null ? target : lerpAngle(angle, target, 1 - Math.pow(1 - RESPONSE, dt / 16.667));
          var i = ((Math.round(angle / STEP) % N) + N) % N;
          draw(frames[i] || center, frames[i] ? i : 'c');
        }
        raf = requestAnimationFrame(tick);
      }
      function start() { if (!raf && inView && center) { last = 0; raf = requestAnimationFrame(tick); } }
      function loaded() { if (--pending === 0) { resize(); canvas.classList.add('ready'); start(); } }
      function load(url, cb) { var img = new Image(); img.onload = function () { cb(img); loaded(); }; img.onerror = loaded; img.src = url; }
      function begin() {
        load('/assets/hero-frames/center.webp', function (img) { center = img; });
        for (var k = 0; k < N; k++) (function (k) {
          load('/assets/hero-frames/' + (k < 10 ? '0' : '') + k + '.webp', function (img) { frames[k] = img; });
        })(k);
      }
      window.addEventListener('pointermove', function (e) {
        var r = hero.getBoundingClientRect(); pointer = { x: e.clientX - r.left, y: e.clientY - r.top };
      }, { passive: true });
      document.documentElement.addEventListener('pointerleave', function () { pointer = null; });
      window.addEventListener('resize', function () { if (center) resize(); }, { passive: true });
      new IntersectionObserver(function (es) { inView = es[0].isIntersecting; start(); }).observe(hero);
      // Frames are not needed for first paint: fetch them once the page has settled.
      if (document.readyState === 'complete') begin(); else window.addEventListener('load', begin);
    }());
    if (window.innerWidth <= 480) {
      const s = document.getElementById('heroSubhead');
      if (s) s.innerHTML = 'Stop shouting to nobody.<br>Start speaking to somebody.';
    }
    // Testimonial carousel: stacked image/video panels + cross-fading quote cards
    (function () {
      var stack     = document.getElementById('testimonialStack');
      var cardStack = document.getElementById('testimonialCardStack');
      var dotsWrap  = document.getElementById('testimonialDots');
      if (!stack || !cardStack) return;

      var stackItems = Array.from(stack.querySelectorAll('.testimonial-stack-item'));
      var cards      = Array.from(cardStack.querySelectorAll('.testimonial-card'));
      var dots       = dotsWrap ? Array.from(dotsWrap.querySelectorAll('.testimonial-dot')) : [];
      var active     = 0;
      var AUTOPLAY_MS = 6000;
      var autoplayTimer = null;
      var reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;

      // Split each quote into words for the per-word blur-in effect.
      cards.forEach(function (card) {
        var q = card.querySelector('.testimonial-card-quote');
        if (!q || q.dataset.wrapped) return;
        var words = q.textContent.trim().split(/\s+/);
        q.innerHTML = words.map(function (w, i) {
          return '<span class="word" style="transition-delay:' + (i * 16) + 'ms">' + w + '</span>';
        }).join(' ');
        q.dataset.wrapped = 'true';
      });

      function stopVideo(item) {
        if (!item.classList.contains('playing')) return;
        var iframe = item.querySelector('iframe');
        if (iframe) iframe.remove();
        item.classList.remove('playing');
      }

      function stopAutoplay() {
        if (autoplayTimer) { clearInterval(autoplayTimer); autoplayTimer = null; }
      }

      function goTo(newIndex) {
        if (newIndex === active || !stackItems.length) return;
        var prevActive = active;

        stackItems.forEach(function (item, i) {
          if (i === prevActive) stopVideo(item);
          item.setAttribute('data-state', i === newIndex ? 'active' : 'behind');
        });

        cards.forEach(function (card, i) {
          var isNext = i === newIndex;
          card.setAttribute('data-active', String(isNext));
          if (isNext) {
            var q = card.querySelector('.testimonial-card-quote');
            if (q) {
              q.classList.remove('blur-in');
              void q.offsetWidth;
              requestAnimationFrame(function () { q.classList.add('blur-in'); });
            }
          }
        });

        dots.forEach(function (dot, i) { dot.setAttribute('aria-current', String(i === newIndex)); });

        active = newIndex;
      }

      dots.forEach(function (dot, i) {
        dot.addEventListener('click', function () { stopAutoplay(); goTo(i); });
      });
      stackItems.forEach(function (item) {
        item.addEventListener('click', stopAutoplay);
      });

      // Run the first blur-in and start a brief autoplay once the carousel scrolls into view.
      var section = document.querySelector('.section-testimonial');
      if (section) {
        var initObs = new IntersectionObserver(function (entries) {
          entries.forEach(function (e) {
            if (e.isIntersecting) {
              var q = cards[active] && cards[active].querySelector('.testimonial-card-quote');
              if (q) q.classList.add('blur-in');
              if (!reducedMotion && stackItems.length > 1) {
                autoplayTimer = setInterval(function () { goTo((active + 1) % stackItems.length); }, AUTOPLAY_MS);
              }
              initObs.unobserve(e.target);
            }
          });
        }, { threshold: 0.3 });
        initObs.observe(section);

        section.addEventListener('mouseenter', stopAutoplay);
      }
    }());

