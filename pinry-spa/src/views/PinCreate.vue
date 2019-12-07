<template>
  <div class="pin-create">
    <div></div>
  </div>
</template>

<script>
import modals from '../components/modals';
import API from '../components/api';

export default {
  name: 'PinCreateFromURL',
  data() {
    return {
      meta: {
        url: null,
        referer: null,
        description: null,
      },
      user: {
        loggedIn: false,
        meta: null,
      },
    };
  },
  methods: {
    initialize(force = false) {
      const self = this;
      API.User.fetchUserInfo(force).then(
        (user) => {
          if (user === null) {
            self.user.loggedIn = false;
            self.user.meta = {};
          } else {
            self.user.meta = user;
            self.user.loggedIn = true;
            self.createPin();
          }
        },
      );
    },
    onCreated() {
      this.$buefy.dialog.alert(
        'Please turn off this page by hand since '
        + 'Javascript has no permission to do this',
      );
    },
    createPin() {
      modals.openPinEdit(
        this,
        { username: this.user.meta.username, fromUrl: this.meta },
        this.onCreated,
      );
    },
  },
  created() {
    this.meta = this.$route.query;
    this.initialize();
  },
};
</script>

<style scoped>

</style>
