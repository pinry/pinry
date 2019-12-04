<template>
  <div class="login-modal">
    <form action="">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Login</p>
        </header>
        <section class="modal-card-body">
          <b-field label="Username"
                   :type="username.type"
                   :message="username.error">
            <b-input
              type="string"
              v-model="username.value"
              placeholder="Your Username"
              maxlength="30"
              required>
            </b-input>
          </b-field>

          <b-field label="Password"
                   :type="password.type"
                   :message="password.error">
            <b-input
              type="password"
              v-model="password.value"
              password-reveal
              placeholder="Your password"
              required>
            </b-input>
          </b-field>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">Close</button>
          <button
            @click="doLogin"
            class="button is-primary">Login</button>
        </footer>
      </div>
    </form>
  </div>
</template>

<script>
import api from './api';
import form from './utils/form';

const fields = ['username', 'password'];

export default {
  name: 'LoginForm',
  data() {
    return form.createFormModel(fields);
  },
  methods: {
    resetStatus() {
      form.FormHelper(this, fields).resetAllFields();
    },
    doLogin() {
      this.resetStatus();
      const self = this;
      const promise = api.User.logIn(self.username.value, self.password.value);
      const helper = form.FormHelper(self);
      promise.then(
        (user) => {
          self.$emit('login.succeed', user);
          self.$parent.close();
        },
        (resp) => {
          if (resp.data.username) {
            helper.markFieldAsDanger('username', resp.data.username);
          }
          if (resp.data.password) {
            helper.markFieldAsDanger('password', resp.data.password);
          }
        },
      );
    },
  },
};
</script>
