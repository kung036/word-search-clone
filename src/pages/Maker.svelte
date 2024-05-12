<script>
  import Header from "../components/Header.svelte";
  import { onMount, onDestroy } from "svelte";
  import { handleLogin } from "../js/login";
  let form = {};
  form.words = [];

  const handleResize = () => {
    const wordElements = document.querySelectorAll(".word");

    // 화면의 너비에 따라 word 크기를 조정
    wordElements.forEach((wordElement) => {
      // 화면의 너비에 따라 word 크기를 조정
      if (window.innerWidth < 600) {
        wordElement.style.width = "calc(15% - 2px)";
      } else {
        wordElement.style.width = "calc(20% - 5px)";
      }
    });
  };

  // 입력값 서버 요청
  const handleSubmit = async (event) => {
    // 단어는 최소 3개 이상 입력
    if (form.words.length < 3) {
      alert("단어를 3개 이상 입력하세요");
      return;
    }

    // 단어들이 알파벳이거나 같은 단어가 있으면 생성 안됨
    for (const word in form.words) {
      console.log("word : ", word);
      // if (!/^[a-zA-Z]+$/.test(word)) {
      //   alert("영어만 입력 가능합니다");
      //   return;
      // }
      // if (form.words.includes(word)) {
      //   alert("서로 다른 단어를 입력하세요");
      //   return;
      // }
    }

    // word 대문자로 변경
    for (let i = 0; i < form.words.length; i++) {
      const uppercaseWords = form.words[i].toUpperCase(); // 현재 단어를 대문자로 변환
      form.words[i] = uppercaseWords; // 변환된 단어로 해당 인덱스의 요소를 교체
    }

    // FormData 형태로 변경
    const formData = new FormData();
    for (const key in form) {
      formData.append(key, form[key]);
    }

    // 서버 요청
    const serverUrl = import.meta.env.VITE_SERVER_URL;
    const accessToken = window.localStorage.getItem("token");
    const res = await fetch(serverUrl + "/game", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
      body: formData,
    });

    // 게임 만들기 요청 성공 시
    if (res.status === 200) {
      // 게임 아이디 저장
      const data = await res.json();
      window.localStorage.setItem("game_id", data.game_id);

      alert("게임 만들기에 성공했습니다.");
      window.location.hash = "/game";
    } else if (res.status === 401) {
      alert("로그인이 필요합니다.");
      handleLogin();
    } else {
      alert("게임 만들기에 실패했습니다.");
    }
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

<form id="maker-form" on:submit|preventDefault={handleSubmit}>
  <div class="maker-box">
    <h1>게임 만들기</h1>
    <!-- 제목 -->
    <div class="maker-box__info">
      <div>
        <label for="title">Title</label>
        <input type="text" id="title" bind:value={form.title} required />
      </div>
    </div>
    <!-- 설명 -->
    <div class="maker-box__info">
      <div>
        <label for="description">Description</label>
        <input
          type="text"
          id="description"
          bind:value={form.description}
          required
        />
      </div>
    </div>
    <!-- 단어 입력 -->
    <div>
      <label for="word-list">Word List</label>
      <p style="margin:0;">
        Between 3 and 30 words. Puzzles are randomly generated using a selection
        of your words at play time.
      </p>
    </div>
    <div class="wordlist">
      {#each Array.from({ length: 30 }) as _, i}
        <div id={"wrd" + i} class="word">
          <input type="text" bind:value={form.words[i]} />
        </div>
      {/each}
    </div>
    <!-- 게임 생성 버튼 -->
    <div>
      <button class="maker-btn" type="submit">게임 만들기</button>
    </div>
  </div>
</form>
