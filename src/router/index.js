import { createRouter, createWebHistory } from 'vue-router'
import StartseiteView from '@/views/StartseiteView.vue'
import UeberDasToolView from '@/views/UeberDasToolView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'startseite',
      component: StartseiteView
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
      path: '/auth/account-bestaetigen',
      name: 'account-bestaetigen',
      component: () => import('@/views/AuthAccountBestaetigenView.vue'),
      meta: {
        requiresAuth: false
      }
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
        requiredUserRolleId: [1]
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
        }
      ]
    },
    {
      path: '/einstellungen/profil',
      name: 'profil',
      component: () => import('@/views/EinstellungenProfilView.vue')
    },

    {
      path: '/keine-zugangsberechtigung',
      name: 'keine-zugangsberechtigung',
      component: () => import('@/views/KeineZugangsberechtigungView.vue')
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

router.beforeEach((to, _) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn) {
      return { name: 'anmelden' }
    }
    if (to.meta.requiredUserRolle && !to.meta.requiredUserRolleId.includes(authStore.userRolleId)) {
      return { name: 'keine-zugangsberechtigung' }
    }
  }
})

export default router
