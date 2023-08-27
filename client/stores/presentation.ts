import { defineStore } from "pinia";
import { ExtendedPresentationAPI, PresentationAPI } from "~/utils/presentations";
import { useAuthStore } from "./auth";

export const usePresentStore = defineStore("presentation", () => {
  const presentations = ref<ExtendedPresentationAPI[] | null>(null);

  const authStore = useAuthStore();

  const fetchPresentations = async () => {
    const response = await listPresentations({
      creator__id: authStore.user?.id,
    });

    presentations.value = response;
  };

  const allProcessed = computed(() => {
    if (presentations.value === null) fetchPresentations();
    return presentations.value?.findIndex((p) => p.result.pptx_status !== "Готово") === -1;
  });

  return {
    allProcessed,
    fetchPresentations,
    presentations,
  };
});
