<template>
  <h1 class="fs-2">Добро пожаловать в <b>NeoPitch</b></h1>
  <div class="fs-4 text-muted">Мы генерируем презентации для питчинга ваших проектов</div>

  <div class="row mt-5">
    <div class="col-12 col-sm-6 col-md-4 mb-3 mb-sm-0">
      <div class="card card-body h-100 py-3" id="generatePresentationCard">
        <div class="display-3 bi bi-gear-wide-connected mb-2"></div>
        <div class="fs-4">Генерация</div>
        <NuxtLink to="/generate" class="display-none stretched-link"></NuxtLink>
      </div>
    </div>

    <div class="col-12 col-sm-6 col-md-4">
      <div class="card card-body h-100 py-3" id="myPresentationsCard">
        <div class="display-3 bi bi-archive-fill mb-2"></div>
        <div class="fs-4">Архив</div>
        <NuxtLink to="/archive" class="display-none stretched-link"></NuxtLink>
      </div>
    </div>
  </div>
</template>

<style>
.card {
  --bs-card-color: rgba(0, 0, 0, 0.831) !important;
  --bs-secondary-color: rgba(0, 0, 0, 0.649) !important;
  font-weight: 600;
}

#generatePresentationCard {
  background-color: #c89afe;
}

#myPresentationsCard {
  background-color: #c2bc01;
}

.card:hover {
  scale: 1.005;
  transition: scale 0.1s ease-in-out;
}
</style>
