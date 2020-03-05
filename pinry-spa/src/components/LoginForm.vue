<template>
  <div class="login-modal">
    <div>
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">Login</p>
        </header>
        <section class="modal-card-body">
          <b-field label="Username"
                   :type="form.username.type"
                   :message="form.username.error">
            <b-input
              name="username"
              type="text"
              v-model="form.username.value"
              placeholder="Your Username"
              maxlength="30"
              required>
            </b-input>
          </b-field>

          <b-field label="Password"
                   :type="form.password.type"
                   :message="form.password.error">
            <b-input
              type="password"
              v-model="form.password.value"
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
    </div>
  </div>
</template>

<script>
import api from './api';
import ModelForm from './utils/ModelForm';

const fields = ['username', 'password'];

export default {
  name: 'LoginForm',
  data() {
    const model = ModelForm.fromFields(fields);
    return {
      form: model.form,
      helper: model,
    };
  },
  methods: {
    doLogin() {
      this.helper.resetAllFields();
      const self = this;
      const promise = api.User.logIn(
        self.form.username.value,
        self.form.password.value,
      );
      promise.then(
        (user) => {
          self.$emit('login.succeed', user);
          self.$parent.close();
          window.location.reload();
        },
        (resp) => {
          self.helper.markFieldsAsDanger(resp.data);
        },
      );
    },
  },
};
</script>
