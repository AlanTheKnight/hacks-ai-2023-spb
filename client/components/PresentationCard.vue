<script setup lang="ts">
import { ExtendedPresentationAPI } from "~/utils/presentations";

defineProps<{ obj: ExtendedPresentationAPI }>();
</script>

<template>
  <div class="card card-body text-light mb-2">
    <h2 class="fw-bold">Запрос #{{ obj.id }}</h2>
    <div>Статус: {{ obj.result.pptx_status }}</div>

    <NuxtLink v-if="obj.result.pptx_status === 'Готово'" :to="obj.result.pptx" class="stretched-link"/>
  </div>
</template>
