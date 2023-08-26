<script lang="ts" setup>
import { usePresentStore } from "~/stores/presentation";

const isLoading = ref(false);

const useCustomLogo = ref(false);
const useCustomName = ref(false);
const description = ref("");

const submitCallback = async () => {
  isLoading.value = true;

  const response = await createPresentation({
    generate_logo: !useCustomLogo.value,
    generate_name: !useCustomName.value,
    description: description.value,
  });

  const presentStore = usePresentStore();
  presentStore.setCurrentPresentation(response.id.toString());
};
</script>

<template>
  <div class="mb-5">
    <h1 class="text-center fw-bold">Генерация презентации</h1>
    <div class="text-center text-muted mb-5">
      Ответьте на несколько вопросов и создайте уникальную презентацию<br />для питчинга своего
      проекта!
    </div>

    <div v-if="!isLoading">
      <FormKit type="form" submit-label="Начать генерацию!" @submit="submitCallback">
        <div class="mb-4">
          <h3 class="fs-4 mb-3">1. Название проекта</h3>
          <div class="alert alert-success" v-if="!useCustomName">
            <i class="bi-stars me-2"></i>ИИ сгенерирует название для вас
          </div>
          <div class="form-check form-switch mb-3">
            <input
              id="useCustomLogoSwitch"
              class="form-check-input"
              type="checkbox"
              role="switch"
              v-model="useCustomName" />
            <label class="form-check-label" for="useCustomLogoSwitch"
              >У меня уже есть своё название</label
            >
          </div>
          <div v-if="useCustomName">
            <FormKit type="text" validation-label="«название»" />
          </div>
        </div>

        <div class="mb-4">
          <h3 class="fs-4 mb-3">2. Логотип</h3>

          <div class="alert alert-success" v-if="!useCustomLogo">
            <i class="bi-stars me-2"></i>ИИ сгенерирует логотип для вас
          </div>

          <div class="form-check form-switch mb-3">
            <input
              id="useCustomLogoSwitch"
              class="form-check-input"
              type="checkbox"
              role="switch"
              v-model="useCustomLogo" />
            <label class="form-check-label" for="useCustomLogoSwitch">Использовать своё лого</label>
          </div>

          <div v-if="useCustomLogo">
            <FormKit type="file" validation-label="«логотип»" accept=".png" />
          </div>
        </div>

        <div class="mb-4">
          <h3 class="fs-4 mb-3">3. Подробное описание проекта</h3>
          <FormKit
            type="textarea"
            rows="10"
            name="description"
            v-model="description"
            outer-class="mb-3"
            validation-visibility="blur"
            validation-label="«описание проекта»"
            validation="required" />
        </div>
      </FormKit>
    </div>
    <div v-else>
      <LoadingScreen />
    </div>
  </div>
</template>

<style>
form-control {
  background-color: #161c23;
  border-color: rgba(255, 255, 255, 0.645);
}

.radio-wrapper,
.checkbox-wrapper {
  display: flex;
}

.radio-wrapper .checkbox-label,
.checkbox-wrapper .checkbox-label,
.radio-wrapper .radio-label,
.checkbox-wrapper .radio-label {
  margin-left: 0.5rem;
}

.formkit-message.is-invalid {
  color: var(--bs-danger);
}

.formkit-messages {
  margin-top: 0.3rem;
}

[data-invalid="true"] .formkit-input {
  border-color: var(--bs-danger);
  padding-right: calc(1.5em + 0.75rem);
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 12 12' width='12' height='12' fill='none' stroke='%23dc3545'%3e%3ccircle cx='6' cy='6' r='4.5'/%3e%3cpath stroke-linejoin='round' d='M5.8 3.6h.4L6 6.5z'/%3e%3ccircle cx='6' cy='8.2' r='.6' fill='%23dc3545' stroke='none'/%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right calc(0.375em + 0.1875rem) center;
  background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
}

.formkit-options {
  list-style: none;
  margin: 0;
  padding: 0;
}

.form-check-inline .formkit-options {
  display: flex;
  gap: 1rem;
}

.form-control:focus {
  background-color: #212932;
}

.formkit-no-files {
  display: block;
  margin-top: 0.3rem !important;
}
</style>
