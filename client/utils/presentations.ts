export interface CreatePresentationAPI {
  description: string;
  generate_logo: boolean;
  generate_name: boolean;
  name?: string;
  logo?: File;
}

export interface PresentationAPI {
  checko_url: string | null;
  description: string;
  generate_logo: boolean;
  generate_name: boolean;
  id: number;
}

export interface ExtendedPresentationAPI extends PresentationAPI {
  result: {
    pptx_status: string;
    pptx: string;
  };
}

export const createPresentation = async (data: CreatePresentationAPI) => {
  const fd = new FormData();
  fd.append("description", data.description);
  fd.append("generate_logo", (data.generate_logo ? "true" : "false"));
  fd.append("generate_name", (data.generate_name ? "true" : "false"));
  if (data.name) fd.append("name", data.name);
  if (data.logo) fd.append("logo", data.logo);

  return $fetch<PresentationAPI>("presentations/", {
    method: "POST",
    body: fd,
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const getPresentation = async (id: string) => {
  return $fetch<PresentationAPI>("presentations/" + id, {
    headers: {
      "Content-Type": "application/json",
    },
  });
};

export interface ListPresentationsFilters {
  creator__id?: number;
  result__pptx?: "Готово" | "Обработка";
}

export const listPresentations = async (query?: ListPresentationsFilters) => {
  return $fetch<ExtendedPresentationAPI[]>("presentations/", {
    headers: {
      "Content-Type": "application/json",
    },
    query: query,
  });
};
