/**
 * NexaBank — main.js
 */

document.addEventListener("DOMContentLoaded", function () {

  var scrollContainer = document.querySelector("[data-scroll-container]");
  if (scrollContainer && typeof LocomotiveScroll !== "undefined") {
    var locoScroll = new LocomotiveScroll({
      el: scrollContainer,
      smooth: true,
      smoothMobile: false,
      lerp: 0.08,
    });
    window.addEventListener("resize", function () { locoScroll.update(); });
  }

  document.querySelectorAll(".toggle-pw").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var targetId = btn.getAttribute("data-target");
      var input = document.getElementById(targetId);
      if (!input) return;
      var icon = btn.querySelector("i");
      if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("bi-eye", "bi-eye-slash");
      } else {
        input.type = "password";
        icon.classList.replace("bi-eye-slash", "bi-eye");
      }
    });
  });

  setTimeout(function () {
    document.querySelectorAll(".flash-container .alert").forEach(function (el) {
      if (window.bootstrap && window.bootstrap.Alert) {
        window.bootstrap.Alert.getOrCreateInstance(el).close();
      } else {
        el.style.display = "none";
      }
    });
  }, 5000);

});
