import { Ref } from 'vue';

export interface AdminCheckResult {
  isAdmin: Ref<boolean>;
  isCheckingAdmin: Ref<boolean>;
  adminCheckError: Ref<Error | null>;
  checkIsAdmin: (idToken?: string | null) => Promise<boolean>;
  redirectToAdminPortalIfAdmin: (adminPortalUrl: string) => Promise<boolean>;
}

export function useAdminCheck(): AdminCheckResult;
