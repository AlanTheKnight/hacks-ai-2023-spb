export enum LocalData {
  ACCESS_TOKEN = "access_token",
  REFRESH_TOKEN = "refresh_token",
}

export function setLocalData(key: LocalData, value: string, serialize = false): void {
  if (serialize) value = JSON.stringify(value);
  if (process.client) localStorage.setItem(key, value);
}

export function getLocalData(key: LocalData): string | null {
  const value = process.client ? localStorage.getItem(key) : null;
  if (!value) return null;
  return value;
}

export function clearLocalData(): void {
  if (!process.client) return;
  localStorage.removeItem(LocalData.ACCESS_TOKEN);
  localStorage.removeItem(LocalData.REFRESH_TOKEN);
}
