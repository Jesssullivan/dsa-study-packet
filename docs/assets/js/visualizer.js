/* Generic algorithm step-visualizer — no dependencies.
 * Renders a trace JSON of frames using three primitives only:
 *   array (cells + named pointers + highlights), grid (2D table), vars (k=v).
 * Adding an algorithm = adding trace data, never code here.
 * Usage: <div class="algo-viz" data-trace="../../../assets/traces/<algo>.json"></div>
 */
(function () {
  "use strict";

  function el(tag, cls, txt) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (txt != null) e.textContent = txt;
    return e;
  }

  function renderArray(s) {
    var wrap = el("div", "viz-array-wrap");
    if (s.name) wrap.appendChild(el("div", "viz-name", s.name));
    var row = el("div", "viz-array");
    var hi = {}; (s.highlight || []).forEach(function (i) { hi[i] = 1; });
    var ptrs = s.pointers || {}, ptrAt = {};
    Object.keys(ptrs).forEach(function (k) {
      var i = ptrs[k]; if (i == null) return;
      (ptrAt[i] = ptrAt[i] || []).push(k);
    });
    (s.data || []).forEach(function (v, i) {
      var cell = el("div", "viz-cell" + (hi[i] ? " viz-hi" : ""));
      cell.appendChild(el("span", "viz-val", String(v)));
      cell.appendChild(el("span", "viz-idx", String(i)));
      if (ptrAt[i]) cell.appendChild(el("span", "viz-ptr", ptrAt[i].join(",")));
      row.appendChild(cell);
    });
    wrap.appendChild(row);
    return wrap;
  }

  function renderGrid(s) {
    var wrap = el("div", "viz-grid-wrap");
    if (s.name) wrap.appendChild(el("div", "viz-name", s.name));
    var table = el("table", "viz-grid");
    var hi = {}; (s.highlight || []).forEach(function (c) { hi[c[0] + "," + c[1]] = 1; });
    (s.data || []).forEach(function (rowData, r) {
      var tr = el("tr");
      rowData.forEach(function (v, c) {
        tr.appendChild(el("td", hi[r + "," + c] ? "viz-hi" : null, String(v)));
      });
      table.appendChild(tr);
    });
    wrap.appendChild(table);
    return wrap;
  }

  function renderVars(s) {
    var wrap = el("div", "viz-vars-wrap");
    if (s.name) wrap.appendChild(el("div", "viz-name", s.name));
    var box = el("div", "viz-vars"), data = s.data || {};
    Object.keys(data).forEach(function (k) {
      var item = el("span", "viz-var");
      item.appendChild(el("span", "viz-var-k", k));
      item.appendChild(el("span", "viz-var-v", String(data[k])));
      box.appendChild(item);
    });
    wrap.appendChild(box);
    return wrap;
  }

  function renderStructure(s) {
    if (s.kind === "grid") return renderGrid(s);
    if (s.kind === "vars") return renderVars(s);
    return renderArray(s);
  }

  function mount(container, trace) {
    container.innerHTML = "";
    container.classList.add("viz-ready");
    var header = el("div", "viz-header");
    header.appendChild(el("strong", null, trace.title || trace.algorithm || "Visualizer"));
    if (trace.input) header.appendChild(el("span", "viz-input", " " + trace.input));
    container.appendChild(header);

    var stage = el("div", "viz-stage"); container.appendChild(stage);
    var caption = el("div", "viz-caption"); container.appendChild(caption);

    var controls = el("div", "viz-controls");
    var first = el("button", "viz-btn", "⏮");
    var prev = el("button", "viz-btn", "◀");
    var play = el("button", "viz-btn viz-play", "Play");
    var next = el("button", "viz-btn", "▶");
    var last = el("button", "viz-btn", "⏭");
    var counter = el("span", "viz-counter");
    [first, prev, play, next, last, counter].forEach(function (c) { controls.appendChild(c); });
    container.appendChild(controls);

    var frames = trace.frames || [], idx = 0, timer = null;

    function draw() {
      stage.innerHTML = "";
      var f = frames[idx] || { structures: [] };
      (f.structures || []).forEach(function (s) { stage.appendChild(renderStructure(s)); });
      caption.textContent = f.caption || "";
      counter.textContent = "step " + (idx + 1) + " / " + frames.length;
      first.disabled = prev.disabled = idx === 0;
      next.disabled = last.disabled = idx >= frames.length - 1;
    }
    function go(i) { idx = Math.max(0, Math.min(frames.length - 1, i)); draw(); }
    function stop() { if (timer) { clearInterval(timer); timer = null; play.textContent = "Play"; } }

    first.onclick = function () { stop(); go(0); };
    prev.onclick = function () { stop(); go(idx - 1); };
    next.onclick = function () { stop(); go(idx + 1); };
    last.onclick = function () { stop(); go(frames.length - 1); };
    play.onclick = function () {
      if (timer) { stop(); return; }
      if (idx >= frames.length - 1) go(0);
      play.textContent = "Pause";
      timer = setInterval(function () {
        if (idx >= frames.length - 1) { stop(); return; }
        go(idx + 1);
      }, 900);
    };
    draw();
  }

  function initOne(c) {
    if (c.dataset.vizInit) return;
    c.dataset.vizInit = "1";
    var url = c.getAttribute("data-trace");
    if (!url) return;
    fetch(url).then(function (r) { return r.json(); })
      .then(function (t) { mount(c, t); })
      .catch(function (e) { c.textContent = "Visualizer unavailable (" + e + ")."; });
  }

  function initAll() { document.querySelectorAll(".algo-viz[data-trace]").forEach(initOne); }

  if (window.document$ && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(initAll); /* mkdocs-material instant navigation */
  } else if (document.readyState !== "loading") {
    initAll();
  } else {
    document.addEventListener("DOMContentLoaded", initAll);
  }
})();
