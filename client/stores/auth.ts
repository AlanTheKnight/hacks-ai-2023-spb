import { defineStore } from "pinia";
import { LocalData, getLocalData } from "~/utils/local";
import { computed, onMounted, ref } from "vue";
import { APIUser } from "~/utils/auth";
// import router from "@/router";
// import {
//   login,
//   type TelegramUserData,
//   logout,
//   type APIUser,
//   currentUser,
// } from "@/api/services/auth";

export const useAuthStore = defineStore("auth", () => {
  const access_token = ref<string | null>(getLocalData(LocalData.ACCESS_TOKEN));
  const refresh_token = ref<string | null>(getLocalData(LocalData.REFRESH_TOKEN));
  const user = ref<APIUser | null>(null);

  const loggedIn = computed(() => user.value !== null);

  // function currentUserAction() {
  //   currentUser().then((r) => {
  //     user.value = r.data
  //   })
  // }

  function loginAction(data: TelegramUserData) {
    login(data).then((response) => {
      setLocalData(LocalData.ACCESS_TOKEN, response.access);
      setLocalData(LocalData.REFRESH_TOKEN, response.refresh);
      access_token.value = response.access;
      refresh_token.value = response.refresh;
      // currentUserAction()
    });
  }

  // function logoutAction() {
  //   if (!refresh_token.value) return
  //   logout(refresh_token.value).then(() => {
  //     clearLocalData()
  //     user.value = null
  //     router.push('/')
  //   })
  // }

  // onMounted(() => {
  //   if (user.value === null && access_token) {
  //     currentUserAction()
  //   }
  // })

  return {
    user,
    loggedIn,
    loginAction,
    // logoutAction,
    access_token,
    refresh_token,
    // currentUserAction,
  };
});
