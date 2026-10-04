document.body.classList.add('js-ready');
    const obs = new IntersectionObserver((entries) => {
      entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
    }, { threshold: 0.04, rootMargin: '0px 0px -24px 0px' });
    document.querySelectorAll('.reveal').forEach(el => obs.observe(el));

    // Facade video embeds: swap poster + play button for the real iframe on click,
    // so no YouTube branding/title overlay shows before the visitor chooses to play.
    document.querySelectorAll('[data-video-id]').forEach(wrap => {
      function play() {
        if (wrap.classList.contains('playing')) return;
        const iframe = document.createElement('iframe');
        // allow must be set before src: the permission policy has to be in place
        // before the frame starts navigating, or autoplay-with-sound gets silently blocked.
        iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
        iframe.title = wrap.dataset.videoTitle || 'Video';
        iframe.allowFullscreen = true;
        iframe.src = `https://www.youtube-nocookie.com/embed/${wrap.dataset.videoId}?autoplay=1&rel=0&modestbranding=1`;
        iframe.addEventListener('load', () => iframe.classList.add('loaded'));
        wrap.appendChild(iframe);
        wrap.classList.add('playing');
      }
      wrap.addEventListener('click', play);
      wrap.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); play(); } });
    });

    const nav = document.getElementById('mainNav');
    function syncNav() {
      if (!document.body.classList.contains('home')) return;
      nav.classList.toggle('at-top', window.scrollY < 40);
      nav.classList.toggle('scrolled', window.scrollY > window.innerHeight * 0.85);
    }
    window.addEventListener('scroll', syncNav, { passive: true });
    syncNav();

    // ── THROUGHLINE SVG SCROLL TRACKER ──
    (function() {
      const tlNav = document.getElementById('tlNav');
      const tlFill = document.getElementById('tlFill');
      const tlTip = document.getElementById('tlTip');
      if (!tlNav || !tlFill || window.innerWidth < 900) return;

      let currentY2 = 0;
      let rafId;

      function lerp(a, b, t) { return a + (b - a) * t; }

      function frame() {
        const totalH = document.body.scrollHeight - window.innerHeight;
        const scrollPct = totalH > 0 ? Math.min(window.scrollY / totalH, 1) : 0;
        const vh = window.innerHeight;
        const targetY2 = scrollPct * vh;

        currentY2 = lerp(currentY2, targetY2, 0.12);
        tlFill.setAttribute('y2', currentY2);
        if (tlTip) {
          tlTip.setAttribute('cy', currentY2);
          tlTip.setAttribute('opacity', currentY2 > 4 ? '1' : '0');
        }

        rafId = requestAnimationFrame(frame);
      }

      frame();

      window.addEventListener('resize', () => {
        cancelAnimationFrame(rafId);
        currentY2 = 0;
        frame();
      }, { passive: true });
    })();

    // ── DOT CURSOR ──
    (function() {
      if (!matchMedia('(pointer:fine) and (hover:hover)').matches) return;

      const cur = document.createElement('div');
      cur.style.cssText = 'position:fixed;pointer-events:none;z-index:9999;width:10px;height:10px;border-radius:50%;background:#C2714F;transform:translate(-50%,-50%);opacity:0;will-change:left,top;left:-20px;top:-20px;';
      document.body.appendChild(cur);

      document.addEventListener('mousemove', e => {
        cur.style.opacity = '1';
        cur.style.left = e.clientX + 'px';
        cur.style.top = e.clientY + 'px';
      }, { passive: true });

      document.addEventListener('mouseleave', () => { cur.style.opacity = '0'; });
    })();

    (function(){var b=document.getElementById('navHamburger'),o=document.getElementById('navMobile');if(!b||!o)return;function t(open){b.classList.toggle('open',open);o.classList.toggle('open',open);b.setAttribute('aria-expanded',String(open));o.setAttribute('aria-hidden',String(!open));document.body.style.overflow=open?'hidden':'';}b.addEventListener('click',function(){t(!b.classList.contains('open'));});o.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){t(false);});});document.addEventListener('keydown',function(e){if(e.key==='Escape')t(false);});}());
  
    (function(){var KEY='tlco_consent_v1',stored=localStorage.getItem(KEY);function grantAnalytics(){if(window.gtag)gtag('consent','update',{analytics_storage:'granted',ad_storage:'granted',ad_user_data:'granted',ad_personalization:'granted'});if(!window._liLoaded){window._liLoaded=true;window._linkedin_partner_id='9504276';window._linkedin_data_partner_ids=window._linkedin_data_partner_ids||[];window._linkedin_data_partner_ids.push('9504276');(function(l){if(!l){window.lintrk=function(a,b){window.lintrk.q.push([a,b])};window.lintrk.q=[];}var s=document.getElementsByTagName('script')[0],b=document.createElement('script');b.type='text/javascript';b.async=true;b.src='https://snap.licdn.com/li.lms-analytics/insight.min.js';s.parentNode.insertBefore(b,s);})(window.lintrk);}}if(stored==='accepted'){grantAnalytics();}document.addEventListener('DOMContentLoaded',function(){var banner=document.getElementById('cookieBanner');function show(){if(!banner)return;banner.classList.add('visible');requestAnimationFrame(function(){document.documentElement.style.setProperty('--cookie-banner-h',banner.offsetHeight+'px');});window.addEventListener('resize',function(){if(banner.classList.contains('visible'))document.documentElement.style.setProperty('--cookie-banner-h',banner.offsetHeight+'px');});}function hide(){if(!banner)return;banner.classList.remove('visible');document.documentElement.style.setProperty('--cookie-banner-h','0px');}window.tlcoOpenConsent=function(){localStorage.removeItem(KEY);show();};if(!stored){show();}var ac=document.getElementById('cookieAccept'),dc=document.getElementById('cookieDecline');if(ac)ac.addEventListener('click',function(){localStorage.setItem(KEY,'accepted');hide();grantAnalytics();});if(dc)dc.addEventListener('click',function(){localStorage.setItem(KEY,'declined');hide();});});}());
console.log('%cLooking for the throughline?', 'font-size:16px;font-weight:bold;color:#C2714F;');
console.log('%cWe find them for brands like yours. throughline.community/contact', 'font-size:12px;color:#2C3E35;');
