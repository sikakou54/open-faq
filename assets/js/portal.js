/* FAQ 設計ポータル — 共通シェル構築スクリプト
   各 HTML は <article class="content"> の本文だけを持ち、サイドバー・トップバー・
   パンくず・目次・検索・テーマ切替を本スクリプトが読み込み時に注入する。
   ナビは window.NAV、検索は window.SEARCH_INDEX を参照する(いずれも file:// 可)。
   アイコンは Bootstrap Icons(CDN)。本スクリプトが <head> に CSS を読み込む。 */
(function(){
  "use strict";
  var ROOT = window.PORTAL_ROOT || "";

  /* --- アイコン(Bootstrap Icons CDN)を読み込む --- */
  if(!document.querySelector('link[data-portal-icons]')){
    var iconCss = document.createElement('link');
    iconCss.rel = 'stylesheet';
    iconCss.href = 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css';
    iconCss.setAttribute('data-portal-icons', '');
    document.head.appendChild(iconCss);
  }
  var NAV = window.NAV || [];
  var IDX = window.SEARCH_INDEX || [];
  var pageId = (document.body.getAttribute('data-page-id') || "").replace(/^\.\//,'');
  var isHome = pageId === "index.html" || document.body.classList.contains('page-home');
  var isDiagram = document.body.classList.contains('page-diagram');

  function esc(s){ return String(s).replace(/[&<>"]/g,function(c){
    return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }
  function reEsc(s){ return s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'); }

  /* --- ページ メタ情報の逆引き --- */
  var meta = null;
  NAV.forEach(function(sys){
    sys.cats.forEach(function(cat){
      function scan(p){
        if(p.url === pageId){
          meta = {sysKey:sys.key, sysLabel:sys.label, catKey:cat.key,
                  catLabel:cat.label, title:p.title, kind:p.kind};
        }
      }
      cat.pages.forEach(function(p){
        scan(p);
        if(p.children) p.children.forEach(scan);
      });
    });
  });

  /* --- サイドバー --- */
  function buildSidebar(){
    var h = [];
    h.push('<a class="brand" href="'+ROOT+'index.html"><span class="brand-mark">FAQ</span>'+
           '<span class="brand-text">設計ポータル</span></a>');
    h.push('<div class="search-box"><i class="bi bi-search search-icon" aria-hidden="true"></i>'+
           '<input type="search" id="search-input" '+
           'placeholder="ドキュメント内を検索…" autocomplete="off" aria-label="検索">'+
           '<div class="search-results" id="search-results" hidden></div></div>');
    h.push('<div class="nav-scroll">');
    h.push('<a class="nav-home'+(isHome?' active':'')+'" href="'+ROOT+'index.html">'+
           '<i class="bi bi-house-door" aria-hidden="true"></i> ポータルトップ</a>');
    NAV.forEach(function(sys){
      var sysOpen = meta && meta.sysKey === sys.key;
      h.push('<details class="nav-system"'+(sysOpen?' open':'')+'>');
      h.push('<summary>'+esc(sys.label)+'</summary>');
      var flat = sys.cats.length === 1 && sys.cats[0].key === "__root__";
      function pageHit(p){
        return p.url===pageId || (p.children && p.children.some(function(c){return c.url===pageId;}));
      }
      function pushPage(p){
        if(p.children && p.children.length){
          var grpOpen = sysOpen && pageHit(p);
          h.push('<li><details class="nav-subcat"'+(grpOpen?' open':'')+'>');
          h.push('<summary>'+esc(p.title)+'</summary><ul>');
          if(p.url){ h.push('<li>'+link({url:p.url,title:'画面一覧・共通',kind:p.kind})+'</li>'); }
          p.children.forEach(function(c){ h.push('<li>'+link(c)+'</li>'); });
          h.push('</ul></details></li>');
        } else {
          h.push('<li>'+link(p)+'</li>');
        }
      }
      sys.cats.forEach(function(cat){
        var catOpen = sysOpen && cat.pages.some(pageHit);
        if(flat){
          cat.pages.forEach(function(p){ h.push(link(p)); });
        } else {
          h.push('<details class="nav-cat"'+(catOpen?' open':'')+'>');
          h.push('<summary>'+esc(cat.label)+'</summary><ul>');
          cat.pages.forEach(pushPage);
          h.push('</ul></details>');
        }
      });
      h.push('</details>');
    });
    h.push('</div>');
    function link(p){
      var active = p.url === pageId;
      return '<a class="nav-link'+(active?' active':'')+'" href="'+ROOT+p.url+'"'+
        (active?' aria-current="page"':'')+'>'+esc(p.title)+
        (p.kind==='diagram'?' <span class="nav-badge">図</span>':'')+'</a>';
    }
    var nav = document.createElement('nav');
    nav.className = 'sidebar'; nav.id = 'sidebar';
    nav.setAttribute('aria-label','ドキュメントナビゲーション');
    nav.innerHTML = h.join('');
    return nav;
  }

  /* --- パンくず --- */
  function buildBreadcrumb(){
    var parts = [];
    if(isHome){ parts.push('<span aria-current="page">ポータル</span>'); }
    else {
      parts.push('<a href="'+ROOT+'index.html">ポータル</a>');
      if(meta){
        parts.push('<span>'+esc(meta.sysLabel)+'</span>');
        if(meta.catLabel && meta.catKey !== '__root__' && meta.catLabel !== meta.sysLabel)
          parts.push('<span>'+esc(meta.catLabel)+'</span>');
        parts.push('<span aria-current="page">'+esc(meta.title)+'</span>');
      } else {
        parts.push('<span aria-current="page">'+esc(document.title.split('|')[0].trim())+'</span>');
      }
    }
    return parts.join('<span class="sep">/</span>');
  }

  /* --- DOM 組み立て --- */
  var article = document.querySelector('article.content') || document.querySelector('main') || document.body.firstElementChild;

  // page-meta タグ(本文ページのみ)
  if(meta && !isHome && !isDiagram && meta.catKey !== '__root__'){
    var pm = document.createElement('div'); pm.className='page-meta';
    pm.innerHTML = '<span class="tag tag-sys">'+esc(meta.sysLabel)+'</span>'+
      (meta.catLabel?'<span class="tag tag-cat">'+esc(meta.catLabel)+'</span>':'');
    article.insertBefore(pm, article.firstChild);
  } else if(meta && !isHome && meta.catKey === '__root__'){
    var pm2 = document.createElement('div'); pm2.className='page-meta';
    pm2.innerHTML = '<span class="tag tag-sys">'+esc(meta.sysLabel)+'</span>';
    article.insertBefore(pm2, article.firstChild);
  }

  var skip = document.createElement('a');
  skip.className='skip-link'; skip.href='#content'; skip.textContent='本文へスキップ';

  var topbar = document.createElement('header');
  topbar.className='topbar';
  topbar.innerHTML =
    '<button class="menu-toggle" id="menu-toggle" aria-label="メニュー" aria-expanded="false"><i class="bi bi-list" aria-hidden="true"></i></button>'+
    '<nav class="breadcrumb" aria-label="パンくず">'+buildBreadcrumb()+'</nav>'+
    '<button class="theme-toggle" id="theme-toggle" aria-label="テーマ切替" title="ライト / ダーク切替"><i class="bi bi-circle-half" aria-hidden="true"></i></button>';

  var layout = document.createElement('div'); layout.className='layout';
  var sidebar = buildSidebar();
  var main = document.createElement('main'); main.className='main'; main.id='main';
  var wrap = document.createElement('div'); wrap.className='content-wrap';

  // article を移設
  article.parentNode.removeChild(article);
  wrap.appendChild(article);

  var tocAside = null;
  if(!isDiagram){
    tocAside = document.createElement('aside');
    tocAside.className='toc'; tocAside.id='toc';
    tocAside.setAttribute('aria-label','ページ内目次');
    tocAside.innerHTML='<div class="toc-title">目次</div><nav id="toc-nav"></nav>';
    wrap.appendChild(tocAside);
  }
  main.appendChild(wrap);
  layout.appendChild(sidebar); layout.appendChild(main);

  var backdrop = document.createElement('div'); backdrop.className='backdrop'; backdrop.id='backdrop';

  document.body.insertBefore(skip, document.body.firstChild);
  document.body.appendChild(topbar);
  document.body.appendChild(layout);
  document.body.appendChild(backdrop);
  document.body.classList.add('portal-ready');

  /* --- テーマ切替 --- */
  document.getElementById('theme-toggle').addEventListener('click', function(){
    var cur = document.documentElement.dataset.theme === 'dark' ? '' : 'dark';
    document.documentElement.dataset.theme = cur;
    try{ localStorage.setItem('portal-theme', cur); }catch(e){}
  });

  /* --- モバイル サイドバー --- */
  var menuBtn = document.getElementById('menu-toggle');
  function closeNav(){ document.body.classList.remove('nav-open');
    menuBtn.setAttribute('aria-expanded','false'); }
  menuBtn.addEventListener('click', function(){
    var open = document.body.classList.toggle('nav-open');
    menuBtn.setAttribute('aria-expanded', open?'true':'false');
  });
  backdrop.addEventListener('click', closeNav);

  /* --- アクティブ項目を表示域へ --- */
  var act = sidebar.querySelector('.nav-link.active');
  if(act){ var sc = sidebar.querySelector('.nav-scroll');
    if(sc){ var t = act.offsetTop - sc.clientHeight/2; if(t>0) sc.scrollTop = t; } }

  /* --- テーブル横スクロール --- */
  article.querySelectorAll('table').forEach(function(tb){
    if(tb.parentElement && tb.parentElement.classList.contains('table-scroll')) return;
    var w = document.createElement('div'); w.className='table-scroll';
    tb.parentNode.insertBefore(w, tb); w.appendChild(tb);
  });

  /* --- Mermaid 図(CDN)を描画 ---
     本文内の <pre class="mermaid"> / .mermaid をフロー図・遷移図として描画する。
     ライブラリは CDN から動的読み込み(アイコンと同様に通信が必要)。
     読み込めない場合はソース(コードブロック)がそのまま残る(グレースフルデグレード)。 */
  (function(){
    var mNodes = Array.prototype.slice.call(article.querySelectorAll('.mermaid'));
    if(!mNodes.length) return;
    mNodes.forEach(function(el){
      if(!el.hasAttribute('data-mermaid-src'))
        el.setAttribute('data-mermaid-src', (el.textContent||'').replace(/^\s*\n/,''));
    });
    function themeName(){ return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'default'; }
    var busy = false;
    function renderMermaid(){
      if(busy) return; busy = true;
      import('https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs')
        .then(function(mod){
          var mermaid = mod.default;
          mNodes.forEach(function(el){
            el.removeAttribute('data-processed');
            el.textContent = el.getAttribute('data-mermaid-src');
          });
          mermaid.initialize({ startOnLoad:false, theme: themeName(),
            securityLevel:'loose', flowchart:{ htmlLabels:true, useMaxWidth:true } });
          return mermaid.run({ nodes: mNodes });
        })
        .then(function(){ busy = false; })
        .catch(function(err){ busy = false; if(window.console) console.error('Mermaid 描画失敗:', err); });
    }
    renderMermaid();
    /* テーマ切替に追従して再描画(切替ハンドラが dataset.theme を更新した後に実行) */
    var tBtn = document.getElementById('theme-toggle');
    if(tBtn) tBtn.addEventListener('click', function(){ setTimeout(renderMermaid, 0); });
  })();

  /* --- 見出しアンカー + 目次 + スクロールスパイ --- */
  var heads = article.querySelectorAll('h2, h3');
  var usedIds = {};
  heads.forEach(function(h){
    if(!h.id){
      var base = h.textContent.trim().replace(/\s+/g,'-'), id = base, k = 2;
      while(usedIds[id] || document.getElementById(id)){ id = base+'-'+k; k++; }
      h.id = id;
    }
    usedIds[h.id] = true;
    var a = document.createElement('a');
    a.className='heading-anchor'; a.href='#'+h.id;
    a.innerHTML='<i class="bi bi-link-45deg" aria-hidden="true"></i>';
    a.setAttribute('aria-label','この見出しへのリンク'); h.appendChild(a);
  });
  var tocNav = tocAside ? document.getElementById('toc-nav') : null;
  if(tocNav && heads.length >= 2){
    heads.forEach(function(h){
      var a = document.createElement('a'); a.href='#'+h.id;
      a.textContent = h.textContent.replace(/#$/,'').trim();
      a.className = h.tagName==='H3' ? 'lvl-3':'lvl-2';
      tocNav.appendChild(a);
    });
    var links = tocNav.querySelectorAll('a');
    var spy = function(){
      var pos = window.scrollY + 90, cur = null;
      heads.forEach(function(h){ if(h.offsetTop <= pos) cur = h.id; });
      links.forEach(function(l){ l.classList.toggle('active', l.getAttribute('href')==='#'+cur); });
    };
    window.addEventListener('scroll', spy, {passive:true}); spy();
  } else if(tocAside){ tocAside.style.display='none'; }

  /* --- 検索 --- */
  var input = document.getElementById('search-input');
  var box = document.getElementById('search-results');
  function snippet(text, q){
    var i = text.toLowerCase().indexOf(q.toLowerCase()); if(i<0) return '';
    var s = (i>30?'…':'')+text.slice(Math.max(0,i-30), Math.min(text.length,i+q.length+50))+
            (i+q.length+50<text.length?'…':'');
    return esc(s).replace(new RegExp(reEsc(esc(q)),'ig'), function(m){return '<mark>'+m+'</mark>';});
  }
  var selIdx = -1;
  function render(results, q){
    selIdx = -1;
    if(!results.length){ box.innerHTML='<div class="sr-empty">該当なし</div>'; box.hidden=false; return; }
    box.innerHTML = results.map(function(r){
      var sn = snippet(r.b, q) || esc(r.h.join(' / '));
      return '<a href="'+ROOT+r.u+'"><span class="sr-title">'+esc(r.t)+'</span>'+
        '<span class="sr-path">'+esc(r.s)+(r.c?(' › '+esc(r.c)):'')+'</span>'+
        (sn?('<span class="sr-path">'+sn+'</span>'):'')+'</a>';
    }).join('');
    box.hidden=false;
  }
  function search(q){
    q = q.trim(); if(q.length<1){ box.hidden=true; return; }
    var ql = q.toLowerCase(), scored = [];
    IDX.forEach(function(r){
      var s = 0;
      if(r.t.toLowerCase().indexOf(ql)>=0) s+=10;
      if(r.u.toLowerCase().indexOf(ql)>=0) s+=5;
      if(r.h.join(' ').toLowerCase().indexOf(ql)>=0) s+=4;
      if(r.b.toLowerCase().indexOf(ql)>=0) s+=1;
      if(s>0) scored.push({r:r,s:s});
    });
    scored.sort(function(a,b){return b.s-a.s;});
    render(scored.slice(0,30).map(function(x){return x.r;}), q);
  }
  input.addEventListener('input', function(){ search(this.value); });
  input.addEventListener('focus', function(){ if(this.value) search(this.value); });
  input.addEventListener('keydown', function(e){
    var items = box.querySelectorAll('a');
    if(e.key==='ArrowDown'){ e.preventDefault(); selIdx=Math.min(selIdx+1,items.length-1); }
    else if(e.key==='ArrowUp'){ e.preventDefault(); selIdx=Math.max(selIdx-1,0); }
    else if(e.key==='Enter'){ if(selIdx>=0&&items[selIdx]) location.href=items[selIdx].href; return; }
    else if(e.key==='Escape'){ box.hidden=true; this.blur(); return; }
    else return;
    items.forEach(function(it,i){ it.classList.toggle('sel', i===selIdx);
      if(i===selIdx) it.scrollIntoView({block:'nearest'}); });
  });
  document.addEventListener('click', function(e){
    if(!box.contains(e.target) && e.target!==input) box.hidden=true;
  });
})();
