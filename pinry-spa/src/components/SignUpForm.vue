<template>
  <div class="signup-modal">
    <form action="">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Sign Up</p>
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

          <b-field label="Email"
                   :type="email.type"
                   :message="email.error">
            <b-input
              type="email"
              v-model="email.value"
              password-reveal
              placeholder="Your email"
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
          <b-field label="Password repeat"
                   :type="password_repeat.type"
                   :message="password_repeat.error">
            <b-input
              type="password"
              v-model="password_repeat.value"
              password-reveal
              placeholder="Your password again"
              required>
            </b-input>
          </b-field>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">Close</button>
          <button
            @click="doRegister"
            class="button is-primary">Register</button>
        </footer>
      </div>
    </form>
  </div>
</template>

<script>
import api from './api';

export default {
  name: 'SignUpForm',
  data() {
    return {
      username: {
        value: null,
        error: null,
        type: null,
      },
      email: {
        value: null,
        error: null,
        type: null,
      },
      password: {
        value: null,
        error: null,
        type: null,
      },
      password_repeat: {
        value: null,
        error: null,
        type: null,
      },
    };
  },
  methods: {
    resetStatus() {
      this.resetField('username');
      this.resetField('email');
      this.resetField('password');
      this.resetField('password_repeat');
    },
    resetField(fieldName) {
      this[fieldName].type = 'is-info';
      this[fieldName].error = null;
    },
    markFieldAsDanger(fieldName, errorMsg) {
      this[fieldName].error = errorMsg;
      this[fieldName].type = 'is-danger';
    },
    doRegister() {
      this.resetStatus();
      const self = this;
      const promise = api.User.signUp(
        self.username.value,
        self.email.value,
        self.password.value,
        self.password_repeat.value,
      );
      promise.then(
        (user) => {
          self.$emit('signup.succeed', user);
          self.$parent.close();
        },
        (resp) => {
          Object.entries(resp.data).forEach(
            (errorTuple) => {
              const [key, error] = errorTuple;
              let msg;
              if (Array.isArray(error)) {
                [msg] = error;
              } else {
                msg = error;
              }
              this.markFieldAsDanger(key, msg);
            },
          );
        },
      );
    },
  },
};
</script>
