<script>
  import Header from "../components/Header.svelte";
  import { onMount, onDestroy } from "svelte";

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

  // 로그아웃
  const handleLogout = () => {
    window.localStorage.removeItem("token");
    window.location.reload();
  };

  // 게임 만들기 페이지로 이동
  const handleMaker = () => {
    window.location.hash = "/maker";
    window.location.reload();
  };

  let inputWidth = 200; // 초기 너비 설정

  // 화면 크기가 변경될 때마다 실행되는 함수
  const handleResize = () => {
    inputWidth = Math.min(window.innerWidth / 2, 200); // 화면의 절반 크기로 설정, 최대 너비는 200px로 제한
  };

  // 컴포넌트가 마운트된 후에 실행되는 함수
  onMount(() => {
    handleResize(); // 초기화면 크기 설정
    window.addEventListener("resize", handleResize); // resize 이벤트 리스너 등록
  });

  // 컴포넌트가 파괴될 때 resize 이벤트 리스너 제거
  onDestroy(() => {
    window.removeEventListener("resize", handleResize);
  });
</script>

<Header />

<main>
  <h1>Welcome to Word Search Game</h1>
  {#if !token || token === "sign"}
    <button on:click={handleLogin} id="login-btn">로그인</button>
    <button on:click={handleSign} id="sign-btn">회원가입</button>
  {:else}
    <div class="game-link-input">
      게임링크 :
      <input
        type="text"
        id="textInput"
        placeholder="http://localhost:5173/..."
      />
    </div>
    <div class="button-box">
      <button on:click={handleMaker} id="logout-btn">게임 만들기</button>
      <button on:click={handleLogout} id="logout-btn">로그아웃</button>
    </div>
  {/if}
</main>
