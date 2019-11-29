<template>
  <div class="p-header">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="container">
        <div class="navbar-brand">
          <a class="navbar-item" href="/">
            <img src="../assets/logo-dark.png" height="28">
          </a>
          <a role="button" class="navbar-burger burger"
             aria-label="menu" aria-expanded="false"
             v-on:click="toggleMenu"
             data-target="PinryNav">
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
            <span aria-hidden="true"></span>
          </a>
        </div>
        <div id="PinryNav" class="navbar-menu" :class="{ 'is-active': active}">
          <div class="navbar-start">
            <a class="navbar-item">
              BookmarkLet
            </a>
            <a class="navbar-item" v-show="user.loggedIn">
              Create Pin
            </a>
            <div
              v-show="user.loggedIn"
              class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                My Collections
              </a>
              <div class="navbar-dropdown">
                <router-link
                  to="/boards"
                  class="navbar-item">
                  Boards
                </router-link>
                <router-link
                  to="/pins"
                  class="navbar-item">
                  Pins
                </router-link>
              </div>
            </div>
            <div class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                Browser Extensions
              </a>
              <div class="navbar-dropdown">
                <a class="navbar-item">
                  Chrome
                </a>
                <a class="navbar-item">
                  Firefox
                </a>
              </div>
            </div>
          </div>
          <div class="navbar-end">
            <div class="navbar-item">
              <div class="buttons">
                <a
                  v-show="!user.loggedIn"
                  class="button is-primary">
                  <strong>Sign up</strong>
                </a>
                <a
                  v-show="!user.loggedIn"
                  v-on:click="logIn"
                  class="button is-light">
                  Log in
                </a>
                <a
                  v-show="user.loggedIn"
                  v-on:click="logOut"
                  class="button is-light">
                  Log out
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import api from './api';
import LoginForm from './LoginForm.vue';

export default {
  name: 'p-header',
  data() {
    return {
      active: false,
      user: {
        loggedIn: false,
        meta: {},
      },
    };
  },
  methods: {
    toggleMenu() {
      this.active = !this.active;
    },
    onLoginSucceed() {
      this.initializeUser();
    },
    logOut() {
      api.User.logOut().then(
        () => {
          window.location.reload();
        },
      );
    },
    logIn() {
      this.$buefy.modal.open({
        parent: this,
        component: LoginForm,
        hasModalCard: true,
        events: {
          'login.succeed': this.onLoginSucceed,
        },
      });
    },
    initializeUser() {
      const self = this;
      api.User.fetchUserInfo().then(
        (user) => {
          if (user === null) {
            self.user.loggedIn = false;
            self.user.meta = {};
          } else {
            self.user.meta = user;
            self.user.loggedIn = true;
          }
        },
      );
    },
  },
  beforeMount() {
    this.initializeUser();
  },
};
</script>

<style scoped>

</style>
