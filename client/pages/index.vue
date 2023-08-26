<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";

const authStore = useAuthStore();
</script>

<template>
  <div class="container mt-5">
    <div v-if="authStore.user === null">
      <div class="row justify-content-center">
        <div class="col-12 col-md-8 col-lg-6 col-xl-5">
          <div class="card card-body d-flex align-items-center">
            <i class="bi bi-lock-fill display-3 my-3"></i>
            <h5 class="text-center">У вас нет доступа к этой странице</h5>
            <div class="text-muted text-center">Войдите в свой аккаунт при помощи Telegram</div>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <PresentationGenCard />
    </div>
  </div>
</template>
