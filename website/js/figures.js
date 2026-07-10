/**
 * Animated SVG overlays for AI plates.
 * Plates stay static; overlays provide motion language.
 */
(function () {
  "use strict";

  var OVERLAYS = {
    scan: function () {
      return (
        '<line class="ov-scan" x1="0" y1="18%" x2="100%" y2="18%"/>' +
        '<line class="ov-scan" x1="0" y1="52%" x2="100%" y2="52%" style="animation-delay:-1.5s"/>' +
        '<line class="ov-scan" x1="0" y1="82%" x2="100%" y2="82%" style="animation-delay:-3s"/>'
      );
    },
    endpoints: function () {
      return (
        '<circle class="ov-pulse" cx="12%" cy="50%" r="7"/>' +
        '<circle class="ov-pulse" cx="88%" cy="50%" r="7" style="animation-delay:-1.2s"/>' +
        '<line x1="14%" y1="50%" x2="86%" y2="50%" stroke="rgba(201,169,98,0.35)" stroke-width="1" stroke-dasharray="4 6"/>' +
        '<circle class="ov-dot" r="3">' +
        '<animateMotion dur="5s" repeatCount="indefinite" path="M 14,0 L 86,0"/>' +
        "</circle>"
      );
    },
    witness: function () {
      return (
        '<circle class="ov-pulse" cx="42%" cy="58%" r="8"/>' +
        '<circle class="ov-ring" cx="42%" cy="58%" r="16" style="transform-origin:42% 58%"/>' +
        '<line x1="8%" y1="58%" x2="92%" y2="58%" stroke="rgba(201,169,98,0.25)" stroke-width="1"/>'
      );
    },
    residual: function () {
      return (
        '<rect class="ov-field" x="10%" y="20%" width="80%" height="60%" rx="2"/>' +
        '<circle class="ov-pulse" cx="70%" cy="40%" r="5" style="animation-delay:-0.8s"/>' +
        '<circle class="ov-pulse" cx="30%" cy="65%" r="6" style="animation-delay:-1.6s"/>'
      );
    },
    seal: function () {
      return (
        '<circle class="ov-ring" cx="50%" cy="50%" r="28" style="transform-origin:50% 50%"/>' +
        '<circle class="ov-pulse" cx="50%" cy="50%" r="6"/>'
      );
    },
    chain: function () {
      return (
        '<polyline fill="none" stroke="rgba(201,169,98,0.35)" stroke-width="1.2" points="10,70 28,40 46,55 64,30 82,48 92,35"/>' +
        '<circle class="ov-dot" r="3.5"><animateMotion dur="6s" repeatCount="indefinite" path="M10,70 L28,40 L46,55 L64,30 L82,48 L92,35"/></circle>'
      );
    },
    bars: function () {
      return (
        '<line class="ov-scan" x1="15%" y1="85%" x2="15%" y2="25%" style="animation-duration:3s"/>' +
        '<line class="ov-scan" x1="35%" y1="85%" x2="35%" y2="40%" style="animation-duration:3.4s;animation-delay:-0.5s"/>' +
        '<line class="ov-scan" x1="55%" y1="85%" x2="55%" y2="20%" style="animation-duration:2.8s;animation-delay:-1s"/>' +
        '<line class="ov-scan" x1="75%" y1="85%" x2="75%" y2="45%" style="animation-duration:3.2s;animation-delay:-1.5s"/>'
      );
    }
  };

  function mountOverlay(frame, kind) {
    if (!kind || !OVERLAYS[kind]) return;
    var layer = document.createElement("div");
    layer.className = "figure-overlay";
    layer.setAttribute("aria-hidden", "true");
    layer.innerHTML =
      '<svg viewBox="0 0 100 100" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">' +
      "<defs>" +
      '<linearGradient id="ovGoldFade" x1="0" y1="0" x2="1" y2="1">' +
      '<stop offset="0%" stop-color="#c9a962" stop-opacity="0.05"/>' +
      '<stop offset="50%" stop-color="#e8d5a3" stop-opacity="0.2"/>' +
      '<stop offset="100%" stop-color="#c9a962" stop-opacity="0.05"/>' +
      "</linearGradient>" +
      "</defs>" +
      OVERLAYS[kind]() +
      "</svg>";
    frame.appendChild(layer);
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".figure-frame[data-overlay]").forEach(function (frame) {
      mountOverlay(frame, frame.getAttribute("data-overlay"));
    });
  });
})();
