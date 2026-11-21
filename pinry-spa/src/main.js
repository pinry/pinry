import { createApp } from 'vue';
import {
  Button,
  Checkbox,
  Dialog,
  Field,
  Icon,
  Input,
  Loading,
  Modal,
  Select,
  Skeleton,
  Tag,
  Taginput,
  Toast,
  Upload,
} from 'buefy';
import 'buefy/dist/css/buefy.css';
import '@mdi/font/css/materialdesignicons.css';
import './components/utils/theme.scss';
import App from './App.vue';
import router from './router';
import i18n from './components/utils/i18n';
import setUpAxiosCsrfConfig from './components/utils/csrf';
import { initTheme } from './components/utils/theme';

setUpAxiosCsrfConfig();
initTheme();

const app = createApp(App);
app.use(router);
app.use(i18n);
// Only the Buefy components the app uses, so the rest is left out of the bundle.
[
  Button, Checkbox, Dialog, Field, Icon, Input, Loading,
  Modal, Select, Skeleton, Tag, Taginput, Toast, Upload,
].forEach(plugin => app.use(plugin));
app.mount('#app');
