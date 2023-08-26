import { defineStore } from "pinia";
import { LocalData, getLocalData } from "~/utils/local";
import { APIUser, TelegramUserData } from "~/utils/auth";

export const useAuthStore = defineStore("auth", () => {
  const access_token = ref<string | null>(getLocalData(LocalData.ACCESS_TOKEN));
  const refresh_token = ref<string | null>(getLocalData(LocalData.REFRESH_TOKEN));
  const user = ref<APIUser | null>(null);

  const loggedIn = computed(() => user.value !== null);

  const router = useRouter();

  function getCurrentUserAction() {
    getCurrentUser().then((r) => {
      user.value = r;
    });
  }

  function updateAccessToken(token: string) {
    access_token.value = token;
    setLocalData(LocalData.ACCESS_TOKEN, token);
  }

  function loginAction(data: TelegramUserData) {
    login(data).then((response) => {
      setLocalData(LocalData.ACCESS_TOKEN, response.access);
      setLocalData(LocalData.REFRESH_TOKEN, response.refresh);
      access_token.value = response.access;
      refresh_token.value = response.refresh;
      getCurrentUserAction();
      router.push("/");
    });
  }

  function logoutAction() {
    if (!refresh_token.value) return;
    logout(refresh_token.value).then(() => {
      clearLocalData();
      user.value = null;
      router.push("/");
    });
  }

  return {
    user,
    loggedIn,
    loginAction,
    logoutAction,
    access_token,
    refresh_token,
    updateAccessToken,
    getCurrentUserAction,
  };
});
