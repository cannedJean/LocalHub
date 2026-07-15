import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PlacesView from '../views/PlacesView.vue'
import BoardListView from '../views/BoardListView.vue'
import PostFormView from '../views/PostFormView.vue'
import PostDetailView from '../views/PostDetailView.vue'
import SourcesView from '../views/SourcesView.vue'
import NotFoundView from '../views/NotFoundView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: HomeView },
    { path: '/places', name: 'places', component: PlacesView },
    { path: '/map', name: 'map', component: PlacesView, props: { mapFirst: true } },
    { path: '/boards', name: 'boards', component: BoardListView },
    { path: '/boards/new', name: 'post-new', component: PostFormView },
    { path: '/boards/:id/edit', name: 'post-edit', component: PostFormView },
    { path: '/boards/:id', name: 'post-detail', component: PostDetailView },
    { path: '/sources', name: 'sources', component: SourcesView },
    { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundView },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
