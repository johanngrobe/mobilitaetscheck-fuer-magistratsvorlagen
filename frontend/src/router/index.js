import { createRouter, createWebHistory } from 'vue-router'
import StartseiteView from '@/views/StartseiteView.vue'
import UeberDasToolView from '@/views/UeberDasToolView.vue'
import { useAuthStore } from '@/stores/auth'
import { apiClient } from '@/services/axios'

let setupStatusPromise = null

export function resetSetupStatus() {
  setupStatusPromise = null
}

function getSetupStatus() {
  if (!setupStatusPromise) {
    setupStatusPromise = apiClient
      .get('/public/setup-status')
      .then((r) => r.data.needsSetup)
      .catch(() => false)
  }
  return setupStatusPromise
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'startseite',
      component: StartseiteView
    },
    {
      path: '/impressum',
      name: 'impressum',
      component: () => import('@/views/ImpressumView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/datenschutzerklaerung',
      name: 'datenschutzerklaerung',
      component: () => import('@/views/DatenschutzerklaerungView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/nutzungsbedingungen',
      name: 'nutzungsbedingungen',
      component: () => import('@/views/NutzungsbedingungenView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/ueber-das-tool',
      name: 'ueber-das-tool',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: UeberDasToolView
    },
    {
      path: '/auth/anmelden',
      name: 'anmelden',
      component: () => import('@/views/AuthAnmeldenView.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/auth/registrieren',
      name: 'registrieren',
      component: () => import('@/views/AuthRegistrierenView.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/auth/registrieren/einladung',
      name: 'registrieren-einladung',
      component: () => import('@/views/AuthRegistrierenView.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/auth/account-bestaetigen',
      name: 'account-bestaetigen',
      component: () => import('@/views/AuthAccountBestaetigenView.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/auth/account-nicht-verifiziert',
      name: 'account-nicht-verifiziert',
      component: () => import('@/views/AuthNichtVerifiziertView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/auth/passwort-vergessen',
      name: 'passwort-vergessen',
      component: () => import('@/views/AuthPasswortVergessenView.vue')
    },
    {
      path: '/auth/passwort-zuruecksetzen',
      name: 'passwort-zuruecksetzen',
      component: () => import('@/views/AuthPasswortZuruecksetzenView.vue')
    },
    {
      path: '/magistratsvorlage',
      name: 'magistratsvorlage-liste',
      component: () => import('@/views/MagistratsvorlagenView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/magistratsvorlage/neu',
      name: 'magistratsvorlage-neu',
      component: () => import('@/views/MagistratsvorlageNeuView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/magistratsvorlage/:id',
      name: 'magistratsvorlage-id',
      component: () => import('@/views/MagistratsvorlageIdView.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: 'daten',
          name: 'magistratsvorlage-id-daten',
          component: () => import('@/views/MagistratsvorlageIdDatenView.vue')
        },
        {
          path: 'klimacheck',
          name: 'magistratsvorlage-id-klimacheck',
          component: () => import('@/views/MagistratsvorlageIdKlimacheckView.vue')
        },
        {
          path: 'mobilitaetscheck',
          name: 'magistratsvorlage-id-mobilitaetscheck',
          component: () => import('@/views/MagistratsvorlageIdMobilitaetscheckView.vue')
        },
        {
          path: 'klimarelevanzpruefung',
          name: 'magistratsvorlage-id-klimarelevanzpruefung',
          component: () => import('@/views/MagistratsvorlageIdKlimarelevanzpruefungView.vue')
        },
        {
          path: 'klimarelevanzpruefung/neu',
          name: 'magistratsvorlage-id-klimarelevanzpruefung-neu',
          component: () => import('@/views/MagistratsvorlageIdKlimarelevanzpruefungNeuView.vue')
        },
        {
          path: 'klimarelevanzpruefung/:klimarelevanzpruefungId',
          name: 'magistratsvorlage-id-klimarelevanzpruefung-id',
          component: () => import('@/views/MagistratsvorlageIdKlimarelevanzpruefungIdView.vue')
        },
        {
          path: 'mobilitaetscheck/neu',
          name: 'magistratsvorlage-id-mobilitaetscheck-neu',
          component: () => import('@/views/MagistratsvorlageIdMobilitaetscheckNeuView.vue')
        },
        {
          path: 'mobilitaetscheck/neu/:checkId',
          name: 'mobilitaetscheck-ziele-neu',
          component: () => import('@/views/MagistratsvorlageIdMobilitaetscheckNeuZieleView.vue')
        },
        {
          path: 'klimacheck/neu',
          name: 'magistratsvorlage-id-klimacheck-neu',
          component: () => import('@/views/MagistratsvorlageIdKlimacheckNeuView.vue')
        }
      ]
    },
    {
      path: '/datenbank/user',
      name: 'datenbank-user',
      component: () => import('@/views/DatenbankUserView.vue'),
      meta: {
        requiresAuth: true,
        requiredUserRolleId: [2]
      }
    },
    {
      path: '/einstellungen',
      name: 'einstellungen',
      component: () => import('@/views/EinstellungenView.vue'),
      meta: {
        requiresAuth: true,
        requiredUserRolleId: [1, 2]
      },
      children: [
        {
          path: 'leitziel',
          name: 'leitziel',
          component: () => import('@/views/EinstellungenLeitzielView.vue')
        },
        {
          path: 'textblock',
          name: 'textblock',
          component: () => import('@/views/EinstellungenTextblockView.vue')
        },
        {
          path: 'indikator',
          name: 'indikator',
          component: () => import('@/views/EinstellungenIndikatorView.vue')
        },
        {
          path: 'tag',
          name: 'tag',
          component: () => import('@/views/EinstellungenTagView.vue')
        },
        {
          path: 'accountverwaltung',
          name: 'accountverwaltung',
          component: () => import('@/views/EinstellungenAccountverwaltungView.vue')
        },
        {
          path: 'gemeinde-gebiet',
          name: 'gemeinde-gebiet',
          component: () => import('@/views/EinstellungenGemeindeGebietView.vue')
        },
        {
          path: 'leitziel-sets',
          name: 'leitziel-sets',
          component: () => import('@/views/EinstellungenZielSetView.vue')
        },
        {
          path: 'einladungen',
          name: 'einladungen',
          component: () => import('@/views/EinstellungenEinladungenView.vue')
        },
        {
          path: 'gruppen',
          name: 'gruppen',
          component: () => import('@/views/EinstellungenGruppenView.vue')
        }
      ]
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('@/views/AdminView.vue'),
      meta: {
        requiresAuth: true,
        requiresPlatformAdmin: true
      },
      children: [
        {
          path: 'kommunen',
          name: 'admin-kommunen',
          component: () => import('@/views/AdminGemeindenView.vue')
        },
        {
          path: 'benutzer',
          name: 'admin-benutzer',
          component: () => import('@/views/AdminUsersView.vue')
        },
        {
          path: 'einladungen',
          name: 'admin-einladungen',
          component: () => import('@/views/AdminEinladungenView.vue')
        },
        {
          path: 'datenschutz',
          name: 'admin-datenschutz',
          component: () => import('@/views/AdminDatenschutzView.vue')
        },
        {
          path: 'nutzungsbedingungen',
          name: 'admin-nutzungsbedingungen',
          component: () => import('@/views/AdminNutzungsbedingungenView.vue')
        },
        {
          path: 'email-vorlagen',
          name: 'admin-email-vorlagen',
          component: () => import('@/views/AdminEmailVorlagenView.vue')
        },
        {
          path: 'branding',
          name: 'admin-branding',
          component: () => import('@/views/AdminBrandingView.vue')
        },
        {
          path: 'ueber-das-tool',
          name: 'admin-ueber-das-tool',
          component: () => import('@/views/AdminUeberDasToolView.vue')
        },
        {
          path: 'impressum',
          name: 'admin-impressum',
          component: () => import('@/views/AdminImpressumView.vue')
        },
        {
          path: 'startseite',
          name: 'admin-startseite',
          component: () => import('@/views/AdminStartseiteView.vue')
        }
      ]
    },
    {
      path: '/einstellungen/profil',
      name: 'profil',
      component: () => import('@/views/EinstellungenProfilView.vue'),
      meta: { requiresAuth: true }
    },

    {
      path: '/oeffentlich/magistratsvorlage/:id',
      name: 'oeffentlich-magistratsvorlage-id',
      component: () => import('@/views/OeffentlichMagistratsvorlageIdView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/keine-zugangsberechtigung',
      name: 'keine-zugangsberechtigung',
      component: () => import('@/views/KeineZugangsberechtigungView.vue')
    },
    {
      path: '/setup',
      name: 'setup',
      component: () => import('@/views/SetupView.vue'),
      meta: { requiresAuth: false }
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach(async (to) => {
  const needsSetup = await getSetupStatus()

  if (needsSetup) {
    if (to.name !== 'setup') return { name: 'setup' }
    return
  }

  if (to.name === 'setup') return { name: 'startseite' }

  const authStore = useAuthStore()

  if (to.meta.requiresAuth || to.meta.requiresPlatformAdmin) {
    if (!authStore.isLoggedIn) {
      return { name: 'anmelden' }
    }
    if (!authStore.isVerified) {
      return { name: 'account-nicht-verifiziert' }
    }
    if (to.meta.requiresPlatformAdmin && authStore.userRolleId !== 3) {
      return { name: 'keine-zugangsberechtigung' }
    }
    if (
      to.meta.requiredUserRolleId &&
      !to.meta.requiredUserRolleId.includes(authStore.userRolleId)
    ) {
      return { name: 'keine-zugangsberechtigung' }
    }
  }
})

export default router
