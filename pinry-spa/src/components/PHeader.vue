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
            <a class="navbar-item" :href="bookmarklet">
              Bookmarklet
            </a>
            <div
              v-if="user.loggedIn"
              class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                Create
              </a>
              <div class="navbar-dropdown">
                <a
                  @click="createPin"
                  class="navbar-item">
                  Pin
                </a>
                <a
                  @click="createBoard"
                  class="navbar-item">
                  Board
                </a>
              </div>
            </div>
            <div
              v-if="user.loggedIn"
              class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                My
              </a>
              <div class="navbar-dropdown">
                <router-link
                  :to="{ name: 'boards4user', params: {username: user.meta.username} }"
                  class="navbar-item">
                  Boards
                </router-link>
                <router-link
                  :to="{ name: 'user', params: {user: user.meta.username} }"
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
                <a class="navbar-item" href="https://chrome.google.com/webstore/detail/jmhdcnmfkglikfjafdmdikoonedgijpa/">
                  Chrome
                </a>
                <a class="navbar-item" href="https://addons.mozilla.org/en-US/firefox/addon/add-to-pinry/">
                  Firefox
                </a>
              </div>
            </div>
          </div>
          <div class="navbar-end">
            <router-link
              :to="{ name: 'search' }"
              class="navbar-item">
              <b-icon
                type="is-dark"
                icon="magnify"
                custom-size="mdi-24px">
              </b-icon>
            </router-link>
            <div class="navbar-item">
              <div class="buttons">
                <a
                  @click="signUp"
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
import modals from './modals';

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
  computed: {
    bookmarklet() {
      const url = new URL(window.location);
      const host = url.origin;
      return `javascript:void((function(d){var s=d.createElement('script');s.id='pinry-bookmarklet';s.src='${host}/static/js/bookmarklet.js?'+Math.random()*10000000000000000;d.body.appendChild(s)})(document));`;
    },
  },
  methods: {
    toggleMenu() {
      this.active = !this.active;
    },
    onLoginSucceed() {
      this.initializeUser(true);
    },
    onSignUpSucceed() {
      this.initializeUser(true);
    },
    logOut() {
      api.User.logOut().then(
        () => {
          window.location.reload();
        },
      );
    },
    logIn() {
      modals.openLogin(this, this.onLoginSucceed);
    },
    createPin() {
      modals.openPinEdit(
        this,
        { username: this.user.meta.username },
      );
    },
    createBoard() {
      modals.openBoardCreate(this);
    },
    signUp() {
      modals.openSignUp(this, this.onSignUpSucceed);
    },
    initializeUser(force = false) {
      const self = this;
      api.User.fetchUserInfo(force).then(
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
