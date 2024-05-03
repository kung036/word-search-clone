<script>
  import "./css/sytle.css";
  import Router from "svelte-spa-router";
  import { user$ } from "./store";
  import { onMount } from "svelte";
  import Login from "./pages/Login.svelte";
  import Maker from "./pages/Maker.svelte";
  import Sign from "./pages/Sign.svelte";
  import Loading from "./pages/Loading.svelte";
  import Main from "./pages/Main.svelte";

  let isLoading = true;

  const checkLogin = async () => {
    const token = localStorage.getItem("token"); // access token
    if (!token) return (isLoading = false);

    isLoading = false;
  };
  // router 설정
  const routes = {
    "/": Main,
    "/maker": Maker,
    "/sign": Sign,
  };

  // 렌더링될 때마다 동작
  onMount(() => checkLogin());
</script>

{#if isLoading}
  <Loading />
{:else if !$user$}
  <Login />
{:else}
  <Router {routes} />
{/if}
