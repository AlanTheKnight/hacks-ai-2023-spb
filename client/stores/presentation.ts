import { defineStore } from "pinia";
import { PresentationAPI } from "~/utils/presentations";

export const usePresentStore = defineStore("presentation", () => {
  const currentPresentationId = ref<string | null>(getLocalData(LocalData.CURRENT_PRESENTATION));
  const curPresentation = ref<PresentationAPI | null>(null);

  async function setCurrentPresentation(id: string) {
    currentPresentationId.value = id;
    setLocalData(LocalData.CURRENT_PRESENTATION, id);
    fetchCurrentPres();
  }

  async function fetchCurrentPres() {
    if (currentPresentationId.value) {
      curPresentation.value = await getPresentation(currentPresentationId.value);
    }
  }

  return {
    currentPresentation: curPresentation,
    currentPresentationId,
    setCurrentPresentation,
    fetchCurrentPres,
  };
});
