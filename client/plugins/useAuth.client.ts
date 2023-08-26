import { defineNuxtPlugin } from "#app";
import { ofetch } from "ofetch";
import { getLocalData, LocalData } from "~/utils/local";

const defaultHeaders = {
  "Content-Type": "application/json",
  "Accept-Language": "ru-RU",
};

export default defineNuxtPlugin((nuxtApp) => {
  globalThis.$fetch = ofetch.create({
    baseURL: "/api/",
    headers: defaultHeaders,
    async onRequest({ request, options }) {
      const token = getLocalData(LocalData.ACCESS_TOKEN);
      if (token)
        options.headers = {
          ...defaultHeaders,
          Authorization: `Bearer ${token}`,
        };
      else console.log("No token found!");
    },
    async onRequestError({ request, response, options }) {
      if (response?.status === 403) {
        console.log("AUTH ERROR");
      }
    },
  });
});
