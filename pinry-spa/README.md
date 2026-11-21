# pinry-spa

The Pinry web app: Vue 3, Vite, Buefy 3 (Bulma 1), vue-router and vue-i18n.

## Project setup
This project requires Node.js 26 and pnpm 12 (pinned in `package.json`).

```
npm install -g pnpm@12
pnpm install
```

### Dev server with hot reload
Proxies `/api`, `/admin`, `/media` and `/static` to Django on `127.0.0.1:8000`.
```
pnpm serve
```

### Production build into `dist/`
```
pnpm build
```

### Lint
```
pnpm lint
```

See the [Vite configuration reference](https://vite.dev/config/).
