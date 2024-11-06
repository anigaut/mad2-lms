import { createRouter, createWebHistory } from 'vue-router'

const userRoutes = [
  {path:'/',
   name: 'home',
   component: () => import('../views/user/UserHome.vue'),
   meta: { title: "Opus Books" }},

  {path: '/login', 
   name: 'test', 
   component: () => import('../views/user/UserLogin.vue'),
   meta: { title: "Login to Opus" }},

  {path: '/register', 
   name:  'login', 
   component: () => import('../views/user/UserRegister.vue'),
   meta: { title: "Create Opus Account" }},

  {path: '/search/:query',
   name:'search',
   component: () => import('../views/user/Search.vue'),
   meta: { title: "Search Results" }},

  {path: '/browse-genres',
   name: 'browse', 
   component: () => import('../views/user/BrowseGenres.vue'),
   meta: { title: "Browse Genres" }},

  {path: '/genres/:genre',
   name: 'browseByGenre',
   component: () => import('../views/user/BrowseByGenre.vue'),
   meta: { title: "Browse by Genre" }},

  {path: '/books/:book',
   name: 'BookDetails',
   component: () => import('../views/user/BookDetails.vue'),
   meta: {title: "Book Details"}},

   {path: '/read/:book',
    name: 'readBook',
    component: () => import('../views/user/ReadBook.vue'),
    meta: {title: "Read Book"}
   }
]

const adminRoutes = [
  {path:'/admin/', 
   name:'adminHome', 
   component: () => import('../views/admin/AdminHome.vue'),
   meta: { title: "Admin Home" }},

  // {path:'/admin/register/', 
  //  name:'adminRegister', 
  //  component: () => import('../views/admin/AdminRegister.vue'),
  //  meta: { title: "Register" }},

  {path:'/admin/login/',
   name:'adminLogin',
   component: () => import('../views/admin/AdminLogin.vue'),
   meta: { title: "Admin Login" }},

  {path:'/admin/users', 
   name:'manageUsers', 
   component: () => import('../views/admin/Users.vue'),
   meta: { title: "Manage Users" }},

  {path: '/admin/genres',
   name:'manageGenres',
   component: () => import('../views/admin/Genres.vue'),
   meta: { title: "Manage Genres" }},

  {path: '/admin/books',
   name: 'manageBooks',
   component: () => import('../views/admin/Books.vue'),
   meta: { title: "Manage Books" }},

  {path: '/admin/requests',
   name:'pendingRequests',
   component: () => import('../views/admin/Requests.vue'),
   meta: { title: "Requests" }},

  {path: '/admin/borrowings',
   name: 'currentBorrowings',
   component: () => import('../views/admin/Borrowings.vue'),
   meta: { title: "Borrowings" }}
]

const allRoutes = userRoutes.concat(adminRoutes);

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: allRoutes
});

router.beforeEach((to, from) => {
  document.title = to.meta?.title ?? "Opus Books"
})

export default router
