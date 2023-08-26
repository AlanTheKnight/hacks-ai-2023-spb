import path from "path";

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: ["@formkit/nuxt", "@pinia/nuxt"],
  css: ["~/assets/styles/main.scss", "bootstrap-icons/font/bootstrap-icons.css"],
  components: ["~/components"],
  ssr: true,
  nitro: {
    output: {
      publicDir: path.join(__dirname, "../backend/output"),
    },
  },
  formkit: {
    configFile: "./formkit.config.ts",
  },
  app: {
    head: {
      title: "NeoPitch",
      link: [
        {
          rel: "preconnect",
          href: "https://fonts.googleapis.com",
        },
        {
          rel: "preconnect",
          href: "https://fonts.gstatic.com",
          crossorigin: "anonymous",
        },
        {
          href: "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;600;700;800;900&display=swap",
          rel: "stylesheet",
        },
        {
          rel: "icon",
          href: "/favicon.ico",
        },
      ],
      htmlAttrs: {
        "data-bs-theme": "dark",
      },
    },
  },
});
