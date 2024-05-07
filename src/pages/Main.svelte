<script>
  import Header from "../components/Header.svelte";
  import { onMount, onDestroy } from "svelte";
  import { handleLogin } from "../js/login";
  import { changeGamePage } from "../js/game-page";
  import { handleLogout } from "../js/logout";
  import { handleMyGame } from "../js/game-list";

  const token = window.localStorage.getItem("token");

  // 회원가입 페이지로 이동하기
  const handleSign = () => {
    window.localStorage.setItem("token", "sign");
    window.location.hash = "/sign";
    window.location.reload();
  };

  // 게임 만들기 페이지로 이동
  const handleMaker = async () => {
    // 회원 여부 확인
    const serverUrl = import.meta.env.VITE_SERVER_URL;
    const accessToken = window.localStorage.getItem("token");
    const res = await fetch(serverUrl + "/user", {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    });

    // 게임 만들기 요청 성공 시
    if (res.status === 401) {
      alert("로그인이 필요합니다.");
      handleLogin();
    } else if (res.status === 200) {
      window.location.hash = "/maker";
      window.location.reload();
    }
  };

  // 게임링크로 이동
  let gameLink = "";
  function handleSubmit() {
    // 폼이 제출되었을 때 호출되는 함수
    changeGamePage(gameLink); // changeGamePage 함수에 입력된 게임 링크 전달
  }

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
    <form class="game-link-input" on:submit|preventDefault={handleSubmit}>
      게임링크 :
      <input
        type="text"
        id="textInput"
        placeholder="http://localhost:5173/..."
        bind:value={gameLink}
      />
      <button type="submit">입력</button>
    </form>
    <div class="button-box">
      <button on:click={handleMaker} id="logout-btn">게임 만들기</button>
      <button on:click={handleLogout} id="logout-btn">로그아웃</button>
      <button on:click={handleMyGame} id="logout-btn">나의 게임</button>
    </div>
  {/if}
</main>
