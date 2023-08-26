import { defineNuxtPlugin } from "#app";
import { ofetch } from "ofetch";
import { useAuthStore } from "~/stores/auth";
import { getLocalData, LocalData } from "~/utils/local";

const defaultHeaders = {
  "Content-Type": "application/json",
  "Accept-Language": "ru-RU",
};

export default defineNuxtPlugin((nuxtApp) => {
  globalThis.$fetch = ofetch.create({
    baseURL: "/api/",
    retry: 2,
    retryStatusCodes: [401, 403],
    headers: defaultHeaders,
    async onRequest({ request, options }) {
      const token = getLocalData(LocalData.ACCESS_TOKEN);
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
            refresh: getLocalData(LocalData.REFRESH_TOKEN),
          },
        })
          .catch((error) => {
            const authStore = useAuthStore();
            // authStore.logoutAction();
            return Promise.reject(error);
          })
          .then((response) => {
            setLocalData(LocalData.ACCESS_TOKEN, response.access);
            options.headers = {
              ...defaultHeaders,
              Authorization: `Bearer ${response.access}`,
            };
            options.retry = 1;
            return Promise.resolve();
          });
      }
    },
  });
});
