<template>
  <div class="profile-for-user">
    <PHeader></PHeader>
    <UserProfileCard :in-profile="true" :username="filters.userFilter"></UserProfileCard>
    <Profile v-if="profile.token" :token="profile.token"></Profile>
  </div>
</template>

<script>
import PHeader from '../components/PHeader.vue';
import UserProfileCard from '../components/UserProfileCard.vue';
import Profile from '../components/user/profile.vue';
import api from '../components/api';

export default {
  name: 'Profile4User',
  data() {
    return {
      filters: { userFilter: null },
      profile: {},
    };
  },
  components: {
    PHeader,
    UserProfileCard,
    Profile,
  },
  created() {
    this.initializeBoard();
    this.initializeUser(this.filters.userFilter);
  },
  beforeRouteUpdate(to, from, next) {
    this.filters = { userFilter: to.params.username };
    next();
  },
  methods: {
    initializeBoard() {
      this.filters = { userFilter: this.$route.params.username };
    },
    initializeUser(username) {
      const self = this;
      api.User.fetchUserInfoByName(username).then(
        (user) => {
          if (user === null) {
            // Keep the URL; the catch-all route needs the path as its param.
            self.$router.replace({
              name: 'PageNotFound',
              params: { pathMatch: self.$route.path.substring(1).split('/') },
            });
          } else {
            self.profile = user;
            self.loadOwnToken(user.username);
          }
        },
      );
    },
    loadOwnToken(username) {
      // The public profile never carries the token, so fetch it from
      // the requester's own profile when this page is theirs.
      const self = this;
      api.User.fetchUserInfo(true).then(
        (me) => {
          if (me !== null && me.username === username) {
            self.profile = { ...self.profile, token: me.token };
          }
        },
      );
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
