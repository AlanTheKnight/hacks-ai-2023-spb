export const scrollToSection = (elId: string) => {
  const el = document.querySelector(elId);
  if (!el) return;
  hideNavbar();
  const elementPosition = el.getBoundingClientRect().top;
  const offset = 75;
  const offsetPosition = elementPosition + window.scrollY - offset;
  window.scrollTo({ top: offsetPosition, behavior: "smooth" });
};

export const hideNavbar = () => {
  const btn = document.getElementById("mainNavbarToggler");
  if (btn && !btn.classList.contains("collapsed")) {
    const content = document.getElementById("mainNavbarContent");
    content!.classList.remove("show");
    btn.classList.add("collapsed");
  }
};
