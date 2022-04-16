<template>
  <div class="login-modal">
    <div @keydown="triggerDoLogin">
      <div class="modal-card" style="width: auto">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ $t("loginTitle") }}</p>
        </header>
        <section class="modal-card-body">
          <b-field v-bind:label="$t('usernameLabel')"
                   :type="form.username.type"
                   :message="form.username.error">
            <b-input
              name="username"
              type="text"
              v-model="form.username.value"
              v-bind:placeholder="$t('usernamePlaceholder')"
              maxlength="30"
              required>
            </b-input>
          </b-field>

          <b-field v-bind:label="$t('passwordLabel')"
                   :type="form.password.type"
                   :message="form.password.error">
            <b-input
              type="password"
              v-model="form.password.value"
              password-reveal
              v-bind:placeholder="$t('passwordLoginPlaceholder')"
              required>
            </b-input>
          </b-field>
        </section>
        <footer class="modal-card-foot">
          <button class="button" type="button" @click="$parent.close()">{{ $t("closeButton") }}</button>
          <button
            @click="doLogin"
            class="button is-primary">{{ $t("loginButton") }}</button>
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
    triggerDoLogin(e) {
      if (e.keyCode === 13) {
        this.doLogin();
        return false;
      }
      return true;
    },
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
