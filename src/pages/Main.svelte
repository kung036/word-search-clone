<script>
  import Header from "../components/Header.svelte";

  const token = window.localStorage.getItem("token");

  // 로그인 페이지로 이동하기
  const handleLogin = () => {
    window.localStorage.removeItem("token");
    window.location.hash = "/login";
    window.location.reload();
  };

  // 회원가입 페이지로 이동하기
  const handleSign = () => {
    window.localStorage.setItem("token", "sign");
    window.location.hash = "/sign";
    window.location.reload();
  };
</script>

<Header />

<main>
  <h1>Welcome to Word Search Game</h1>
  <div class="button-box">
    {#if !token || token === "sign"}
      <button on:click={handleLogin} id="login-btn">로그인</button>
      <button on:click={handleSign} id="sign-btn">회원가입</button>
    {/if}
  </div>
</main>
