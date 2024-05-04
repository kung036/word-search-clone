<script>
  import "./css/style.css";
  import Router from "svelte-spa-router";
  import { onMount } from "svelte";
  import Login from "./pages/Login.svelte";
  import Maker from "./pages/Maker.svelte";
  import Sign from "./pages/Sign.svelte";
  import Loading from "./pages/Loading.svelte";
  import Main from "./pages/Main.svelte";
  import NotFound from "./pages/NotFound.svelte";

  let isLoading = true;
  let token = window.localStorage.getItem("token"); // access token

  const checkLogin = async () => {
    token = window.localStorage.getItem("token"); // access token
    if (!token) return (isLoading = false);

    isLoading = false;
  };
  // router 설정
  const routes = {
    "/": Main,
    "/maker": Maker,
    "/sign": Sign,
    "/login": Login,
    "*": NotFound,
  };

  // 렌더링될 때마다 동작
  onMount(() => checkLogin());
</script>

{#if isLoading}
  <Loading />
{:else if token === null}
  <Login />
{:else if token === "sign"}
  <Sign />
{:else}
  <Router {routes} />
{/if}
