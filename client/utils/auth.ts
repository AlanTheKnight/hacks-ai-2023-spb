export interface TelegramUserData {
  auth_date: number;
  first_name: string;
  hash: string;
  id: number;
  last_name?: string;
  username: string;
  photo_url?: string;
}

export enum AuthAPIURLS {
  CURRENT_USER = "auth/users/me",
  LOGIN = "auth/login",
  LOGOUT = "auth/logout",
  REFRESH_TOKEN = "auth/refresh",
}

export interface APIUser {
  photo_url: string | null;
  username: string;
  id: number;
  telegram_id: number;
}

export interface APITokens {
  access: string;
  refresh: string;
}

export const login = async (data: TelegramUserData) => {
  return $fetch<APITokens>(AuthAPIURLS.LOGIN, {
    method: "POST",
    body: data,
    headers: {
      "Content-Type": "application/json",
    },
  });
};

export const getCurrentUser = async () => {
  return $fetch<APIUser>(AuthAPIURLS.CURRENT_USER, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

export const logout = async (refresh_token: string) => {
  $fetch(AuthAPIURLS.LOGOUT, {
    method: "POST",
    body: { refresh: refresh_token },
    headers: {
      "Content-Type": "application/json",
    },
  });
};
