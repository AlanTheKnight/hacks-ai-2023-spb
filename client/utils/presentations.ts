export interface CreatePresentationAPI {
  description: string;
  generate_logo: boolean;
  generate_name: boolean;
}

export interface PresentationAPI {
  checko_url: string | null;
  description: string;
  generate_logo: boolean;
  generate_name: boolean;
  id: number;
}

export const createPresentation = async (data: CreatePresentationAPI) => {
  return $fetch<PresentationAPI>("presentations/", {
    method: "POST",
    body: data,
  });
};

export const getPresentation = async (id: string) => {
  return $fetch<PresentationAPI>("presentations/" + id)
}
