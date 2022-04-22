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
              {{ $t("bookmarkletLink") }}
            </a>
            <div
              v-if="user.loggedIn"
              class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                {{ $t("createLink") }}
              </a>
              <div class="navbar-dropdown">
                <a
                  @click="createPin"
                  class="navbar-item">
                  {{ $t("pinLink") }}
                </a>
                <a
                  @click="createBoard"
                  class="navbar-item">
                  {{ $t("boardLink") }}
                </a>
              </div>
            </div>
            <div
              v-if="user.loggedIn"
              class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                {{ $t("myLink") }}
              </a>
              <div class="navbar-dropdown">
                <router-link
                  :to="{ name: 'boards4user', params: {username: user.meta.username} }"
                  class="navbar-item">
                  {{ $t("boardsLink") }}
                </router-link>
                <router-link
                  :to="{ name: 'user', params: {user: user.meta.username} }"
                  class="navbar-item">
                  {{ $t("pinsLink") }}
                </router-link>
                <router-link
                  :to="{ name: 'profile4user', params: {username: user.meta.username} }"
                  class="navbar-item">
                  {{ $t("profileLink") }}
                </router-link>
              </div>
            </div>
            <div class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                {{ $t("browserExtensionsLink") }}
              </a>
              <div class="navbar-dropdown">
                <a class="navbar-item" href="https://chrome.google.com/webstore/detail/jmhdcnmfkglikfjafdmdikoonedgijpa/">
                  {{ $t("chromeLink") }}
                </a>
                <a class="navbar-item" href="https://addons.mozilla.org/en-US/firefox/addon/add-to-pinry/">
                  {{ $t("firefoxLink") }}
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
            <div
              class="navbar-item has-dropdown is-hoverable">
              <a class="navbar-link">
                <b-icon
                  type="is-dark"
                  icon="translate"
                  custom-size="mdi-24px">
                </b-icon>
              </a>
              <div class="navbar-dropdown">
                <a
                  v-for="locale in $i18n.availableLocales"
                  :key="`locale-${locale}`"
                  @click="setLocale(locale)"
                  class="navbar-item">
                  {{ langs[locale] }}
                </a>
              </div>
            </div>
            <div class="navbar-item">
              <div class="buttons">
                <a
                  @click="signUp"
                  v-show="!user.loggedIn"
                  class="button is-primary">
                  <strong>{{ $t("signUpLink") }}</strong>
                </a>
                <a
                  v-show="!user.loggedIn"
                  v-on:click="logIn"
                  class="button is-light">
                  {{ $t("logInLink") }}
                </a>
                <a
                  v-show="user.loggedIn"
                  v-on:click="logOut"
                  class="button is-light">
                  {{ $t("logOutLink") }}
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
import localeUtils from '@/components/utils/i18n';
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
      langs: localeUtils.langCode2Name,
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
    setLocale(locale) {
      this.$i18n.locale = locale;
      localStorage.setItem('localeCode', locale);
    },
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
