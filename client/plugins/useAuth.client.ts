import { defineNuxtPlugin } from "#app";
import { ofetch } from "ofetch";
import { useAuthStore } from "~/stores/auth";

const defaultHeaders = {
  "Content-Type": "application/json",
  "Accept-Language": "ru-RU",
};

export default defineNuxtPlugin((nuxtApp) => {
  const authStore = useAuthStore();

  globalThis.$fetch = ofetch.create({
    baseURL: "/api/",
    retry: 1,
    retryDelay: 200,
    retryStatusCodes: [401],
    headers: defaultHeaders,
    async onRequest({ request, options }) {
      const token = authStore.access_token;
      if (token && !(request === AuthAPIURLS.LOGIN))
        options.headers = {
          ...defaultHeaders,
          Authorization: `Bearer ${token}`,
        };
    },
    async onResponseError({ request, response, options }) {
      if (response?.status === 401 || response?.status === 403) {
        ofetch("/api/" + AuthAPIURLS.REFRESH_TOKEN, {
          method: "POST",
          body: {
            refresh: authStore.refresh_token,
          },
        })
          .then((response) => {
            authStore.updateAccessToken(response.access);
            return Promise.resolve();
          })
          .catch((error) => {
            authStore.logoutAction();
            return Promise.reject(error);
          });
      }
    },
  });
});
